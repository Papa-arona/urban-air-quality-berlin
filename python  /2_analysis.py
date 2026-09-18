import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

from shapely.geometry import Point
from shapely.ops import unary_union

import config
from functions import idw



# --------------------------------------------------
# Load data
# --------------------------------------------------

df = pd.read_csv(
    config.CLEAN_NO2,
    parse_dates=["datetime"]
)

stations = gpd.read_file(
    config.STATIONS_GEOJSON
).to_crs(config.CRS)

traffic = gpd.read_file(
    config.TRAFFIC_FILE
).to_crs(config.CRS)

landuse = gpd.read_file(
    config.LANDUSE_FILE
).to_crs(config.CRS)

cams = gpd.read_file(
    config.CAMS_FILE
).to_crs(config.CRS)


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
# 2. Station map
# --------------------------------------------------

means = (
    df.groupby("station")["no2"]
    .mean()
    .reset_index()
)

stations = stations.merge(
    means,
    on="station"
)

colors = {
    "Traffic": "#E5A800",
    "Urban background": "#E53935",
    "Outskirts of the City": "#168BD8"
}

fig, ax = plt.subplots(figsize=(9, 8))

for name, group in stations.groupby("station_type"):
    group.plot(
        ax=ax,
        color=colors.get(name, "grey"),
        edgecolor="black",
        markersize=90,
        label=name
    )

stations.boundary.plot(
    ax=ax,
    color="black",
    linewidth=1.2
)

ax.set_title(
    "Berlin NO₂ Monitoring Stations"
)

ax.legend(
    title="Station type"
)

ax.set_axis_off()

plt.tight_layout()

plt.savefig(
    config.FIGURES / "02_station_map.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# 3. Traffic network and traffic nodes
# --------------------------------------------------

traffic = traffic[
    traffic["road_type"].isin(
        ["motorway", "primary", "tertiary"]
    )
].copy()

traffic["traffic_class"] = pd.cut(
    traffic["traffic_volume"],
    bins=config.TRAFFIC_BINS,
    labels=config.TRAFFIC_LABELS,
    include_lowest=True
)

traffic_colors = [
    "#3BAF2C",
    "#5FCF1A",
    "#8BD417",
    "#F2B705",
    "#F5CC3B",
    "#FF8C00",
    "#E60000",
    "#9B1FA8"
]

fig, ax = plt.subplots(figsize=(10, 8))

for class_name, group in traffic.groupby(
    "traffic_class",
    observed=False
):

    group.plot(
        ax=ax,
        color=traffic_colors[
            list(config.TRAFFIC_LABELS).index(
                class_name
            )
        ],
        linewidth=1,
        label=class_name
    )


# intersections
pairs = gpd.sjoin(
    traffic[["geometry"]],
    traffic[["geometry"]],
    predicate="intersects"
)

points = []

for idx, row in pairs.iterrows():

    other = row["index_right"]

    if idx >= other:
        continue

    geom = traffic.loc[
        idx,
        "geometry"
    ].intersection(
        traffic.loc[
            other,
            "geometry"
        ]
    )

    if geom.geom_type == "Point":
        points.append(geom)


nodes = gpd.GeoDataFrame(
    geometry=points,
    crs=traffic.crs
)

node_counts = gpd.sjoin(
    nodes,
    traffic[["geometry"]],
    predicate="intersects"
).groupby(
    level=0
).size()

nodes["Join_Count"] = node_counts

nodes = nodes[
    nodes["Join_Count"] >= 5
]

nodes.plot(
    ax=ax,
    facecolor="white",
    edgecolor="black",
    markersize=55
)

ax.set_title(
    "Berlin Traffic Network and Traffic Nodes"
)

ax.legend(
    title="Vehicles per day",
    loc="upper right"
)

ax.set_axis_off()

plt.tight_layout()

plt.savefig(
    config.FIGURES / "03_traffic_network.png",
    dpi=300
)

plt.close()

nodes.to_file(
    config.PROCESSED / "traffic_nodes.gpkg",
    driver="GPKG"
)


# --------------------------------------------------
# 4. Land use
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 8))

landuse.plot(
    ax=ax,
    column="landuse",
    categorical=True,
    legend=True,
    edgecolor="black",
    linewidth=0.15
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
# 5. IDW NO2 map
# --------------------------------------------------

x = stations.geometry.x.to_numpy()
y = stations.geometry.y.to_numpy()
values = stations["no2"].to_numpy()

grid_x, grid_y = np.meshgrid(
    np.linspace(
        x.min() - 5000,
        x.max() + 5000,
        200
    ),
    np.linspace(
        y.min() - 5000,
        y.max() + 5000,
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

no2_bins = [
    0,
    10.5,
    12.7,
    14.8,
    16.8,
    20.8,
    24.8,
    1000
]

no2_labels = [
    "7.1 - 10.5",
    "10.6 - 12.7",
    "12.8 - 14.8",
    "14.9 - 16.8",
    "16.9 - 20.8",
    "20.8 - 24.8",
    ">= 24.9"
]

grid_class = np.digitize(
    grid_z,
    no2_bins
)

cmap = plt.get_cmap(
    "RdYlBu_r",
    len(no2_labels)
)

fig, ax = plt.subplots(figsize=(10, 8))

image = ax.imshow(
    grid_class,
    extent=[
        grid_x.min(),
        grid_x.max(),
        grid_y.min(),
        grid_y.max()
    ],
    origin="lower",
    cmap=cmap,
    vmin=1,
    vmax=len(no2_labels)
)

traffic.plot(
    ax=ax,
    color="grey",
    linewidth=0.25
)

stations.plot(
    ax=ax,
    color="black",
    markersize=18
)

plt.colorbar(
    image,
    ax=ax,
    ticks=np.arange(
        1,
        len(no2_labels) + 1
    )
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


# --------------------------------------------------
# 6. CAMS comparison
# --------------------------------------------------

cams["no2_class"] = pd.cut(
    cams["no2"],
    bins=no2_bins,
    labels=no2_labels,
    include_lowest=True
)

fig, ax = plt.subplots(figsize=(10, 8))

cams.plot(
    ax=ax,
    column="no2_class",
    categorical=True,
    legend=True,
    edgecolor="none"
)

traffic.plot(
    ax=ax,
    color="grey",
    linewidth=0.25
)

ax.set_title(
    "CAMS NO₂ Spatial Distribution"
)

ax.set_axis_off()

plt.tight_layout()

plt.savefig(
    config.FIGURES / "06_cams_comparison.png",
    dpi=300
)

plt.close()


print("step 2 done")
