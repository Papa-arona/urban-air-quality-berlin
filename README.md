# Urban Air Quality and Mobility in Berlin


## Project Overview

This project investigates the spatial distribution of nitrogen dioxide
(NO₂) concentrations across Berlin and examines the relationship between
air pollution, road traffic and urban land use.

## Study Area and Monitoring Network

Berlin's air-quality monitoring network contains urban-background,
traffic and suburban monitoring stations. These station measurements
provided the observations used in the spatial analysis.

<img width="3507" height="2480" alt="image" src="https://github.com/user-attachments/assets/04515a8b-c7bf-4e24-a875-f61102217956" />


### Daily NO₂ Patterns

The monitoring stations were grouped into traffic, urban-background and
outskirts categories to examine differences in the daily NO₂ cycle.

<img width="662" height="410" alt="image" src="https://github.com/user-attachments/assets/12a493af-bcd5-46f1-96d2-f4389f6e073a" />

## Traffic Data

Average daily traffic volumes were analysed across Berlin's road network.
Traffic measurement nodes were used to connect traffic intensity with the
air-quality results.

<img width="3507" height="2480" alt="image" src="https://github.com/user-attachments/assets/3e736fbe-85bb-4a73-a20d-45d325ceb5d5" />

## Land Use and Land Cover

Land-use information was included to provide additional context for the
distribution of emissions and urban development across Berlin.

<img width="3507" height="2480" alt="image" src="https://github.com/user-attachments/assets/25aeafbb-8e16-4ff0-822f-9f1749aa0021" />

## Spatial Distribution of NO₂

Inverse Distance Weighting was used to estimate NO₂ concentrations between
the monitoring stations. The resulting surface indicates higher estimated
concentrations in central and traffic-intensive parts of Berlin, with lower
values toward several peripheral areas.

<img width="3507" height="2480" alt="image" src="https://github.com/user-attachments/assets/58d6cecf-c16c-423f-859d-529227a23d45" />


## Relationship Between Traffic and NO₂

Estimated average daily vehicle volumes increased across the NO₂
concentration classes. The fitted relationship produced an R² value of
approximately 0.836, indicating a strong association in the analysed data.

<img width="619" height="488" alt="image" src="https://github.com/user-attachments/assets/51d5b61e-b689-40b1-a240-5f715fe0a52b" />

## Comparison with CAMS Data

The station-based interpolation was compared with the coarser spatial
pattern represented by the CAMS atmospheric dataset. The comparison
illustrates the difference between local monitoring-based estimates and
regional gridded atmospheric information.

<img width="1126" height="1220" alt="image" src="https://github.com/user-attachments/assets/0884606a-5006-4480-931f-5525ba32643b" />

