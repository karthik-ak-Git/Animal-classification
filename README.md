# 🐾 Animal Classification 🦁🐦🐻

A professional deep learning web app to classify 15 animal species from images, featuring a PyTorch ResNet18 model, FastAPI backend, Bootstrap 5 frontend, feedback-driven retraining, Grad-CAM visualizations, and optional OpenCLIP validation.

---

## ✨ Features

- 🔬 **ResNet18 (PyTorch):** Classifies images into 15 animal classes
- ⚡ **FastAPI Backend:** Endpoints for prediction and user feedback
- 🌱 **Bootstrap 5 Frontend:** "Natural Explorer" theme, mobile-friendly & accessible
- 📝 **Feedback System:** Users can submit corrections and (optionally) new classes
- 🔁 **Retraining:** `feedback_trainer.py` script retrains the model with new feedback
- 👁️‍🗨️ **Grad-CAM:** Visualize what the model focuses on in each image
- 🤖 **OpenCLIP Validation (Optional):** Checks if user feedback is meaningful

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

---

## 🛠️ Tech Stack

- **Backend:** Python 3.8+, [PyTorch](https://pytorch.org/) (ResNet18), FastAPI, Uvicorn
- **Frontend:** HTML5, CSS3, JavaScript, [Bootstrap 5](https://getbootstrap.com/), Bootstrap Icons
- **Visualization:** Grad-CAM, Matplotlib
- **Feedback & Retraining:** JSON logging, `feedback_trainer.py`
- **Optional:** [OpenCLIP](https://github.com/mlfoundations/open_clip)

---

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd Animal-Classification
   ```
2. **(Recommended) Create a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate # on other system: source venv/bin/activate   
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   > **For GPU users:**
   > Install the correct CUDA version of torch/torchvision/torchaudio. For CUDA 11.8 (e.g. RTX 3050):
   > ```bash
   >    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   > ```
   > See [PyTorch Get Started](https://pytorch.org/get-started/locally/) for more options.

---

## 🖥️ Running the Backend

Start the FastAPI server with Uvicorn:
```bash
uvicorn main_api:app --reload
```
- The API will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🌐 Using the Frontend

- Open `frontend/index.html` in your browser, or serve the `frontend/` folder with a static file server.
- Upload an animal image, get a prediction, and submit feedback if the prediction is wrong.
- The UI is mobile-friendly and accessible.

---

## 🧠 Prediction & Feedback Scripts

- **Prediction:**
  ```bash
  python predict.py --image path/to/image.jpg
  ```
- **Feedback Correction:**
  - Use the web UI to submit corrections, or
  - Use the API endpoint `/feedback` (see FastAPI docs at `/docs`)
- **Retraining with Feedback:**
  ```bash
  python feedback_trainer.py
  ```
  - Uses feedback from `outputs/correction_log.json` to improve the model.

---

## 👁️ Grad-CAM Visualization

- To visualize model attention on an image:
  ```bash
  python gradcam_test.py --image path/to/image.jpg
  ```
- The output will show a heatmap overlay of where the model is focusing.

---

## 🤖 OpenCLIP Validation (Optional)

- To check if user feedback is meaningful using OpenCLIP, ensure `open-clip-torch` is installed.
- This is integrated in the feedback validation pipeline (see code for details).

---

## 📁 Project Structure

```
Animal Classification/
├── data/                # Data loading scripts
├── dataset/             # Animal image dataset
├── frontend/            # HTML, CSS, JS for the web UI
├── outputs/             # Model weights, logs, feedback
├── main_api.py          # FastAPI backend
├── model.py             # Model definition (ResNet18)
├── train.py             # Training script
├── predict.py           # Prediction script
├── gradcam_test.py      # Grad-CAM visualization
├── feedback_trainer.py  # Retraining with feedback
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🎬 YouTube Demo

[![YouTube Demo](https://img.shields.io/badge/YouTube-Demo-red?logo=youtube)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

> _Replace the above link with your actual demo video!_

---

## 🙏 Credits

- Project Lead: _Your Name_
- Contributors: _Add names here_
- Special thanks: _Add acknowledgments_

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). 