# utils.py
import matplotlib.pyplot as plt
import torch


def show_batch_images(dataloader, class_map):
    data_iter = iter(dataloader)
    images, labels = next(data_iter)

    fig, axs = plt.subplots(3, 3, figsize=(10, 10))
    axs = axs.flatten()
    class_names = list(class_map.keys())\

    for img, lbl, ax in zip(images[:9], labels[:9], axs):
        img = img.permute(1, 2, 0).numpy()
        ax.imshow(img)
        ax.set_title(class_names[lbl])
        ax.axis('off')
    plt.tight_layout()
    plt.show()


def save_model(model, path="outputs/model.pth"):
    torch.save(model.state_dict(), path)
