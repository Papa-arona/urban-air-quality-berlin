import re
import pandas as pd
import geopandas as gpd

import config
from functions import clean_numeric


print("Preparing data...")


# NO2 data

df = pd.read_csv(
    config.NO2_URL,
    sep=";",
    encoding="utf-8"
)

date_col = df.columns[0]

df[date_col] = pd.to_datetime(
    df[date_col],
    dayfirst=True,
    errors="coerce"
)

df = df.rename(
    columns={date_col: "datetime"}
)

station_cols = [
    c for c in df.columns
    if re.match(r"^\d{3}\s", str(c))
]

df = df.melt(
    id_vars="datetime",
    value_vars=station_cols,
    var_name="station",
    value_name="no2"
)

df["no2"] = clean_numeric(df["no2"])

df = df.dropna(
    subset=["datetime", "no2"]
)

df["hour"] = df["datetime"].dt.hour
df["month"] = df["datetime"].dt.month


# Station information
# This CSV was created from the station information collected earlier.

stations = pd.read_csv(
    config.STATIONS_FILE
)

stations = stations.rename(
    columns={
        "Stations": "station",
        "Types": "station_type",
        "Latitude": "latitude",
        "Longitude": "longitude"
    }
)

stations = stations[
    [
        "station",
        "station_type",
        "latitude",
        "longitude"
    ]
]

df = df.merge(
    stations,
    on="station",
    how="left"
)


# Save cleaned NO2 data

df.to_csv(
    config.CLEAN_NO2,
    index=False
)


# Create station spatial layer

geo = gpd.GeoDataFrame(
    stations,
    geometry=gpd.points_from_xy(
        stations["longitude"],
        stations["latitude"]
    ),
    crs="EPSG:4326"
)

geo.to_file(
    config.STATIONS_GEOJSON,
    driver="GeoJSON"
)


print("Data preparation finished.")
