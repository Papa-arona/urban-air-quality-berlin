# ============================================================
# DEFINE PARAMETERS
# Urban Air Quality and Mobility in Berlin
# ============================================================

from pathlib import Path


## ---- define directories ----

main_dir = Path(__file__).resolve().parent.parent

data_dir = main_dir / "data"
raw_dir = data_dir / "raw"
processed_dir = data_dir / "processed"

gis_dir = main_dir / "gis"
figures_dir = main_dir / "figures"


## ---- create directories ----

for directory in [
    raw_dir,
    processed_dir,
    figures_dir,
]:
    directory.mkdir(
        parents=True,
        exist_ok=True
    )


## ---- define data source ----

viz_url = (
    "https://viz.berlin.de/en/umwelt/air-quality/"
)


## ---- define dates ----

start_date = "2025-01-01"
end_date = "2025-12-31"


## ---- define pollutant ----

pollutant = "NO2"


## ---- define time interval ----

time_interval = "hourly"


## ---- define GIS files ----

berlin_boundary = (
    gis_dir / "berlin_boundary" / "berlin.shp"
)

station_file = (
    gis_dir / "stations" / "stations.geojson"
)

traffic_file = (
    gis_dir / "traffic" / "traffic.shp"
)

land_cover_file = (
    gis_dir / "land_cover" / "land_cover.shp"
)
