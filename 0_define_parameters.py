from pathlib import Path


# ============================================================
# PROJECT
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

GIS_DIR = PROJECT_DIR / "gis"
FIGURES_DIR = PROJECT_DIR / "figures"


# ============================================================
# DATA
# ============================================================

NO2_FILE = RAW_DIR / "no2.csv"
TRAFFIC_FILE = RAW_DIR / "traffic.gpkg"
LANDUSE_FILE = RAW_DIR / "landuse.gpkg"

STATION_FILE = GIS_DIR / "stations.csv"


# ============================================================
# OUTPUTS
# ============================================================

CLEAN_NO2_FILE = PROCESSED_DIR / "no2_clean.csv"
FLAGGED_NO2_FILE = PROCESSED_DIR / "no2_flagged.csv"

STATIONS_FILE = PROCESSED_DIR / "stations.geojson"

TRAFFIC_RESULT_FILE = (
    PROCESSED_DIR / "traffic_no2.csv"
)

LANDUSE_RESULT_FILE = (
    PROCESSED_DIR / "no2_landuse.csv"
)

VALIDATION_FILE = (
    PROCESSED_DIR / "validation_results.csv"
)


# ============================================================
# STUDY PARAMETERS
# ============================================================

POLLUTANT = "NO2"

PERIOD = "1h"

STUDY_CRS = "EPSG:25833"

GRID_SIZE = 200

IDW_POWER = 2


# ============================================================
# BERLIN AIR QUALITY DATA
# ============================================================

NO2_URL = (
    "https://luftdaten.berlin.de/core/no2.csv"
)


# ============================================================
# CREATE OUTPUT DIRECTORIES
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
