from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "figures"

NO2_FILE = RAW / "no2.csv"
TRAFFIC_FILE = RAW / "traffic.gpkg"
PREPARED_TRAFFIC_FILE = RAW / "traffic_prepared.gpkg"
LANDUSE_FILE = RAW / "landuse.gpkg"
BOUNDARY_FILE = RAW / "berlin_boundary.gpkg"
CAMS_FILE = RAW / "cams.gpkg"

STATIONS_FILE = RAW / "stations.csv"

CLEAN_NO2 = PROCESSED / "no2_clean.csv"
STATIONS_GEOJSON = PROCESSED / "stations.geojson"
NO2_ZONES = PROCESSED / "no2_zones.gpkg"
TRAFFIC_NO2 = PROCESSED / "traffic_no2.csv"
VALIDATION = PROCESSED / "validation_results.csv"

NO2_URL = "https://luftdaten.berlin.de/core/no2.csv"

CRS = "EPSG:25833"

IDW_POWER = 2

NO2_BINS = [
    7.1,
    10.5,
    12.7,
    14.8,
    16.8,
    20.8,
    24.8,
    float("inf")
]

NO2_LABELS = [
    "7.1–10.5",
    "10.6–12.7",
    "12.8–14.8",
    "14.9–16.8",
    "16.9–20.8",
    "20.9–24.8",
    "≥24.9"
]

PROCESSED.mkdir(
    parents=True,
    exist_ok=True
)

FIGURES.mkdir(
    parents=True,
    exist_ok=True
)