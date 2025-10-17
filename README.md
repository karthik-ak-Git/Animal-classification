# 🐾 Animal Classification 🦁🐦🐻

A professional deep learning web application for classifying animal species from images. Built with PyTorch (ResNet18), FastAPI backend, and a responsive Bootstrap 5 frontend with a feedback system for continuous improvement.

---

## ✨ Features

- 🔬 **ResNet18 (PyTorch):** Deep learning model for animal classification
- ⚡ **FastAPI Backend:** RESTful API with prediction and feedback endpoints
- 🌱 **Bootstrap 5 Frontend:** Modern, mobile-friendly, and accessible interface
- 📝 **Feedback System:** Users can submit corrections to improve the model
- 🔁 **Retraining Pipeline:** Automatically incorporate feedback into model training
- 👁️‍🗨️ **Grad-CAM Visualization:** See what the model focuses on in images
- 📊 **Evaluation Tools:** Confusion matrix, accuracy reports, and performance metrics

---

## 🐾 Supported Animal Classes

- Bear
- Bird
- Cat
- Cow
- Deer
- Dog
- Dolphin
- Elephant
- Giraffe
- Horse
- Kangaroo
- Lion
- Panda
- Tiger
- Zebra

_(And more - check your dataset folder for the complete list)_

---

## 🛠️ Tech Stack

- **Backend:** Python 3.8+, PyTorch, FastAPI, Uvicorn
- **Model:** ResNet18 (pretrained on ImageNet, fine-tuned on animal dataset)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Data Processing:** torchvision, NumPy, Pillow
- **Visualization:** Matplotlib, TensorBoard, Grad-CAM
- **Evaluation:** scikit-learn

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
├── data/                     # Data loading utilities
│   └── dataloader.py        # Custom dataset and data loaders
├── dataset/                  # Animal image dataset (organized by class)
│   ├── Bear/
│   ├── Bird/
│   ├── Cat/
│   └── ...
├── frontend/                 # Web interface
│   ├── index.html           # Main UI
│   ├── scripts.js           # Frontend logic
│   └── styles.css           # Styling
├── logs/                     # TensorBoard training logs
├── outputs/                  # Model outputs and feedback
│   ├── best_model.pth       # Trained model weights
│   └── correction_log.json  # User feedback data
├── main_api.py              # FastAPI backend server
├── model.py                 # ResNet18 model definition
├── train.py                 # Training script
├── evaluate.py              # Model evaluation
├── predict.py               # Prediction script
├── feedback_trainer.py      # Retraining with feedback
├── utils.py                 # Utility functions
├── start.py                 # Server startup script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

---

## 🔧 API Endpoints

### `GET /`
Serves the main web interface

### `GET /health`
Returns server and model status

### `GET /classes`
Returns list of all available animal classes

### `POST /predict`
Upload an image and get predictions
- **Input:** Image file (JPEG, PNG, etc.)
- **Output:** Top predictions with confidence scores

### `POST /feedback`
Submit correction feedback
- **Input:** Original prediction, correct class, confidence
- **Output:** Confirmation with feedback ID

**Full API documentation:** http://127.0.0.1:8000/docs (when server is running)

---

## 🐛 Troubleshooting

### Model not loading
- Ensure you've trained the model first: `python train.py`
- Check that `outputs/best_model.pth` exists
- Verify the dataset folder structure is correct

### CUDA/GPU errors
- Check CUDA compatibility: `python -c "import torch; print(torch.cuda.is_available())"`
- Install correct PyTorch version for your CUDA version
- The model will automatically fall back to CPU if CUDA is unavailable

### Port already in use
- Change the port in `start.py`
- Or kill the process using port 8000

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Activate your virtual environment

---

## � Performance Tips

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

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 TODO / Future Enhancements

- [ ] Add more animal classes
- [ ] Implement model quantization for faster inference
- [ ] Add data augmentation techniques
- [ ] Create mobile app version
- [ ] Add multilingual support
- [ ] Implement user authentication
- [ ] Add database for feedback storage
- [ ] Create automated retraining pipeline
- [ ] Add A/B testing for model versions

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- PyTorch team for the excellent deep learning framework
- FastAPI for the modern web framework
- Bootstrap team for the UI components
- ResNet paper authors for the architecture

---

**Made with ❤️ and 🐍 Python**
 