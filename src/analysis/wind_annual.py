# src/analysis/wind_annual.py
from pathlib import Path

import pandas as pd
import numpy as np
from typing import Optional

from src.constants import AnnualStatsDataFrame, WindDataFrameFormat, LOCAL_DATA_FOLDER, ANALYSED_DATA_PREFIX, \
    LOCAL_ANALYSED_DATA_FOLDER
from src.utils import get_path, build_filename, save_as_csv


def calculate_annual_average_wind_speed(wind_df: pd.DataFrame) -> pd.Series:
    return wind_df.groupby(wind_df.index.year)[WindDataFrameFormat.WIND_SPEED].mean()


def calculate_annual_median_wind_speed(wind_df: pd.DataFrame) -> pd.Series:
    return wind_df.groupby(wind_df.index.year)[WindDataFrameFormat.WIND_SPEED].median()


def calculate_annual_minimum_wind_speed(wind_df: pd.DataFrame) -> pd.Series:
    return wind_df.groupby(wind_df.index.year)[WindDataFrameFormat.WIND_SPEED].min()


def calculate_annual_maximum_wind_speed(wind_df: pd.DataFrame) -> pd.Series:
    return wind_df.groupby(wind_df.index.year)[WindDataFrameFormat.WIND_SPEED].max()


def calculate_annual_standard_deviation_wind_speed(wind_df: pd.DataFrame) -> pd.Series:
    return wind_df.groupby(wind_df.index.year)[WindDataFrameFormat.WIND_SPEED].std()


def calculate_circular_mean(wind_directions: pd.Series) -> float:
    wind_radians = np.radians(wind_directions)
    u_mean = np.cos(wind_radians).mean()
    v_mean = np.sin(wind_radians).mean()
    wind_average_direction_radian = np.arctan2(u_mean, v_mean)

    return np.degrees(wind_average_direction_radian) % 360


def calculate_annual_circular_average_direction(wind_df: pd.DataFrame) -> Optional[pd.Series]:
    clean_wind_df = wind_df.dropna(subset=WindDataFrameFormat.WIND_DIRECTION)

    if len(clean_wind_df) == 0:
        return None

    return clean_wind_df.groupby(clean_wind_df.index.year)[WindDataFrameFormat.WIND_DIRECTION].apply(
        calculate_circular_mean)

def get_wind_statistics_annual_file_path(station_id, start_year, end_year) -> Path:
    directory = get_path(LOCAL_DATA_FOLDER, LOCAL_ANALYSED_DATA_FOLDER, station_id)
    filename = build_filename(ANALYSED_DATA_PREFIX, station_id, "annual", start_year, end_year)
    return directory / filename

def calculate_annual_wind_statistics(wind_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate comprehensive annual wind statistics"""

    annual_stats = pd.DataFrame({
        AnnualStatsDataFrame.WIND_SPEED_MEAN: calculate_annual_average_wind_speed(wind_df),
        AnnualStatsDataFrame.WIND_SPEED_MEDIAN: calculate_annual_median_wind_speed(wind_df),
        AnnualStatsDataFrame.WIND_SPEED_MINIMUM: calculate_annual_minimum_wind_speed(wind_df),
        AnnualStatsDataFrame.WIND_SPEED_MAXIMUM: calculate_annual_maximum_wind_speed(wind_df),
        AnnualStatsDataFrame.WIND_SPEED_STANDARD_DEVIATION: calculate_annual_standard_deviation_wind_speed(wind_df),
        AnnualStatsDataFrame.WIND_DIRECTION_AVERAGE: calculate_annual_circular_average_direction(wind_df)
    })
    annual_stats.index.name = AnnualStatsDataFrame.INDEX

    annual_stats = annual_stats.round(AnnualStatsDataFrame.DECIMAL_PLACE)
    return annual_stats

def get_annual_wind_statistics(wind_df: pd.DataFrame, station_id: str) -> pd.DataFrame:
    start_year = wind_df.index.min().year
    end_year = wind_df.index.max().year
    file_path = get_wind_statistics_annual_file_path(station_id=station_id, start_year=start_year, end_year=end_year)

    annual_wind_statistics = calculate_annual_wind_statistics(wind_df)

    save_as_csv(annual_wind_statistics, file_path)

    return annual_wind_statistics