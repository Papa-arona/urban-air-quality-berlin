from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "figures"

NO2_FILE = RAW / "no2.csv"
TRAFFIC_FILE = RAW / "traffic.gpkg"
LANDUSE_FILE = RAW / "landuse.gpkg"
STATIONS_FILE = ROOT / "stations" / "stations.csv"

CLEAN_NO2 = PROCESSED / "no2_clean.csv"
STATIONS_GEOJSON = PROCESSED / "stations.geojson"
TRAFFIC_NO2 = PROCESSED / "traffic_no2.csv"
LANDUSE_NO2 = PROCESSED / "landuse_no2.csv"
VALIDATION = PROCESSED / "validation_results.csv"

NO2_URL = "https://luftdaten.berlin.de/core/no2.csv"

CRS = "EPSG:25833"
IDW_POWER (p) = 2

CAMS_FILE = RAW / "cams.gpkg"

TRAFFIC_BINS = [
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

TRAFFIC_LABELS = [
    "20 - 4500",
    "4500 - 6540",
    "6540 - 8620",
    "8620 - 11080",
    "11080 - 14160",
    "14160 - 18700",
    "18700 - 26080",
    "26080 - 91080"
]
