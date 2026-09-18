import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import linregress

import config


print("validation...")


df = pd.read_csv(
    config.TRAFFIC_NO2
)

df = df.dropna(
    subset=[
        "traffic_volume",
        "mean_no2"
    ]
)


df["no2_class"] = pd.cut(
    df["mean_no2"],
    bins=[
        0,
        10.5,
        12.7,
        14.8,
        16.8,
        20.8,
        24.8,
        1000
    ],
    labels=[
        "7.1 - 10.5",
        "10.6 - 12.7",
        "12.8 - 14.8",
        "14.9 - 16.8",
        "16.9 - 20.8",
        "20.8 - 24.8",
        ">= 24.9"
    ]
)


summary = (
    df.groupby("no2_class", observed=False)
    ["traffic_volume"]
    .mean()
    .reset_index()
)


x = range(len(summary))

result = linregress(
    list(x),
    summary["traffic_volume"]
)


r_squared = result.rvalue ** 2


summary.to_csv(
    config.VALIDATION,
    index=False
)


plt.figure(figsize=(8, 5))

plt.scatter(
    x,
    summary["traffic_volume"],
    s=55
)

line = (
    result.intercept
    + result.slope * pd.Series(x)
)

plt.plot(
    x,
    line,
    label=f"R² = {r_squared:.3f}"
)

plt.xticks(
    list(x),
    summary["no2_class"],
    rotation=25
)

plt.xlabel(
    "Spatial class (NO₂ µg/m³)"
)

plt.ylabel(
    "Estimated avg. vehicles/day"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    config.FIGURES /
    "07_traffic_no2_validation.png",
    dpi=300
)

plt.close()


print(
    f"R² = {r_squared:.3f}"
)

print("step 3 done")
