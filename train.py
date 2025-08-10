# Train.py
import torch
from torch.utils.tensorboard import SummaryWriter


def train(model, train_loader, val_loader, criterion, optimizer, scheduler, device, num_epochs=50, save_path="outputs/best_model.pth"):
    best_val_loss = float("inf")
    patience = 5
    epochs_no_improve = 0
    writer = SummaryWriter(log_dir="logs")

    for epoch in range(1, num_epochs + 1):
        model.train()
        total_loss, correct, total = 0, 0, 0

        for imgs, labels in train_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * imgs.size(0)
            correct += (outputs.argmax(1) == labels).sum().item()
            total += imgs.size(0)

        avg_train_loss = total_loss / total
        train_acc = correct / total

        # Validation phase
        model.eval()
        val_loss, val_correct, val_total = 0, 0, 0

        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(device), labels.to(device)
                outputs = model(imgs)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * imgs.size(0)
                val_correct += (outputs.argmax(1) == labels).sum().item()
                val_total += imgs.size(0)

        avg_val_loss = val_loss / val_total
        val_acc = val_correct / val_total

        # tensorBoard logging
        writer.add_scalar("Loss/train", avg_train_loss, epoch)
        writer.add_scalar("Accuracy/train", train_acc, epoch)
        writer.add_scalar("Accuracy/val", avg_val_loss, epoch)
        writer.add_scalar("Loss/val", val_acc, epoch)

        # Scheduler step
        scheduler.step(avg_val_loss)

        # save best model
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), save_path)
            epochs_no_improve = 0
        else:
            epochs_no_improve += 1

        print(f"\033[96m Epoch {epoch:02d}| Train Loss: {avg_train_loss:.4f} | Train Acc: {train_acc:.4f} | Val Loss: {avg_val_loss:.4f} | Val Acc: {val_acc:.4f}\033[0m")
        # Early stopping

        if epochs_no_improve >= patience:
            print(
                f"\n Early stopping trigged after {epoch} epochs (no val improvement in {patience} rounds).\n")
            break

    writer.close()
