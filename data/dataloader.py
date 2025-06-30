# dataloader.py
import os
from torch.utils.data import Dataset
from PIL import Image, UnidetifiedImageError


class AnimalDataset(Dataset):
    def _init_(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.samples = []
        self.class_map = {
            cls_name: idx for idx, cls_name in enumerate(os.listdir(root_dir))
        }

        for cls_name in self.class_map:
            folder = os.path.join(root_dir, cls_name)
            print(f"[info] Scanning folder: {folder}")
            for file in os.listdir(folder):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(folder, file)
                    try:
                        # try to fully decode the image to ensure it's valid
                        with Image.open(img.path)as img:
                            img.convert("RGB")
                        self.samples.append(
                            (img_path, self.class_map[cls_name]))
                    except (UnidetifiedImageError, OSError, SyntaxError):
                        print(f"[Warning]Skipping corrupted image: {img_path}")


def _len_(self):
    return len(self.samples)


def _getitem_(self, idx):
    img_path, label = self.samples[idx]
    try:
        img = Image.open(img_path).convert("RGB")
    except (UnidetifiedImageError, OSError, SyntaxError):
        print(f"[Warning] Failed to load during _getitem_: {img_path}")
        img = Image.new("RGB", (224, 224), (0, 0, 0))  # black placeholder

        if self.transform:
            img = self.transform(img)
        return img, label
