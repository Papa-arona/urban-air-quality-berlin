from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "figures"

NO2_FILE = RAW / "no2.csv"
TRAFFIC_FILE = RAW / "traffic.gpkg"
LANDUSE_FILE = RAW / "landuse.gpkg"
CAMS_FILE = RAW / "cams.gpkg"
BOUNDARY_FILE = RAW / "berlin_boundary.gpkg"

STATIONS_FILE = RAW / "stations.csv"

CLEAN_NO2 = PROCESSED / "no2_clean.csv"
STATIONS_GEOJSON = PROCESSED / "stations.geojson"
TRAFFIC_NO2 = PROCESSED / "traffic_no2.csv"
LANDUSE_NO2 = PROCESSED / "landuse_no2.csv"
VALIDATION = PROCESSED / "validation_results.csv"

NO2_URL = "https://luftdaten.berlin.de/core/no2.csv"

CRS = "EPSG:25833"
IDW_POWER = 2

PROCESSED.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)
