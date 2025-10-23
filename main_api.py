from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import io
import json
import os
import base64
import asyncio
from pathlib import Path
from src.model import AnimalCNN
import numpy as np
from datetime import datetime
from typing import Optional

# Initialize FastAPI app
app = FastAPI(
    title="Animal Classification API",
    version="2.0.0",
    description="Professional AI-powered animal species classification with feedback loop",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add security middleware
try:
    from src.security import RateLimitMiddleware, SecurityHeadersMiddleware

    # Add rate limiting (100 requests per 60 seconds)
    app.add_middleware(RateLimitMiddleware, calls=100, period=60)

    # Add security headers
    app.add_middleware(SecurityHeadersMiddleware)

    print("✅ Security middleware enabled")
except ImportError:
    print("⚠️  Security middleware not available")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
model = None
class_names = []
class_map = {}
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Image transformation - optimized for memory
transform = transforms.Compose([
    # Use antialias for better quality
    transforms.Resize((224, 224), antialias=True),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


def load_model():
    """Load the trained model and class information with memory optimization"""
    global model, class_names, class_map

    try:
        print("🔄 Loading model and dataset...")

        # Get class names by scanning directory structure only (no image loading)
        dataset_path = "dataset"
        if os.path.exists(dataset_path):
            # Just get folder names as class names - don't load images
            class_names = [d for d in sorted(os.listdir(dataset_path))
                           if os.path.isdir(os.path.join(dataset_path, d))]
            class_map = {cls_name: idx for idx,
                         cls_name in enumerate(class_names)}
            print(f"📊 Found {len(class_names)} animal classes")
        else:
            print("⚠️  Dataset directory not found")
            class_names = []
            class_map = {}

        # Initialize model
        # Default fallback
        num_classes = len(class_names) if class_names else 10
        model = AnimalCNN(num_classes=num_classes)

        # Load trained weights if available
        model_path = "outputs/best_model.pth"
        if os.path.exists(model_path):
            print(f"📥 Loading model weights from {model_path}")
            # Load with map_location to avoid GPU memory issues
            checkpoint = torch.load(model_path, map_location=device)
            model.load_state_dict(checkpoint)
            del checkpoint  # Free memory immediately
            print(f"✅ Model weights loaded successfully")
        else:
            print("⚠️  No trained model found. Using untrained model.")

        model.to(device)
        model.eval()

        # Note: Disabled half precision as it may cause issues with some operations
        # Keep using full precision for stability

        print(f"✅ Model loaded successfully with {num_classes} classes")
        print(f"🖥️  Using device: {device}")

    except Exception as e:
        print(f"❌ Error loading model: {e}")
        # Don't raise the error, just log it
        # The app will continue without the model
        model = None
        class_names = []
        class_map = {}


# Helper class for dataset loading
class AnimalDataset(torch.utils.data.Dataset):
    """Simple dataset loader for animal images"""

    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.samples = []
        self.class_map = {}

        if not os.path.exists(root_dir):
            return

        # Get all class directories
        classes = [d for d in sorted(os.listdir(root_dir))
                   if os.path.isdir(os.path.join(root_dir, d))]

        self.class_map = {cls_name: idx for idx,
                          cls_name in enumerate(classes)}

        # Load all image paths
        for class_name in classes:
            class_dir = os.path.join(root_dir, class_name)
            for img_name in os.listdir(class_dir):
                if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(class_dir, img_name)
                    self.samples.append((img_path, self.class_map[class_name]))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        image = Image.open(img_path).convert('RGB')

        if self.transform:
            image = self.transform(image)

        return image, label


async def run_incremental_training():
    """
    Run reinforcement learning training that:
    1. Uses only the latest feedback data (old data already cleared)
    2. Updates model immediately on every feedback
    3. Focuses on the most recent corrections
    """
    try:
        print("🧠 Starting reinforcement learning training...")

        # Import training modules
        from torch.utils.data import DataLoader, ConcatDataset, WeightedRandomSampler
        from torch import nn, optim
        import random

        # Check if we have feedback data
        feedback_dir = "outputs/feedback_data"
        if not os.path.exists(feedback_dir) or not os.listdir(feedback_dir):
            print("⚠️  No feedback data found for training")
            return

        # Create dataset from feedback images (only latest feedback)
        feedback_dataset = AnimalDataset(feedback_dir, transform=transform)
        if len(feedback_dataset) == 0:
            print("⚠️  Feedback dataset is empty")
            return

        print(f"📊 Found {len(feedback_dataset)} latest feedback samples")

        # Get classes that need updates
        feedback_classes = set(feedback_dataset.class_map.keys())
        print(
            f"🎯 Classes requiring updates: {', '.join(sorted(feedback_classes))}")

        # Load original dataset for replay (prevent catastrophic forgetting)
        original_dataset = AnimalDataset("dataset", transform=transform)

        # Smart sampling: more samples from classes that got feedback
        replay_size = min(100, len(original_dataset))

        # Separate indices by whether they're in feedback classes
        feedback_class_indices = []
        other_class_indices = []

        for idx, (_, label) in enumerate(original_dataset.samples):
            class_name = list(original_dataset.class_map.keys())[
                list(original_dataset.class_map.values()).index(label)]
            if class_name in feedback_classes:
                feedback_class_indices.append(idx)
            else:
                other_class_indices.append(idx)

        # Sample more from feedback classes (70%), less from others (30%)
        feedback_replay = min(int(replay_size * 0.7),
                              len(feedback_class_indices))
        other_replay = replay_size - feedback_replay

        replay_indices = []
        if feedback_class_indices:
            replay_indices.extend(random.sample(feedback_class_indices, min(
                feedback_replay, len(feedback_class_indices))))
        if other_class_indices:
            replay_indices.extend(random.sample(
                other_class_indices, min(other_replay, len(other_class_indices))))

        replay_samples = torch.utils.data.Subset(
            original_dataset, replay_indices)

        # Combine feedback data with replay samples
        combined_dataset = ConcatDataset([feedback_dataset, replay_samples])
        train_loader = DataLoader(combined_dataset, batch_size=8, shuffle=True)

        print(
            f"📚 Training set: {len(feedback_dataset)} latest feedback + {len(replay_samples)} replay = {len(combined_dataset)} total")

        # Freeze all layers except the final classification layer
        # Note: model is accessed from global scope (no assignment needed)

        # Freeze all parameters first
        for param in model.parameters():
            param.requires_grad = False

        # Unfreeze only the final layer (fc or classifier)
        if hasattr(model, 'base_model') and hasattr(model.base_model, 'fc'):
            # For AnimalCNN with base_model.fc structure
            for param in model.base_model.fc.parameters():
                param.requires_grad = True
            print("🔓 Unfroze final classification layer (base_model.fc)")
        elif hasattr(model, 'fc'):
            # For models with direct fc
            for param in model.fc.parameters():
                param.requires_grad = True
            print("🔓 Unfroze final classification layer (fc)")

        model.train()

        # Use weighted cross entropy to focus on feedback classes
        criterion = nn.CrossEntropyLoss()

        # Only optimize parameters that require gradients
        trainable_params = filter(
            lambda p: p.requires_grad, model.parameters())
        # Slightly higher LR for last layer only
        optimizer = optim.Adam(trainable_params, lr=1e-4)

        # Train for few epochs
        num_epochs = 5  # More epochs since we're only training last layer
        for epoch in range(num_epochs):
            total_loss = 0
            correct = 0
            total = 0

            for images, labels in train_loader:
                images, labels = images.to(device), labels.to(device)

                optimizer.zero_grad()
                outputs = model(images)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                total_loss += loss.item() * images.size(0)
                _, predicted = outputs.max(1)
                correct += predicted.eq(labels).sum().item()
                total += labels.size(0)

            avg_loss = total_loss / total
            accuracy = 100.0 * correct / total
            print(
                f"📘 Epoch {epoch+1}/{num_epochs} | Loss: {avg_loss:.4f} | Accuracy: {accuracy:.2f}%")

        # Save updated model
        model_path = "outputs/best_model.pth"
        torch.save(model.state_dict(), model_path)
        print(f"✅ Model updated and saved to {model_path}")

        # Set model back to evaluation mode
        model.eval()

        # For reinforcement learning, don't backup - just clear for next feedback
        print("� Reinforcement training completed - ready for next feedback")

        print("✅ Reinforcement training completed successfully!")

    except Exception as e:
        print(f"❌ Error during incremental training: {e}")
        import traceback
        traceback.print_exc()


@app.on_event("startup")
async def startup_event():
    """Load model on startup with timeout handling"""
    import asyncio

    try:
        # Set a timeout for model loading
        await asyncio.wait_for(
            asyncio.to_thread(load_model),
            timeout=60.0  # 60 second timeout
        )
        print("✅ Startup completed successfully")
    except asyncio.TimeoutError:
        print("⚠️  Model loading timed out, continuing with basic setup")
        # Continue without model - endpoints will return appropriate errors
    except Exception as e:
        print(f"❌ Startup error: {e}")
        # Continue without model - endpoints will return appropriate errors


@app.get("/health")
async def health_check():
    """Health check endpoint for Render"""
    try:
        import psutil
        memory_info = psutil.virtual_memory()
        return {
            "status": "healthy",
            "model_loaded": model is not None,
            "classes_available": len(class_names) if class_names else 0,
            "device": str(device),
            "memory_usage_mb": round(memory_info.used / 1024 / 1024, 2),
            "memory_available_mb": round(memory_info.available / 1024 / 1024, 2),
            "memory_percent": round(memory_info.percent, 2)
        }
    except ImportError:
        return {
            "status": "healthy",
            "model_loaded": model is not None,
            "classes_available": len(class_names) if class_names else 0,
            "device": str(device),
            "memory_monitoring": "unavailable"
        }


@app.get("/api/health")
async def api_health_check():
    """Alternative health check endpoint for compatibility"""
    return await health_check()


@app.get("/api/classes")
async def api_get_classes():
    """Alternative classes endpoint for compatibility"""
    return await get_classes()


@app.post("/api/predict")
async def api_predict_image(file: UploadFile = File(...)):
    """Alternative predict endpoint for compatibility"""
    return await predict_image(file)


@app.post("/api/feedback")
async def api_feedback_image(
    file: UploadFile = File(...),
    predicted_class: str = Form(...),
    correct_class: str = Form(...),
    confidence: float = Form(...),
    comments: str = Form("")
):
    """Alternative feedback endpoint for compatibility"""
    # Call the main feedback function directly
    return await submit_feedback({
        "predicted_class": predicted_class,
        "correct_class": correct_class,
        "confidence": confidence,
        "comments": comments,
        "file": file
    })


@app.get("/")
async def root():
    """Serve the main HTML page"""
    try:
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return {"message": "Frontend not found. Please check if frontend/index.html exists."}


@app.get("/classes")
async def get_classes():
    """Get available animal classes"""
    if not class_names:
        raise HTTPException(status_code=500, detail="Model not loaded")

    return {
        "status": "success",
        "num_classes": len(class_names),
        "classes": class_names
    }


@app.get("/analytics")
async def get_analytics():
    """Get model performance analytics and metrics"""
    try:
        from src.analytics import MetricsTracker

        tracker = MetricsTracker()
        report = tracker.generate_report()

        return {
            "status": "success",
            "metrics": report
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate analytics: {str(e)}"
        )


@app.get("/analytics/dashboard")
async def get_analytics_dashboard():
    """Generate and return analytics dashboard image"""
    try:
        from src.analytics import generate_analytics_report
        import base64

        # Generate dashboard
        _, dashboard_path = generate_analytics_report()

        # Read and encode image
        with open(dashboard_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

        return {
            "status": "success",
            "dashboard": f"data:image/png;base64,{image_data}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate dashboard: {str(e)}"
        )


@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """Predict animal class from uploaded image"""
    try:
        # Check if model is loaded
        if model is None:
            raise HTTPException(
                status_code=503,
                detail="Model is still loading. Please try again in a few moments."
            )

        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400, detail="File must be an image")

        # Read image data
        image_data = await file.read()

        # Validate file size (max 10MB)
        if len(image_data) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400, detail="Image file too large (max 10MB)")

        # Open image and convert to RGB immediately
        with Image.open(io.BytesIO(image_data)) as img:
            # Convert to RGB and resize in one step to save memory
            img = img.convert('RGB')

            # Apply transformation
            image_tensor = transform(img).unsqueeze(0).to(device)

        # Clear image data from memory
        del image_data

        # Get prediction with memory optimization
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = F.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)

        predicted_class = class_names[predicted.item()]
        confidence_score = confidence.item()

        # Get top 3 predictions
        top3_probs, top3_indices = torch.topk(probabilities, 3, dim=1)
        top3_classes = [class_names[idx] for idx in top3_indices[0]]
        top3_scores = top3_probs[0].tolist()

        # Clear tensors from memory
        del image_tensor, outputs, probabilities, top3_probs, top3_indices

        # Determine base class (simplified logic)
        base_class = predicted_class.split(
            '_')[0] if '_' in predicted_class else predicted_class

        return {
            "prediction": predicted_class,
            "base_class": base_class,
            "confidence": round(confidence_score, 4),
            "breeds": top3_classes,
            "scores": [round(score, 4) for score in top3_scores]
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/visualize")
async def visualize_prediction(file: UploadFile = File(...)):
    """Generate Grad-CAM visualization for uploaded image"""
    try:
        # Check if model is loaded
        if model is None:
            raise HTTPException(
                status_code=503,
                detail="Model is still loading. Please try again in a few moments."
            )

        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400, detail="File must be an image")

        # Read image data
        image_data = await file.read()

        # Validate file size (max 10MB)
        if len(image_data) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400, detail="Image file too large (max 10MB)")

        # Open and process image
        original_image = Image.open(io.BytesIO(image_data)).convert('RGB')
        image_tensor = transform(original_image).unsqueeze(0).to(device)

        # Import Grad-CAM module
        try:
            from src.gradcam import generate_gradcam_visualization
            import cv2

            # Generate visualization
            result = generate_gradcam_visualization(
                model, image_tensor, original_image
            )

            # Convert overlaid image to base64
            overlaid_pil = Image.fromarray(result['overlaid_image'])
            buffer = io.BytesIO()
            overlaid_pil.save(buffer, format='JPEG')
            buffer.seek(0)
            overlaid_base64 = base64.b64encode(buffer.read()).decode('utf-8')

            # Get predicted class name
            predicted_class = class_names[result['predicted_class']]

            return {
                "predicted_class": predicted_class,
                "confidence": round(result['confidence'], 4),
                "visualization": f"data:image/jpeg;base64,{overlaid_base64}",
                "success": True
            }

        except ImportError as e:
            raise HTTPException(
                status_code=500,
                detail="Grad-CAM module not available. Install opencv-python.")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Visualization failed: {str(e)}")


@app.post("/feedback")
async def submit_feedback(feedback: dict):
    """Submit feedback for model correction with incremental learning"""
    try:
        # Extract feedback data from JSON
        predicted_class = feedback.get("predicted_class", "")
        correct_class = feedback.get("correct_class", "")
        confidence = feedback.get("confidence", 0.0)
        comments = feedback.get("comments", "")
        timestamp = feedback.get("timestamp", datetime.now().isoformat())
        image_data = feedback.get("image_data", None)  # Base64 image data

        # Clear old feedback data BEFORE saving new feedback
        feedback_dir = "outputs/feedback_data"
        if os.path.exists(feedback_dir):
            import shutil
            shutil.rmtree(feedback_dir)  # Remove all old feedback data
        os.makedirs(feedback_dir, exist_ok=True)

        # Save the image if provided
        image_path = None
        if image_data:
            try:
                # Remove data URL prefix if present
                if "," in image_data:
                    image_data = image_data.split(",")[1]

                import base64
                image_bytes = base64.b64decode(image_data)

                # Create directory for correct class
                class_dir = os.path.join(feedback_dir, correct_class)
                os.makedirs(class_dir, exist_ok=True)

                # Save image with timestamp
                timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_filename = f"{timestamp_str}_{predicted_class}_to_{correct_class}.jpg"
                image_path = os.path.join(class_dir, image_filename)

                with open(image_path, "wb") as f:
                    f.write(image_bytes)

                print(f"💾 Saved feedback image: {image_path}")
            except Exception as img_error:
                print(f"⚠️  Failed to save image: {img_error}")
                image_path = None

        # Create feedback data
        feedback_data = {
            "predicted_class": predicted_class,
            "correct_class": correct_class,
            "confidence": confidence,
            "comments": comments,
            "timestamp": timestamp,
            "image_path": image_path
        }

        # Save feedback to log file
        feedback_file = "outputs/correction_log.json"
        os.makedirs("outputs", exist_ok=True)

        existing_feedback = []
        if os.path.exists(feedback_file):
            try:
                with open(feedback_file, 'r') as f:
                    existing_feedback = json.load(f)
            except:
                existing_feedback = []

        existing_feedback.append(feedback_data)

        with open(feedback_file, 'w') as f:
            json.dump(existing_feedback, f, indent=2)

        feedback_id = len(existing_feedback)

        # Always trigger incremental training for reinforcement learning
        print("🔄 Triggering reinforcement training (every feedback)")
        try:
            import asyncio
            asyncio.create_task(run_incremental_training())
            response_data = {
                "status": "success",
                "message": "Feedback submitted - Model retraining initiated",
                "feedback_id": feedback_id,
                "image_saved": image_path is not None,
                "retraining_triggered": True
            }
        except Exception as train_error:
            print(f"⚠️  Failed to trigger training: {train_error}")
            response_data = {
                "status": "success",
                "message": "Feedback submitted successfully",
                "feedback_id": feedback_id,
                "image_saved": image_path is not None,
                "retraining_triggered": False
            }

        return response_data

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to submit feedback: {str(e)}")

# Mount static files
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

if __name__ == "__main__":
    import uvicorn
    import os

    # Get port from environment variable (for Render deployment)
    port = int(os.environ.get("PORT", 8000))

    # Bind to 0.0.0.0 to allow external connections
    uvicorn.run(app, host="0.0.0.0", port=port)
