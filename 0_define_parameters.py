from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

STATIONS_DIR = PROJECT_DIR / "stations"
FIGURES_DIR = PROJECT_DIR / "figures"


# ============================================================
# INPUT FILES
# ============================================================

NO2_FILE = RAW_DIR / "no2.csv"

TRAFFIC_FILE = RAW_DIR / "traffic.gpkg"

LANDUSE_FILE = RAW_DIR / "landuse.gpkg"

STATIONS_FILE = STATIONS_DIR / "stations.csv"


# ============================================================
# OUTPUT FILES
# ============================================================

CLEAN_NO2_FILE = PROCESSED_DIR / "no2_clean.csv"

STATIONS_GEOJSON = PROCESSED_DIR / "stations.geojson"

TRAFFIC_NO2_FILE = PROCESSED_DIR / "traffic_no2.csv"

LANDUSE_NO2_FILE = PROCESSED_DIR / "landuse_no2.csv"

VALIDATION_FILE = PROCESSED_DIR / "validation_results.csv"


# ============================================================
# DATA SOURCE
# ============================================================

NO2_URL = "https://luftdaten.berlin.de/core/no2.csv"


# ============================================================
# ANALYSIS SETTINGS
# ============================================================

CRS_LATLON = "EPSG:4326"

CRS_PROJECTED = "EPSG:25833"

IDW_POWER = 2

IDW_GRID_SIZE = 200


# ============================================================
# CREATE DIRECTORIES
# ============================================================

RAW_DIR.mkdir(
    parents=True,
    exist_ok=True
)

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)

FIGURES_DIR.mkdir(
    parents=True,
    exist_ok=True
)
