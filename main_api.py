from fastapi import FastAPI, File, UploadFile, HTTPException, Form
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
from model import AnimalCNN
from data.dataloader import AnimalDataset

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

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Global variables for model and class names
model = None
class_names = []
device = None
transform = None

@app.on_event("startup")
async def load_model():
    """Load the trained model and setup on startup"""
    global model, class_names, device, transform
    
    print("🚀 Loading animal classification model...")
    
    # Setup device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🖥️ Using device: {device}")
    
    # Setup transforms
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])
    
    # Load class names from dataset
    try:
        dataset = AnimalDataset("dataset", transform)
        class_names = list(dataset.class_map.keys())
        num_classes = len(class_names)
        print(f"📦 Loaded {len(class_names)} animal classes")
    except Exception as e:
        print(f"⚠️ Warning: Could not load dataset classes: {e}")
        # Fallback to generic classes if dataset loading fails
        class_names = [f"Class_{i}" for i in range(75)]  # Assuming 75 classes
        num_classes = 75
    
    # Load the trained model
    try:
        model = AnimalCNN(num_classes=num_classes).to(device)
        checkpoint = torch.load("outputs/best_model.pth", map_location=device)
        # The checkpoint contains the state dict directly, not wrapped in 'model_state_dict'
        model.load_state_dict(checkpoint)
        model.eval()
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        raise HTTPException(status_code=500, detail="Failed to load model")

@app.get("/")
async def root():
    """Serve the frontend interface"""
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "num_classes": len(class_names) if class_names else 0,
        "device": str(device) if device else "unknown"
    }

@app.get("/classes")
async def get_classes():
    """Get list of available animal classes"""
    return {
        "classes": class_names,
        "count": len(class_names)
    }

@app.post("/predict")
async def predict_animal(file: UploadFile = File(...)):
    """Predict animal class from uploaded image"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and process image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Apply transforms
        image_tensor = transform(image).unsqueeze(0).to(device)
        
        # Get prediction
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = F.softmax(outputs, dim=1)
            predicted_class_idx = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class_idx].item()
        
        # Get top 3 predictions
        top3_probs, top3_indices = torch.topk(probabilities[0], 3)
        
        # Format response
        prediction = class_names[predicted_class_idx]
        
        # Determine base animal category (simplified logic)
        base_category = get_base_category(prediction)
        
        # Get breed suggestions
        breeds = [class_names[idx.item()] for idx in top3_indices]
        
        return {
            "prediction": prediction,
            "base_class": base_category,
            "confidence": round(confidence, 4),
            "breeds": breeds,
            "top_predictions": [
                {
                    "class": class_names[idx.item()],
                    "confidence": round(prob.item(), 4)
                }
                for prob, idx in zip(top3_probs, top3_indices)
            ]
        }
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

def get_base_category(animal_name: str) -> str:
    """Determine the base animal category from the specific breed/type"""
    animal_name_lower = animal_name.lower()
    
    # Define base categories
    base_categories = {
        "dog": ["dog", "labrador", "german shepherd", "golden retriever", "pug"],
        "cat": ["cat", "persian", "siamese", "maine coon", "bengal"],
        "bear": ["bear", "grizzly", "polar", "black", "asiatic"],
        "elephant": ["elephant", "african", "asian"],
        "lion": ["lion", "african", "asiatic"],
        "tiger": ["tiger", "bengal", "siberian"],
        "horse": ["horse", "arabian", "thoroughbred", "clydesdale"],
        "cow": ["cow", "angus", "jersey", "domestic"],
        "bird": ["bird", "eagle", "parrot", "owl", "penguin"],
        "deer": ["deer", "red", "mule"],
        "giraffe": ["giraffe", "masai", "reticulated"],
        "zebra": ["zebra", "plains", "mountain"],
        "kangaroo": ["kangaroo", "red", "eastern grey"],
        "dolphin": ["dolphin", "bottlenose", "spinner"],
        "panda": ["panda", "giant", "red"]
    }
    
    for category, keywords in base_categories.items():
        if any(keyword in animal_name_lower for keyword in keywords):
            return category.title()
    
    # Default to the first word if no match found
    return animal_name.split()[0].title()

@app.post("/feedback")
async def submit_feedback(
    correction: str = Form(...),
    original_prediction: str = Form(...),
    image_hash: str = Form(None)
):
    """Submit feedback/correction for a prediction"""
    try:
        # Load existing feedback
        feedback_file = "outputs/correction_log.json"
        feedback_data = []
        
        if os.path.exists(feedback_file):
            with open(feedback_file, 'r') as f:
                feedback_data = json.load(f)
        
        # Add new feedback
        from datetime import datetime
        feedback_entry = {
            "original_prediction": original_prediction,
            "correction": correction,
            "image_hash": image_hash,
            "timestamp": datetime.now().isoformat()
        }
        
        feedback_data.append(feedback_entry)
        
        # Save updated feedback
        with open(feedback_file, 'w') as f:
            json.dump(feedback_data, f, indent=2)
        
        return {"message": "Feedback submitted successfully", "status": "success"}
        
    except Exception as e:
        print(f"❌ Feedback error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to submit feedback: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
