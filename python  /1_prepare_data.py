import re
import requests
import xml.etree.ElementTree as ET

import pandas as pd
import geopandas as gpd

import config
from functions import clean_numeric


TRAFFIC_WFS = (
    "https://gdi.berlin.de/services/wfs/"
    "ua_verkehrsmengen_2019"
)

LANDUSE_WFS = (
    "https://gdi.berlin.de/services/wfs/"
    "ua_flaechennutzung"
)


def get_wfs_layer(url, keywords):
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetCapabilities"
    }

    response = requests.get(
        url,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    root = ET.fromstring(
        response.content
    )

    layers = []

    for feature in root.iter():
        if feature.tag.endswith("FeatureType"):

            name = None
            title = None

            for child in feature:

                if child.tag.endswith("Name"):
                    name = child.text

                if child.tag.endswith("Title"):
                    title = child.text

            if name:
                layers.append(
                    (name, title or "")
                )

    for name, title in layers:

        text = (
            f"{name} {title}"
        ).lower()

        if any(
            word.lower() in text
            for word in keywords
        ):
            return (
                f"{url}"
                f"?service=WFS"
                f"&version=2.0.0"
                f"&request=GetFeature"
                f"&typeNames={name}"
                f"&outputFormat=application/json"
            )

    raise ValueError(
        f"No WFS layer found at {url}"
    )


print("Preparing data...")


# --------------------------------------------------
# Download NO2
# --------------------------------------------------

response = requests.get(
    config.NO2_URL,
    timeout=60
)

response.raise_for_status()

config.NO2_FILE.write_bytes(
    response.content
)


df = pd.read_csv(
    config.NO2_FILE,
    sep=";",
    encoding="utf-8"
)


# --------------------------------------------------
# Clean NO2
# --------------------------------------------------

date_col = df.columns[0]

df[date_col] = pd.to_datetime(
    df[date_col],
    dayfirst=True,
    errors="coerce"
)

df = df.rename(
    columns={
        date_col: "datetime"
    }
)

station_cols = [
    c for c in df.columns
    if re.match(
        r"^\d{3}\s",
        str(c)
    )
]

df = df.melt(
    id_vars="datetime",
    value_vars=station_cols,
    var_name="station",
    value_name="no2"
)

df["no2"] = clean_numeric(
    df["no2"]
)

df = df.dropna(
    subset=["datetime", "no2"]
)

df["hour"] = df["datetime"].dt.hour
df["month"] = df["datetime"].dt.month

df["station_id"] = (
    df["station"]
    .str.extract(r"^(\d{3})")[0]
)


# --------------------------------------------------
# Station information
# --------------------------------------------------

stations = pd.read_csv(
    config.STATIONS_FILE
)

stations = stations.rename(
    columns={
        "Stations": "station_name",
        "Types": "station_type",
        "Latitude": "latitude",
        "Longitude": "longitude"
    }
)

stations["station_id"] = (
    stations["station_name"]
    .astype(str)
    .str.extract(r"^(\d{3})")[0]
)

stations = stations[
    [
        "station_id",
        "station_name",
        "station_type",
        "latitude",
        "longitude"
    ]
]

df = df.merge(
    stations,
    on="station_id",
    how="left"
)

df.to_csv(
    config.CLEAN_NO2,
    index=False
)


# --------------------------------------------------
# Station map layer
# --------------------------------------------------

station_geo = gpd.GeoDataFrame(
    stations,
    geometry=gpd.points_from_xy(
        stations["longitude"],
        stations["latitude"]
    ),
    crs="EPSG:4326"
)

station_geo.to_file(
    config.STATIONS_GEOJSON,
    driver="GeoJSON"
)


# --------------------------------------------------
# Traffic data
# --------------------------------------------------

print("Downloading traffic data...")

traffic_url = get_wfs_layer(
    TRAFFIC_WFS,
    ["verkehrsmengen", "dtv", "verkehr"]
)

traffic = gpd.read_file(
    traffic_url
)

traffic.to_file(
    config.TRAFFIC_FILE,
    driver="GPKG"
)


# --------------------------------------------------
# Land-use data
# --------------------------------------------------

print("Downloading land-use data...")

landuse_url = get_wfs_layer(
    LANDUSE_WFS,
    ["flaechennutzung", "flächennutzung", "land"]
)

landuse = gpd.read_file(
    landuse_url
)

landuse.to_file(
    config.LANDUSE_FILE,
    driver="GPKG"
)


# --------------------------------------------------
# Berlin boundary
# --------------------------------------------------

boundary = gpd.GeoDataFrame(
    geometry=[
        landuse.geometry.union_all()
    ],
    crs=landuse.crs
)

boundary.to_file(
    config.BOUNDARY_FILE,
    driver="GPKG"
)


print("Data preparation finished.")
