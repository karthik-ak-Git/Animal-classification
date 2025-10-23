"""Analytics and metrics tracking system"""
import json
import os
from datetime import datetime
from typing import Dict, List
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import seaborn as sns


class MetricsTracker:
    """Track and analyze model performance metrics"""

    def __init__(
        self,
        log_file="outputs/correction_log.json",
        metrics_file="outputs/metrics.json",
    ):
        self.log_file = log_file
        self.metrics_file = metrics_file

    def load_feedback_data(self) -> List[Dict]:
        """Load feedback/correction data"""
        if not os.path.exists(self.log_file):
            return []

        with open(self.log_file, "r") as f:
            return json.load(f)

    def calculate_accuracy(self) -> Dict:
        """Calculate model accuracy from feedback"""
        feedback_data = self.load_feedback_data()

        if not feedback_data:
            return {"accuracy": None, "total_predictions": 0}

        # Count correct vs incorrect predictions
        total = len(feedback_data)
        # Feedback is typically only for incorrect predictions
        incorrect = total

        # If you track all predictions (correct + incorrect), adjust this
        return {
            "total_feedback": total,
            "reported_errors": incorrect,
            "feedback_over_time": self._feedback_timeline(feedback_data),
        }

    def _feedback_timeline(self, feedback_data: List[Dict]) -> List[Dict]:
        """Group feedback by time periods"""
        timeline = defaultdict(int)

        for entry in feedback_data:
            timestamp = entry.get("timestamp", "")
            if timestamp:
                date = timestamp.split("T")[0]  # Get date part
                timeline[date] += 1

        return [{"date": k, "count": v} for k, v in sorted(timeline.items())]

    def class_confusion_analysis(self) -> Dict:
        """Analyze which classes are most confused"""
        feedback_data = self.load_feedback_data()

        confusion_pairs = []
        predicted_counts = Counter()
        correct_counts = Counter()

        for entry in feedback_data:
            predicted = entry.get("predicted_class", "")
            correct = entry.get("correct_class", "")

            if predicted and correct:
                confusion_pairs.append((predicted, correct))
                predicted_counts[predicted] += 1
                correct_counts[correct] += 1

        # Find most common confusions
        most_confused = Counter(confusion_pairs).most_common(10)

        return {
            "most_confused_pairs": [
                {"predicted": p, "actual": a, "count": c} for (p, a), c in most_confused
            ],
            "most_mispredicted_classes": dict(predicted_counts.most_common(10)),
            "most_corrected_to_classes": dict(correct_counts.most_common(10)),
        }

    def confidence_analysis(self) -> Dict:
        """Analyze confidence scores for correct vs incorrect predictions"""
        feedback_data = self.load_feedback_data()

        confidences = [
            entry.get("confidence", 0)
            for entry in feedback_data
            if "confidence" in entry
        ]

        if not confidences:
            return {"avg_confidence": None, "confidence_distribution": []}

        return {
            "avg_confidence": sum(confidences) / len(confidences),
            "min_confidence": min(confidences),
            "max_confidence": max(confidences),
            "confidence_scores": confidences,
        }

    def generate_report(self) -> Dict:
        """Generate comprehensive analytics report"""
        return {
            "timestamp": datetime.now().isoformat(),
            "accuracy_metrics": self.calculate_accuracy(),
            "confusion_analysis": self.class_confusion_analysis(),
            "confidence_analysis": self.confidence_analysis(),
        }

    def save_metrics(self):
        """Save metrics to file"""
        report = self.generate_report()

        os.makedirs(os.path.dirname(self.metrics_file), exist_ok=True)
        with open(self.metrics_file, "w") as f:
            json.dump(report, f, indent=2)

        return report

    def visualize_metrics(self, save_path="outputs/metrics_dashboard.png"):
        """Generate visualization dashboard"""
        report = self.generate_report()

        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(
            "Animal Classification Analytics Dashboard", fontsize=16, fontweight="bold"
        )

        # 1. Feedback Timeline
        ax1 = axes[0, 0]
        timeline = report["accuracy_metrics"].get("feedback_over_time", [])
        if timeline:
            dates = [t["date"] for t in timeline]
            counts = [t["count"] for t in timeline]
            ax1.plot(dates, counts, marker="o", linewidth=2, markersize=8)
            ax1.set_title("Feedback Submissions Over Time", fontweight="bold")
            ax1.set_xlabel("Date")
            ax1.set_ylabel("Number of Feedbacks")
            ax1.tick_params(axis="x", rotation=45)
            ax1.grid(True, alpha=0.3)
        else:
            ax1.text(0.5, 0.5, "No timeline data", ha="center", va="center")
            ax1.set_title("Feedback Timeline")

        # 2. Most Confused Classes
        ax2 = axes[0, 1]
        confused = report["confusion_analysis"]["most_confused_pairs"][:5]
        if confused:
            labels = [f"{c['predicted']}\n→\n{c['actual']}" for c in confused]
            counts = [c["count"] for c in confused]
            ax2.barh(labels, counts, color="coral")
            ax2.set_title("Top 5 Confused Class Pairs", fontweight="bold")
            ax2.set_xlabel("Count")
            ax2.invert_yaxis()
        else:
            ax2.text(0.5, 0.5, "No confusion data", ha="center", va="center")
            ax2.set_title("Confused Classes")

        # 3. Confidence Distribution
        ax3 = axes[1, 0]
        confidences = report["confidence_analysis"].get("confidence_scores", [])
        if confidences:
            ax3.hist(
                confidences, bins=20, color="skyblue", edgecolor="black", alpha=0.7
            )
            ax3.axvline(
                report["confidence_analysis"]["avg_confidence"],
                color="red",
                linestyle="--",
                linewidth=2,
                label=f"Avg: {report['confidence_analysis']['avg_confidence']:.3f}",
            )
            ax3.set_title("Confidence Score Distribution", fontweight="bold")
            ax3.set_xlabel("Confidence Score")
            ax3.set_ylabel("Frequency")
            ax3.legend()
            ax3.grid(True, alpha=0.3)
        else:
            ax3.text(0.5, 0.5, "No confidence data", ha="center", va="center")
            ax3.set_title("Confidence Distribution")

        # 4. Most Mispredicted Classes
        ax4 = axes[1, 1]
        mispredicted = report["confusion_analysis"]["most_mispredicted_classes"]
        if mispredicted:
            classes = list(mispredicted.keys())[:8]
            counts = [mispredicted[c] for c in classes]
            ax4.bar(classes, counts, color="lightcoral", edgecolor="black")
            ax4.set_title("Most Frequently Mispredicted Classes", fontweight="bold")
            ax4.set_xlabel("Class")
            ax4.set_ylabel("Misprediction Count")
            ax4.tick_params(axis="x", rotation=45)
            ax4.grid(True, alpha=0.3, axis="y")
        else:
            ax4.text(0.5, 0.5, "No misprediction data", ha="center", va="center")
            ax4.set_title("Mispredicted Classes")

        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"📊 Dashboard saved to {save_path}")

        return save_path


def generate_analytics_report():
    """Convenience function to generate and save analytics"""
    tracker = MetricsTracker()
    report = tracker.save_metrics()
    dashboard_path = tracker.visualize_metrics()

    print("✅ Analytics report generated successfully")
    print(f"📄 Metrics: outputs/metrics.json")
    print(f"📊 Dashboard: {dashboard_path}")

    return report, dashboard_path


if __name__ == "__main__":
    generate_analytics_report()
