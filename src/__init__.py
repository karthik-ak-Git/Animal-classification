"""Animal Classification - Core Source Package"""

__version__ = "2.0.0"

from .model import AnimalCNN
from .train import train
from .evaluate import evaluate

__all__ = [
    "AnimalCNN",
    "train",
    "evaluate",
]
