# Wind Data Analysis (Work in Progress)

Automated analysis of wind measurement data from German Weather Service (DWD) stations.
This project downloads, processes, and analyzes historical wind data.

## Project Goals

- Download wind data automatically from DWD open data portal
- Perform statistical analysis of wind patterns and trends
- Create visualizations for wind direction and speed analysis

Analyse von Winddaten der Messstation Helgoland (DWD).

## Features
- [x] Automated data download from DWD opendata url
- [x] Data preprocessing and DataFrame conversion
- [ ] Annual wind statistics (dominant direction, speed statistics)
- [ ] Monthly pattern analysis
- [ ] Wind rose diagrams

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

Currently analyzes Helgoland (Station-ID: 02115):
- wind speed measurements since 1959
- wind direction data since 1975
- hourly data

## Project Structur
```
wind_data_analysis/
├── data/                 # Downloaded data (auto-created)
├── src/
│   ├── constants.py      # Configuration constants
│   ├── data_loader.py    # Data download and preprocessing
│   ├── visualization.py  # Plotting and visualization
│   └── wind_analysis.py  # Statistical analysis functions
├── .gitignore
├── main.py              # Main execution script
├── README.md           # This file
└── requirements.txt     # Python dependencies
```