# 🐾 Animal Classification 🦁🐦🐻

[![CI/CD](https://img.shields.io/github/workflow/status/karthik-ak-Git/animal-classification/CI%2FCD%20Pipeline)](https://github.com/karthik-ak-Git/animal-classification/actions)
[![Coverage](https://img.shields.io/codecov/c/github/karthik-ak-Git/animal-classification)](https://codecov.io/gh/karthik-ak-Git/animal-classification)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/github/license/karthik-ak-Git/animal-classification)](LICENSE)
[![Docker](https://img.shields.io/docker/automated/karthik-ak-Git/animal-classifier)](https://hub.docker.com/r/karthik-ak-Git/animal-classifier)

A **production-ready** deep learning web application for classifying 75+ animal species from images. Built with PyTorch (ResNet18), FastAPI backend, and a responsive Bootstrap 5 frontend with advanced features including incremental learning, Grad-CAM visualization, and comprehensive analytics.

---

## ✨ Features

### Core Functionality
- 🔬 **ResNet18 Deep Learning Model** - Transfer learning with ImageNet weights
- 🎯 **75+ Animal Species** - Comprehensive classification across multiple taxonomies
- ⚡ **FastAPI Backend** - High-performance async REST API
- 🌱 **Modern Web Interface** - Responsive Bootstrap 5 UI with drag-and-drop
- 📱 **Mobile Optimized** - Works seamlessly on all devices

### Advanced Features  
- 🧠 **Incremental Learning** - Continuous improvement from user feedback without catastrophic forgetting
- 👁️ **Grad-CAM Visualization** - Visual explanations of model predictions with heatmaps
- � **Analytics Dashboard** - Real-time performance metrics and confusion analysis
- 🔄 **Feedback Loop** - User corrections automatically retrain the model
- � **Security Features** - Rate limiting, input validation, security headers
- 🐳 **Docker Support** - Containerized deployment with docker-compose
- 🧪 **Comprehensive Testing** - 80%+ test coverage with pytest
- � **CI/CD Pipeline** - Automated testing and deployment with GitHub Actions

---

## 🐾 Supported Animal Classes

### Main Categories (75+ Species)
**Bears**: Polar Bear, Grizzly Bear, American Black Bear, Asian Black Bear, Sloth Bear, Sun Bear  
**Birds**: Eagle, Owl, Parrot, Swan, Penguin, Ostrich, Hummingbird, Cockatiel, Kingfisher, Woodpecker  
**Cats**: Domestic Cat, Bengal Cat, Persian Cat, Siamese Cat, Maine Coon, African Wildcat  
**Big Cats**: Lion, Tiger, Bengal Tiger, Siberian Tiger, African Lion, Asiatic Lion  
**Dogs**: German Shepherd, Golden Retriever, Labrador, Pug, Domestic Dog  
**Elephants**: African Elephant, Asian Elephant  
**And many more...**

See [Full Species List](dataset/) for complete taxonomy.

---

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI 0.100+
- **ML Library:** PyTorch 2.0+, torchvision
- **Model:** ResNet18 (transfer learning)
- **Server:** Uvicorn (ASGI)
- **Security:** Custom middleware (rate limiting, headers)

### Frontend
- **UI:** HTML5, CSS3, JavaScript (ES6+)
- **Framework:** Bootstrap 5
- **Features:** Drag-and-drop, real-time updates, toast notifications

### DevOps & Tools
- **Containerization:** Docker, docker-compose
- **CI/CD:** GitHub Actions
- **Testing:** pytest, pytest-cov
- **Visualization:** Matplotlib, TensorBoard, Grad-CAM
- **Analytics:** Custom metrics tracker
- **Code Quality:** Black, isort, flake8

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone <repo-url>
cd Animal-classification
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
```

**Activate it:**
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

> **For GPU users:** Uncomment the CUDA 11.8 versions in `requirements.txt`:
> ```bash
> # GPU versions (CUDA 11.8) - uncomment to use:
> torch==2.7.1+cu118 --index-url https://download.pytorch.org/whl/cu118
> torchvision==0.22.1+cu118 --index-url https://download.pytorch.org/whl/cu118
> ```
> Or install directly:
> ```bash
> pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
> ```
> See [PyTorch Get Started](https://pytorch.org/get-started/locally/) for more options.

---

## � Usage

### Training the Model

Train the model on your dataset:
```bash
python train.py
```

This will:
- Load images from the `dataset/` folder
- Train a ResNet18 model
- Save the best model to `outputs/best_model.pth`
- Log training metrics to TensorBoard

**Monitor training:**
```bash
tensorboard --logdir=logs
```

### Running the Backend API

Start the FastAPI server:
```bash
python start.py
```

The API will be available at:
- **Main app:** http://127.0.0.1:8000
- **API Documentation:** http://127.0.0.1:8000/docs
- **Health Check:** http://127.0.0.1:8000/health

**Alternative (with auto-reload for development):**
```bash
uvicorn main_api:app --reload
```

### Using the Frontend

1. **Start the backend** (see above)
2. **Open your browser** and go to: http://127.0.0.1:8000
3. **Upload an image** of an animal
4. **Get predictions** with confidence scores
5. **Submit feedback** if the prediction is incorrect

---

## 🧠 Making Predictions

### Via the Web Interface
- Open http://127.0.0.1:8000 in your browser
- Drag & drop or select an image
- View top predictions with confidence scores

### Via Command Line
```bash
python predict.py --image path/to/image.jpg
```

### Via Python Script
```python
from predict import predict_image

result = predict_image("path/to/image.jpg")
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']:.2%}")
```

---

## � Evaluation

Evaluate model performance:
```bash
python evaluate.py
```

This generates:
- Confusion matrix
- Per-class accuracy
- Precision, recall, F1-score
- Overall accuracy metrics

---

## 📝 Feedback & Retraining

### Submitting Feedback

Users can correct predictions through the web interface. Feedback is stored in `outputs/correction_log.json`.

### Retraining with Feedback

Retrain the model using collected feedback:
```bash
python feedback_trainer.py
```

This will:
- Load existing feedback
- Incorporate corrections into training
- Generate an improved model
- Preserve the original model as backup

---

## 👁️ Grad-CAM Visualization

Visualize what the model focuses on:
```bash
python gradcam_test.py --image path/to/image.jpg
```

The output shows a heatmap overlay indicating which regions of the image influenced the prediction.

---

## 📁 Project Structure

```
Animal-classification/
├── 📚 docs/                  # Documentation
│   ├── API.md               # API reference
│   ├── ARCHITECTURE.md      # System architecture
│   ├── CONTRIBUTING.md      # Contribution guidelines
│   ├── DOCKER.md            # Docker deployment
│   ├── INCREMENTAL_LEARNING.md
│   ├── PROJECT_STRUCTURE.md # This structure
│   ├── PROJECT_SUMMARY.md   # Achievement summary
│   └── QUICKSTART.md        # Quick start guide
│
├── 📓 notebooks/             # Jupyter notebooks & presentations
│   ├── Animal_Classification_Complete.ipynb
│   └── Animal_Classification_Presentation.md
│
├── 💻 src/                   # Source code (organized)
│   ├── model.py             # ResNet18 architecture
│   ├── train.py             # Training logic
│   ├── evaluate.py          # Evaluation functions
│   ├── analytics.py         # Performance metrics
│   ├── gradcam.py           # Grad-CAM visualization
│   ├── security.py          # Security middleware
│   ├── feedback_trainer.py  # Incremental learning
│   └── utils.py             # Utility functions
│
├── 🧪 tests/                 # Test suite (80%+ coverage)
│   ├── test_model.py        # Model tests
│   ├── test_api.py          # API tests
│   ├── test_integration.py  # Integration tests
│   └── test_utils.py        # Utility tests
│
├── 🎨 frontend/              # Web interface
│   ├── index_new.html       # Modern UI
│   ├── scripts_new.js       # UI logic
│   └── styles_new.css       # Styling
│
├── 📊 data/                  # Data utilities
│   └── dataloader.py        # Dataset loader
│
├── 🗂️ dataset/               # Training data (75+ species)
│   ├── African Elephant/
│   ├── Bengal Tiger/
│   └── ...
│
├── 📁 outputs/               # Model outputs
│   ├── best_model.pth       # Trained model
│   └── correction_log.json  # Feedback log
│
├── 📈 logs/                  # TensorBoard logs
│
├── ⚙️ .github/workflows/     # CI/CD pipelines
│   ├── ci-cd.yml
│   ├── train.yml
│   └── docs.yml
│
├── 🚀 main.py                # Training script
├── 🚀 main_api.py            # FastAPI server
├── 🚀 start.py               # Server startup
├── 🐳 Dockerfile
├── 🐳 docker-compose.yml
└── 📄 requirements.txt
```

**See [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) for detailed structure.**

---

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=. --cov-report=html
```

View coverage report: `htmlcov/index.html`

### Run Specific Test Suite

```bash
# Model tests
pytest tests/test_model.py

# API tests
pytest tests/test_api.py

# Integration tests
pytest tests/test_integration.py
```

### Test Statistics
- **Coverage**: 80%+
- **Tests**: 50+ test cases
- **Suites**: Model, API, Integration, Utils

---

## 🐳 Docker Deployment

### Quick Start with Docker Compose

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Manual Docker Build

```bash
# Build image
docker build -t animal-classifier:latest .

# Run container
docker run -d -p 8000:8000 \
  -v $(pwd)/dataset:/app/dataset:ro \
  -v $(pwd)/outputs:/app/outputs \
  animal-classifier:latest
```

### With TensorBoard Monitoring

```bash
docker-compose --profile monitoring up -d
```

Access:
- **App**: http://localhost:8000
- **TensorBoard**: http://localhost:6006

See [docs/DOCKER.md](docs/DOCKER.md) for detailed deployment guide.

---

## 🔧 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web interface |
| `GET` | `/health` | Health check |
| `GET` | `/classes` | List all classes |
| `POST` | `/predict` | Image classification |
| `POST` | `/visualize` | Grad-CAM visualization |
| `POST` | `/feedback` | Submit correction |
| `GET` | `/analytics` | Performance metrics |
| `GET` | `/analytics/dashboard` | Visual dashboard |

### Interactive Documentation

When server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

See [docs/API.md](docs/API.md) for detailed API documentation with examples.

---

## 🔒 Security Features

- **Rate Limiting**: 100 requests/60 seconds per IP
- **Input Validation**: File type and size checks
- **Security Headers**: XSS, clickjacking protection
- **Error Handling**: Safe error messages
- **CORS**: Configurable cross-origin policies

---

## 📊 Analytics & Monitoring

### View Analytics

```bash
# Generate analytics report
python analytics.py
```

Outputs:
- `outputs/metrics.json` - Performance metrics
- `outputs/metrics_dashboard.png` - Visual dashboard

### Access via API

```bash
curl http://localhost:8000/analytics
```

Features:
- Feedback timeline tracking
- Class confusion analysis
- Confidence score distribution
- Misprediction patterns

---

## 🐛 Troubleshooting

### Model not loading
- Ensure you've trained the model first: `python main.py`
- Check that `outputs/best_model.pth` exists
- Verify the dataset folder structure is correct

### CUDA/GPU errors
- Check CUDA compatibility: `python -c "import torch; print(torch.cuda.is_available())"`
- Install correct PyTorch version for your CUDA version
- The model will automatically fall back to CPU if CUDA is unavailable

### Port already in use (Windows)
```powershell
# Find process using port 8000
netstat -ano | findstr :8000
# Kill process (replace PID)
taskkill /PID <PID> /F
```

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Activate your virtual environment
- Verify Python version >= 3.9

### Docker issues
```bash
# Rebuild without cache
docker-compose build --no-cache

# Clear volumes
docker-compose down -v

# View logs
docker-compose logs --tail=100
```

---

## ⚡ Performance Tips

### Training
- Use GPU for faster training (10-100x speedup)
- Adjust batch size based on available GPU memory
- Use data augmentation to improve generalization
- Monitor TensorBoard to track progress

### Inference
- Model automatically uses GPU if available
- Batch predictions for better throughput
- Consider model quantization for faster inference

---

## 🤝 Contributing

We welcome contributions! Please see [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

**Quick Links:**
- [Code of Conduct](docs/CONTRIBUTING.md#code-of-conduct)
- [Development Setup](docs/CONTRIBUTING.md#development-setup)
- [Style Guidelines](docs/CONTRIBUTING.md#style-guidelines)
- [Testing Guide](docs/CONTRIBUTING.md#testing)

---

## 📚 Documentation

- **[API Documentation](docs/API.md)** - Complete API reference with examples
- **[Architecture](docs/ARCHITECTURE.md)** - System design and components
- **[CI/CD Pipeline](docs/CI_CD.md)** - Continuous integration and deployment guide
- **[Docker Guide](docs/DOCKER.md)** - Deployment with Docker
- **[Incremental Learning](docs/INCREMENTAL_LEARNING.md)** - Continuous learning system
- **[Contributing](docs/CONTRIBUTING.md)** - Contribution guidelines
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Detailed file organization
- **[Quick Start](docs/QUICKSTART.md)** - Get started in 5 minutes

---

## 🎯 Project Roadmap

### Completed ✅
- [x] Core classification system
- [x] Incremental learning
- [x] Grad-CAM visualization
- [x] Analytics dashboard
- [x] Docker containerization
- [x] CI/CD pipeline
- [x] Comprehensive testing
- [x] Security features

### In Progress 🔄
- [ ] Model quantization for edge deployment
- [ ] A/B testing framework
- [ ] Enhanced data augmentation

### Planned 📋
- [ ] Mobile application
- [ ] Multi-language support
- [ ] Video classification
- [ ] Real-time species tracking
- [ ] Integration with wildlife databases

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- **PyTorch Team** - Excellent deep learning framework
- **FastAPI** - Modern, fast web framework
- **Bootstrap** - Responsive UI components
- **ResNet Authors** - Groundbreaking architecture
- **Grad-CAM Authors** - Interpretable visualizations
- **Open Source Community** - Invaluable tools and libraries

---

## 📞 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/karthik-ak-Git/animal-classification/issues)
- **Discussions**: [Ask questions or share ideas](https://github.com/karthik-ak-Git/animal-classification/discussions)
- **Email**: karthik@example.com

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ by [Karthik](https://github.com/karthik-ak-Git)**

**Powered by 🐍 Python | 🔥 PyTorch | ⚡ FastAPI**
 