import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def plot_class_distribution(y: pd.Series, save_path: str):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    counts = y.value_counts()
    labels = ["Normal", "Fraud"]
    colors = ["#2196F3", "#F44336"]

    axes[0].bar(labels, counts.values, color=colors, edgecolor="black", linewidth=0.7)
    axes[0].set_title("Class Distribution (Count)", fontsize=13, fontweight="bold")
    axes[0].set_ylabel("Count")
    for i, v in enumerate(counts.values):
        axes[0].text(i, v + 500, f"{v:,}", ha="center", fontweight="bold")

    axes[1].pie(
        counts.values,
        labels=labels,
        autopct="%1.3f%%",
        colors=colors,
        startangle=90,
        wedgeprops={"edgecolor": "black", "linewidth": 0.7},
    )
    axes[1].set_title("Class Distribution (Percentage)", fontsize=13, fontweight="bold")

    plt.suptitle("Class Imbalance Analysis", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()


def plot_amount_by_class(df: pd.DataFrame, save_path: str):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for ax, (cls, label, color) in zip(
        axes,
        [(0, "Normal Transactions", "#2196F3"), (1, "Fraudulent Transactions", "#F44336")],
    ):
        data = df[df["Class"] == cls]["Amount"]
        ax.hist(data, bins=60, color=color, alpha=0.85, edgecolor="white", linewidth=0.3)
        ax.set_title(label, fontsize=12, fontweight="bold")
        ax.set_xlabel("Transaction Amount (USD)")
        ax.set_ylabel("Frequency")
        ax.axvline(data.median(), color="black", linestyle="--", linewidth=1.2, label=f"Median: ${data.median():.2f}")
        ax.legend()

    plt.suptitle("Transaction Amount Distribution by Class", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()


def plot_time_distribution(df: pd.DataFrame, save_path: str):
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))

    for ax, (cls, label, color) in zip(
        axes,
        [(0, "Normal", "#2196F3"), (1, "Fraud", "#F44336")],
    ):
        data = df[df["Class"] == cls]["Time"]
        ax.hist(data, bins=100, color=color, alpha=0.8, edgecolor="white", linewidth=0.2)
        ax.set_title(f"Transaction Time - {label}", fontsize=12, fontweight="bold")
        ax.set_xlabel("Time (seconds from first transaction)")
        ax.set_ylabel("Frequency")

    plt.suptitle("Temporal Distribution of Transactions", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()

def plot_correlation_heatmap(df: pd.DataFrame, save_path: str):
    plt.figure(figsize=(22, 18))
    corr = df.corr()
    mask = None
    sns.heatmap(
        corr,
        cmap="coolwarm",
        center=0,
        linewidths=0.3,
        annot=False,
        square=True,
        cbar_kws={"shrink": 0.8},
    )
    plt.title("Feature Correlation Heatmap", fontsize=16, fontweight="bold", pad=20)
    plt.tight_layout()
    plt.savefig(save_path, dpi=120, bbox_inches="tight")
    plt.close()

def plot_feature_boxplots(df: pd.DataFrame, save_path: str):
    features = [f"V{i}" for i in range(1, 15)]
    fig, axes = plt.subplots(3, 5, figsize=(20, 12))
    axes = axes.flatten()

    for i, feat in enumerate(features):
        normal = df[df["Class"] == 0][feat]
        fraud = df[df["Class"] == 1][feat]
        axes[i].boxplot(
            [normal, fraud],
            labels=["Normal", "Fraud"],
            patch_artist=True,
            boxprops=dict(facecolor="#90CAF9"),
            medianprops=dict(color="black"),
        )
        axes[i].set_title(feat, fontsize=10, fontweight="bold")
        axes[i].tick_params(labelsize=8)

    for j in range(len(features), len(axes)):
        fig.delaxes(axes[j])

    plt.suptitle("Feature Distribution: Normal vs Fraud (V1–V14)", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_path, dpi=130, bbox_inches="tight")
    plt.close()

def generate_eda_report(df: pd.DataFrame, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    total = len(df)
    fraud_count = df["Class"].sum()
    normal_count = total - fraud_count

    print("=" * 60)
    print("           EXPLORATORY DATA ANALYSIS REPORT")
    print("=" * 60)
    print(f"Dataset Shape         : {df.shape}")
    print(f"Total Transactions    : {total:,}")
    print(f"Normal Transactions   : {normal_count:,} ({normal_count/total*100:.4f}%)")
    print(f"Fraudulent Transactions: {fraud_count:,} ({fraud_count/total*100:.4f}%)")
    print(f"Missing Values        : {df.isnull().sum().sum()}")
    print(f"Duplicate Rows        : {df.duplicated().sum()}")
    print("\n--- Amount Statistics by Class ---")
    print(df.groupby("Class")["Amount"].describe().round(2).to_string())
    print("=" * 60)

    plot_class_distribution(df["Class"], os.path.join(output_dir, "01_class_distribution.png"))
    plot_amount_by_class(df, os.path.join(output_dir, "02_amount_distribution.png"))
    plot_time_distribution(df, os.path.join(output_dir, "03_time_distribution.png"))
    plot_correlation_heatmap(df, os.path.join(output_dir, "04_correlation_heatmap.png"))
    plot_feature_boxplots(df, os.path.join(output_dir, "05_feature_boxplots.png"))

    print("EDA plots saved successfully.")
