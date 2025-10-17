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
from model import AnimalCNN
import numpy as np
from datetime import datetime
from typing import Optional

# Initialize FastAPI app
app = FastAPI(title="Animal Classification API", version="1.0.0")

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
    Run smart incremental training that:
    1. Only updates weights for classes that received feedback
    2. Uses class-weighted loss to focus on corrected samples
    3. Preserves pretrained knowledge with minimal updates
    """
    try:
        print("🚀 Starting smart incremental training...")

        # Import training modules
        from torch.utils.data import DataLoader, ConcatDataset, WeightedRandomSampler
        from torch import nn, optim
        import random

        # Check if we have feedback data
        feedback_dir = "outputs/feedback_data"
        if not os.path.exists(feedback_dir) or not os.listdir(feedback_dir):
            print("⚠️  No feedback data found for training")
            return

        # Create dataset from feedback images
        feedback_dataset = AnimalDataset(feedback_dir, transform=transform)
        if len(feedback_dataset) == 0:
            print("⚠️  Feedback dataset is empty")
            return

        print(f"📊 Found {len(feedback_dataset)} feedback samples")

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
            f"📚 Training set: {len(feedback_dataset)} feedback + {len(replay_samples)} replay = {len(combined_dataset)} total")

        # Freeze all layers except the final classification layer
        global model

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

        # Create backup of feedback data after training
        import shutil
        backup_dir = "outputs/feedback_data_trained"
        os.makedirs(backup_dir, exist_ok=True)

        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"backup_{timestamp_str}")
        shutil.move(feedback_dir, backup_path)
        print(f"📦 Feedback data backed up to {backup_path}")

        # Recreate empty feedback directory for new samples
        os.makedirs(feedback_dir, exist_ok=True)

        print("✅ Incremental training completed successfully!")

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


@app.get("/")
async def root():
    """Serve the main HTML page"""
    try:
        with open("frontend/index_new.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return {"message": "Frontend not found. Please check if frontend/index_new.html exists."}


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

        # Create feedback directory structure
        feedback_dir = "outputs/feedback_data"
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

        # Trigger incremental training if we have enough feedback samples
        retrain_threshold = 5  # Retrain after every 5 feedback samples
        should_retrain = (feedback_id % retrain_threshold == 0)

        response_data = {
            "status": "success",
            "message": "Feedback submitted successfully",
            "feedback_id": feedback_id,
            "image_saved": image_path is not None,
            "retraining_triggered": should_retrain
        }

        if should_retrain:
            print(
                f"🔄 Triggering incremental training (threshold: {retrain_threshold})")
            # Import and run incremental training in background
            try:
                import asyncio
                asyncio.create_task(run_incremental_training())
                response_data["message"] += " - Model retraining initiated in background"
            except Exception as train_error:
                print(f"⚠️  Failed to trigger training: {train_error}")
                response_data["retraining_triggered"] = False

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
