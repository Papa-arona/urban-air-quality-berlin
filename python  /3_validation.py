import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from scipy.stats import linregress

import config
from functions import idw

print("Running validation...")

df = pd.read_csv(
    config.CLEAN_NO2
)

stations = gpd.read_file(
    config.STATIONS_GEOJSON
).to_crs(config.CRS)

traffic = gpd.read_file(
    config.TRAFFIC_FILE
).to_crs(config.CRS)

nodes = gpd.read_file(
    config.PROCESSED / "traffic_nodes.gpkg"
).to_crs(config.CRS)

# Match station IDs
df["station_id"] = (
    df["station_id"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    .str.zfill(3)
)

stations["station_id"] = (
    stations["station_id"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    .str.zfill(3)
)

# Mean NO2 at each station
means = (
    df.groupby(["station_id", "station"])["no2"]
    .mean()
    .reset_index()
)

stations = stations.merge(
    means[["station_id", "no2"]],
    on="station_id",
    how="left"
)

stations = stations.dropna(
    subset=["no2"]
)

# IDW interpolation
x = stations.geometry.x.to_numpy()
y = stations.geometry.y.to_numpy()
values = stations["no2"].to_numpy()

grid_x, grid_y = np.meshgrid(
    np.linspace(
        x.min() - 3000,
        x.max() + 3000,
        200
    ),
    np.linspace(
        y.min() - 3000,
        y.max() + 3000,
        200
    )
)

grid_z = idw(
    np.column_stack([x, y]),
    values,
    grid_x,
    grid_y,
    config.IDW_POWER
)

# Traffic volume
traffic_column = "dtv"

traffic[traffic_column] = pd.to_numeric(
    traffic[traffic_column],
    errors="coerce"
)

traffic = traffic.dropna(
    subset=[traffic_column]
)

# Match each traffic node to the nearest road
nodes = gpd.sjoin_nearest(
    nodes,
    traffic[[traffic_column, "geometry"]],
    how="left"
)

# Extract interpolated NO2 value at each node
nodes["no2"] = [
    grid_z[
        np.abs(
            grid_y[:, 0] - point.y
        ).argmin(),
        np.abs(
            grid_x[0, :] - point.x
        ).argmin()
    ]
    for point in nodes.geometry
]

# NO2 classes used in the analysis
bins = [
    7.1,
    10.5,
    12.7,
    14.8,
    16.8,
    20.8,
    24.8,
    np.inf
]

labels = [
    "7.1 - 10.5",
    "10.6 - 12.7",
    "12.8 - 14.8",
    "14.9 - 16.8",
    "16.9 - 20.8",
    "20.8 - 24.8",
    ">= 24.9"
]

nodes["no2_class"] = pd.cut(
    nodes["no2"],
    bins=bins,
    labels=labels
)

# # Average traffic volume by NO2 class

grouped = (
    nodes.groupby(
        "no2_class",
        observed=False
    )[traffic_column]
    .agg(
        mean_traffic="mean",
        observations="count"
    )
    .reset_index()
    .dropna()
)

result = grouped.rename(
    columns={
        "mean_traffic": traffic_column
    }
)

# Regression

x = np.arange(len(result))
y = result[traffic_column]

regression = linregress(
    x,
    y
)

r_squared = regression.rvalue ** 2

result["slope"] = regression.slope
result["intercept"] = regression.intercept
result["r_squared"] = r_squared
result["p_value"] = regression.pvalue

result.to_csv(
    config.VALIDATION,
    index=False
)
# Plot
plt.figure(
    figsize=(9, 5)
)

plt.scatter(
    x,
    y,
    s=60
)

plt.plot(
    x,
    regression.intercept
    + regression.slope * x
)

plt.xticks(
    x,
    result["no2_class"],
    rotation=25
)

plt.xlabel(
    "NO₂ concentration class [µg/m³]"
)

plt.ylabel(
    "Estimated average vehicles/day"
)

plt.title(
    f"Traffic volume and NO₂ concentration\n"
    f"R² = {r_squared:.3f}"
)

plt.tight_layout()

plt.savefig(
    config.FIGURES / "07_traffic_no2_validation.png",
    dpi=300
)

plt.close()

print(
    f"R² = {r_squared:.3f}"
)

print(
    "Validation finished."
)