# evaluate.py
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import torch


def evaluate(model, loader, classes):
    device = next(model.parameters()).device
    model.eval()

    all_preds = []
    all_labels = []

    with torch.no_grad():
        for batch in loader:
            images, labels = batch
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            preds = torch.argmax(outputs, dim=1)

            all_preds.append(preds)
            all_labels.append(labels)

    # 🧠 Combine all predictions and labels
    y_pred = torch.cat(all_preds).cpu().numpy()
    y_true = torch.cat(all_labels).cpu().numpy()

    # 🏷️ Restrict to classes actually used in test set
    used_labels = sorted(set(y_true) | set(y_pred))
    used_class_names = [classes[i] for i in used_labels]

    # 📋 Classification Report
    print("\n📋 Classification Report:")
    print(
        classification_report(
            y_true, y_pred, labels=used_labels, target_names=used_class_names
        )
    )

    # 🧩 Confusion Matrix
    cm = confusion_matrix(y_true, y_pred, labels=used_labels)
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        xticklabels=used_class_names,
        yticklabels=used_class_names,
        cmap="Blues",
    )
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.show()
