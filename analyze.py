# analyze.py
# FINDINGS (2024):
# The two factors that actually separate cars that later broke down from those that did not are
# km_since_service (correlation 0.40: cars in the 10-15k range broke down at 43% vs 3% for
# freshly-serviced cars) and avg_daily_km (correlation 0.25: high-mileage-per-day cars broke
# down at roughly 3x the rate of low-usage ones). Total odometer and age_years correlate at
# almost zero — the obvious "older/higher-mileage cars break down more" assumption is not
# supported by this data. Risk score is built from these two factors only.

import pandas as pd

df = pd.read_csv("fleet_history.csv")

# --- 1. Verify which columns separate the two groups --------------------------

print("=== Mean by outcome ===")
print(
    df.groupby("broke_down")[
        ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]
    ]
    .mean()
    .round(2)
)
print()

print("=== Pearson correlation with broke_down ===")
corr = (
    df[["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years", "broke_down"]]
    .corr()["broke_down"]
    .drop("broke_down")
    .sort_values(ascending=False)
)
print(corr.round(3))
print()

print("=== Breakdown rate by km_since_service band ===")
df["kss_band"] = pd.cut(
    df["km_since_service"],
    bins=[0, 5_000, 10_000, 15_000, 99_999],
    labels=["0–5 k", "5–10 k", "10–15 k", "15 k+"],
)
print(
    df.groupby("kss_band", observed=True)["broke_down"]
    .agg(cars="count", breakdowns="sum", rate="mean")
    .round(3)
)
print()

print("=== Breakdown rate by avg_daily_km band ===")
df["daily_band"] = pd.cut(
    df["avg_daily_km"],
    bins=[0, 100, 150, 200, 999],
    labels=["< 100", "100–150", "150–200", "200 +"],
)
print(
    df.groupby("daily_band", observed=True)["broke_down"]
    .agg(cars="count", breakdowns="sum", rate="mean")
    .round(3)
)
print()

# --- 2. Build a 0–100 risk score from the two predictive factors --------------
# Both components are min-max normalised so they sit on the same scale.
# Weights reflect their relative correlations: km_since_service 0.40, avg_daily_km 0.25.

kss_min, kss_max = df["km_since_service"].min(), df["km_since_service"].max()
daily_min, daily_max = df["avg_daily_km"].min(), df["avg_daily_km"].max()

df["kss_norm"]   = (df["km_since_service"] - kss_min) / (kss_max - kss_min)
df["daily_norm"] = (df["avg_daily_km"]     - daily_min) / (daily_max - daily_min)

W_KSS   = 0.62   # share of (0.40 / (0.40 + 0.25))
W_DAILY = 0.38   # share of (0.25 / (0.40 + 0.25))

df["risk_score"] = ((df["kss_norm"] * W_KSS + df["daily_norm"] * W_DAILY) * 100).round(1)

# --- 3. Print cars ranked by risk, highest first ------------------------------

ranked = df[["car_id", "km_since_service", "avg_daily_km", "risk_score", "broke_down"]].sort_values(
    "risk_score", ascending=False
)

print("=== Fleet ranked by breakdown risk (highest first) ===")
print(f"{'Car':<12} {'km_since_svc':>13} {'avg_daily_km':>13} {'risk_score':>11} {'broke_down':>11}")
print("-" * 62)
for _, row in ranked.iterrows():
    marker = " <-- actual breakdown" if row["broke_down"] == 1 else ""
    print(
        f"{row['car_id']:<12} {int(row['km_since_service']):>13,} {int(row['avg_daily_km']):>13,}"
        f" {row['risk_score']:>11.1f}{marker}"
    )

print()
top10_hit_rate = ranked.head(10)["broke_down"].mean()
print(f"Breakdown rate in top-10 risk cars : {top10_hit_rate*100:.0f}%  (vs {df['broke_down'].mean()*100:.0f}% fleet average)")
print(f"Breakdown rate in bottom-10 risk cars: {ranked.tail(10)['broke_down'].mean()*100:.0f}%")
