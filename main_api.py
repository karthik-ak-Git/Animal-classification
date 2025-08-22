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
from pathlib import Path
from model import AnimalCNN
import numpy as np
from datetime import datetime

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
    transforms.Resize((224, 224), antialias=True),  # Use antialias for better quality
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
            class_map = {cls_name: idx for idx, cls_name in enumerate(class_names)}
            print(f"📊 Found {len(class_names)} animal classes")
        else:
            print("⚠️  Dataset directory not found")
            class_names = []
            class_map = {}
        
        # Initialize model
        num_classes = len(class_names) if class_names else 10  # Default fallback
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
        
        # Enable memory efficient inference
        if hasattr(model, 'half') and device.type == 'cuda':
            model.half()  # Use half precision only on GPU
        
        print(f"✅ Model loaded successfully with {num_classes} classes")
        print(f"🖥️  Using device: {device}")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        # Don't raise the error, just log it
        # The app will continue without the model
        model = None
        class_names = []
        class_map = {}

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
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image data
        image_data = await file.read()
        
        # Validate file size (max 10MB)
        if len(image_data) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image file too large (max 10MB)")
        
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
        base_class = predicted_class.split('_')[0] if '_' in predicted_class else predicted_class
        
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
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/feedback")
async def submit_feedback(
    original_prediction: str = Form(...),
    correct_class: str = Form(...),
    confidence: float = Form(...),
    image_data: str = Form(...)
):
    """Submit feedback for model correction"""
    try:
        # Create feedback data
        feedback_data = {
            "original_prediction": original_prediction,
            "correct_class": correct_class,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
            "image_data": image_data[:100] + "..." if len(image_data) > 100 else image_data  # Truncate long data
        }
        
        # Save feedback to file (you can modify this to save to database)
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
        
        return {
            "status": "success",
            "message": "Feedback submitted successfully",
            "feedback_id": len(existing_feedback)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit feedback: {str(e)}")

# Mount static files
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get port from environment variable (for Render deployment)
    port = int(os.environ.get("PORT", 8000))
    
    # Bind to 0.0.0.0 to allow external connections
    uvicorn.run(app, host="0.0.0.0", port=port)
