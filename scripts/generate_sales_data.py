import numpy as np
import pandas as pd

np.random.seed(42)

START_DATE = "2023-01-01"
END_DATE = "2024-12-31"

PRODUCTS = [
    {"id": "P001", "base_demand": 20, "price": 10.0},
    {"id": "P002", "base_demand": 8, "price": 25.0},
    {"id": "P003", "base_demand": 3, "price": 50.0},
]

STORE_ID = "STORE_001"

dates = pd.date_range(start=START_DATE, end=END_DATE, freq="D")

rows = []

for product in PRODUCTS:
    trend = np.linspace(0, 5, len(dates))
    weekly_seasonality = 1 + 0.2 * np.sin(2 * np.pi * dates.dayofweek / 7)
    yearly_seasonality = 1 + 0.3 * np.sin(2 * np.pi * dates.dayofyear / 365)

    for i, date in enumerate(dates):
        promo = np.random.rand() < 0.1  # 10% días con promo
        promo_multiplier = 1.5 if promo else 1.0

        noise = np.random.normal(0, 2)
        demand = (
            product["base_demand"]
            * weekly_seasonality[i]
            * yearly_seasonality[i]
            * promo_multiplier
            + trend[i]
            + noise
        )

        # Días sin ventas
        if np.random.rand() < 0.05:
            demand = 0

        # Outliers (ventas extremas)
        if np.random.rand() < 0.01:
            demand *= 4

        units_sold = max(0, int(round(demand)))

        rows.append({
            "date": date.date(),
            "product_id": product["id"],
            "store_id": STORE_ID,
            "units_sold": units_sold,
            "price": product["price"],
            "promotion_flag": promo
        })

df = pd.DataFrame(rows)

output_path = "../data/raw/store_001/sales_2023_2024.csv"
df.to_csv(output_path, index=False)

print(f"Datos generados en {output_path}")
