# main.py
from src.constants import STATION_ID_HELGOLAND
from src.data_loader import load_station_wind_data
from src.wind_analysis import get_annual_wind_statistics

if __name__ == "__main__":
    wind_data = load_station_wind_data()
    annual_wind_analyzis = get_annual_wind_statistics(wind_data[STATION_ID_HELGOLAND])