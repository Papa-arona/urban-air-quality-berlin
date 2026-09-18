import re
import time

import pandas as pd
import geopandas as gpd

from geopy.geocoders import Nominatim

import config
from functions import clean_numeric


print("prep data...")

# NO2
df = pd.read_csv(
    config.NO2_FILE,
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

stations = pd.read_csv(
    config.STATIONS_FILE
)

df = df.merge(
    stations[["station", "station_type"]],
    on="station",
    how="left"
)

df.to_csv(
    config.CLEAN_NO2,
    index=False
)


# Station coordinates
if not config.STATIONS_GEOJSON.exists():

    print("geocoding stations...")

    geolocator = Nominatim(
        user_agent="berlin-no2-project"
    )

    lat = []
    lon = []

    for station in stations["station"]:

        location = geolocator.geocode(
            f"{station}, Berlin, Germany"
        )

        if location:
            lat.append(location.latitude)
            lon.append(location.longitude)
        else:
            lat.append(None)
            lon.append(None)

        time.sleep(1)

    stations["latitude"] = lat
    stations["longitude"] = lon

    stations = stations.dropna(
        subset=["latitude", "longitude"]
    )

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

print("step 1 finished.")
