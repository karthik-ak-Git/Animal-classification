"""Unit tests for model architecture and functionality"""
from src.model import AnimalCNN
import pytest
import torch
import torch.nn as nn
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class TestAnimalCNN:
    """Test suite for AnimalCNN model"""

    @pytest.fixture
    def model(self):
        """Create a model instance for testing"""
        return AnimalCNN(num_classes=10)

    def test_model_initialization(self, model):
        """Test that model initializes correctly"""
        assert isinstance(model, nn.Module)
        assert hasattr(model, 'base_model')
        assert hasattr(model.base_model, 'fc')

    def test_model_output_shape(self, model):
        """Test that model outputs correct shape"""
        batch_size = 4
        dummy_input = torch.randn(batch_size, 3, 224, 224)
        output = model(dummy_input)

        assert output.shape == (batch_size, 10)
        assert not torch.isnan(output).any()

    def test_model_gradient_flow(self, model):
        """Test that gradients flow through layer4"""
        dummy_input = torch.randn(1, 3, 224, 224)
        output = model(dummy_input)
        loss = output.sum()
        loss.backward()

        # Check that layer4 has gradients
        layer4_has_grad = False
        for name, param in model.base_model.named_parameters():
            if 'layer4' in name and param.grad is not None:
                layer4_has_grad = True
                break

        assert layer4_has_grad, "Layer4 should have gradients"

    def test_model_fc_layer(self, model):
        """Test that FC layer is correctly configured"""
        fc = model.base_model.fc
        assert isinstance(fc, nn.Sequential)
        assert len(fc) == 4  # Linear, ReLU, Dropout, Linear

    def test_model_num_classes(self):
        """Test model with different number of classes"""
        for num_classes in [5, 10, 75, 100]:
            model = AnimalCNN(num_classes=num_classes)
            dummy_input = torch.randn(1, 3, 224, 224)
            output = model(dummy_input)
            assert output.shape[1] == num_classes

    def test_model_device_compatibility(self, model):
        """Test that model works on CPU"""
        device = torch.device('cpu')
        model = model.to(device)
        dummy_input = torch.randn(1, 3, 224, 224).to(device)
        output = model(dummy_input)
        assert output.device.type == 'cpu'

    def test_model_eval_mode(self, model):
        """Test that model can switch between train and eval modes"""
        model.train()
        assert model.training

        model.eval()
        assert not model.training

    def test_model_state_dict(self, model):
        """Test that model state dict can be saved and loaded"""
        state_dict = model.state_dict()
        assert isinstance(state_dict, dict)
        assert len(state_dict) > 0

        # Create new model and load state
        new_model = AnimalCNN(num_classes=10)
        new_model.load_state_dict(state_dict)

        # Check parameters match
        for (name1, param1), (name2, param2) in zip(
            model.named_parameters(), new_model.named_parameters()
        ):
            assert name1 == name2
            assert torch.equal(param1, param2)
