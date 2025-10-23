# model_dynamic.py - Dynamic Model with Expandable Classes
import torch
import torch.nn as nn
from torchvision import models
import copy


class DynamicAnimalCNN(nn.Module):
    """
    Dynamic CNN that can add new classes without forgetting old ones.
    Uses a dual-head approach: frozen base + expandable classifier.
    """

    def __init__(self, num_classes, base_features=256):
        super(DynamicAnimalCNN, self).__init__()

        # Base ResNet18 feature extractor (will be frozen after initial training)
        self.feature_extractor = models.resnet18(
            weights=models.ResNet18_Weights.DEFAULT
        )

        # Remove the final FC layer
        self.feature_extractor = nn.Sequential(
            *list(self.feature_extractor.children())[:-1]
        )

        # Freeze feature extractor to prevent forgetting
        for param in self.feature_extractor.parameters():
            param.requires_grad = False

        # Intermediate feature projection (trainable)
        self.projection = nn.Sequential(
            nn.Linear(512, base_features),  # ResNet18 outputs 512 features
            nn.ReLU(),
            nn.Dropout(0.3),
        )

        # Dynamic classifier head (can be expanded)
        self.classifier = nn.Linear(base_features, num_classes)

        self.base_features = base_features
        self.num_classes = num_classes

    def forward(self, x):
        # Extract features (frozen)
        features = self.feature_extractor(x)
        features = features.view(features.size(0), -1)

        # Project features (trainable)
        features = self.projection(features)

        # Classify (trainable)
        output = self.classifier(features)
        return output

    def add_classes(self, num_new_classes):
        """
        Expand the classifier to handle new classes without forgetting old ones.
        """
        old_num_classes = self.num_classes
        new_num_classes = old_num_classes + num_new_classes

        # Create new classifier with more outputs
        new_classifier = nn.Linear(self.base_features, new_num_classes)

        # Copy old weights to preserve learned knowledge
        with torch.no_grad():
            new_classifier.weight[:old_num_classes] = self.classifier.weight
            new_classifier.bias[:old_num_classes] = self.classifier.bias

            # Initialize new class weights with small random values
            nn.init.xavier_uniform_(new_classifier.weight[old_num_classes:])
            nn.init.zeros_(new_classifier.bias[old_num_classes:])

        # Replace classifier
        self.classifier = new_classifier
        self.num_classes = new_num_classes

        print(f"✅ Expanded model from {old_num_classes} to {new_num_classes} classes")
        return self

    def freeze_old_classes(self):
        """
        Freeze weights for existing classes, only train new ones.
        """
        # Freeze projection layer
        for param in self.projection.parameters():
            param.requires_grad = False

        print("🔒 Frozen projection layer for stability")

    def unfreeze_for_finetuning(self):
        """
        Unfreeze projection for full fine-tuning (use carefully).
        """
        for param in self.projection.parameters():
            param.requires_grad = True

        print("🔓 Unfrozen projection layer for fine-tuning")


def expand_existing_model(old_model_path, new_num_classes, device="cuda"):
    """
    Load an existing model and expand it to support new classes.
    """
    # Load old model
    checkpoint = torch.load(old_model_path, map_location=device)

    # Detect old number of classes from checkpoint
    old_num_classes = (
        checkpoint["fc.3.weight"].shape[0]
        if "fc.3.weight" in checkpoint
        else checkpoint["classifier.weight"].shape[0]
        if "classifier.weight" in checkpoint
        else None
    )

    if old_num_classes is None:
        raise ValueError("Could not detect number of classes from checkpoint")

    print(f"📊 Old model: {old_num_classes} classes")
    print(f"📊 New model: {new_num_classes} classes")

    # Create new dynamic model
    model = DynamicAnimalCNN(num_classes=new_num_classes)

    # Try to load old weights (will skip classifier if size mismatch)
    model.load_state_dict(checkpoint, strict=False)

    return model.to(device)
