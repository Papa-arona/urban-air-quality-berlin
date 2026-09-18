import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

import config
from functions import idw


print("Running analysis...")

df = pd.read_csv(
    config.CLEAN_NO2,
    parse_dates=["datetime"]
)

stations = gpd.read_file(
    config.STATIONS_GEOJSON
)


# -------------------------
# Temporal analysis
# -------------------------

hourly = (
    df.groupby(
        ["station_type", "hour"]
    )["no2"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(9, 5))

for name, group in hourly.groupby("station_type"):
    plt.plot(
        group["hour"],
        group["no2"],
        marker="o",
        label=name
    )

plt.xlabel("Hour")
plt.ylabel("NO₂ (µg/m³)")
plt.title("Average hourly NO₂")
plt.legend()
plt.tight_layout()

plt.savefig(
    config.FIGURES / "daily_no2_pattern.png",
    dpi=300
)

plt.close()


# -------------------------
# Station averages
# -------------------------

means = (
    df.groupby("station")["no2"]
    .mean()
    .reset_index()
)

stations = stations.merge(
    means,
    on="station"
)

stations = stations.to_crs(
    config.CRS
)


# -------------------------
# Station map
# -------------------------

fig, ax = plt.subplots(
    figsize=(8, 8)
)

stations.plot(
    ax=ax,
    column="no2",
    cmap="RdYlGn_r",
    legend=True,
    markersize=60
)

ax.set_title(
    "Mean NO₂ at monitoring stations"
)

ax.set_axis_off()

plt.tight_layout()

plt.savefig(
    config.FIGURES / "station_map.png",
    dpi=300
)

plt.close()


# -------------------------
# IDW
# -------------------------

x = stations.geometry.x.to_numpy()
y = stations.geometry.y.to_numpy()
values = stations["no2"].to_numpy()

margin = 3000

grid_x, grid_y = np.meshgrid(
    np.linspace(
        x.min() - margin,
        x.max() + margin,
        200
    ),
    np.linspace(
        y.min() - margin,
        y.max() + margin,
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

fig, ax = plt.subplots(
    figsize=(8, 8)
)

image = ax.imshow(
    grid_z,
    extent=[
        grid_x.min(),
        grid_x.max(),
        grid_y.min(),
        grid_y.max()
    ],
    origin="lower",
    cmap="RdYlGn_r"
)

stations.plot(
    ax=ax,
    color="black",
    markersize=15
)

plt.colorbar(
    image,
    ax=ax,
    label="NO₂ (µg/m³)"
)

ax.set_title(
    "NO₂ spatial distribution"
)

plt.tight_layout()

plt.savefig(
    config.FIGURES / "no2_idw.png",
    dpi=300
)

plt.close()


# -------------------------
# Traffic
# -------------------------

traffic = gpd.read_file(
    config.TRAFFIC_FILE
).to_crs(config.CRS)

traffic_cols = [
    c for c in traffic.columns
    if "dtvw" in c.lower()
]

traffic_field = traffic_cols[0]

traffic[traffic_field] = pd.to_numeric(
    traffic[traffic_field],
    errors="coerce"
)

traffic = traffic.dropna(
    subset=[traffic_field]
)

joined = gpd.sjoin_nearest(
    stations,
    traffic[[traffic_field, "geometry"]],
    how="left"
)

traffic_result = joined[
    [
        "station",
        "station_type",
        "no2",
        traffic_field
    ]
].rename(
    columns={
        "no2": "mean_no2",
        traffic_field: "traffic_volume"
    }
)

traffic_result.to_csv(
    config.TRAFFIC_NO2,
    index=False
)

plt.figure(figsize=(7, 5))

plt.scatter(
    traffic_result["traffic_volume"],
    traffic_result["mean_no2"]
)

plt.xlabel("Traffic volume")
plt.ylabel("Mean NO₂ (µg/m³)")
plt.title("Traffic and NO₂")

plt.tight_layout()

plt.savefig(
    config.FIGURES / "traffic_no2_relationship.png",
    dpi=300
)

plt.close()


# -------------------------
# Land use
# -------------------------

landuse = gpd.read_file(
    config.LANDUSE_FILE
).to_crs(config.CRS)

fields = [
    c for c in landuse.columns
    if c != landuse.geometry.name
    and landuse[c].dtype == "object"
]

landuse_field = fields[0]

landuse_join = gpd.sjoin(
    stations,
    landuse[[landuse_field, "geometry"]],
    how="left",
    predicate="within"
)

landuse_result = landuse_join[
    [
        "station",
        "station_type",
        "no2",
        landuse_field
    ]
]

landuse_result.to_csv(
    config.LANDUSE_NO2,
    index=False
)

summary = (
    landuse_result
    .groupby(landuse_field)["no2"]
    .mean()
)

summary.plot(
    kind="bar",
    figsize=(9, 5)
)

plt.ylabel("Mean NO₂ (µg/m³)")
plt.xlabel("Land-use category")
plt.title("NO₂ and land use")
plt.tight_layout()

plt.savefig(
    config.FIGURES / "no2_landuse.png",
    dpi=300
)

plt.close()

print("Analysis finished.")
