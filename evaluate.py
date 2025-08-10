# Evaluate.py
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
import torch


def evaluate(model, loader, classes):
    device = next(model.parameters()).device
    model.eval()

    all_preds = []
    all_labels = []

    with torch.no_grad():
        for batch in loader:
            images, labels = device
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            preds = torch.argmax(outputs, dim=1)

            all_preds.append(preds)
            all_labels.append(labels)

    # combine all predictions and labels
    y_pred = torch.cat(all_preds).cpu().numpy()
    y_true = torch.cat(all_labels).cpu().numpy()

    # resritct to classes actually used in test set
    used_labels = sorted(set(y_true)) | set(y_pred)
    used_class_names = [classes[i] for i in used_labels]

    # classification report
    print("\n Classification report")
    print(classification_report(y_true, y_pred,
          labels=used_labels, target_names=used_class_names))

    # confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=used_labels)
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=used_class_names,
                yticklabels=used_class_names, cmap='Blues')
    plt.title("Confusion matrix")
    plt.xlabel("Prediction")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.show()
