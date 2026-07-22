# Urban Air Quality and Mobility in Berlin

## Project Overview

This project investigates the spatial distribution of nitrogen dioxide
(NO₂) concentrations across Berlin and examines the relationship between
air pollution, road traffic and urban land use.

## Methodology

The project combined *R programming, web-based data acquisition and GIS analysis**. Air-quality measurements were automatically collected from the official monitoring website using *web scraping in R*, then cleaned, structured and visualised to examine temporal NO₂ patterns. Monitoring-station addresses were *geocoded* to create spatial point features.

Traffic and land-use data were accessed through *Web Feature Services (WFS)* and integrated into the GIS environment. All spatial layers were checked, reprojected to a common coordinate reference system and clipped to the Berlin boundary.

An *Inverse Distance Weighting (IDW)* interpolation was applied to the monitoring-station measurements to estimate a continuous NO₂ concentration surface. The interpolated results were compared with traffic volumes, land-use patterns and gridded CAMS atmospheric data using spatial overlay, classification and cartographic visualisation techniques.

## Study Area and Monitoring Network

Berlin's air-quality monitoring network contains urban-background,
traffic and suburban monitoring stations. These station measurements
provided the observations used in the spatial analysis.

<img width="1448" height="1086" alt="image" src="https://github.com/user-attachments/assets/fce7da44-c494-4b6a-8111-b1e41e885d37" />


### Daily NO₂ Patterns

This graph compares average NO₂ concentrations throughout the day across
the three monitoring-station categories. Traffic stations generally show
stronger concentration peaks, reflecting the influence of daily mobility
patterns

<img width="662" height="410" alt="image" src="https://github.com/user-attachments/assets/12a493af-bcd5-46f1-96d2-f4389f6e073a" />

## Traffic Data

Average daily traffic volumes were analysed across Berlin's road network.
Traffic measurement nodes were used to connect traffic intensity with the
air-quality results. The datasets were accessed through the GeoBerlin WFS. 

<img width="1448" height="1086" alt="image" src="https://github.com/user-attachments/assets/684dfdf7-9c44-4ab5-9c25-828dd829e79e" />

## Land Use and Land Cover

Land-use information was included to provide additional context for the
distribution of emissions and urban development across Berlin.

<img width="1448" height="1086" alt="image" src="https://github.com/user-attachments/assets/edb09b58-9aba-407b-9383-8b32463c5633" />


## Spatial Distribution of NO₂

IDW was used to transform point-based monitoring
measurements into a continuous NO₂ concentration surface.The resulting surface indicates higher estimated
concentrations in central and traffic-intensive parts of Berlin, with lower
values toward several peripheral areas.

<img width="1448" height="1086" alt="image" src="https://github.com/user-attachments/assets/30262b83-6c42-4892-a558-b7f5ebcabc2b" />

## Relationship Between Traffic and NO₂

Estimated average daily vehicle volumes increased across the NO₂
concentration classes. The fitted relationship produced an R² value of
approximately 0.836, indicating a strong association in the analysed data.

<img width="619" height="488" alt="image" src="https://github.com/user-attachments/assets/51d5b61e-b689-40b1-a240-5f715fe0a52b" />

## Comparison with CAMS Data

The IDW interpolation was visually compared with gridded CAMS atmospheric
data. A common concentration colour scheme was used to facilitate comparison
between areas of relatively low and high NO₂ concentration.

The comparison demonstrates the difference between a locally interpolated
surface based on monitoring stations and a coarser atmospheric grid product.

<img width="1448" height="1086" alt="image" src="https://github.com/user-attachments/assets/91a101a9-64e4-412f-8e63-b356d1d3b655" />

## Full Report

A detailed explanation of the literature review, atmospheric chemistry,
data processing, methodology and results is available. Reach me out on LinkdeIn if you are interested: https://www.linkedin.com/in/papa-arona-ndiaye-83740120b/ 
