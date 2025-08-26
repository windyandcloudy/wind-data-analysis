# Wind Data Analysis (Work in Progress)

Automated analysis of wind measurement data from German Weather Service (DWD) stations.
This project downloads, processes, and analyzes historical wind data.

## Project Goals

- Download wind data automatically from DWD open data portal
- Assess data quality and completeness for reliable analysis
- Detect and analyze temporal data gaps and missing periods
- Perform statistical analysis of wind patterns and trends
- Compare different DWD wind datasets (wind vs wind_synop)
- Create visualizations for wind direction and speed analysis

## Features

- [x] Automated data download from DWD opendata portal
- [x] Data preprocessing and DataFrame conversion
- [x] Structured data storage
- [x] Q1-Q4 classification based on completeness of data
- [ ] Missing data periods detection and analysis
- [x] Annual wind speed statistics (mean, median, min/max, standard deviation)
- [x] Annual wind direction statistics (circular wind direction)
- [ ] Monthly and seasonal pattern analysis
- [ ] Comparative analysis: wind vs wind_synop datasets
- [ ] Wind rose diagrams
- [ ] Time series plots for trends
- [ ] Data quality visualization
- [ ] CSV-based registry with station info (Station Ids, names, coordinates, ...)

## Quick Start

### Installation
```
pip install -r requirements.txt
```

### Usage
```
python main.py
```

## Default Analysis

Currently analyses Helgoland (Station-ID: 02115) historical wind data:
- Wind speed measurements: since 1959 (hourly data)
- Wind direction data: since 1975 (hourly data)
- Measurement gaps:
  - No wind direction measurements: 1959 - 1974
  - No wind measurement sensors installed: 2018-11-28 to 2019-11-15
  - 88 % data loss in 2019
  - small data gaps in 2018, 2021 (ca. 9 % data loss each)

## Project Structur
```
wind_data_analysis/
├── src/
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── data_quality.py
│   │   ├── wind_annual.py
│   │   ├── wind_comparison.py
│   │   └── wind_monthly.py
│   ├── constants.py
│   ├── data_loader.py
│   ├── visualization.py
│   └── wind_analysis.py
├── README.md
├── main.py
└── requirements.txt

```