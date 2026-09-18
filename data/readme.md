# Data

The analysis uses data from several public sources.

## 1. Station data

The station information used by the analysis is provided in:

```text
data/raw/stations.csv
```

The file contains the station names, station types and geographic coordinates.

## 2. NO₂ measurements

Hourly NO₂ measurements are obtained from the Berlin air-quality monitoring network.

Source:

Berlin Air Quality Monitoring Network

https://luftdaten.berlin.de/pollution/no2

The measurements are downloaded automatically by `1_prepare_data.py` and saved as:

```text
data/raw/no2.csv
```

## 3. Traffic data

The traffic analysis uses Berlin traffic-volume data from the Berlin Environmental Atlas / Berlin Open Data.

Source:

Verkehrsmengen DTV 2019 (Umweltatlas) - WFS

https://daten.berlin.de/datensaetze/verkehrsmengen-dtv-2019-umweltatlas-wfs-50921da5

The dataset is downloaded by `1_prepare_data.py` and saved as:

```text
data/raw/traffic.gpkg
```

## 4. Land-use data

The land-use analysis uses the Berlin Environmental Atlas land-use dataset.

Source:

Flächennutzung (Umweltatlas) - ab 2021 - WFS

https://daten.berlin.de/datensaetze/flachennutzung-umweltatlas-ab-2021-wfs-80589f72

The dataset is downloaded by `1_prepare_data.py` and saved as:

```text
data/raw/landuse.gpkg
```

## 5. Berlin boundary

A Berlin boundary layer is used to define the study area for the spatial analysis and maps.

The boundary is obtained from the Berlin Geoportal / geodata services by `1_prepare_data.py` and saved as:

```text
data/raw/berlin_boundary.gpkg
```

## Input structure

The raw data used by the project are stored as:

```text
data/
│
├── README.md
│
└── raw/
    ├── stations.csv
    ├── no2.csv
    ├── traffic.gpkg
    ├── landuse.gpkg
    └── berlin_boundary.gpkg
```

The Python workflow reads these datasets and generates the project figures automatically.
