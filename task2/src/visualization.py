"""All visualization functions for the segmentation project."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

PALETTE = "Set2"
STYLE = "whitegrid"
SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots")

sns.set_style(STYLE)
plt.rcParams.update({"figure.dpi": 120, "font.size": 11})


def _save(fig, name):
    os.makedirs(SAVE_DIR, exist_ok=True)
    path = os.path.join(SAVE_DIR, name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {path}")


def plot_gender_distribution(df):
    fig, ax = plt.subplots(figsize=(6, 5))
    counts = df["Gender"].value_counts()
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%",
           colors=["#5B8DB8", "#E88D8D"], startangle=140, textprops={"fontsize": 12})
    ax.set_title("Gender Distribution", fontsize=14, fontweight="bold")
    _save(fig, "01_gender_distribution.png")


def plot_distributions(df):
    cols = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    for ax, col in zip(axes, cols):
        sns.histplot(df[col], kde=True, ax=ax, color="#5B8DB8", edgecolor="white")
        ax.set_title(f"{col} Distribution", fontweight="bold")
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
    fig.suptitle("Feature Distributions", fontsize=15, fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "02_feature_distributions.png")


def plot_boxplots(df):
    cols = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    for ax, col in zip(axes, cols):
        sns.boxplot(y=df[col], ax=ax, color="#98D8C8")
        ax.set_title(f"{col} Boxplot", fontweight="bold")
    fig.suptitle("Boxplots — Outlier Check", fontsize=15, fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "03_boxplots.png")


def plot_correlation_heatmap(df):
    num_df = df.select_dtypes(include="number").drop(
        columns=["CustomerID", "Cluster", "Gender_Encoded"], errors="ignore"
    )
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(num_df.corr(), annot=True, fmt=".2f", cmap="coolwarm",
                linewidths=0.5, ax=ax)
    ax.set_title("Correlation Heatmap", fontsize=14, fontweight="bold")
    fig.tight_layout()
    _save(fig, "04_correlation_heatmap.png")


def plot_elbow(wcss):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(range(1, len(wcss) + 1), wcss, marker="o", color="#E88D8D", linewidth=2)
    ax.set_title("Elbow Method — Optimal K Selection", fontsize=14, fontweight="bold")
    ax.set_xlabel("Number of Clusters (K)")
    ax.set_ylabel("WCSS (Within-Cluster Sum of Squares)")
    ax.grid(True, linestyle="--", alpha=0.5)
    _save(fig, "05_elbow_method.png")


def plot_clusters_2d(df, km, X_scaled, feature_cols):
    # Use first two features for the 2D plot
    x_col, y_col = feature_cols[0], feature_cols[1]
    centroids_orig = km.cluster_centers_

    segments = df["Segment"].unique()
    palette = sns.color_palette(PALETTE, len(segments))
    color_map = dict(zip(sorted(segments), palette))

    fig, ax = plt.subplots(figsize=(10, 7))
    for seg in sorted(df["Segment"].unique()):
        subset = df[df["Segment"] == seg]
        ax.scatter(subset[x_col], subset[y_col], label=seg,
                   color=color_map[seg], alpha=0.7, edgecolors="white", s=80)

    # Plot centroids (inverse-transform from scaled space using original feature means)
    cluster_centers = df.groupby("Cluster")[[x_col, y_col]].mean()
    ax.scatter(cluster_centers[x_col], cluster_centers[y_col],
               s=250, marker="X", color="black", zorder=5, label="Centroids")

    ax.set_title("Customer Segments — K-Means Clustering", fontsize=14, fontweight="bold")
    ax.set_xlabel(x_col, fontsize=12)
    ax.set_ylabel(y_col, fontsize=12)
    ax.legend(title="Segment", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()
    _save(fig, "06_cluster_scatter.png")


def plot_segment_profiles(df, feature_cols):
    summary = df.groupby("Segment")[feature_cols].mean().reset_index()
    fig, axes = plt.subplots(1, len(feature_cols), figsize=(5 * len(feature_cols), 5))
    if len(feature_cols) == 1:
        axes = [axes]
    palette = sns.color_palette(PALETTE, len(summary))
    for ax, col in zip(axes, feature_cols):
        sns.barplot(data=summary, x="Segment", y=col, hue="Segment",
                    palette=palette, legend=False, ax=ax)
        ax.set_title(f"Avg {col} per Segment", fontweight="bold")
        ax.set_xlabel("")
        ax.tick_params(axis="x", rotation=20)
    fig.suptitle("Segment Profiles", fontsize=15, fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "07_segment_profiles.png")


def plot_cluster_size(df):
    counts = df["Segment"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=counts.index, y=counts.values, hue=counts.index,
                palette=sns.color_palette(PALETTE, len(counts)), legend=False, ax=ax)
    ax.set_title("Customer Count per Segment", fontsize=14, fontweight="bold")
    ax.set_xlabel("Segment")
    ax.set_ylabel("Number of Customers")
    ax.tick_params(axis="x", rotation=15)
    for bar, val in zip(ax.patches, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                str(val), ha="center", fontsize=11)
    fig.tight_layout()
    _save(fig, "08_segment_sizes.png")
