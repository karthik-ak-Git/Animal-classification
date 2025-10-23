"""Grad-CAM visualization module for model interpretability"""
import torch
import torch.nn.functional as F
import numpy as np
import cv2
from PIL import Image


class GradCAM:
    """Gradient-weighted Class Activation Mapping (Grad-CAM) implementation"""

    def __init__(self, model, target_layer):
        """
        Initialize Grad-CAM

        Args:
            model: PyTorch model
            target_layer: Target layer for visualization (e.g., model.base_model.layer4)
        """
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None

        # Register hooks
        self.target_layer.register_forward_hook(self.save_activation)
        self.target_layer.register_backward_hook(self.save_gradient)

    def save_activation(self, module, input, output):
        """Hook to save activations"""
        self.activations = output.detach()

    def save_gradient(self, module, grad_input, grad_output):
        """Hook to save gradients"""
        self.gradients = grad_output[0].detach()

    def generate_heatmap(self, input_tensor, target_class=None):
        """
        Generate Grad-CAM heatmap

        Args:
            input_tensor: Input image tensor (1, 3, H, W)
            target_class: Target class index (if None, use predicted class)

        Returns:
            numpy array: Heatmap (H, W)
        """
        self.model.eval()

        # Forward pass
        output = self.model(input_tensor)

        if target_class is None:
            target_class = output.argmax(dim=1).item()

        # Zero gradients
        self.model.zero_grad()

        # Backward pass
        class_score = output[0, target_class]
        class_score.backward()

        # Calculate weights (global average pooling of gradients)
        weights = torch.mean(self.gradients, dim=(2, 3), keepdim=True)

        # Weighted combination of activation maps
        cam = torch.sum(weights * self.activations, dim=1, keepdim=True)

        # Apply ReLU (only positive contributions)
        cam = F.relu(cam)

        # Normalize to [0, 1]
        cam = cam.squeeze().cpu().numpy()
        cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)

        return cam

    def overlay_heatmap(self, image, heatmap, alpha=0.4, colormap=cv2.COLORMAP_JET):
        """
        Overlay heatmap on original image

        Args:
            image: Original PIL Image or numpy array
            heatmap: Grad-CAM heatmap (H, W)
            alpha: Transparency of heatmap overlay
            colormap: OpenCV colormap

        Returns:
            numpy array: Overlaid image (RGB)
        """
        # Convert PIL Image to numpy if needed
        if isinstance(image, Image.Image):
            image = np.array(image)

        # Resize heatmap to match image size
        h, w = image.shape[:2]
        heatmap_resized = cv2.resize(heatmap, (w, h))

        # Apply colormap
        heatmap_colored = cv2.applyColorMap(
            (heatmap_resized * 255).astype(np.uint8), colormap
        )
        heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)

        # Overlay
        overlaid = (alpha * heatmap_colored + (1 - alpha) * image).astype(np.uint8)

        return overlaid


def generate_gradcam_visualization(
    model, image_tensor, original_image, target_class=None
):
    """
    Convenience function to generate Grad-CAM visualization

    Args:
        model: AnimalCNN model
        image_tensor: Preprocessed image tensor (1, 3, 224, 224)
        original_image: Original PIL Image
        target_class: Target class index (if None, use predicted class)

    Returns:
        dict: Contains 'heatmap', 'overlaid_image', 'predicted_class'
    """
    # Get the target layer (layer4 in ResNet)
    target_layer = model.base_model.layer4[-1]

    # Create Grad-CAM instance
    gradcam = GradCAM(model, target_layer)

    # Generate heatmap
    heatmap = gradcam.generate_heatmap(image_tensor, target_class)

    # Overlay on original image
    overlaid = gradcam.overlay_heatmap(original_image, heatmap)

    # Get predicted class
    with torch.no_grad():
        output = model(image_tensor)
        predicted_class = output.argmax(dim=1).item()
        confidence = F.softmax(output, dim=1)[0, predicted_class].item()

    return {
        "heatmap": heatmap,
        "overlaid_image": overlaid,
        "predicted_class": predicted_class,
        "confidence": confidence,
    }
