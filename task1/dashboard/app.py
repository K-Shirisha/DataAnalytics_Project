"""
Sales & Revenue Analysis Dashboard
Run with:  streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales & Revenue Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .kpi-card {
        background: linear-gradient(135deg, #1e3a5f, #2d6a9f);
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .kpi-title { font-size: 14px; opacity: 0.85; margin-bottom: 6px; }
    .kpi-value { font-size: 26px; font-weight: bold; }
    .main-header {
        font-size: 32px;
        font-weight: bold;
        color: #1e3a5f;
        border-bottom: 3px solid #2d6a9f;
        padding-bottom: 8px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Load & clean data ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    data_path = Path(__file__).parent.parent / "data" / "sales_data.csv"
    df = pd.read_csv(data_path)

    # Data cleaning
    df.drop_duplicates(inplace=True)
    df.dropna(subset=["Sales", "Profit", "Quantity"], inplace=True)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Year"] = df["Order Date"].dt.year
    return df

df_raw = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.markdown("## 📊 Filters")

# Region filter
regions = ["All"] + sorted(df_raw["Region"].unique().tolist())
selected_region = st.sidebar.multiselect(
    "Region", options=df_raw["Region"].unique().tolist(),
    default=df_raw["Region"].unique().tolist()
)

# Category filter
categories = df_raw["Category"].unique().tolist()
selected_category = st.sidebar.multiselect(
    "Category", options=categories, default=categories
)

# Date filter
min_date = df_raw["Order Date"].min().date()
max_date = df_raw["Order Date"].max().date()
date_range = st.sidebar.date_input(
    "Date Range", value=(min_date, max_date),
    min_value=min_date, max_value=max_date
)

st.sidebar.markdown("---")
st.sidebar.info("Dashboard built with Streamlit & Plotly")

# ── Apply filters ─────────────────────────────────────────────────────────────
df = df_raw.copy()
if selected_region:
    df = df[df["Region"].isin(selected_region)]
if selected_category:
    df = df[df["Category"].isin(selected_category)]
if len(date_range) == 2:
    df = df[
        (df["Order Date"].dt.date >= date_range[0]) &
        (df["Order Date"].dt.date <= date_range[1])
    ]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">📊 Sales & Revenue Analysis Dashboard</div>', unsafe_allow_html=True)
st.caption(f"Showing {len(df):,} records after filters")

# ── KPI Section ───────────────────────────────────────────────────────────────
total_sales   = df["Sales"].sum()
total_profit  = df["Profit"].sum()
total_qty     = int(df["Quantity"].sum())
avg_sales     = df["Sales"].mean()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

col1, col2, col3, col4, col5 = st.columns(5)

kpis = [
    (col1, "Total Sales",       f"${total_sales:,.0f}"),
    (col2, "Total Profit",      f"${total_profit:,.0f}"),
    (col3, "Units Sold",        f"{total_qty:,}"),
    (col4, "Avg Order Value",   f"${avg_sales:,.0f}"),
    (col5, "Profit Margin",     f"{profit_margin:.1f}%"),
]

for col, title, value in kpis:
    with col:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-title">{title}</div>'
            f'<div class="kpi-value">{value}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Sales Trend + Revenue by Category ──────────────────────────────────
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Sales Trend Over Time")
    monthly = (
        df.groupby("Month")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Month")
    )
    fig_trend = px.line(
        monthly, x="Month", y="Sales",
        markers=True,
        labels={"Sales": "Total Sales ($)", "Month": "Month"},
        color_discrete_sequence=["#2d6a9f"],
    )
    fig_trend.update_layout(
        xaxis_tickangle=-45, hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#e0e0e0"),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col_right:
    st.subheader("Revenue by Category")
    cat_sales = df.groupby("Category")["Sales"].sum().reset_index()
    fig_cat = px.bar(
        cat_sales, x="Category", y="Sales",
        color="Category",
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={"Sales": "Total Sales ($)"},
    )
    fig_cat.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#e0e0e0"),
    )
    st.plotly_chart(fig_cat, use_container_width=True)

# ── Row 2: Top 5 Products + Regional Sales ────────────────────────────────────
col_left2, col_right2 = st.columns([1, 1])

with col_left2:
    st.subheader("Top 5 Products by Sales")
    top5 = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .nlargest(5)
        .reset_index()
        .sort_values("Sales")
    )
    fig_top5 = px.bar(
        top5, x="Sales", y="Product Name",
        orientation="h",
        color="Sales",
        color_continuous_scale="Blues",
        labels={"Sales": "Total Sales ($)", "Product Name": ""},
    )
    fig_top5.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#e0e0e0"),
    )
    st.plotly_chart(fig_top5, use_container_width=True)

with col_right2:
    st.subheader("Regional Sales Distribution")
    region_sales = df.groupby("Region")["Sales"].sum().reset_index()
    fig_pie = px.pie(
        region_sales, names="Region", values="Sales",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hole=0.4,
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Row 3: Profit Analysis ────────────────────────────────────────────────────
st.subheader("Profit Analysis by Category & Region")

col_p1, col_p2 = st.columns(2)

with col_p1:
    profit_cat = df.groupby("Category")["Profit"].sum().reset_index()
    fig_prof_cat = px.bar(
        profit_cat, x="Category", y="Profit",
        color="Profit",
        color_continuous_scale=["#d73027", "#fee08b", "#1a9850"],
        labels={"Profit": "Total Profit ($)"},
        title="Profit by Category",
    )
    fig_prof_cat.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#e0e0e0"),
    )
    st.plotly_chart(fig_prof_cat, use_container_width=True)

with col_p2:
    profit_region = df.groupby("Region")["Profit"].sum().reset_index()
    fig_prof_reg = px.bar(
        profit_region, x="Region", y="Profit",
        color="Profit",
        color_continuous_scale=["#d73027", "#fee08b", "#1a9850"],
        labels={"Profit": "Total Profit ($)"},
        title="Profit by Region",
    )
    fig_prof_reg.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#e0e0e0"),
    )
    st.plotly_chart(fig_prof_reg, use_container_width=True)

# ── Raw data table ────────────────────────────────────────────────────────────
with st.expander("View Raw Data"):
    st.dataframe(
        df.sort_values("Order Date", ascending=False).reset_index(drop=True),
        use_container_width=True,
        height=300,
    )
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Filtered Data as CSV", csv, "filtered_sales.csv", "text/csv")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Sales & Revenue Analysis Dashboard | Built with Streamlit & Plotly")
