import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap

import config
from functions import idw, clean_numeric


print("Running analysis...")


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

boundary = gpd.read_file(
    config.BOUNDARY_FILE
).to_crs(config.CRS)


# --------------------------------------------------
# Annual NO2 values for 2025
# --------------------------------------------------

station_info = pd.read_csv(
    config.STATIONS_FILE
)

station_info["station_id"] = (
    station_info["Stations"]
    .astype(str)
    .str.extract(r"^(\d{3})")[0]
    .str.zfill(3)
)

annual_no2_column = next(
    column
    for column in station_info.columns
    if str(column)
    .strip()
    .lower()
    .startswith("mean annual no2")
)

station_info["annual_no2"] = clean_numeric(
    station_info[annual_no2_column]
)

stations["station_id"] = (
    stations["station_id"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    .str.zfill(3)
)

stations = stations.merge(
    station_info[
        [
            "station_id",
            "annual_no2"
        ]
    ],
    on="station_id",
    how="left"
)


# --------------------------------------------------
# 1. Diurnal NO2
# Recovered original 05.05.2026 data
# --------------------------------------------------

hours = np.arange(24)

urban_background = [
    7, 8, 7, 8, 8, 9,
    10, 10, 15, 14, 12, 18,
    18, 25, 21, 15, 10, 6,
    4, 4, 4, 4, 6, 5
]

traffic_values = [
    8, 9, 9, 8, 8, 8,
    12, 17, 25, 24, 31, 29,
    28, 22, 15, 12, 9, 12,
    8, 10, 9, 9, 8, 7
]

outskirts = [
    9, 6, np.nan, 6, 5, 5,
    9, 15, 16, 15, 9, 12,
    13, 10, 9, 6, 4, 4,
    9, 6, 5, 5, 7, 7
]

fig, ax = plt.subplots(
    figsize=(10, 5.5)
)

ax.plot(
    hours,
    urban_background,
    color="#4f81bd",
    linewidth=2,
    label="Urban background"
)

ax.plot(
    hours,
    traffic_values,
    color="#d94b3f",
    linewidth=2,
    label="Traffic"
)

ax.plot(
    hours,
    outskirts,
    color="#f2b632",
    linewidth=2,
    label="Outskirts of the City"
)

ax.set_title(
    "Diurnal Cycle of NO₂ [µg/m³]",
    fontsize=15,
    color="#666666"
)

ax.set_xlabel(
    "Time [h]"
)

ax.set_ylabel(
    ""
)

ax.set_xlim(
    0,
    23
)

ax.set_ylim(
    0,
    40
)

ax.set_xticks(
    range(0, 24, 2)
)

ax.grid(
    axis="y",
    alpha=0.25
)

ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, 0.94),
    ncol=3,
    frameon=False
)

fig.tight_layout()

fig.savefig(
    config.FIGURES /
    "01_diurnal_no2.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# --------------------------------------------------
# 2. Monitoring stations
# --------------------------------------------------

station_colors = {
    "Outskirts of the city": "#238bd2",
    "Outskirts of the City": "#238bd2",
    "Traffic": "#f2a900",
    "Urban background": "#e62b25"
}

fig, ax = plt.subplots(
    figsize=(10, 8)
)

boundary.plot(
    ax=ax,
    facecolor="white",
    edgecolor="#333333",
    linewidth=1.5
)

for name, group in stations.groupby(
    "station_type"
):

    group.plot(
        ax=ax,
        color=station_colors.get(
            name,
            "#777777"
        ),
        edgecolor="black",
        linewidth=0.8,
        markersize=190,
        zorder=3,
        label=name
    )

for _, row in stations.iterrows():

    ax.annotate(
        str(row["station_id"]),
        (
            row.geometry.x,
            row.geometry.y
        ),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=8
    )

ax.set_title(
    "Berlin NO₂ Monitoring Stations",
    fontsize=15,
    fontweight="bold"
)

ax.legend(
    title="BLUME Stations",
    loc="lower left",
    frameon=True
)

ax.set_axis_off()

fig.tight_layout()

fig.savefig(
    config.FIGURES /
    "02_station_map.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# --------------------------------------------------
# 3. Traffic network
# --------------------------------------------------

traffic["dtv"] = pd.to_numeric(
    traffic["dtv"],
    errors="coerce"
)

traffic = traffic.dropna(
    subset=["dtv"]
).copy()

traffic = gpd.clip(
    traffic,
    boundary
)

traffic_bins = [
    20,
    4500,
    6540,
    8620,
    11080,
    14160,
    18700,
    26080,
    91080
]

traffic_labels = [
    "20–4500",
    "4500–6540",
    "6540–8620",
    "8620–11080",
    "11080–14160",
    "14160–18700",
    "18700–26080",
    "26080–91080"
]

traffic["traffic_class"] = pd.cut(
    traffic["dtv"].clip(
        lower=20,
        upper=91080
    ),
    bins=traffic_bins,
    labels=traffic_labels,
    include_lowest=True
)

traffic_colors = [
    "#27a65a",
    "#63bb5e",
    "#8ed34f",
    "#f4c72e",
    "#f5d76e",
    "#f39a31",
    "#ef3f30",
    "#9b2ca3"
]

fig, ax = plt.subplots(
    figsize=(10, 8)
)

boundary.plot(
    ax=ax,
    facecolor="white",
    edgecolor="#555555",
    linewidth=1.5
)

traffic.plot(
    ax=ax,
    column="traffic_class",
    categorical=True,
    cmap=ListedColormap(
        traffic_colors
    ),
    linewidth=1.0,
    legend=True,
    legend_kwds={
        "title":
        "Number of motor vehicles per 24 hours"
    }
)


# --------------------------------------------------
# Traffic nodes
#
# The original nodes came from the old filtered
# Geofabrik road network. That file is no longer
# available locally, so this creates a comparable
# node layer from the available road network.
# --------------------------------------------------

roads = traffic[
    traffic.geometry.notna()
].copy()

roads = roads.explode(
    index_parts=False
).reset_index(
    drop=True
)

endpoint_records = []

for road_id, geometry in enumerate(
    roads.geometry
):

    if geometry.geom_type == "LineString":

        coordinates = list(
            geometry.coords
        )

        endpoint_records.extend(
            [
                {
                    "road_id": road_id,
                    "x": coordinates[0][0],
                    "y": coordinates[0][1]
                },
                {
                    "road_id": road_id,
                    "x": coordinates[-1][0],
                    "y": coordinates[-1][1]
                }
            ]
        )

endpoint_points = pd.DataFrame(
    endpoint_records
)

if len(endpoint_points) > 0:

    tolerance = 60

    endpoint_points["grid_x"] = (
        endpoint_points["x"] /
        tolerance
    ).round()

    endpoint_points["grid_y"] = (
        endpoint_points["y"] /
        tolerance
    ).round()

    node_rows = []

    for (
        grid_x,
        grid_y
    ), group in endpoint_points.groupby(
        [
            "grid_x",
            "grid_y"
        ]
    ):

        road_count = (
            group["road_id"]
            .nunique()
        )

        if road_count >= 5:

            node_rows.append(
                {
                    "x": (
                        group["x"].mean()
                    ),
                    "y": (
                        group["y"].mean()
                    ),
                    "Join_Count":
                        road_count
                }
            )

    if node_rows:

        nodes = gpd.GeoDataFrame(
            node_rows,
            geometry=gpd.points_from_xy(
                [row["x"] for row in node_rows],
                [row["y"] for row in node_rows]
            ),
            crs=traffic.crs
        )

        nodes.plot(
            ax=ax,
            marker="o",
            facecolor="white",
            edgecolor="black",
            linewidth=1.5,
            markersize=80,
            zorder=5,
            label="Traffic Nodes"
        )

        nodes.to_file(
            config.PROCESSED /
            "traffic_nodes.gpkg",
            driver="GPKG"
        )

ax.set_title(
    "Berlin Traffic Network and Major Traffic Nodes",
    fontsize=15,
    fontweight="bold"
)

ax.set_axis_off()

fig.tight_layout()

fig.savefig(
    config.FIGURES /
    "03_traffic_network.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# --------------------------------------------------
# 4. Land use / land cover
# --------------------------------------------------

landuse_columns = [
    column
    for column in landuse.columns
    if column != landuse.geometry.name
]

landuse_column = next(
    (
        column
        for column in landuse_columns
        if any(
            word in column.lower()
            for word in [
                "nutzung",
                "landuse",
                "land_use",
                "klasse",
                "class"
            ]
        )
    ),
    landuse_columns[0]
)


def simplify_landuse(value):

    text = str(value).lower()

    text = (
        text
        .replace("ä", "a")
        .replace("ö", "o")
        .replace("ü", "u")
        .replace("ß", "ss")
    )

    if (
        "wasser" in text
        or "gewasser" in text
    ):
        return "Water"

    if (
        "acker" in text
        or "landwirtschaft" in text
        or "crop" in text
    ):
        return "Crops"

    if (
        "wohn" in text
        or "mischnutzung" in text
    ):
        return "Residential"

    if (
        "gewerbe" in text
        or "industrie" in text
        or "versorgung" in text
        or "entsorgung" in text
    ):
        return "Industrial"

    if (
        "einzelhandel" in text
        or "handel" in text
        or "retail" in text
        or "kerngebiet" in text
    ):
        return "Commercial and Retail"

    if (
        "grun" in text
        or "wald" in text
        or "park" in text
        or "friedhof" in text
        or "kleingarten" in text
        or "baumschule" in text
        or "wochenendhaus" in text
    ):
        return "Greenery"

    if (
        "brache" in text
        and (
            "wiese" in text
            or "vegetationsbestand" in text
            or "geholz" in text
            or "baum" in text
        )
    ):
        return "Greenery"

    return "Unclassified"


landuse["lulc_group"] = (
    landuse[landuse_column]
    .apply(simplify_landuse)
)

lulc_order = [
    "Residential",
    "Water",
    "Greenery",
    "Industrial",
    "Commercial and Retail",
    "Crops",
    "Unclassified"
]

landuse["lulc_group"] = pd.Categorical(
    landuse["lulc_group"],
    categories=lulc_order,
    ordered=True
)

lulc_colors = [
    "#ef2b2d",
    "#9fd7ea",
    "#198f3a",
    "#d8bd77",
    "#183c9c",
    "#77df1b",
    "#ffffff"
]

fig, ax = plt.subplots(
    figsize=(10, 8)
)

boundary.plot(
    ax=ax,
    facecolor="white",
    edgecolor="black",
    linewidth=1.4
)

landuse.plot(
    ax=ax,
    column="lulc_group",
    categorical=True,
    cmap=ListedColormap(
        lulc_colors
    ),
    edgecolor="black",
    linewidth=0.15,
    legend=True,
    legend_kwds={
        "title": ""
    }
)

ax.set_title(
    "Land Use and Land Cover in Berlin",
    fontsize=15,
    fontweight="bold"
)

ax.set_axis_off()

fig.tight_layout()

fig.savefig(
    config.FIGURES /
    "04_landuse.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# --------------------------------------------------
# 5. IDW interpolation
# --------------------------------------------------

stations_valid = stations.dropna(
    subset=["annual_no2"]
).copy()

x = stations_valid.geometry.x.to_numpy()
y = stations_valid.geometry.y.to_numpy()
values = stations_valid[
    "annual_no2"
].to_numpy()

minx, miny, maxx, maxy = (
    boundary.total_bounds
)

grid_x, grid_y = np.meshgrid(
    np.linspace(
        minx,
        maxx,
        300
    ),
    np.linspace(
        miny,
        maxy,
        300
    )
)

grid_z = idw(
    np.column_stack(
        [
            x,
            y
        ]
    ),
    values,
    grid_x,
    grid_y,
    config.IDW_POWER
)

berlin_shape = (
    boundary.geometry
    .union_all()
)

inside = (
    berlin_shape
    .contains(
        gpd.points_from_xy(
            grid_x.ravel(),
            grid_y.ravel()
        )
    )
)

inside = np.asarray(
    inside
).reshape(
    grid_x.shape
)

grid_z = np.where(
    inside,
    grid_z,
    np.nan
)


# --------------------------------------------------
# Seven original NO2 classes
# --------------------------------------------------

no2_breaks = [
    10.5,
    12.7,
    14.8,
    16.8,
    20.8,
    24.8
]

no2_labels = [
    "7.1–10.5",
    "10.6–12.7",
    "12.8–14.8",
    "14.9–16.8",
    "16.9–20.8",
    "20.8–24.8",
    "≥24.9"
]

no2_class_index = np.digitize(
    grid_z,
    no2_breaks,
    right=True
)

no2_class_index = np.where(
    np.isnan(grid_z),
    np.nan,
    no2_class_index
)

# Colours taken from the original map
no2_colors = [
    "#f46d43",
    "#313695",
    "#74add1",
    "#abd9e9",
    "#fee090",
    "#fdae61",
    "#d73027"
]

fig, ax = plt.subplots(
    figsize=(10, 8)
)

image = ax.imshow(
    no2_class_index,
    extent=[
        minx,
        maxx,
        miny,
        maxy
    ],
    origin="lower",
    cmap=ListedColormap(
        no2_colors
    ),
    vmin=0,
    vmax=6,
    interpolation="nearest"
)

# Light traffic context
traffic.plot(
    ax=ax,
    color="black",
    linewidth=0.12,
    alpha=0.35,
    zorder=2
)

boundary.boundary.plot(
    ax=ax,
    color="black",
    linewidth=1.5,
    zorder=4
)

stations_valid.plot(
    ax=ax,
    color="black",
    edgecolor="white",
    linewidth=0.8,
    markersize=35,
    zorder=5
)

legend_handles = [
    plt.Line2D(
        [0],
        [0],
        marker="s",
        linestyle="",
        markersize=11,
        markerfacecolor=color,
        markeredgecolor=color,
        label=label
    )
    for color, label in zip(
        no2_colors,
        no2_labels
    )
]

ax.legend(
    handles=legend_handles,
    title="Annual mean NO₂ [µg/m³]",
    loc="upper right",
    frameon=True
)

ax.set_title(
    "Spatial Distribution of NO₂ in Berlin",
    fontsize=15,
    fontweight="bold"
)

ax.set_axis_off()

fig.tight_layout()

fig.savefig(
    config.FIGURES /
    "05_no2_idw.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


print("Analysis finished.")