# Urban Air Quality and Mobility in Berlin

This project analyses the spatial distribution of nitrogen dioxide (NO₂) across Berlin and examines its relationship with road traffic and urban land use.

The analysis is implemented as a Python workflow covering data preparation, temporal and spatial analysis, IDW interpolation and validation.

## Workflow

```text
NO₂ measurements
       ↓
Data preparation
       ↓
Temporal + spatial analysis
       ↓
Traffic + land use
       ↓
IDW interpolation
       ↓
Validation
       ↓
Results
```

## Data

Hourly NO₂ measurements are obtained from the Berlin air-quality monitoring network.

Station information is stored in:

```text
data/raw/stations.csv
```

Additional spatial datasets are stored in:

```text
data/raw/
```

## Run the project

Install the required Python packages:

```bash
pip install pandas numpy scipy matplotlib geopandas shapely pyproj geopy requests beautifulsoup4
```

Run the complete workflow:

```bash
python main.py
```

The workflow consists of:

```text
1_prepare_data.py
        ↓
2_analysis.py
        ↓
3_validation.py
        ↓
4_export_results.py
```

## Figures

### Diurnal NO₂ Pattern

Shows the daily variation of NO₂ concentrations for different monitoring-station categories.

![Diurnal NO₂ Pattern](figures/01_diurnal_no2.png)

### Monitoring Stations

Shows the locations and categories of the NO₂ monitoring stations used in the analysis.

![Monitoring Stations](figures/02_station_map.png)

### Traffic Network

Shows the Berlin road network, traffic intensity and traffic nodes used in the analysis.

![Traffic Network](figures/03_traffic_network.png)

### Land Use

Shows the main land-use categories across Berlin and provides spatial context for NO₂.

![Land Use](figures/04_landuse.png)

### Spatial Distribution of NO₂

Shows the annual 2025 NO₂ distribution interpolated from monitoring stations using Inverse Distance Weighting (IDW).

![Spatial Distribution of NO₂](figures/05_no2_idw.png)

### Traffic and NO₂ Validation

Shows the relationship between NO₂ concentration classes and estimated average daily traffic.

![Traffic and NO₂ Validation](figures/07_traffic_no2_validation.png)

## Repository Structure

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
│       ├── stations.csv
│       ├── no2.csv
│       ├── traffic.gpkg
│       ├── landuse.gpkg
│       └── berlin_boundary.gpkg
│
└── figures/
    ├── 01_diurnal_no2.png
    ├── 02_station_map.png
    ├── 03_traffic_network.png
    ├── 04_landuse.png
    ├── 05_no2_idw.png
    └── 07_traffic_no2_validation.png
```
