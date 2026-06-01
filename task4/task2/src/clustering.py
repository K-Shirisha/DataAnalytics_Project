"""K-Means clustering model training and evaluation."""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def compute_elbow(X_scaled, max_k=10):
    """Compute WCSS for k=1 to max_k to find the elbow point."""
    wcss = []
    for k in range(1, max_k + 1):
        km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
        km.fit(X_scaled)
        wcss.append(km.inertia_)
    return wcss


def fit_kmeans(X_scaled, n_clusters):
    """Train a KMeans model and return the fitted model."""
    km = KMeans(n_clusters=n_clusters, init="k-means++", n_init=10, random_state=42)
    km.fit(X_scaled)
    score = silhouette_score(X_scaled, km.labels_)
    print(f"KMeans fitted | k={n_clusters} | Silhouette Score: {score:.4f}")
    return km


def assign_clusters(df, km):
    """Add cluster labels to the original DataFrame."""
    df = df.copy()
    df["Cluster"] = km.labels_
    return df


def label_segments(df, feature_cols):
    """Assign human-readable segment names based on cluster stats."""
    summary = df.groupby("Cluster")[feature_cols].mean()

    income_col = "Annual Income (k$)"
    score_col = "Spending Score (1-100)"

    labels = {}
    for cluster_id, row in summary.iterrows():
        income = row.get(income_col, 50)
        score = row.get(score_col, 50)
        if income >= 70 and score >= 60:
            labels[cluster_id] = "Premium Customers"
        elif income >= 70 and score < 45:
            labels[cluster_id] = "Careful Spenders"
        elif income < 45 and score >= 55:
            labels[cluster_id] = "High Spenders"
        elif income < 45 and score < 45:
            labels[cluster_id] = "Budget Customers"
        else:
            labels[cluster_id] = "Average Customers"

    df["Segment"] = df["Cluster"].map(labels)
    return df, labels
