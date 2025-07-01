# dataloader.py
import os
from torch.utils.data import Dataset
from PIL import Image, UnidentifiedImageError


class AnimalDataset(Dataset):
    def _init_(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.samples = []
        self.class_map = {
            cls_name: idx for idx, cls_name in enumerate(sorted(os.listdir(root_dir)))
        }

        for cls_name in self.class_map:
            folder = os.path.join(root_dir, cls_name)
            print(f"[info]Scanning folder: {folder}")
            for file in os.listdir(folder):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(folder, file)
                    try:
                        # try to fully decode the image to ensure it's valid
                        with Image.open(img_path) as img:
                            img.convert('RGB')
                        self.samples.append(
                            (img_path, self.class_map[cls_name]))
                    except (UnidentifiedImageError, OSError, SyntaxError):
                        print(
                            f"[warning]Skipping invalied or currupt image: {img_path}")
