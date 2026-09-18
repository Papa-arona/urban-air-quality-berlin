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

df["station_id"] = (
    df["station"]
    .str.extract(r"^(\d{3})")[0]
)


# Station metadata

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
        "station_type",
        "latitude",
        "longitude"
    ]
]


# Combine NO2 and station information

df = df.merge(
    stations,
    on="station_id",
    how="left"
)


# Save cleaned data

df.to_csv(
    config.CLEAN_NO2,
    index=False
)


# Station layer

station_data = (
    stations
    .dropna(
        subset=[
            "latitude",
            "longitude"
        ]
    )
    .drop_duplicates("station_id")
)

geo = gpd.GeoDataFrame(
    station_data,
    geometry=gpd.points_from_xy(
        station_data["longitude"],
        station_data["latitude"]
    ),
    crs="EPSG:4326"
)

geo.to_file(
    config.STATIONS_GEOJSON,
    driver="GeoJSON"
)


print("Data preparation finished.")
