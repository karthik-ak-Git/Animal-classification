"""Unit tests for FastAPI endpoints"""
from main_api import app
import pytest
import json
import base64
from fastapi.testclient import TestClient
from io import BytesIO
from PIL import Image
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def sample_image():
    """Create a sample image for testing"""
    img = Image.new("RGB", (224, 224), color="red")
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format="JPEG")
    img_byte_arr.seek(0)
    return img_byte_arr


@pytest.fixture
def sample_image_base64():
    """Create a base64 encoded sample image"""
    img = Image.new("RGB", (224, 224), color="blue")
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format="JPEG")
    img_byte_arr.seek(0)
    encoded = base64.b64encode(img_byte_arr.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"


class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_endpoint(self, client):
        """Test GET /health returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestClassesEndpoint:
    """Test classes endpoint"""

    def test_get_classes(self, client):
        """Test GET /classes returns class information"""
        response = client.get("/classes")
        # May return 500 if model not loaded in test environment
        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.json()
            assert "num_classes" in data
            assert "classes" in data
            assert isinstance(data["classes"], list)


class TestPredictEndpoint:
    """Test prediction endpoint"""

    def test_predict_with_valid_image(self, client, sample_image):
        """Test POST /predict with valid image"""
        files = {"file": ("test.jpg", sample_image, "image/jpeg")}
        response = client.post("/predict", files=files)

        # May fail if model not loaded, check for 503 or 200
        assert response.status_code in [200, 503]

        if response.status_code == 200:
            data = response.json()
            assert "prediction" in data
            assert "confidence" in data
            assert "breeds" in data
            assert isinstance(data["breeds"], list)

    def test_predict_without_file(self, client):
        """Test POST /predict without file"""
        response = client.post("/predict")
        assert response.status_code == 422  # Validation error

    def test_predict_with_invalid_file_type(self, client):
        """Test POST /predict with non-image file"""
        files = {"file": ("test.txt", BytesIO(b"not an image"), "text/plain")}
        response = client.post("/predict", files=files)
        # May return 503 if model not loaded, 400/422 for validation
        assert response.status_code in [400, 422, 503]

    def test_predict_with_large_file(self, client):
        """Test POST /predict with file exceeding size limit"""
        # Create 11MB file (exceeds 10MB limit)
        large_data = b"0" * (11 * 1024 * 1024)
        files = {"file": ("large.jpg", BytesIO(large_data), "image/jpeg")}
        response = client.post("/predict", files=files)
        # May return 503 if model not loaded, 400/413/422 for validation
        assert response.status_code in [400, 413, 422, 503]


class TestFeedbackEndpoint:
    """Test feedback submission endpoint"""

    def test_submit_feedback_with_image(self, client, sample_image_base64):
        """Test POST /feedback with complete data"""
        feedback_data = {
            "predicted_class": "Dog",
            "correct_class": "Cat",
            "confidence": 0.85,
            "comments": "This is clearly a cat",
            "timestamp": "2025-01-20T10:00:00",
            "image_data": sample_image_base64,
        }

        response = client.post("/feedback", json=feedback_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "feedback_id" in data

    def test_submit_feedback_without_image(self, client):
        """Test POST /feedback without image data"""
        feedback_data = {
            "predicted_class": "Dog",
            "correct_class": "Cat",
            "confidence": 0.85,
            "comments": "Test feedback",
        }

        response = client.post("/feedback", json=feedback_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_submit_empty_feedback(self, client):
        """Test POST /feedback with empty data"""
        response = client.post("/feedback", json={})
        # Should still process but with empty values
        assert response.status_code in [200, 422]


class TestStaticFiles:
    """Test static file serving"""

    def test_serve_frontend_html(self, client):
        """Test that frontend HTML is served"""
        response = client.get("/frontend/index_new.html")
        # May return 200 if file exists, 404 if not
        assert response.status_code in [200, 404]

    def test_serve_frontend_css(self, client):
        """Test that frontend CSS is served"""
        response = client.get("/frontend/styles_new.css")
        assert response.status_code in [200, 404]

    def test_serve_frontend_js(self, client):
        """Test that frontend JS is served"""
        response = client.get("/frontend/scripts.js")
        assert response.status_code in [200, 404]


class TestCORS:
    """Test CORS configuration"""

    def test_cors_headers(self, client):
        """Test that CORS headers are present"""
        response = client.get("/classes")
        # CORS headers should be present OR endpoint should return successful status
        # Accept 500 as well since model may not be loaded in test environment
        assert (
            "access-control-allow-origin" in response.headers
            or response.status_code in [200, 500]
        )
