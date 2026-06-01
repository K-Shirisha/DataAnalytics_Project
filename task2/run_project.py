"""
Main script — runs the full Customer Segmentation pipeline and saves all outputs.
Usage:  python3 run_project.py
"""
import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from src.preprocessing import load_data, inspect_data, clean_data, select_and_scale_features
from src.clustering import compute_elbow, fit_kmeans, assign_clusters, label_segments
from src.visualization import (
    plot_gender_distribution,
    plot_distributions,
    plot_boxplots,
    plot_correlation_heatmap,
    plot_elbow,
    plot_clusters_2d,
    plot_segment_profiles,
    plot_cluster_size,
)

DATA_PATH = os.path.join(BASE_DIR, "data", "Mall_Customers.csv")
FEATURE_COLS = ["Annual Income (k$)", "Spending Score (1-100)", "Age"]
OPTIMAL_K = 5

# ── 1. Load & inspect ──────────────────────────────────────────────────────
print("\n========== STEP 1: Loading Data ==========")
df = load_data(DATA_PATH)
inspect_data(df)

# ── 2. Clean ───────────────────────────────────────────────────────────────
print("\n========== STEP 2: Cleaning Data ==========")
df = clean_data(df)

# ── 3. EDA Visualizations ─────────────────────────────────────────────────
print("\n========== STEP 3: EDA Visualizations ==========")
plot_gender_distribution(df)
plot_distributions(df)
plot_boxplots(df)
plot_correlation_heatmap(df)

# ── 4. Feature Scaling ────────────────────────────────────────────────────
print("\n========== STEP 4: Feature Scaling ==========")
X_scaled, scaler = select_and_scale_features(df, FEATURE_COLS)
print(f"Features scaled: {FEATURE_COLS}")

# ── 5. Elbow Method ───────────────────────────────────────────────────────
print("\n========== STEP 5: Elbow Method ==========")
wcss = compute_elbow(X_scaled, max_k=10)
plot_elbow(wcss)
print(f"Selected optimal K = {OPTIMAL_K}")

# ── 6. K-Means Clustering ─────────────────────────────────────────────────
print("\n========== STEP 6: K-Means Clustering ==========")
km = fit_kmeans(X_scaled, OPTIMAL_K)
df = assign_clusters(df, km)

# ── 7. Segment Labeling ───────────────────────────────────────────────────
print("\n========== STEP 7: Segment Labeling ==========")
df, segment_labels = label_segments(df, FEATURE_COLS)
print("Segment mapping:", segment_labels)

# ── 8. Cluster Visualizations ─────────────────────────────────────────────
print("\n========== STEP 8: Cluster Visualizations ==========")
plot_clusters_2d(df, km, X_scaled, FEATURE_COLS)
plot_segment_profiles(df, FEATURE_COLS)
plot_cluster_size(df)

# ── 9. Segment Summary ────────────────────────────────────────────────────
print("\n========== STEP 9: Segment Summary ==========")
summary = df.groupby("Segment")[FEATURE_COLS].mean().round(2)
summary["Count"] = df["Segment"].value_counts()
print(summary.to_string())

# ── 10. Save clustered dataset ────────────────────────────────────────────
out_path = os.path.join(BASE_DIR, "data", "customers_segmented.csv")
df.to_csv(out_path, index=False)
print(f"\nSegmented dataset saved: {out_path}")
print("\nPipeline complete -- check screenshots/ for all visualizations.")
