# Urban Air Quality and Mobility in Berlin

This project analyses nitrogen dioxide (NO₂) concentrations across Berlin and
examines their relationship with road traffic and urban land use.

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

The additional spatial datasets used in the analysis are not included in
this repository.

Before running the project, download the required datasets and place them
in:

```text
data/raw/
```

See `data/README.md` for the source of each dataset and the required
filename.

The expected input structure is:

```text
data/
└── raw/
    ├── traffic.gpkg
    ├── landuse.gpkg
    ├── cams.gpkg
    └── berlin_boundary.gpkg
```

The NO₂ measurements are downloaded automatically by the first step.

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

## Run the project

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
- prepares the monitoring stations
- geocodes the stations

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

## 3. Validation

`python/3_validation.py`

The traffic information is compared with the NO₂ spatial classes produced
from the interpolation.

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
├── requirements.txt
├── .gitignore
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
│   ├── raw/
│   └── processed/
│
├── stations/
│   └── stations.csv
│
└── figures/
```
