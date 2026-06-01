# Customer Segmentation using K-Means Clustering

A complete, beginner-friendly Machine Learning project that groups mall customers into meaningful segments based on their purchasing behavior and demographics.

---

## Problem Statement

Retail businesses serve thousands of customers with very different income levels, age groups, and spending habits. A one-size-fits-all marketing strategy is inefficient. This project uses **K-Means Clustering** (unsupervised ML) to automatically discover distinct customer groups so the business can tailor its strategy to each segment.

---

## Technologies Used

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Pandas | Data loading & manipulation |
| NumPy | Numerical operations |
| Matplotlib / Seaborn | Static visualizations |
| Scikit-learn | K-Means model, scaling |
| Streamlit | Interactive dashboard |

---

## Dataset

**Mall Customer Segmentation Dataset**

| Column | Description |
|---|---|
| CustomerID | Unique customer identifier |
| Gender | Male / Female |
| Age | Customer age (18–70) |
| Annual Income (k$) | Annual income in thousands of USD |
| Spending Score (1-100) | Mall-assigned spending behavior score |

200 customers · 5 features · No missing values

---

## Project Structure

```
task2/
├── data/
│   ├── Mall_Customers.csv          # Raw dataset
│   └── customers_segmented.csv     # Dataset with cluster labels
├── notebooks/
│   └── customer_segmentation.ipynb # Full Jupyter walkthrough
├── src/
│   ├── preprocessing.py            # Data loading & cleaning
│   ├── clustering.py               # K-Means model
│   └── visualization.py            # All chart functions
├── dashboard/
│   └── app.py                      # Streamlit dashboard
├── screenshots/                    # All generated charts
├── run_project.py                  # One-click pipeline runner
├── insights.txt                    # Business insights report
├── requirements.txt
└── README.md
```

---

## Steps Performed

1. **Data Loading** — Read CSV, inspect shape, dtypes, and first rows
2. **Data Cleaning** — Remove duplicates, handle nulls, encode Gender
3. **EDA** — Gender pie chart, feature histograms, boxplots, correlation heatmap
4. **Feature Scaling** — StandardScaler on Income, Spending Score, Age
5. **Optimal K Selection** — Elbow Method (WCSS vs K plot)
6. **K-Means Clustering** — Fit model with K=5, assign cluster labels
7. **Segment Labeling** — Meaningful names from cluster statistics
8. **Visualizations** — 2D scatter, bar profiles, segment size charts

---

## Model Explanation

**K-Means Clustering** partitions customers into K groups by minimizing the within-cluster sum of squares (WCSS). Each customer belongs to the cluster whose centroid is nearest.

- **Initialization**: k-means++ (smart seeding for faster convergence)
- **Iterations**: until centroids stabilize
- **Optimal K**: chosen at the "elbow" of the WCSS curve (K=5)
- **Silhouette Score**: 0.38 — clusters are well-separated for retail data

---

## Customer Segments Discovered

| Segment | Avg Income | Avg Score | Avg Age | Count |
|---|---|---|---|---|
| Premium Customers | $110k | 77 | 31 yrs | ~47 |
| Careful Spenders | $109k | 20 | 56 yrs | ~60 |
| Budget Customers | $36k | 26 | 42 yrs | ~62 |
| High Spenders | $36k | 65 | 35 yrs | ~25 |
| Average Customers | $63k | 53 | 52 yrs | ~31 |

---

## Visualizations

All charts are saved in `screenshots/`:

| File | Description |
|---|---|
| 01_gender_distribution.png | Pie chart — male/female split |
| 02_feature_distributions.png | Histograms for Age, Income, Score |
| 03_boxplots.png | Boxplots — outlier detection |
| 04_correlation_heatmap.png | Feature correlation matrix |
| 05_elbow_method.png | WCSS vs K — elbow at K=5 |
| 06_cluster_scatter.png | 2D scatter plot of all clusters |
| 07_segment_profiles.png | Avg feature values per segment |
| 08_segment_sizes.png | Customer count per segment |

---

## Business Insights Summary

- **Premium Customers** are the highest-value group — prioritize retention
- **Careful Spenders** earn high but spend low — biggest growth opportunity
- **Budget Customers** are the largest group — volume play with promotions
- **High Spenders** respond to flexible payment and trend marketing
- Full recommendations in `insights.txt`

---

## Installation

```bash
pip install -r requirements.txt
```

---

## How to Run

**Full Pipeline (generates all charts + segmented CSV):**
```bash
python3 run_project.py
```

**Streamlit Dashboard:**
```bash
streamlit run dashboard/app.py
```

**Jupyter Notebook:**
```bash
jupyter lab notebooks/customer_segmentation.ipynb
```

---

## Skills Demonstrated

- Unsupervised Machine Learning
- Data Cleaning & EDA
- Feature Engineering & Scaling
- Cluster Evaluation (Elbow + Silhouette)
- Business Intelligence & Segment Profiling
- Interactive Dashboard Development
