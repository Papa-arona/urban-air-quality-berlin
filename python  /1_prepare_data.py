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

BOUNDARY_WFS = (
    "https://gdi.berlin.de/services/wfs/"
    "alkis_land"
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

        if not feature.tag.endswith(
            "FeatureType"
        ):
            continue

        name = None
        title = None

        for child in feature:

            if child.tag.endswith(
                "Name"
            ):
                name = child.text

            elif child.tag.endswith(
                "Title"
            ):
                title = child.text

        if name:
            layers.append(
                (
                    name,
                    title or ""
                )
            )

    for name, title in layers:

        text = (
            f"{name} {title}"
            .lower()
        )

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
# 1. Hourly NO2 data
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

date_col = df.columns[0]

df[date_col] = pd.to_datetime(
    df[date_col],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

df = df.rename(
    columns={
        date_col: "datetime"
    }
)

station_cols = [
    column
    for column in df.columns
    if re.match(
        r"^\d{3}\s",
        str(column)
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
    subset=[
        "datetime",
        "no2"
    ]
)

df["hour"] = (
    df["datetime"].dt.hour
)

df["month"] = (
    df["datetime"].dt.month
)

df["station_id"] = (
    df["station"]
    .str.extract(
        r"^(\d{3})"
    )[0]
    .str.zfill(3)
)

# --------------------------------------------------
# 2. Station information
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
    .str.extract(
        r"^(\d{3})"
    )[0]
    .str.zfill(3)
)

stations = stations[
    [
        "station_id",
        "station_name",
        "station_type",
        "latitude",
        "longitude"
    ]
].copy()

# --------------------------------------------------
# 3. Combine hourly measurements and stations
# --------------------------------------------------

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
# 4. Station spatial layer
# --------------------------------------------------

station_geo = gpd.GeoDataFrame(
    stations,
    geometry=gpd.points_from_xy(
        stations["longitude"],
        stations["latitude"]
    ),
    crs="EPSG:4326"
)

station_geo.to_crs(
    config.CRS
).to_file(
    config.STATIONS_GEOJSON,
    driver="GeoJSON"
)

# --------------------------------------------------
# 5. Traffic WFS
# --------------------------------------------------

print(
    "Downloading traffic data..."
)

traffic_url = get_wfs_layer(
    TRAFFIC_WFS,
    [
        "verkehrsmengen",
        "dtv",
        "verkehr"
    ]
)

traffic = gpd.read_file(
    traffic_url
)

traffic = traffic[
    traffic.geometry.notna()
].copy()

traffic.to_file(
    config.TRAFFIC_FILE,
    driver="GPKG"
)

# --------------------------------------------------
# 6. Land-use WFS
# --------------------------------------------------

print(
    "Downloading land-use data..."
)

landuse_url = get_wfs_layer(
    LANDUSE_WFS,
    [
        "flaechennutzung",
        "flächennutzung",
        "land"
    ]
)

landuse = gpd.read_file(
    landuse_url
)

landuse = landuse[
    landuse.geometry.notna()
].copy()

landuse.to_file(
    config.LANDUSE_FILE,
    driver="GPKG"
)

# --------------------------------------------------
# 7. Official Berlin boundary
# --------------------------------------------------

print(
    "Downloading Berlin boundary..."
)

boundary_url = get_wfs_layer(
    BOUNDARY_WFS,
    [
        "landesgrenze",
        "berlin landesgrenze",
        "alkis land"
    ]
)

boundary = gpd.read_file(
    boundary_url
)

boundary = boundary[
    boundary.geometry.notna()
].copy()

boundary = boundary.to_crs(
    config.CRS
)

boundary_geometry = (
    boundary.geometry
    .union_all()
    .buffer(0)
)

boundary = gpd.GeoDataFrame(
    {
        "name": ["Berlin"]
    },
    geometry=[boundary_geometry],
    crs=config.CRS
)

boundary.to_file(
    config.BOUNDARY_FILE,
    driver="GPKG"
)

print(
    "Data preparation finished."
)