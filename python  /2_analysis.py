import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

import config
from functions import idw


print("Running analysis...")


# --------------------------------------------------
# Load data
# --------------------------------------------------

df = pd.read_csv(config.CLEAN_NO2, parse_dates=["datetime"])

stations = gpd.read_file(
    config.STATIONS_GEOJSON
).to_crs(config.CRS)

traffic = gpd.read_file(
    config.TRAFFIC_FILE
).to_crs(config.CRS)

landuse = gpd.read_file(
    config.LANDUSE_FILE
).to_crs(config.CRS)

boundary = gpd.read_file(
    config.BOUNDARY_FILE
).to_crs(config.CRS)

cams = None
  
# --------------------------------------------------
# 1. Diurnal NO2
# --------------------------------------------------

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
        label=name
    )

plt.xlabel("Time [h]")
plt.ylabel("NO₂ [µg/m³]")
plt.title("Diurnal Cycle of NO₂")
plt.legend()
plt.tight_layout()

plt.savefig(
    config.FIGURES / "01_diurnal_no2.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# 2. Monitoring stations

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

fig, ax = plt.subplots(figsize=(9, 8))

colors = {
    "Traffic": "orange",
    "Urban background": "red",
    "Outskirts of the city": "dodgerblue",
    "Outskirts of the City": "dodgerblue"
}

for name, group in stations.groupby("station_type"):

    group.plot(
        ax=ax,
        color=colors.get(name, "grey"),
        edgecolor="black",
        markersize=70,
        label=name
    )

boundary.boundary.plot(
    ax=ax,
    color="black"
)

ax.set_title(
    "Berlin NO₂ Monitoring Stations"
)

ax.legend()
ax.set_axis_off()

plt.tight_layout()

plt.savefig(
    config.FIGURES / "02_station_map.png",
    dpi=300
)

plt.close()

# --------------------------------------------------
# 3. Traffic network
# --------------------------------------------------

from shapely.geometry import Point
from shapely.ops import unary_union

traffic_column = "dtv"

traffic[traffic_column] = pd.to_numeric(
    traffic[traffic_column],
    errors="coerce"
)

traffic = traffic.dropna(
    subset=[traffic_column]
).copy()

traffic["traffic_class"] = pd.qcut(
    traffic[traffic_column],
    q=8,
    duplicates="drop"
)

fig, ax = plt.subplots(
    figsize=(10, 8)
)

traffic.plot(
    ax=ax,
    column="traffic_class",
    cmap="RdYlGn_r",
    legend=True,
    linewidth=1
)

boundary.boundary.plot(
    ax=ax,
    color="black",
    linewidth=1
)

network = unary_union(
    traffic.geometry
)

if hasattr(network, "geoms"):
    parts = list(network.geoms)
else:
    parts = [network]

points = []

for line in parts:

    if line.geom_type == "LineString":

        points.append(
            Point(line.coords[0])
        )

        points.append(
            Point(line.coords[-1])
        )

nodes = gpd.GeoDataFrame(
    geometry=points,
    crs=traffic.crs
)

nodes["node_key"] = nodes.geometry.apply(
    lambda point: (
        round(point.x, 2),
        round(point.y, 2)
    )
)

counts = (
    nodes["node_key"]
    .value_counts()
)

nodes["Join_Count"] = (
    nodes["node_key"]
    .map(counts)
)

nodes = nodes[
    nodes["Join_Count"] >= 5
].copy()

nodes = nodes.drop_duplicates(
    subset="node_key"
)

nodes.plot(
    ax=ax,
    color="white",
    edgecolor="black",
    markersize=45
)

nodes.to_file(
    config.PROCESSED / "traffic_nodes.gpkg",
    driver="GPKG"
)

ax.set_title(
    "Berlin Traffic Network and Traffic Nodes"
)

ax.set_axis_off()

plt.tight_layout()

plt.savefig(
    config.FIGURES / "03_traffic_network.png",
    dpi=300
)

plt.close()
# --------------------------------------------------
# 4. Land use
# --------------------------------------------------

landuse_column = next(
    c for c in landuse.columns
    if c.lower() in [
        "landuse",
        "land_use",
        "nutzung",
        "klasse",
        "class"
    ]
)

fig, ax = plt.subplots(
    figsize=(10, 8)
)

landuse.plot(
    ax=ax,
    column=landuse_column,
    categorical=True,
    legend=True,
    edgecolor="black",
    linewidth=0.1
)

boundary.boundary.plot(
    ax=ax,
    color="black"
)

ax.set_title(
    "Land Use in Berlin"
)

ax.set_axis_off()

plt.tight_layout()

plt.savefig(
    config.FIGURES / "04_landuse.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# 5. IDW interpolation
# --------------------------------------------------

x = stations.geometry.x.to_numpy()
y = stations.geometry.y.to_numpy()
values = stations["no2"].dropna().to_numpy()

valid = stations["no2"].notna()

x = stations.loc[valid].geometry.x.to_numpy()
y = stations.loc[valid].geometry.y.to_numpy()

values = stations.loc[
    valid,
    "no2"
].to_numpy()

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

fig, ax = plt.subplots(
    figsize=(10, 8)
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
    cmap="RdYlBu_r"
)

traffic.plot(
    ax=ax,
    color="grey",
    linewidth=0.2
)

boundary.boundary.plot(
    ax=ax,
    color="black",
    linewidth=1
)

stations.plot(
    ax=ax,
    color="black",
    markersize=15
)

plt.colorbar(
    image,
    ax=ax,
    label="NO₂ [µg/m³]"
)

ax.set_title(
    "Spatial Distribution of NO₂"
)

ax.set_axis_off()

plt.tight_layout()

plt.savefig(
    config.FIGURES / "05_no2_idw.png",
    dpi=300
)

plt.close()

# 6. CAMS comparison
# CAMS data will be added later.


print("step 2 is done.")
