from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests to debug 404 issues"""
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

@app.get("/")
async def root():
    """Serve the main frontend interface"""
    logger.info("Serving root endpoint")
    # Always serve embedded HTML for Vercel compatibility
    return HTMLResponse(content=get_embedded_html())

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon.ico - browsers automatically request this"""
    logger.info("Serving favicon.ico")
    return Response(content=get_embedded_favicon(), media_type="image/svg+xml")

@app.get("/static/favicon.svg")
async def static_favicon():
    """Serve favicon.svg at the exact path frontend expects"""
    logger.info("Serving static/favicon.svg")
    return Response(content=get_embedded_favicon(), media_type="image/svg+xml")

@app.get("/static/styles.css")
async def static_css():
    """Serve styles.css at the exact path frontend expects"""
    logger.info("Serving static/styles.css")
    return Response(content=get_embedded_css(), media_type="text/css")

@app.get("/static/scripts.js")
async def static_js():
    """Serve scripts.js at the exact path frontend expects"""
    logger.info("Serving static/scripts.js")
    return Response(content=get_embedded_js(), media_type="application/javascript")

@app.get("/static/{file_path:path}")
async def static_files(file_path: str):
    """Serve other static files (fallback)"""
    logger.info(f"Serving static file: {file_path}")
    return serve_embedded_file(file_path)

def get_embedded_html():
    """Return embedded HTML content - Vercel compatible"""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Animal Classifier</title>
    <link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <link href="/static/styles.css" rel="stylesheet">
</head>
<body>
    <div class="app-container">
        <header class="app-header">
            <div class="container">
                <div class="header-content">
                    <h1 class="app-title">
                        <span class="title-icon">🐾</span>
                        Animal Classifier
                    </h1>
                    <p class="app-subtitle">AI-powered animal and breed identification</p>
                </div>
            </div>
        </header>
        
        <main class="app-main">
            <div class="container">
                <section class="upload-section">
                    <div class="upload-card">
                        <div class="upload-area" id="upload-area">
                            <div class="upload-content">
                                <div class="upload-icon">
                                    <i class="bi bi-cloud-upload"></i>
                                </div>
                                <h3 class="upload-title">Upload an image</h3>
                                <p class="upload-description">Drag and drop or click to select</p>
                                <input type="file" id="image-upload" class="form-control d-none" accept="image/*">
                                <button class="btn btn-primary btn-upload" onclick="document.getElementById('image-upload').click()">
                                    <i class="bi bi-upload me-2"></i>Choose Image
                                </button>
                            </div>
                        </div>
                        
                        <div id="image-preview-container" class="image-preview-container d-none">
                            <div class="preview-wrapper">
                                <img id="image-preview" class="image-preview" alt="Preview">
                                <button class="btn btn-remove" onclick="removeImage()" title="Remove image">
                                    <i class="bi bi-x-lg"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                    
                    <div class="analyze-section">
                        <button id="predict-button" class="btn btn-primary btn-analyze" disabled>
                            <i class="bi bi-search me-2"></i>Analyze Image
                        </button>
                    </div>
                </section>
                
                <section id="result-container" class="result-section d-none">
                    <div class="prediction-card">
                        <div class="prediction-header">
                            <div class="ai-indicator">
                                <i class="bi bi-robot"></i>
                                <span>AI Analysis</span>
                            </div>
                        </div>
                        
                        <div class="prediction-content">
                            <div id="main-class-display" class="main-class-display">
                                <div class="class-emoji" id="class-emoji"></div>
                                <div class="class-text">
                                    <div class="main-class-label" id="main-class-label"></div>
                                </div>
                            </div>
                            
                            <div id="breed-display" class="breed-display d-none">
                                <div class="breed-arrow">→</div>
                                <div class="breed-text">
                                    <div class="breed-name" id="breed-name"></div>
                                    <div class="confidence-text" id="confidence-text"></div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="prediction-actions">
                            <button id="copy-breed-btn" class="btn btn-outline-primary btn-sm d-none">
                                <i class="bi bi-clipboard me-1"></i>Copy Breed
                            </button>
                            <button id="show-feedback-btn" class="btn btn-outline-secondary btn-sm">
                                <i class="bi bi-chat-dots me-1"></i>Report Incorrect
                            </button>
                        </div>
                    </div>
                    
                    <div id="feedback-card" class="feedback-card collapse">
                        <div class="feedback-header">
                            <h6>Help improve the model</h6>
                            <p>What animal is this actually?</p>
                        </div>
                        <div class="feedback-form">
                            <select id="correction-dropdown" class="form-select">
                                <option value="">Select correct class...</option>
                            </select>
                            <button id="submit-correction" class="btn btn-success">
                                <i class="bi bi-check me-1"></i>Submit Correction
                            </button>
                        </div>
                    </div>
                </section>
            </div>
        </main>
        
        <div id="toast-container" class="toast-container"></div>
    </div>
    
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/scripts.js"></script>
</body>
</html>"""

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
    .app-container {
        min-height: 100vh;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .app-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem 0;
        margin-bottom: 3rem;
    }
    
    .header-content {
        text-align: center;
    }
    
    .app-title {
        font-size: 3rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .title-icon {
        font-size: 3.5rem;
        margin-right: 1rem;
    }
    
    .app-subtitle {
        font-size: 1.2rem;
        color: #718096;
        font-weight: 400;
    }
    
    .upload-section {
        max-width: 800px;
        margin: 0 auto 3rem;
    }
    
    .upload-card {
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        padding: 3rem;
        margin-bottom: 2rem;
    }
    
    .upload-area {
        border: 3px dashed #e2e8f0;
        border-radius: 15px;
        padding: 4rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .upload-area:hover {
        border-color: #667eea;
        background: #f7fafc;
    }
    
    .upload-icon {
        font-size: 4rem;
        color: #667eea;
        margin-bottom: 1rem;
    }
    
    .upload-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .upload-description {
        color: #718096;
        margin-bottom: 2rem;
    }
    
    .btn-upload {
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 500;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        transition: all 0.3s ease;
    }
    
    .btn-upload:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }
    
    .image-preview-container {
        margin-top: 2rem;
    }
    
    .preview-wrapper {
        position: relative;
        display: inline-block;
    }
    
    .image-preview {
        max-width: 300px;
        max-height: 300px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .btn-remove {
        position: absolute;
        top: -10px;
        right: -10px;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: #e53e3e;
        border: none;
        color: white;
        font-size: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .btn-remove:hover {
        background: #c53030;
        transform: scale(1.1);
    }
    
    .analyze-section {
        text-align: center;
    }
    
    .btn-analyze {
        padding: 1.2rem 3rem;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 12px;
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        border: none;
        transition: all 0.3s ease;
    }
    
    .btn-analyze:hover:not(:disabled) {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(72, 187, 120, 0.3);
    }
    
    .btn-analyze:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
    
    .result-section {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .prediction-card {
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        padding: 3rem;
        margin-bottom: 2rem;
    }
    
    .prediction-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .ai-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
    }
    
    .prediction-content {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .main-class-display {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .class-emoji {
        font-size: 4rem;
    }
    
    .main-class-label {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2d3748;
    }
    
    .breed-display {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        padding: 1.5rem;
        background: #f7fafc;
        border-radius: 15px;
        border-left: 4px solid #667eea;
    }
    
    .breed-arrow {
        font-size: 2rem;
        color: #667eea;
        font-weight: bold;
    }
    
    .breed-name {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
    }
    
    .confidence-text {
        color: #718096;
        font-size: 0.9rem;
    }
    
    .prediction-actions {
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    .btn-outline-primary, .btn-outline-secondary {
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .btn-outline-primary:hover, .btn-outline-secondary:hover {
        transform: translateY(-2px);
    }
    
    .feedback-card {
        background: #f7fafc;
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
    }
    
    .feedback-header {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .feedback-header h6 {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .feedback-header p {
        color: #718096;
        margin: 0;
    }
    
    .feedback-form {
        display: flex;
        gap: 1rem;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    .form-select {
        min-width: 200px;
        padding: 0.8rem;
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        font-size: 1rem;
    }
    
    .btn-success {
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
        font-weight: 500;
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        border: none;
        transition: all 0.3s ease;
    }
    
    .btn-success:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(72, 187, 120, 0.3);
    }
    
    .toast-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
    }
    
    .toast {
        background: white;
        border-radius: 10px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        padding: 1rem;
        border-left: 4px solid #48bb78;
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @media (max-width: 768px) {
        .app-title {
            font-size: 2rem;
        }
        
        .title-icon {
            font-size: 2.5rem;
        }
        
        .upload-card {
            padding: 2rem;
        }
        
        .upload-area {
            padding: 2rem 1rem;
        }
        
        .prediction-card {
            padding: 2rem;
        }
        
        .main-class-label {
            font-size: 2rem;
        }
        
        .feedback-form {
            flex-direction: column;
        }
        
        .form-select {
            min-width: 100%;
        }
    }
    """

def get_embedded_js():
    """Return embedded JavaScript content"""
    return """
    let selectedImage = null;
    let animalClasses = [];
    
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Animal Classification App loaded successfully!');
        initializeApp();
    });
    
    function initializeApp() {
        loadAnimalClasses();
        setupEventListeners();
        initializeDragAndDrop();
    }
    
    function setupEventListeners() {
        const imageUpload = document.getElementById('image-upload');
        const uploadArea = document.getElementById('upload-area');
        const predictButton = document.getElementById('predict-button');
        const showFeedbackBtn = document.getElementById('show-feedback-btn');
        const submitCorrectionBtn = document.getElementById('submit-correction');
        
        imageUpload.addEventListener('change', handleImageSelect);
        uploadArea.addEventListener('click', () => imageUpload.click());
        predictButton.addEventListener('click', analyzeImage);
        showFeedbackBtn.addEventListener('click', toggleFeedbackForm);
        submitCorrectionBtn.addEventListener('click', submitFeedback);
    }
    
    function initializeDragAndDrop() {
        const uploadArea = document.getElementById('upload-area');
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#667eea';
            uploadArea.style.background = '#f7fafc';
        });
        
        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#e2e8f0';
            uploadArea.style.background = 'transparent';
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#e2e8f0';
            uploadArea.style.background = 'transparent';
            
            const files = e.dataTransfer.files;
            if (files.length > 0 && files[0].type.startsWith('image/')) {
                handleImageFile(files[0]);
            }
        });
    }
    
    function handleImageSelect(event) {
        const file = event.target.files[0];
        if (file) {
            handleImageFile(file);
        }
    }
    
    function handleImageFile(file) {
        if (!file.type.startsWith('image/')) {
            showToast('Please select a valid image file', 'error');
            return;
        }
        
        const reader = new FileReader();
        reader.onload = function(e) {
            selectedImage = file;
            displayImagePreview(e.target.result);
            document.getElementById('predict-button').disabled = false;
        };
        reader.readAsDataURL(file);
    }
    
    function displayImagePreview(imageSrc) {
        const previewContainer = document.getElementById('image-preview-container');
        const imagePreview = document.getElementById('image-preview');
        
        imagePreview.src = imageSrc;
        previewContainer.classList.remove('d-none');
        document.getElementById('upload-area').style.display = 'none';
    }
    
    function removeImage() {
        selectedImage = null;
        document.getElementById('image-preview-container').classList.add('d-none');
        document.getElementById('upload-area').style.display = 'block';
        document.getElementById('predict-button').disabled = true;
        document.getElementById('result-container').classList.add('d-none');
        document.getElementById('image-upload').value = '';
    }
    
    async function analyzeImage() {
        if (!selectedImage) {
            showToast('Please select an image first', 'error');
            return;
        }
        
        const predictButton = document.getElementById('predict-button');
        predictButton.disabled = true;
        predictButton.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Analyzing...';
        
        try {
            const formData = new FormData();
            formData.append('file', selectedImage);
            
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const result = await response.json();
                displayPrediction(result);
            } else {
                throw new Error('Prediction failed');
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('Failed to analyze image. Please try again.', 'error');
        } finally {
            predictButton.disabled = false;
            predictButton.innerHTML = '<i class="bi bi-search me-2"></i>Analyze Image';
        }
    }
    
    function displayPrediction(result) {
        const resultContainer = document.getElementById('result-container');
        const mainClassLabel = document.getElementById('main-class-label');
        const classEmoji = document.getElementById('class-emoji');
        const breedDisplay = document.getElementById('breed-display');
        const breedName = document.getElementById('breed-name');
        const confidenceText = document.getElementById('confidence-text');
        const copyBreedBtn = document.getElementById('copy-breed-btn');
        
        mainClassLabel.textContent = result.prediction;
        classEmoji.textContent = getAnimalEmoji(result.prediction);
        
        if (result.breeds && result.breeds.length > 0) {
            breedName.textContent = result.breeds[0];
            confidenceText.textContent = `Confidence: ${(result.confidence * 100).toFixed(1)}%`;
            breedDisplay.classList.remove('d-none');
            copyBreedBtn.classList.remove('d-none');
        } else {
            breedDisplay.classList.add('d-none');
            copyBreedBtn.classList.add('d-none');
        }
        
        resultContainer.classList.remove('d-none');
        populateFeedbackDropdown();
        showToast('Image analyzed successfully!', 'success');
    }
    
    function getAnimalEmoji(animalClass) {
        const emojiMap = {
            'Cat': '🐱', 'Dog': '🐕', 'Horse': '🐎', 'Bird': '🐦', 'Elephant': '🐘',
            'Lion': '🦁', 'Tiger': '🐯', 'Bear': '🐻', 'Cow': '🐄', 'Deer': '🦌',
            'Dolphin': '🐬', 'Penguin': '🐧', 'Parrot': '🦜', 'Zebra': '🦓', 'Giraffe': '🦒'
        };
        
        for (const [key, emoji] of Object.entries(emojiMap)) {
            if (animalClass.toLowerCase().includes(key.toLowerCase())) {
                return emoji;
            }
        }
        return '🐾';
    }
    
    async function loadAnimalClasses() {
        try {
            const response = await fetch('/classes');
            if (response.ok) {
                const data = await response.json();
                animalClasses = data.classes;
            }
        } catch (error) {
            console.error('Failed to load animal classes:', error);
        }
    }
    
    function populateFeedbackDropdown() {
        const dropdown = document.getElementById('correction-dropdown');
        dropdown.innerHTML = '<option value="">Select correct class...</option>';
        
        animalClasses.forEach(className => {
            const option = document.createElement('option');
            option.value = className;
            option.textContent = className;
            dropdown.appendChild(option);
        });
    }
    
    function toggleFeedbackForm() {
        const feedbackCard = document.getElementById('feedback-card');
        feedbackCard.classList.toggle('show');
    }
    
    async function submitFeedback() {
        const correction = document.getElementById('correction-dropdown').value;
        if (!correction) {
            showToast('Please select a correction', 'error');
            return;
        }
        
        try {
            const formData = new FormData();
            formData.append('correction', correction);
            formData.append('original_prediction', document.getElementById('main-class-label').textContent);
            
            const response = await fetch('/feedback', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                showToast('Feedback submitted successfully!', 'success');
                document.getElementById('feedback-card').classList.remove('show');
            } else {
                throw new Error('Failed to submit feedback');
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('Failed to submit feedback. Please try again.', 'error');
        }
    }
    
    function showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.style.borderLeftColor = type === 'success' ? '#48bb78' : type === 'error' ? '#e53e3e' : '#667eea';
        toast.textContent = message;
        
        toastContainer.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 5000);
    }
    
    document.addEventListener('click', function(e) {
        if (e.target.id === 'copy-breed-btn') {
            const breedName = document.getElementById('breed-name').textContent;
            navigator.clipboard.writeText(breedName).then(() => {
                showToast('Breed name copied to clipboard!', 'success');
            });
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
        "deployment": "vercel",
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
