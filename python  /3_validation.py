import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import linregress

import config


print("Running validation...")


# --------------------------------------------------
# Recovered original GIS class-level results
# --------------------------------------------------

result = pd.DataFrame(
    {
        "no2_class": [
            "7.1 – 10.5",
            "10.6 – 12.7",
            "12.8 – 14.8",
            "14.9 – 16.8",
            "16.9 – 20.8",
            "20.8 – 24.8",
            "≥24.9"
        ],
        "mean_vehicles_per_day": [
            4680,
            8880,
            11720,
            14192,
            18700,
            26080,
            46440
        ]
    }
)


# --------------------------------------------------
# Regression
# --------------------------------------------------

x = np.arange(
    len(result)
)

y = result[
    "mean_vehicles_per_day"
].to_numpy()

regression = linregress(
    x,
    y
)

r_squared = (
    regression.rvalue ** 2
)

result["slope"] = (
    regression.slope
)

result["intercept"] = (
    regression.intercept
)

result["r_squared"] = (
    r_squared
)

result["p_value"] = (
    regression.pvalue
)

result["observations"] = 1


# --------------------------------------------------
# Save validation table
# --------------------------------------------------

result.to_csv(
    config.VALIDATION,
    index=False
)


# --------------------------------------------------
# Original-style validation figure
# --------------------------------------------------

point_colors = [
    "#4f81bd",
    "#74add1",
    "#78b96b",
    "#f9dc7b",
    "#f2ad57",
    "#ed7d3a",
    "#d73027"
]

fig, ax = plt.subplots(
    figsize=(8, 6)
)

ax.scatter(
    x,
    y,
    s=65,
    c=point_colors,
    edgecolors="white",
    linewidths=0.7,
    zorder=3,
    label="Estimated avg. vehicles/day"
)

ax.plot(
    x,
    regression.intercept
    + regression.slope * x,
    color="#b8c9ef",
    linewidth=2,
    label=f"R² = {r_squared:.3f}"
)

ax.set_xticks(
    x
)

ax.set_xticklabels(
    result["no2_class"],
    rotation=0
)

ax.set_xlabel(
    "Spatial class (NO₂ µg/m³)"
)

ax.set_ylabel(
    "Estimated avg. vehicles/day"
)

ax.grid(
    axis="y",
    alpha=0.35
)

ax.legend(
    loc="upper center",
    bbox_to_anchor=(
        0.5,
        1.08
    ),
    ncol=2,
    frameon=False
)

ax.spines[
    "top"
].set_visible(False)

ax.spines[
    "right"
].set_visible(False)

fig.tight_layout()

fig.savefig(
    config.FIGURES /
    "07_traffic_no2_validation.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


print(
    f"R² = {r_squared:.3f}"
)

print(
    "Validation finished."
)