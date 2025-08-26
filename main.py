# main.py
from src.constants import STATION_ID_HELGOLAND
from src.data_loader import load_station_wind_data
from src.analysis import get_annual_data_quality_statistics, get_annual_wind_statistics

if __name__ == "__main__":
    wind_data = load_station_wind_data()

    helgoland_data = wind_data[STATION_ID_HELGOLAND]

    data_quality_stats = get_annual_data_quality_statistics(wind_df=helgoland_data, station_id=STATION_ID_HELGOLAND)
    wind_data_analysis_annual = get_annual_wind_statistics(wind_df=helgoland_data, station_id=STATION_ID_HELGOLAND)