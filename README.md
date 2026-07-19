# Urban Air Quality and Mobility in Berlin


## Project Overview

This project investigates the spatial distribution of nitrogen dioxide
(NO₂) concentrations across Berlin and examines the relationship between
air pollution, road traffic and urban land use.

## Study Area and Monitoring Network

Berlin's air-quality monitoring network contains urban-background,
traffic and suburban monitoring stations. These station measurements
provided the observations used in the spatial analysis.

<img width="1448" height="1086" alt="image" src="https://github.com/user-attachments/assets/fce7da44-c494-4b6a-8111-b1e41e885d37" />


### Daily NO₂ Patterns

The monitoring stations were grouped into traffic, urban-background and
outskirts categories to examine differences in the daily NO₂ cycle.

<img width="662" height="410" alt="image" src="https://github.com/user-attachments/assets/12a493af-bcd5-46f1-96d2-f4389f6e073a" />

## Traffic Data

Average daily traffic volumes were analysed across Berlin's road network.
Traffic measurement nodes were used to connect traffic intensity with the
air-quality results.

<img width="1448" height="1086" alt="image" src="https://github.com/user-attachments/assets/684dfdf7-9c44-4ab5-9c25-828dd829e79e" />

## Land Use and Land Cover

Land-use information was included to provide additional context for the
distribution of emissions and urban development across Berlin.

<img width="1448" height="1086" alt="image" src="https://github.com/user-attachments/assets/edb09b58-9aba-407b-9383-8b32463c5633" />


## Spatial Distribution of NO₂

Inverse Distance Weighting was used to estimate NO₂ concentrations between
the monitoring stations. The resulting surface indicates higher estimated
concentrations in central and traffic-intensive parts of Berlin, with lower
values toward several peripheral areas.

<img width="1448" height="1086" alt="image" src="https://github.com/user-attachments/assets/30262b83-6c42-4892-a558-b7f5ebcabc2b" />

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

<img width="1448" height="1086" alt="image" src="https://github.com/user-attachments/assets/91a101a9-64e4-412f-8e63-b356d1d3b655" />

