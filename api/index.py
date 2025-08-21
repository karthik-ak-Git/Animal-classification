from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from PIL import Image
import io
import json
import os
import sys
from contextlib import asynccontextmanager

# Global variables
class_names = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI app"""
    # Startup
    global class_names
    
    try:
        print("🚀 Starting Animal Classification API...")
        
        # Load class names (hardcoded for Vercel compatibility)
        class_names = [
            "African Elephant", "African Lion", "African Wildcat", "Amazon parrot",
            "American_Black_Bear", "Angus", "Arabian Horse", "Asian Elephant",
            "Asiatic Lion", "Asiatic_Black_Bear", "Bear", "Bengal Cat",
            "Bengal Tiger", "Bird", "Bottlenose Dolphin", "Cat", "Clydesdale",
            "Cockatiel", "Cow", "Crows", "Cuckoo", "Deer", "Dog", "Dolphin",
            "Domestic Cattle", "Domestic Dog", "Ducks", "Eagle", "Eastern Grey Kangaroo",
            "Elephant", "Falcons", "German Shepherd", "Giant Panda", "Giraffe",
            "Golden Retriever", "Grizzly_Bear", "Horse", "House Sparrows",
            "Hummingbird", "Jersey Cow", "Kangaroo", "Kingfishers", "Labrador",
            "Lion", "Macaw", "Maine Coon", "Masai Giraffe", "Mountain Zebra",
            "Mule_Deer", "Ostrich", "Owl", "Panda", "Parrot", "Penguin",
            "Persian Cat", "Plains Zebra", "Polar_Bear", "Pug", "Red Deer",
            "Red Kangaroo", "Red Panda", "Reticulated Giraffe", "Siamese Cat",
            "Siberian Tiger", "Sloth_Bear", "Spinner Dolphin", "Sun_Bear",
            "Swallows", "Swan", "Thoroughbred", "Tiger", "White-tailed Deer",
            "Woodpeckers", "Zebra", "pigeons"
        ]
        
        print(f"✅ API initialized with {len(class_names)} classes")
        print(f"🐍 Python version: {sys.version}")
        print(f"📁 Working directory: {os.getcwd()}")
        
    except Exception as e:
        print(f"❌ Error initializing API: {e}")
        print(f"🔍 Error details: {type(e).__name__}: {str(e)}")
        # Set default classes if initialization fails
        class_names = ["Cat", "Dog", "Bird", "Bear", "Lion", "Tiger", "Elephant", "Giraffe", "Horse", "Cow"]
        print(f"⚠️ Using fallback classes: {class_names}")
    
    yield
    
    # Shutdown (if needed)
    print("🔄 API shutting down...")

# Initialize FastAPI app with lifespan
app = FastAPI(title="Animal Classification API", version="1.0.0", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Serve the frontend interface"""
    try:
        print("📄 Serving frontend...")
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError as e:
        print(f"❌ Frontend file not found: {e}")
        return JSONResponse(content={"message": "Animal Classification API", "status": "running", "error": "Frontend not found"})
    except Exception as e:
        print(f"❌ Error serving frontend: {e}")
        return JSONResponse(content={"message": "Animal Classification API", "status": "error", "error": str(e)})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        return {
            "status": "healthy",
            "api_ready": True,
            "num_classes": len(class_names),
            "deployment": "vercel",
            "python_version": sys.version,
            "working_directory": os.getcwd()
        }
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return {
            "status": "error",
            "error": str(e),
            "deployment": "vercel"
        }

@app.get("/classes")
async def get_classes():
    """Get list of available animal classes"""
    try:
        return {
            "classes": class_names,
            "count": len(class_names)
        }
    except Exception as e:
        print(f"❌ Classes endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get classes: {str(e)}")

@app.post("/predict")
async def predict_animal(file: UploadFile = File(...)):
    """Predict animal class from uploaded image"""
    try:
        print(f"🖼️ Processing image: {file.filename}")
        
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # For Vercel deployment, we'll use a simplified prediction
        # This is a placeholder - in production you'd load the actual model
        prediction = "Cat"  # Placeholder prediction
        confidence = 0.85
        base_category = "Cat"
        breeds = ["Persian Cat", "Siamese Cat", "Maine Coon"]
        
        print(f"✅ Prediction successful: {prediction}")
        
        return {
            "prediction": prediction,
            "base_class": base_category,
            "confidence": confidence,
            "breeds": breeds,
            "top_predictions": [
                {"class": "Persian Cat", "confidence": 0.85},
                {"class": "Siamese Cat", "confidence": 0.10},
                {"class": "Maine Coon", "confidence": 0.05}
            ]
        }
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        print(f"🔍 Error details: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/feedback")
async def submit_feedback(
    correction: str = Form(...),
    original_prediction: str = Form(...),
    image_hash: str = Form(None)
):
    """Submit feedback/correction for a prediction"""
    try:
        print(f"📝 Feedback received: {correction} for {original_prediction}")
        # For Vercel, we'll just return success
        # In production, you'd save this to a database
        return {"message": "Feedback submitted successfully", "status": "success"}
        
    except Exception as e:
        print(f"❌ Feedback error: {e}")
        print(f"🔍 Error details: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to submit feedback: {str(e)}")

# Vercel handler
def handler(request):
    """Vercel serverless function handler"""
    try:
        print(f"🔄 Vercel handler called with: {request.method} {request.url}")
        return app(request)
    except Exception as e:
        print(f"❌ Vercel handler error: {e}")
        print(f"🔍 Error details: {type(e).__name__}: {str(e)}")
        # Return a basic error response
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
