# CLAUDE.md

## Project Title
Sales & Revenue Analysis Dashboard

---

## Project Objective
Build an interactive Sales & Revenue Analysis Dashboard using Python to analyze sales performance, revenue trends, profits, top-performing products, and regional sales insights.

The project should demonstrate:
- Data cleaning
- Data analysis
- Data visualization
- Dashboard development
- Business insights generation

---

# Tech Stack

Use:
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit

Optional:
- Scikit-learn (for future enhancements)

---

# Dataset Requirements

Use a CSV dataset containing columns similar to:

- Order Date
- Product Name
- Category
- Region
- Sales
- Profit
- Quantity

Recommended dataset:
Superstore Sales Dataset from Kaggle.

---

# Folder Structure

project/
│
├── data/
│   └── sales_data.csv
│
├── notebooks/
│   └── analysis.ipynb
│
├── dashboard/
│   └── app.py
│
├── screenshots/
│
├── requirements.txt
├── README.md
└── insights.txt

---

# Features Required

## Data Cleaning
- Handle missing values
- Convert Order Date to datetime
- Remove duplicates
- Validate numeric columns

---

## KPI Metrics
Generate and display:
- Total Sales
- Total Profit
- Total Quantity Sold
- Average Sales
- Profit Margin

---

## Visualizations Required

### 1. Sales Trend Over Time
- Monthly sales trend line chart

### 2. Revenue by Category
- Bar chart

### 3. Top 5 Products
- Horizontal bar chart

### 4. Regional Sales Analysis
- Pie chart or bar chart

### 5. Profit Analysis
- Profit by category/region

---

# Dashboard Requirements

Create an interactive dashboard using Streamlit with:
- Sidebar filters
- Region filter
- Category filter
- Date filter
- KPI cards
- Interactive charts

---

# Streamlit Requirements

The dashboard should:
- Run locally using:
  streamlit run app.py
- Have clean UI
- Be responsive
- Use Plotly charts where possible

---

# Deliverables

Generate:
1. Python source code
2. Streamlit dashboard
3. README.md
4. requirements.txt
5. Screenshots of dashboard
6. Insights document

---

# README Requirements

README should contain:
- Project overview
- Technologies used
- Dataset details
- Installation steps
- How to run the project
- Dashboard screenshots
- Business insights

---

# requirements.txt

Include:
pandas
numpy
matplotlib
seaborn
plotly
streamlit

---

# Expected Insights

Generate business insights such as:
- Highest revenue generating category
- Best-selling products
- Most profitable region
- Monthly sales trends
- Loss-making categories

---

# UI Suggestions

Dashboard sections:
1. KPI Summary
2. Sales Trends
3. Category Analysis
4. Product Performance
5. Regional Insights

Use modern layout and clean charts.

---

# Final Goal

Create a professional beginner-friendly data analytics project suitable for:
- Internship submissions
- GitHub portfolio
- Resume projects
- Data analyst interviews

---

# Instructions for Claude

While generating the project:
- Write clean and modular Python code
- Add comments in code
- Create beginner-friendly explanations
- Use proper visualization titles and labels
- Ensure charts are readable
- Generate complete runnable files
- Avoid unnecessary complexity
- Focus on practical business insights
