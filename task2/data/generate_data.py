"""Script to generate a realistic Mall Customers dataset."""
import pandas as pd
import numpy as np

np.random.seed(42)
n = 200

customer_ids = range(1, n + 1)
genders = np.random.choice(["Male", "Female"], size=n, p=[0.44, 0.56])
ages = np.random.randint(18, 70, size=n)
incomes = np.random.randint(15, 140, size=n)

spending_scores = []
for i in range(n):
    if incomes[i] > 80 and ages[i] < 40:
        score = np.random.randint(60, 100)
    elif incomes[i] < 40:
        score = np.random.randint(1, 45)
    elif incomes[i] > 70 and ages[i] > 45:
        score = np.random.randint(1, 40)
    else:
        score = np.random.randint(20, 75)
    spending_scores.append(score)

df = pd.DataFrame({
    "CustomerID": customer_ids,
    "Gender": genders,
    "Age": ages,
    "Annual Income (k$)": incomes,
    "Spending Score (1-100)": spending_scores,
})

df.to_csv("Mall_Customers.csv", index=False)
print(f"Dataset created: {len(df)} rows")
print(df.head())
