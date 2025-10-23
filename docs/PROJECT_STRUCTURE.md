# 📁 Project Structure

```
Animal-classification/
│
├── 📄 README.md                    # Main project documentation
├── 📄 requirements.txt             # Python dependencies
├── 📄 pytest.ini                   # Test configuration
├── 📄 .coveragerc                  # Coverage configuration
├── 📄 .dockerignore                # Docker build exclusions
├── 📄 .gitignore                   # Git exclusions
│
├── 🐳 Dockerfile                   # Container definition
├── 🐳 docker-compose.yml           # Multi-container orchestration
│
├── 🚀 main.py                      # Main training script
├── 🚀 main_api.py                  # FastAPI application
├── 🚀 start.py                     # Server startup script
│
├── 📚 docs/                        # Documentation
│   ├── API.md                      # API reference
│   ├── ARCHITECTURE.md             # System architecture
│   ├── CONTRIBUTING.md             # Contribution guidelines
│   ├── DOCKER.md                   # Docker deployment guide
│   ├── INCREMENTAL_LEARNING.md    # Incremental learning docs
│   ├── PROJECT_SUMMARY.md          # Achievement summary
│   ├── QUICKSTART.md               # Quick start guide
│   └── FIXES_APPLIED.md            # Historical fixes
│
├── 📓 notebooks/                   # Jupyter notebooks
│   ├── Animal_Classification_Complete.ipynb
│   └── Animal_Classification_Presentation.md
│
├── 💻 src/                         # Source code
│   ├── __init__.py                 # Package initialization
│   ├── model.py                    # Model architecture
│   ├── model_dynamic.py            # Dynamic model loader
│   ├── train.py                    # Training logic
│   ├── evaluate.py                 # Evaluation functions
│   ├── utils.py                    # Utility functions
│   ├── analytics.py                # Performance analytics
│   ├── gradcam.py                  # Grad-CAM visualization
│   ├── security.py                 # Security middleware
│   ├── feedback_trainer.py         # Incremental learning
│   └── predict_and_correct.py      # Prediction CLI
│
├── 🧪 tests/                       # Test suite
│   ├── __init__.py
│   ├── test_model.py               # Model tests
│   ├── test_api.py                 # API tests
│   ├── test_integration.py         # Integration tests
│   └── test_utils.py               # Utility tests
│
├── 🎨 frontend/                    # Web interface
│   ├── index_new.html              # Modern UI
│   ├── index.html                  # Legacy UI
│   ├── scripts_new.js              # UI logic
│   ├── scripts.js                  # Legacy logic
│   ├── styles_new.css              # Modern styles
│   └── styles.css                  # Legacy styles
│
├── 📊 data/                        # Data utilities
│   ├── __init__.py
│   └── dataloader.py               # Dataset loader
│
├── 🗂️ dataset/                     # Training data
│   ├── African Elephant/
│   ├── Asian Elephant/
│   ├── Bengal Tiger/
│   └── ... (75+ species)
│
├── 📁 outputs/                     # Model outputs
│   ├── best_model.pth              # Trained model
│   ├── correction_log.json         # Feedback log
│   ├── metrics.json                # Performance metrics
│   ├── metrics_dashboard.png       # Visual dashboard
│   └── feedback_data/              # Feedback images
│
├── 📈 logs/                        # TensorBoard logs
│   └── events.out.tfevents.*
│
├── 🔧 utilss/                      # Additional utilities
│   ├── dataset_manager.py
│   └── logger.py
│
├── ⚙️ .github/                     # CI/CD workflows
│   └── workflows/
│       ├── ci-cd.yml               # Main pipeline
│       ├── train.yml               # Training workflow
│       └── docs.yml                # Documentation build
│
└── 🐍 venv/                        # Virtual environment (gitignored)
```

## 📋 File Descriptions

### Core Files

| File | Purpose |
|------|---------|
| `main.py` | Complete training pipeline |
| `main_api.py` | FastAPI web server |
| `start.py` | Server startup helper |

### Source Code (`src/`)

| File | Purpose |
|------|---------|
| `model.py` | ResNet18 model architecture |
| `train.py` | Training loop with early stopping |
| `evaluate.py` | Evaluation and metrics |
| `analytics.py` | Performance tracking |
| `gradcam.py` | Visual explanations |
| `security.py` | Security middleware |
| `feedback_trainer.py` | Incremental learning |

### Documentation (`docs/`)

| File | Purpose |
|------|---------|
| `API.md` | Complete API reference |
| `ARCHITECTURE.md` | System design |
| `CONTRIBUTING.md` | Contribution guide |
| `DOCKER.md` | Deployment guide |
| `QUICKSTART.md` | 5-minute setup |

### Tests (`tests/`)

| File | Purpose |
|------|---------|
| `test_model.py` | Model architecture tests |
| `test_api.py` | API endpoint tests |
| `test_integration.py` | Integration tests |
| `test_utils.py` | Utility tests |

## 🎯 Import Structure

```python
# From main files
from src.model import AnimalCNN
from src.train import train
from src.evaluate import evaluate
from src.analytics import MetricsTracker
from src.gradcam import generate_gradcam_visualization
from src.security import RateLimitMiddleware

# From data module
from data.dataloader import AnimalDataset
```

## 🚀 Quick Navigation

- **Start Development**: `main.py` or `start.py`
- **API Server**: `main_api.py`
- **Add Features**: `src/`
- **Write Tests**: `tests/`
- **Update Docs**: `docs/`
- **Deploy**: `Dockerfile`, `docker-compose.yml`

## 📝 Notes

- All source code in `src/` is organized by functionality
- Documentation in `docs/` is comprehensive and up-to-date
- Tests in `tests/` provide 80%+ coverage
- Frontend in `frontend/` is ready for production
- Dataset in `dataset/` should be organized by class folders
