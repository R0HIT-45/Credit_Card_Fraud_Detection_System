import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    precision_recall_curve,
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
)
def evaluate_model(model, X_test: np.ndarray, y_test: np.ndarray, model_name: str, output_dir: str) -> dict:
    os.makedirs(output_dir, exist_ok=True)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    roc_auc = roc_auc_score(y_test, y_prob)
    avg_precision = average_precision_score(y_test, y_prob)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print(f"\n{'='*60}")
    print(f"  Evaluation Report — {model_name}")
    print(f"{'='*60}")
    print(classification_report(y_test, y_pred, target_names=["Normal", "Fraud"], digits=4))
    print(f"  ROC-AUC Score         : {roc_auc:.4f}")
    print(f"  Avg Precision (AP)    : {avg_precision:.4f}")
    print(f"{'='*60}")

    safe_name = model_name.lower().replace(" ", "_")
    plot_confusion_matrix(y_test, y_pred, model_name, output_dir, safe_name)
    plot_roc_curve(y_test, y_prob, model_name, output_dir, safe_name)
    plot_precision_recall_curve(y_test, y_prob, model_name, output_dir, safe_name)
    plot_threshold_analysis(y_test, y_prob, model_name, output_dir, safe_name)

    return {
        "Model": model_name,
        "Precision": round(precision, 4),
        "Recall": round(recall, 4),
        "F1-Score": round(f1, 4),
        "ROC-AUC": round(roc_auc, 4),
        "Avg Precision": round(avg_precision, 4),
    }


def plot_confusion_matrix(y_test, y_pred, model_name: str, output_dir: str, safe_name: str):
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Normal", "Fraud"],
        yticklabels=["Normal", "Fraud"],
        linewidths=0.5,
        linecolor="gray",
        ax=ax,
    )
    ax.set_title(f"Confusion Matrix\n{model_name}", fontsize=13, fontweight="bold")
    ax.set_ylabel("Actual Label", fontsize=11)
    ax.set_xlabel("Predicted Label", fontsize=11)

    tn, fp, fn, tp = cm.ravel()
    ax.text(
        0.5,
        -0.18,
        f"TN={tn:,}  FP={fp:,}  FN={fn:,}  TP={tp:,}",
        transform=ax.transAxes,
        ha="center",
        fontsize=10,
        color="dimgray",
    )

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"06_confusion_matrix_{safe_name}.png"), dpi=150, bbox_inches="tight")
    plt.close()


def plot_roc_curve(y_test, y_prob, model_name: str, output_dir: str, safe_name: str):
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color="#E91E63", lw=2.5, label=f"ROC Curve (AUC = {auc:.4f})")
    plt.plot([0, 1], [0, 1], color="#9E9E9E", lw=1.5, linestyle="--", label="Random Classifier")
    plt.fill_between(fpr, tpr, alpha=0.08, color="#E91E63")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate (FPR)", fontsize=12)
    plt.ylabel("True Positive Rate (TPR)", fontsize=12)
    plt.title(f"ROC Curve — {model_name}", fontsize=13, fontweight="bold")
    plt.legend(loc="lower right", fontsize=11)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"07_roc_curve_{safe_name}.png"), dpi=150, bbox_inches="tight")
    plt.close()


def plot_precision_recall_curve(y_test, y_prob, model_name: str, output_dir: str, safe_name: str):
    precision_vals, recall_vals, _ = precision_recall_curve(y_test, y_prob)
    ap = average_precision_score(y_test, y_prob)
    baseline = y_test.sum() / len(y_test)

    plt.figure(figsize=(8, 6))
    plt.plot(recall_vals, precision_vals, color="#3F51B5", lw=2.5, label=f"PR Curve (AP = {ap:.4f})")
    plt.axhline(y=baseline, color="#9E9E9E", linestyle="--", lw=1.5, label=f"Baseline (= {baseline:.4f})")
    plt.fill_between(recall_vals, precision_vals, alpha=0.08, color="#3F51B5")
    plt.xlabel("Recall", fontsize=12)
    plt.ylabel("Precision", fontsize=12)
    plt.title(f"Precision-Recall Curve — {model_name}", fontsize=13, fontweight="bold")
    plt.legend(loc="upper right", fontsize=11)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"08_precision_recall_{safe_name}.png"), dpi=150, bbox_inches="tight")
    plt.close()


def plot_threshold_analysis(y_test, y_prob, model_name: str, output_dir: str, safe_name: str):
    thresholds = np.linspace(0.01, 0.99, 200)
    precisions, recalls, f1s = [], [], []

    for t in thresholds:
        y_pred_t = (y_prob >= t).astype(int)
        precisions.append(precision_score(y_test, y_pred_t, zero_division=0))
        recalls.append(recall_score(y_test, y_pred_t, zero_division=0))
        f1s.append(f1_score(y_test, y_pred_t, zero_division=0))

    best_idx = np.argmax(f1s)
    best_threshold = thresholds[best_idx]

    plt.figure(figsize=(10, 6))
    plt.plot(thresholds, precisions, label="Precision", color="#2196F3", lw=2)
    plt.plot(thresholds, recalls, label="Recall", color="#4CAF50", lw=2)
    plt.plot(thresholds, f1s, label="F1 Score", color="#F44336", lw=2)
    plt.axvline(best_threshold, color="black", linestyle="--", lw=1.5, label=f"Best Threshold = {best_threshold:.2f}")
    plt.xlabel("Decision Threshold", fontsize=12)
    plt.ylabel("Score", fontsize=12)
    plt.title(f"Threshold Analysis — {model_name}", fontsize=13, fontweight="bold")
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"09_threshold_analysis_{safe_name}.png"), dpi=150, bbox_inches="tight")
    plt.close()

    print(f"  Optimal Threshold: {best_threshold:.2f} (Best F1 = {f1s[best_idx]:.4f})")


def compare_models(results: list, output_dir: str):
    df = pd.DataFrame(results).set_index("Model")
    metrics = ["Precision", "Recall", "F1-Score", "ROC-AUC", "Avg Precision"]

    print(f"\n{'='*60}")
    print("  Final Model Comparison")
    print(f"{'='*60}")
    print(df[metrics].to_string())
    print(f"{'='*60}")

    fig, ax = plt.subplots(figsize=(11, 6))
    x = np.arange(len(metrics))
    width = 0.35
    colors = ["#2196F3", "#FF5722"]

    for i, (model_name, row) in enumerate(df.iterrows()):
        bars = ax.bar(x + i * width, [row[m] for m in metrics], width, label=model_name, color=colors[i], alpha=0.85, edgecolor="black", linewidth=0.6)
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005, f"{bar.get_height():.3f}", ha="center", va="bottom", fontsize=8.5)

    ax.set_xlabel("Metric", fontsize=12)
    ax.set_ylabel("Score", fontsize=12)
    ax.set_title("Model Performance Comparison", fontsize=14, fontweight="bold")
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(metrics, fontsize=11)
    ax.set_ylim(0, 1.1)
    ax.legend(fontsize=11)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "10_model_comparison.png"), dpi=150, bbox_inches="tight")
    plt.close()

    df[metrics].to_csv(os.path.join(output_dir, "../reports/model_comparison.csv"))
    print("Model comparison chart and CSV saved.")
