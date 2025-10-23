# ⚡ Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/karthik-ak-Git/animal-classification.git
cd animal-classification

# Start with Docker
docker-compose up -d

# Access application
open http://localhost:8000
```

### Option 2: Local Development

```bash
# Clone repository
git clone https://github.com/karthik-ak-Git/animal-classification.git
cd animal-classification

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python start.py
```

---

## 📝 Common Tasks

### Run Tests
```bash
pytest                          # All tests
pytest --cov=.                  # With coverage
pytest tests/test_api.py       # Specific suite
```

### View Analytics
```bash
python analytics.py             # Generate dashboard
curl http://localhost:8000/analytics  # View metrics
```

### Docker Commands
```bash
docker-compose up -d            # Start
docker-compose logs -f          # View logs
docker-compose down             # Stop
docker-compose build --no-cache # Rebuild
```

### Training
```bash
python main.py                  # Full training
python feedback_trainer.py     # Incremental training
tensorboard --logdir=logs       # Monitor training
```

---

## 🔗 Important URLs

| Service | URL |
|---------|-----|
| **Main App** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |
| **Health Check** | http://localhost:8000/health |
| **TensorBoard** | http://localhost:6006 |
| **Analytics** | http://localhost:8000/analytics |

---

## 📦 Key Files

| File | Purpose |
|------|---------|
| `main_api.py` | FastAPI application |
| `model.py` | ResNet18 architecture |
| `train.py` | Training logic |
| `analytics.py` | Metrics tracking |
| `gradcam.py` | Visualization |
| `security.py` | Security middleware |

---

## 🐛 Quick Fixes

### Port 8000 in use?
```powershell
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Model not found?
```bash
# Train a model first
python main.py
```

### Import errors?
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Documentation

- **[README.md](README.md)** - Full project overview
- **[API.md](API.md)** - API reference
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[DOCKER.md](DOCKER.md)** - Docker guide

---

## 🎯 Next Steps

1. ✅ Run the application
2. ✅ Test predictions
3. ✅ Submit feedback
4. ✅ View analytics
5. ✅ Explore API docs
6. ✅ Run tests
7. ✅ Deploy with Docker

---

**Need help?** Open an issue on [GitHub](https://github.com/karthik-ak-Git/animal-classification/issues)
