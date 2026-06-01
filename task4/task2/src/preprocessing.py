"""Data loading, cleaning, and preprocessing utilities."""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def load_data(filepath):
    """Load CSV data and return a DataFrame."""
    df = pd.read_csv(filepath)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def inspect_data(df):
    """Print basic dataset information."""
    print("\n--- Dataset Info ---")
    df.info()
    print("\n--- First 5 Rows ---")
    print(df.head())
    print("\n--- Basic Statistics ---")
    print(df.describe())
    print("\n--- Missing Values ---")
    print(df.isnull().sum())
    print("\n--- Duplicate Rows ---")
    print(f"Duplicates: {df.duplicated().sum()}")


def clean_data(df):
    """Handle missing values, duplicates, and type issues."""
    df = df.drop_duplicates()
    df = df.dropna()

    numeric_cols = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna()

    # Encode Gender as binary feature
    if "Gender" in df.columns:
        df["Gender_Encoded"] = df["Gender"].map({"Male": 0, "Female": 1})

    print(f"\nCleaned dataset: {df.shape[0]} rows remaining")
    return df


def select_and_scale_features(df, feature_cols):
    """Extract and standardize selected feature columns."""
    X = df[feature_cols].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, scaler
