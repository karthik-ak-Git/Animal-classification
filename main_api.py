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
from data.dataloader import AnimalDataset
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

# Image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def load_model():
    """Load the trained model and class information"""
    global model, class_names, class_map
    
    try:
        # Load dataset to get class information
        dataset = AnimalDataset("dataset", transform=None)
        class_names = list(dataset.class_map.keys())
        class_map = dataset.class_map
        
        # Initialize model
        num_classes = len(class_names)
        model = AnimalCNN(num_classes=num_classes)
        
        # Load trained weights if available
        model_path = "outputs/best_model.pth"
        if os.path.exists(model_path):
            model.load_state_dict(torch.load(model_path, map_location=device))
            print(f"✅ Model loaded from {model_path}")
        else:
            print("⚠️  No trained model found. Using untrained model.")
        
        model.to(device)
        model.eval()
        
        print(f"✅ Model loaded successfully with {num_classes} classes")
        print(f"🖥️  Using device: {device}")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        raise e

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    load_model()

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

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "num_classes": len(class_names) if class_names else 0,
        "device": str(device)
    }

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """Predict animal class from uploaded image"""
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and process image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Apply transformation
        image_tensor = transform(image).unsqueeze(0).to(device)
        
        # Get prediction
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
        
        # Determine base class (simplified logic)
        base_class = predicted_class.split('_')[0] if '_' in predicted_class else predicted_class
        
        return {
            "prediction": predicted_class,
            "base_class": base_class,
            "confidence": round(confidence_score, 4),
            "breeds": top3_classes,
            "scores": [round(score, 4) for score in top3_scores]
        }
        
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
app.mount("/static", StaticFiles(directory="frontend"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
