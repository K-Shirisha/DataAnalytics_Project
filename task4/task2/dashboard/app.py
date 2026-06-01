"""Streamlit dashboard for Customer Segmentation project."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from src.preprocessing import load_data, clean_data, select_and_scale_features
from src.clustering import compute_elbow, fit_kmeans, assign_clusters, label_segments
from src.visualization import (
    plot_gender_distribution, plot_distributions, plot_elbow,
    plot_clusters_2d, plot_segment_profiles, plot_cluster_size,
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Mall_Customers.csv")
FEATURE_COLS = ["Annual Income (k$)", "Spending Score (1-100)", "Age"]
OPTIMAL_K = 5

st.set_page_config(page_title="Customer Segmentation", page_icon="🛍️", layout="wide")

st.title("🛍️ Customer Segmentation Dashboard")
st.markdown("**K-Means Clustering | Mall Customer Dataset**")
st.markdown("---")

# --- Load & process data ---
@st.cache_data
def get_data():
    df_raw = load_data(DATA_PATH)
    df_clean = clean_data(df_raw)
    X_scaled, scaler = select_and_scale_features(df_clean, FEATURE_COLS)
    km = fit_kmeans(X_scaled, OPTIMAL_K)
    df_clustered = assign_clusters(df_clean, km)
    df_final, labels = label_segments(df_clustered, FEATURE_COLS)
    return df_final, km, X_scaled

df, km, X_scaled = get_data()

# --- Sidebar filters ---
st.sidebar.header("Filters")
segments = ["All"] + sorted(df["Segment"].unique().tolist())
selected_seg = st.sidebar.selectbox("Filter by Segment", segments)
if selected_seg != "All":
    df_view = df[df["Segment"] == selected_seg]
else:
    df_view = df

gender_filter = st.sidebar.multiselect("Filter by Gender", ["Male", "Female"], default=["Male", "Female"])
df_view = df_view[df_view["Gender"].isin(gender_filter)]

income_range = st.sidebar.slider("Annual Income (k$)", int(df["Annual Income (k$)"].min()),
                                  int(df["Annual Income (k$)"].max()),
                                  (int(df["Annual Income (k$)"].min()), int(df["Annual Income (k$)"].max())))
df_view = df_view[(df_view["Annual Income (k$)"] >= income_range[0]) &
                  (df_view["Annual Income (k$)"] <= income_range[1])]

# --- KPI Cards ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", len(df_view))
col2.metric("Avg Income (k$)", f"{df_view['Annual Income (k$)'].mean():.1f}")
col3.metric("Avg Spending Score", f"{df_view['Spending Score (1-100)'].mean():.1f}")
col4.metric("Avg Age", f"{df_view['Age'].mean():.1f}")

st.markdown("---")

# --- Segment breakdown ---
st.subheader("Customer Segment Distribution")
c1, c2 = st.columns(2)
with c1:
    seg_counts = df_view["Segment"].value_counts().reset_index()
    seg_counts.columns = ["Segment", "Count"]
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=seg_counts, x="Segment", y="Count",
                palette="Set2", ax=ax)
    ax.set_title("Customers per Segment")
    ax.tick_params(axis="x", rotation=20)
    st.pyplot(fig)
    plt.close(fig)

with c2:
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.pie(seg_counts["Count"], labels=seg_counts["Segment"],
            autopct="%1.1f%%", startangle=140,
            colors=sns.color_palette("Set2", len(seg_counts)))
    ax2.set_title("Segment Share")
    st.pyplot(fig2)
    plt.close(fig2)

# --- Scatter plot ---
st.subheader("Income vs Spending Score (Clusters)")
fig3, ax3 = plt.subplots(figsize=(10, 6))
for seg in df_view["Segment"].unique():
    sub = df_view[df_view["Segment"] == seg]
    ax3.scatter(sub["Annual Income (k$)"], sub["Spending Score (1-100)"],
                label=seg, alpha=0.7, s=70)
centers = df_view.groupby("Segment")[["Annual Income (k$)", "Spending Score (1-100)"]].mean()
ax3.scatter(centers["Annual Income (k$)"], centers["Spending Score (1-100)"],
            s=200, marker="X", color="black", zorder=5, label="Centroids")
ax3.set_xlabel("Annual Income (k$)")
ax3.set_ylabel("Spending Score (1-100)")
ax3.set_title("Customer Clusters")
ax3.legend()
ax3.grid(True, linestyle="--", alpha=0.4)
st.pyplot(fig3)
plt.close(fig3)

# --- Segment profiles table ---
st.subheader("Segment Profile Summary")
profile = df_view.groupby("Segment")[FEATURE_COLS].mean().round(2)
profile["Customer Count"] = df_view["Segment"].value_counts()
st.dataframe(profile.style.background_gradient(cmap="YlOrRd"), use_container_width=True)

# --- Raw data ---
with st.expander("View Raw Data"):
    st.dataframe(df_view[["CustomerID", "Gender", "Age", "Annual Income (k$)",
                           "Spending Score (1-100)", "Segment"]].reset_index(drop=True),
                 use_container_width=True)

st.markdown("---")
st.caption("Built with Python · Scikit-learn · Streamlit | Customer Segmentation Project")
