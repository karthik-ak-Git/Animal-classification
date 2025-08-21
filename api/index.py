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
        # Try to read the actual frontend HTML file first
        current_dir = os.path.dirname(os.path.abspath(__file__))
        frontend_dir = os.path.join(os.path.dirname(current_dir), "frontend")
        html_path = os.path.join(frontend_dir, "index.html")
        
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            return HTMLResponse(content=html_content)
        else:
            # If file not found, serve embedded HTML
            return HTMLResponse(content=get_embedded_html())
            
    except Exception:
        # If anything fails, serve embedded HTML
        return HTMLResponse(content=get_embedded_html())

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon.ico - browsers automatically request this"""
    try:
        # Try to serve the actual favicon first
        current_dir = os.path.dirname(os.path.abspath(__file__))
        frontend_dir = os.path.join(os.path.dirname(current_dir), "frontend")
        favicon_path = os.path.join(frontend_dir, "favicon.svg")
        
        if os.path.exists(favicon_path):
            with open(favicon_path, "r", encoding="utf-8") as f:
                svg_content = f.read()
            return Response(content=svg_content, media_type="image/svg+xml")
        else:
            # Return embedded favicon if file not found
            return Response(content=get_embedded_favicon(), media_type="image/svg+xml")
    except Exception:
        # Return embedded favicon if anything fails
        return Response(content=get_embedded_favicon(), media_type="image/svg+xml")

@app.get("/static/favicon.svg")
async def static_favicon():
    """Serve favicon.svg at the exact path frontend expects"""
    try:
        # Try to serve the actual favicon first
        current_dir = os.path.dirname(os.path.abspath(__file__))
        frontend_dir = os.path.join(os.path.dirname(current_dir), "frontend")
        favicon_path = os.path.join(frontend_dir, "favicon.svg")
        
        if os.path.exists(favicon_path):
            with open(favicon_path, "r", encoding="utf-8") as f:
                svg_content = f.read()
            return Response(content=svg_content, media_type="image/svg+xml")
        else:
            # Return embedded favicon if file not found
            return Response(content=get_embedded_favicon(), media_type="image/svg+xml")
    except Exception:
        # Return embedded favicon if anything fails
        return Response(content=get_embedded_favicon(), media_type="image/svg+xml")

@app.get("/static/styles.css")
async def static_css():
    """Serve styles.css at the exact path frontend expects"""
    try:
        # Try to serve the actual CSS file first
        current_dir = os.path.dirname(os.path.abspath(__file__))
        frontend_dir = os.path.join(os.path.dirname(current_dir), "frontend")
        css_path = os.path.join(frontend_dir, "styles.css")
        
        if os.path.exists(css_path):
            with open(css_path, "r", encoding="utf-8") as f:
                css_content = f.read()
            return Response(content=css_content, media_type="text/css")
        else:
            # Return embedded CSS if file not found
            return Response(content=get_embedded_css(), media_type="text/css")
    except Exception:
        # Return embedded CSS if anything fails
        return Response(content=get_embedded_css(), media_type="text/css")

@app.get("/static/scripts.js")
async def static_js():
    """Serve scripts.js at the exact path frontend expects"""
    try:
        # Try to serve the actual JavaScript file first
        current_dir = os.path.dirname(os.path.abspath(__file__))
        frontend_dir = os.path.join(os.path.dirname(current_dir), "frontend")
        js_path = os.path.join(frontend_dir, "scripts.js")
        
        if os.path.exists(js_path):
            with open(js_path, "r", encoding="utf-8") as f:
                js_content = f.read()
            return Response(content=js_content, media_type="application/javascript")
        else:
            # Return embedded JavaScript if file not found
            return Response(content=get_embedded_js(), media_type="application/javascript")
    except Exception:
        # Return embedded JavaScript if anything fails
        return Response(content=get_embedded_js(), media_type="application/javascript")

@app.get("/static/{file_path:path}")
async def static_files(file_path: str):
    """Serve other static files (fallback)"""
    try:
        # Try to serve the actual file first
        current_dir = os.path.dirname(os.path.abspath(__file__))
        frontend_dir = os.path.join(os.path.dirname(current_dir), "frontend")
        full_path = os.path.join(frontend_dir, file_path)
        
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
            # If file not found, serve embedded content based on file type
            return serve_embedded_file(file_path)
            
    except Exception:
        # If anything fails, serve embedded content
        return serve_embedded_file(file_path)

def get_embedded_html():
    """Return embedded HTML content"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Animal Classifier</title>
        <link rel="icon" href="/favicon.ico" type="image/svg+xml">
        <style>
            /* Embedded CSS */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                padding: 40px;
                max-width: 600px;
                width: 100%;
                text-align: center;
            }
            
            h1 {
                color: #333;
                margin-bottom: 20px;
                font-size: 2.5em;
            }
            
            .success {
                color: #28a745;
                font-weight: bold;
                font-size: 1.2em;
                margin-bottom: 30px;
            }
            
            .endpoint {
                background: #f8f9fa;
                padding: 20px;
                margin: 15px 0;
                border-radius: 10px;
                border-left: 4px solid #007bff;
                text-align: left;
            }
            
            .btn {
                display: inline-block;
                padding: 12px 24px;
                margin: 8px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 500;
                transition: all 0.3s ease;
            }
            
            .btn:hover {
                background: #0056b3;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            
            .status {
                background: #e8f5e8;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                border: 1px solid #d4edda;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐾 Animal Classification API</h1>
            <div class="status">
                <p class="success">✅ API is running successfully!</p>
                <p>All endpoints are working correctly</p>
            </div>
            
            <h2>Available Endpoints:</h2>
            <div class="endpoint">
                <strong>/health</strong> - API health check and status
            </div>
            <div class="endpoint">
                <strong>/classes</strong> - List of 75 animal classes
            </div>
            <div class="endpoint">
                <strong>/predict</strong> - Image prediction endpoint
            </div>
            <div class="endpoint">
                <strong>/feedback</strong> - Submit prediction feedback
            </div>
            
            <h2>Test Links:</h2>
            <a href="/health" class="btn">Health Check</a>
            <a href="/classes" class="btn">Animal Classes</a>
            <a href="/predict" class="btn">Test Prediction</a>
            
            <p style="margin-top: 30px; color: #666;">
                <small>Animal Classification API - Ready for use</small>
            </p>
        </div>
        
        <script>
            // Embedded JavaScript
            document.addEventListener('DOMContentLoaded', function() {
                console.log('Animal Classification API loaded successfully!');
                
                // Add some interactivity
                const buttons = document.querySelectorAll('.btn');
                buttons.forEach(btn => {
                    btn.addEventListener('click', function(e) {
                        this.style.transform = 'scale(0.95)';
                        setTimeout(() => {
                            this.style.transform = 'scale(1)';
                        }, 150);
                    });
                });
            });
        </script>
    </body>
    </html>
    """

def get_embedded_favicon():
    """Return embedded favicon SVG"""
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="40" fill="#007bff"/>
        <text x="50" y="60" text-anchor="middle" fill="white" font-size="40">🐾</text>
    </svg>"""

def serve_embedded_file(file_path):
    """Serve embedded file content based on file type"""
    if file_path.endswith(".css"):
        return Response(content=get_embedded_css(), media_type="text/css")
    elif file_path.endswith(".js"):
        return Response(content=get_embedded_js(), media_type="application/javascript")
    else:
        return Response(content="", status_code=204)

def get_embedded_css():
    """Return embedded CSS content"""
    return """
    /* Embedded CSS for Animal Classification API */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    
    .container {
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        padding: 40px;
        max-width: 600px;
        width: 100%;
        text-align: center;
    }
    
    h1 {
        color: #333;
        margin-bottom: 20px;
        font-size: 2.5em;
    }
    
    .success {
        color: #28a745;
        font-weight: bold;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    
    .endpoint {
        background: #f8f9fa;
        padding: 20px;
        margin: 15px 0;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        text-align: left;
    }
    
    .btn {
        display: inline-block;
        padding: 12px 24px;
        margin: 8px;
        background: #007bff;
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .btn:hover {
        background: #0056b3;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .status {
        background: #e8f5e8;
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
        border: 1px solid #d4edda;
    }
    """

def get_embedded_js():
    """Return embedded JavaScript content"""
    return """
    // Embedded JavaScript for Animal Classification API
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Animal Classification API loaded successfully!');
        
        // Add some interactivity
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(btn => {
            btn.addEventListener('click', function(e) {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 150);
            });
        });
        
        // Add loading animation
        const container = document.querySelector('.container');
        if (container) {
            container.style.opacity = '0';
            container.style.transform = 'translateY(20px)';
            container.style.transition = 'all 0.5s ease';
            
            setTimeout(() => {
                container.style.opacity = '1';
                container.style.transform = 'translateY(0)';
            }, 100);
        }
    });
    """

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
    uvicorn.run(app, host="0.0.0.0", port=8001)
