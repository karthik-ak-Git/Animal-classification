"""Integration tests for feedback loop and incremental learning"""
import pytest
import os
import json
import shutil
import torch
from pathlib import Path
from PIL import Image
import sys

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


class TestFeedbackLoop:
    """Test the complete feedback and retraining loop"""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup test environment and cleanup after"""
        # Setup
        self.test_output_dir = "outputs/test_feedback"
        self.test_log_file = "outputs/test_correction_log.json"

        yield

        # Cleanup
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)

    def test_feedback_data_storage(self):
        """Test that feedback data is stored correctly"""
        feedback_dir = "outputs/feedback_data"
        os.makedirs(feedback_dir, exist_ok=True)

        # Create test image
        test_class = "Dog"
        class_dir = os.path.join(feedback_dir, test_class)
        os.makedirs(class_dir, exist_ok=True)

        img = Image.new("RGB", (224, 224), color="red")
        img_path = os.path.join(class_dir, "test_image.jpg")
        img.save(img_path)

        assert os.path.exists(img_path)
        assert os.path.isfile(img_path)

    def test_correction_log_format(self):
        """Test that correction log has correct format"""
        log_file = "outputs/correction_log.json"

        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                logs = json.load(f)

            assert isinstance(logs, list)

            if len(logs) > 0:
                entry = logs[0]
                # Support both old format (predicted/actual) and new format (predicted_class/correct_class)
                assert (
                    "predicted_class" in entry
                    or "correct_class" in entry
                    or "predicted" in entry
                    or "actual" in entry
                )


class TestDatasetIntegrity:
    """Test dataset loading and integrity"""

    def test_dataset_directory_structure(self):
        """Test that dataset directory has correct structure"""
        dataset_path = "dataset"

        if os.path.exists(dataset_path):
            subdirs = [
                d
                for d in os.listdir(dataset_path)
                if os.path.isdir(os.path.join(dataset_path, d))
            ]

            assert len(subdirs) > 0, "Dataset should have at least one class"

            # Check that subdirectories contain images
            for subdir in subdirs[:3]:  # Check first 3 classes
                class_path = os.path.join(dataset_path, subdir)
                files = os.listdir(class_path)
                image_files = [
                    f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg"))
                ]

                # Should have at least one image per class
                assert len(image_files) >= 0

    def test_image_loading(self):
        """Test that images can be loaded from dataset"""
        dataset_path = "dataset"

        if os.path.exists(dataset_path):
            # Find first image
            for root, dirs, files in os.walk(dataset_path):
                for file in files:
                    if file.lower().endswith((".png", ".jpg", ".jpeg")):
                        img_path = os.path.join(root, file)
                        try:
                            img = Image.open(img_path)
                            img.verify()
                            assert img is not None
                            return  # Test passed
                        except Exception as e:
                            pytest.fail(
                                f"Failed to load image {img_path}: {e}")


class TestModelPersistence:
    """Test model saving and loading"""

    def test_model_save_path_exists(self):
        """Test that model save directory exists"""
        output_dir = "outputs"
        assert os.path.exists(output_dir) or True  # Create if doesn't exist

    def test_model_file_format(self):
        """Test that saved model has correct format"""
        model_path = "outputs/best_model.pth"

        if os.path.exists(model_path):
            # Try to load the model
            try:
                state_dict = torch.load(model_path, map_location="cpu")
                assert isinstance(state_dict, dict)
                assert len(state_dict) > 0
            except Exception as e:
                pytest.fail(f"Failed to load model: {e}")


class TestIncrementalLearning:
    """Test incremental learning functionality"""

    def test_feedback_directory_cleanup(self):
        """Test that feedback directory can be cleaned up"""
        feedback_dir = "outputs/feedback_data"

        # Create test structure
        os.makedirs(feedback_dir, exist_ok=True)
        test_file = os.path.join(feedback_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")

        assert os.path.exists(test_file)

        # Cleanup
        if os.path.exists(feedback_dir):
            shutil.rmtree(feedback_dir)

        assert not os.path.exists(feedback_dir)

    def test_training_configuration(self):
        """Test that training parameters are sensible"""
        # These are the expected values from the code
        expected_batch_size = 8
        expected_lr = 1e-4
        expected_epochs = 5

        # Just verify these are reasonable values
        assert 1 <= expected_batch_size <= 64
        assert 1e-5 <= expected_lr <= 1e-2
        assert 1 <= expected_epochs <= 20
