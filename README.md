# Sales & Revenue Analysis Dashboard

An interactive data analytics project that explores sales performance, revenue trends, profit analysis, top products, and regional insights — built for portfolio, internship submissions, and data analyst interviews.

---

## Project Overview

This project analyses a Superstore-style sales dataset (2022–2024) and presents key business insights through:
- A **Streamlit interactive dashboard** with sidebar filters
- A **Jupyter Notebook** with step-by-step EDA and visualisations
- Auto-generated **business insights** document

---

## Technologies Used

| Tool | Purpose |
|---|---|
| Python 3 | Core language |
| Pandas | Data wrangling & cleaning |
| NumPy | Numerical operations |
| Matplotlib | Static visualisations (notebook) |
| Seaborn | Statistical visualisations (notebook) |
| Plotly | Interactive charts (dashboard) |
| Streamlit | Web dashboard framework |

---

## Dataset Details

- **Source:** Superstore-style synthetic dataset (generated via `data/generate_data.py`)
- **Rows:** 2,000 sales records
- **Columns:** Order ID, Order Date, Product Name, Category, Region, Sales, Profit, Quantity
- **Date Range:** January 2022 – December 2024
- **Categories:** Technology, Furniture, Office Supplies
- **Regions:** East, West, South, Central

---

## Folder Structure

```
DataAnalytics_Project/
│
├── data/
│   ├── generate_data.py     ← script to regenerate the dataset
│   └── sales_data.csv       ← the dataset used by the dashboard
│
├── notebooks/
│   └── analysis.ipynb       ← full EDA notebook
│
├── dashboard/
│   └── app.py               ← Streamlit dashboard
│
├── screenshots/             ← add your screenshots here
│
├── requirements.txt
├── insights.txt             ← auto-generated business insights
└── README.md
```

---

## Installation

**1. Clone or download the project**

```bash
git clone <your-repo-url>
cd DataAnalytics_Project
```

**2. Create a virtual environment (optional but recommended)**

```bash
python3 -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## How to Run

### Run the Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```

Open your browser at **http://localhost:8501**

### Run the Jupyter Notebook

```bash
jupyter notebook notebooks/analysis.ipynb
```

---

## Dashboard Features

- **Sidebar Filters:** Region, Category, Date Range
- **KPI Cards:** Total Sales, Total Profit, Units Sold, Avg Order Value, Profit Margin
- **Sales Trend:** Monthly line chart with markers
- **Revenue by Category:** Grouped bar chart
- **Top 5 Products:** Horizontal bar chart
- **Regional Distribution:** Donut pie chart
- **Profit Analysis:** Category and region bar charts (red/green colour coding)
- **Raw Data Table:** Expandable with CSV download

---

## Business Insights

Key findings from the analysis:

- **Technology** is the highest revenue-generating category
- **East region** leads in both sales and profitability
- **Q4 (Oct–Dec)** shows peak seasonal demand
- Some **Office Supplies** sub-categories operate at a loss — rationalisation recommended
- **Apple MacBook Pro** and **Leather Sofa** are the top-selling products by revenue

For the full insights report, see [`insights.txt`](insights.txt).

---

## Screenshots

> Add screenshots of the running dashboard to the `screenshots/` folder and link them here.

---

## Author

Built as a beginner-friendly data analytics portfolio project.  
Suitable for internship submissions, GitHub portfolios, and data analyst interview showcases.
