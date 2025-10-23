# 🏗️ Architecture Documentation

## System Overview

The Animal Classification system is a full-stack deep learning application with the following architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   HTML5    │  │  JavaScript  │  │  Bootstrap 5     │   │
│  │  (UI/UX)   │  │   (Logic)    │  │    (Styling)     │   │
│  └────────────┘  └──────────────┘  └──────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/REST API
┌───────────────────────────┼─────────────────────────────────┐
│                      FastAPI Backend                         │
│  ┌────────────────────────┴──────────────────────────────┐  │
│  │              API Endpoints & Middleware                │  │
│  │  • /predict     • /visualize    • /analytics          │  │
│  │  • /feedback    • /classes      • /health             │  │
│  └──┬──────────┬──────────┬──────────┬──────────┬────────┘  │
│     │          │          │          │          │            │
│  ┌──▼──┐   ┌──▼────┐  ┌──▼─────┐ ┌──▼─────┐ ┌──▼────────┐  │
│  │Rate │   │CORS  │  │Security│ │Logging │ │ Error     │  │
│  │Limit│   │      │  │Headers │ │        │ │ Handling  │  │
│  └─────┘   └──────┘  └────────┘ └────────┘ └───────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────┐
│                    ML Core Components                        │
│  ┌────────────────────────┴──────────────────────────────┐  │
│  │                   ResNet18 Model                       │  │
│  │         (Transfer Learning + Fine-tuning)              │  │
│  └──┬──────────┬──────────┬──────────┬──────────┬────────┘  │
│     │          │          │          │          │            │
│  ┌──▼──────┐ ┌▼────────┐ ┌▼────────┐ ┌▼────────┐ ┌▼───────┐ │
│  │ Predict │ │Grad-CAM │ │Training │ │Feedback │ │Metrics │ │
│  │ Engine  │ │Visualiz.│ │Pipeline │ │  Loop   │ │Tracker │ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └────────┘ │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────┐
│                      Data Layer                              │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│  │  Dataset   │  │   Model      │  │    Feedback      │    │
│  │  (Images)  │  │  Weights     │  │     Data         │    │
│  │  75+ spp.  │  │  (.pth)      │  │   (Corrections)  │    │
│  └────────────┘  └──────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend Layer

**Technology Stack:**
- HTML5 for structure
- CSS3 with Bootstrap 5 for responsive design
- Vanilla JavaScript for interactivity

**Key Features:**
- Drag & drop file upload
- Real-time prediction display
- Feedback submission form
- Progress indicators
- Toast notifications

**Files:**
- `frontend/index_new.html` - Main UI
- `frontend/styles_new.css` - Styling
- `frontend/scripts_new.js` - Client logic

### 2. API Layer (FastAPI)

**Endpoints:**

```python
GET  /                    # Serve frontend
GET  /health             # Health check
GET  /classes            # List available classes
POST /predict            # Image classification
POST /visualize          # Grad-CAM visualization
POST /feedback           # Submit corrections
GET  /analytics          # Performance metrics
GET  /analytics/dashboard # Visual dashboard
```

**Middleware Stack:**
1. **CORS Middleware** - Cross-origin requests
2. **Rate Limiting** - 100 requests/60 seconds
3. **Security Headers** - XSS, clickjacking protection
4. **Error Handling** - Centralized exception handling

### 3. Machine Learning Core

#### Model Architecture

```python
ResNet18 (Pretrained on ImageNet)
├── conv1 (7x7, 64)
├── bn1
├── relu
├── maxpool
├── layer1 (64)  🔒 Frozen
├── layer2 (128) 🔒 Frozen
├── layer3 (256) 🔒 Frozen
├── layer4 (512) ✓ Trainable
└── fc (Custom Classification Head)
    ├── Linear(512, 256)
    ├── ReLU
    ├── Dropout(0.4)
    └── Linear(256, num_classes)
```

**Key Decisions:**
- **Transfer Learning**: Leverages ImageNet knowledge
- **Selective Unfreezing**: Only layer4 trainable for fine-tuning
- **Custom Head**: Adapted for animal classification
- **Dropout**: Prevents overfitting

#### Training Pipeline

```
Data Loading → Preprocessing → Training → Validation → Model Selection
     ↓              ↓             ↓           ↓              ↓
  Dataset      Transforms    Backprop    Metrics      Save Best
  (75 cls)   (224x224 RGB)  + Optimizer  (Acc/Loss)  (best_model.pth)
```

**Training Configuration:**
- Optimizer: Adam (lr=1e-3)
- Scheduler: ReduceLROnPlateau
- Loss: CrossEntropyLoss
- Early Stopping: Patience=5
- Batch Size: 32 (train), 64 (val/test)

### 4. Incremental Learning System

**Workflow:**

```
User Correction → Save Feedback → Trigger Training → Update Model
                                        ↓
                            Smart Replay Sampling
                                  ↓
                    70% feedback classes + 30% others
                                  ↓
                        Train ONLY final layer
                                  ↓
                          Save Updated Model
```

**Key Features:**
- **Catastrophic Forgetting Prevention**
- **Selective Layer Training** (fc layer only)
- **Experience Replay** (smart sampling)
- **Async Training** (non-blocking)

### 5. Grad-CAM Visualization

**Process:**

```
Input Image → Forward Pass → Target Layer Activation → Gradient Computation
                                      ↓
                            Weighted Activation Maps
                                      ↓
                             Heatmap Generation
                                      ↓
                          Overlay on Original Image
```

**Implementation:**
- Target Layer: `layer4[-1]` (last conv layer)
- Colormap: JET (red=high activation)
- Transparency: 40% overlay

### 6. Analytics & Monitoring

**Metrics Tracked:**
- Prediction accuracy over time
- Class confusion patterns
- Confidence score distribution
- Feedback submission timeline
- Most mispredicted classes

**Visualization:**
- Line charts (feedback over time)
- Bar charts (confused classes)
- Histograms (confidence distribution)
- Heatmaps (confusion matrix)

## Data Flow

### Prediction Flow

```
1. User uploads image (frontend)
   ↓
2. POST /predict (API)
   ↓
3. Image validation & preprocessing
   ↓
4. Model inference (PyTorch)
   ↓
5. Softmax probabilities
   ↓
6. Top-3 predictions + confidence
   ↓
7. JSON response to frontend
   ↓
8. Display results with UI animations
```

### Feedback Flow

```
1. User submits correction (frontend)
   ↓
2. POST /feedback (API)
   ↓
3. Clear old feedback data
   ↓
4. Save image to feedback_data/{class}/
   ↓
5. Log correction to correction_log.json
   ↓
6. Trigger async incremental training
   ↓
7. Train on latest feedback + replay samples
   ↓
8. Update model weights (best_model.pth)
   ↓
9. Model automatically reloaded on next prediction
```

## Security Architecture

### Defense Layers

1. **Rate Limiting**
   - Per-IP tracking
   - 100 requests/60 seconds default
   - Customizable per API key

2. **Input Validation**
   - File type checking (MIME validation)
   - File size limits (10MB max)
   - Filename sanitization
   - Path traversal prevention

3. **Security Headers**
   - X-Content-Type-Options: nosniff
   - X-Frame-Options: DENY
   - X-XSS-Protection: enabled
   - HSTS (Strict-Transport-Security)

4. **Error Handling**
   - No stack traces in production
   - Generic error messages
   - Detailed logging for debugging

## Deployment Architecture

### Docker Containerization

```
Multi-stage Build:
1. Builder Stage
   ├── Install build dependencies
   ├── Compile Python packages
   └── Cache dependencies

2. Runtime Stage
   ├── Copy compiled packages
   ├── Copy application code
   ├── Set up environment
   └── Run application
```

### CI/CD Pipeline

```
Push to GitHub
   ↓
GitHub Actions Triggered
   ↓
├── Lint & Format Check
├── Run Tests (3.9, 3.10, 3.11)
├── Security Scan
└── Coverage Report
   ↓
Build Docker Image
   ↓
Push to Docker Hub
   ↓
Deploy to Production
```

## Performance Considerations

### Optimizations

1. **Memory Management**
   - Explicit `del` for large tensors
   - `map_location='cpu'` for model loading
   - Batch processing with size limits

2. **Inference Speed**
   - Model in eval() mode
   - torch.no_grad() context
   - Cached transforms

3. **Async Operations**
   - Non-blocking training
   - Concurrent request handling
   - Background task queue

## Scalability

### Horizontal Scaling

```
Load Balancer (nginx/HAProxy)
        ↓
   ┌────┴────┬────────┬────────┐
   ↓         ↓        ↓        ↓
App-1     App-2    App-3    App-N
   ↓         ↓        ↓        ↓
   └─────┬───┴────────┴────────┘
         ↓
   Shared Storage
   (Model, Dataset)
```

### Caching Strategy

- Model weights: Load once, share across workers
- Predictions: Cache common queries (Redis)
- Static assets: CDN delivery

## Monitoring & Logging

### Metrics Collection

- Request latency
- Prediction accuracy
- Error rates
- Resource usage (CPU, Memory, GPU)

### Log Levels

- ERROR: Critical failures
- WARNING: Degraded performance
- INFO: Normal operations
- DEBUG: Detailed diagnostics

## Future Enhancements

1. **Database Integration** (PostgreSQL/MongoDB)
2. **Message Queue** (RabbitMQ/Kafka)
3. **Model Versioning** (MLflow/DVC)
4. **A/B Testing Framework**
5. **Distributed Training** (PyTorch Distributed)
6. **Edge Deployment** (ONNX/TensorRT)

## References

- [ResNet Paper](https://arxiv.org/abs/1512.03385)
- [Grad-CAM Paper](https://arxiv.org/abs/1610.02391)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PyTorch Documentation](https://pytorch.org/docs/)
