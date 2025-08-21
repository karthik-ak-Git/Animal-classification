from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
import json
import os

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

# Animal classes data
ANIMAL_CLASSES = [
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

@app.get("/")
async def root():
    """Serve the main frontend interface"""
    try:
        # Read the actual frontend HTML file
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Return the actual frontend content
        return HTMLResponse(content=html_content)
        
    except FileNotFoundError:
        # Fallback if frontend file not found
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Animal Classification API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; text-align: center; background: #f5f5f5; }
                .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .endpoint { background: #f0f8ff; padding: 15px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #007bff; }
                .success { color: #28a745; font-weight: bold; }
                .btn { display: inline-block; padding: 10px 20px; margin: 5px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
                .btn:hover { background: #0056b3; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🐾 Animal Classification API</h1>
                <p class="success">✅ API is running successfully!</p>
                
                <h2>Available Endpoints:</h2>
                <div class="endpoint">
                    <strong>/health</strong> - API health check
                </div>
                <div class="endpoint">
                    <strong>/classes</strong> - List of animal classes
                </div>
                <div class="endpoint">
                    <strong>/predict</strong> - Image prediction
                </div>
                
                <h2>Test Links:</h2>
                <a href="/health" class="btn">Health Check</a>
                <a href="/classes" class="btn">Animal Classes</a>
                <a href="/predict" class="btn">Test Prediction</a>
                
                <p><small>Animal Classification API - Ready for use</small></p>
            </div>
        </body>
        </html>
        """)

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon"""
    try:
        # Try to serve the actual favicon
        favicon_path = "frontend/favicon.svg"
        if os.path.exists(favicon_path):
            with open(favicon_path, "r", encoding="utf-8") as f:
                svg_content = f.read()
            return Response(content=svg_content, media_type="image/svg+xml")
        else:
            # Return a simple SVG favicon if file not found
            svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" fill="#007bff"/>
                <text x="50" y="60" text-anchor="middle" fill="white" font-size="40">🐾</text>
            </svg>"""
            return Response(content=svg_content, media_type="image/svg+xml")
    except Exception:
        # Return empty response if anything fails
        return Response(content="", status_code=204)

@app.get("/static/{file_path:path}")
async def static_files(file_path: str):
    """Serve static files (CSS, JS, images)"""
    try:
        # Construct the full path
        full_path = f"frontend/{file_path}"
        
        # Check if file exists
        if os.path.exists(full_path):
            # Determine content type based on file extension
            content_type = "text/plain"
            if file_path.endswith(".css"):
                content_type = "text/css"
            elif file_path.endswith(".js"):
                content_type = "application/javascript"
            elif file_path.endswith(".svg"):
                content_type = "image/svg+xml"
            elif file_path.endswith(".png"):
                content_type = "image/png"
            elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
                content_type = "image/jpeg"
            
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            return Response(content=content, media_type=content_type)
        else:
            # Return empty response for missing files
            return Response(content="", status_code=204)
    except Exception:
        # Return empty response if anything fails
        return Response(content="", status_code=204)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "api_ready": True,
        "num_classes": len(ANIMAL_CLASSES),
        "deployment": "local",
        "version": "1.0.0"
    }

@app.get("/classes")
async def get_classes():
    """Get list of available animal classes"""
    return {
        "classes": ANIMAL_CLASSES,
        "count": len(ANIMAL_CLASSES),
        "status": "success"
    }

@app.post("/predict")
async def predict_animal(file: UploadFile = File(...)):
    """Predict animal class from uploaded image"""
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # For now, return a placeholder prediction
        # In production, you'd load your trained model here
        prediction = "Cat"  # Placeholder prediction
        confidence = 0.85
        base_category = "Cat"
        breeds = ["Persian Cat", "Siamese Cat", "Maine Coon"]
        
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
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/feedback")
async def submit_feedback(
    correction: str = Form(...),
    original_prediction: str = Form(...),
    image_hash: str = Form(None)
):
    """Submit feedback/correction for a prediction"""
    return {"message": "Feedback submitted successfully", "status": "success"}

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
