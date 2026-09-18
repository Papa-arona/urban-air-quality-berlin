# Data

The analysis uses data from several public sources.

The datasets are not stored in the repository. Download the required
datasets and place them in `data/raw/`.

## 1. Station data

The station information used by the analysis is provided in:

```text
data/raw/stations.csv
```

The file contains the station names, station types and geographic
coordinates.

## 2. NO₂ measurements

Hourly NO₂ measurements are obtained from the Berlin air-quality monitoring
network.

Source:

Berlin Air Quality Monitoring Network

https://luftdaten.berlin.de/pollution/no2

The measurements are downloaded automatically by `1_prepare_data.py`.

## 3. Traffic data

The traffic analysis uses Berlin road-network and traffic-volume data from
the Berlin Environmental Atlas / Berlin Open Data.

Source:

Verkehrsmengen DTV 2019 (Umweltatlas) - WFS

https://daten.berlin.de/datensaetze/verkehrsmengen-dtv-2019-umweltatlas-wfs-50921da5


## 4. Land-use data

The land-use analysis uses the Berlin Environmental Atlas land-use dataset.

Source:

Flächennutzung (Umweltatlas) - ab 2021 - WFS

https://daten.berlin.de/datensaetze/flachennutzung-umweltatlas-ab-2021-wfs-80589f72


## 5. CAMS data

The spatial comparison uses gridded NO₂ data from the Copernicus
Atmosphere Monitoring Service.

Source:

CAMS European air quality reanalyses

https://ads.atmosphere.copernicus.eu/datasets/cams-europe-air-quality-reanalyses



## 6. Berlin boundary

A Berlin boundary layer is required for the spatial maps.

The boundary can be obtained from the Berlin Geoportal / Environmental
Atlas geodata services.

Place the dataset in:

## Input structure

After downloading the required datasets:

```text
data/
│
├── README.md
│
└── raw/
    ├── stations.csv
    ├── traffic.gpkg
    ├── landuse.gpkg
    ├── cams.gpkg
    └── berlin_boundary.gpkg
```

The Python workflow reads these datasets and creates the processed data
and figures automatically.
