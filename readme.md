# Urban Air Quality and Mobility in Berlin

This project analyses the spatial distribution of nitrogen dioxide (NO₂)
concentrations across Berlin and examines its relationship with road traffic
and urban land use.

The analysis is implemented as a small Python workflow with separate steps
for data preparation, analysis, validation and export.

## Workflow

```text
NO₂ measurements
       ↓
Data preparation
       ↓
Temporal + spatial analysis
       ↓
Traffic / land use / CAMS
       ↓
IDW interpolation
       ↓
Validation
       ↓
Results
```

## Data

The hourly NO₂ measurements are obtained automatically from the Berlin
air-quality monitoring network.

Station information used by the analysis is stored in:

```text
data/raw/stations.csv
```

The additional spatial datasets are downloaded separately. See
`data/README.md` for the required sources and file locations.

## Run the project

Install the required Python packages:

```bash
pip install pandas numpy scipy matplotlib geopandas shapely pyproj geopy requests beautifulsoup4
```

Run the complete workflow with:

```bash
python main.py
```

The scripts are executed in order:

```text
1_prepare_data.py
        ↓
2_analysis.py
        ↓
3_validation.py
        ↓
4_export_results.py
```

The workflow structure is inspired by the idea of a structured multi-step
analysis workflow described by Aix et al. (2023):

https://doi.org/10.1016/j.scitotenv.2023.164063

## 1. Data preparation

`python/1_prepare_data.py`

This step:

- downloads the NO₂ measurements
- reshapes the station data
- cleans the measurements
- adds temporal information
- combines the measurements with the station information
- creates the station spatial layer

Outputs:

```text
data/processed/no2_clean.csv
data/processed/stations.geojson
```

## 2. Temporal and spatial analysis

`python/2_analysis.py`

This is the main analysis step.

It produces:

- the diurnal cycle of NO₂
- the monitoring-station map
- the traffic network and traffic nodes
- the land-use map
- the IDW NO₂ interpolation
- the CAMS comparison

### Monitoring Stations


### Diurnal NO₂ Pattern

This figure compares average NO₂ concentrations throughout the day across
the monitoring-station categories.


### Traffic Network

Average daily traffic volumes are analysed across Berlin's road network.
Traffic measurement nodes are used to connect traffic intensity with the
NO₂ results.


### Land Use

Land-use information provides spatial context for the distribution of
NO₂ across Berlin.

### Spatial Distribution of NO₂

Inverse Distance Weighting (IDW) is used to transform the monitoring-station
measurements into a continuous NO₂ concentration surface.


## 3. Validation

`python/3_validation.py`

The traffic information is compared with the NO₂ concentration classes
obtained from the spatial analysis.

The script calculates:

- number of observations
- slope
- intercept
- R²
- p-value

Output:

```text
data/processed/validation_results.csv
```

### Traffic and NO₂

The analysed relationship produced an R² of 0.394 for the current dataset and workflow.

## 4. Export

`python/4_export_results.py`

This step collects the final processed data and generated figures.

Processed outputs are stored in:

```text
data/processed/
```

Figures are stored in:

```text
figures/
```

## Repository structure

```text
Urban-Air-Quality-and-Mobility-Berlin/
│
├── README.md
├── main.py
│
├── python/
│   ├── config.py
│   ├── functions.py
│   ├── 1_prepare_data.py
│   ├── 2_analysis.py
│   ├── 3_validation.py
│   └── 4_export_results.py
│
├── data/
│   ├── README.md
│   └── raw/
│       └── stations.csv
│
└── figures/
    ├── 01_diurnal_no2.png
    ├── 02_station_map.png
    ├── 03_traffic_network.png
    ├── 04_landuse.png
    ├── 05_no2_idw.png
    └── 07_traffic_no2_validation.png
```
