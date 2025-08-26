# src/analysis/data_quality.py
from pathlib import Path

import pandas as pd

from src.constants import ANALYSED_DATA_QUALITY_PREFIX, WindDataFrameFormat, DataQualityStatsDataFrame, \
    LOCAL_DATA_FOLDER, LOCAL_ANALYSED_DATA_FOLDER
from src.utils import get_path, save_as_csv, build_filename


class DataQuality:
    EXCELLENT = "Q1"
    GOOD = "Q2"
    POOR = "Q3"
    UNRELIABLE = "Q4"


class DataQualityBoundaries:
    EXCELLENT_TILL = 0.05
    GOOD_TILL = 0.15
    POOR_TILL = 0.3


def categorize_data_quality(missing_ratio):
    if missing_ratio < DataQualityBoundaries.EXCELLENT_TILL:
        return DataQuality.EXCELLENT
    elif missing_ratio < DataQualityBoundaries.GOOD_TILL:
        return DataQuality.GOOD
    elif missing_ratio < DataQualityBoundaries.POOR_TILL:
        return DataQuality.POOR
    else:
        return DataQuality.UNRELIABLE


def categorize_data_quality_for_series(missing_ratio_series: pd.Series):
    return missing_ratio_series.map(categorize_data_quality)


def calculate_data_missing_ratio(count_of_missing_values: pd.Series, expected_number_of_values: pd.Series):
    return count_of_missing_values / expected_number_of_values


def count_nan_values(series: pd.Series) -> int:
    return series.isna().sum()


def count_total_values(series: pd.Series) -> int:
    return len(series)


def calculate_missing_value_count(nan_values: pd.Series, total_values: pd.Series, expected_values: pd.Series):
    return (expected_values - total_values) + nan_values


def calculate_expected_hours_per_year(wind_df: pd.DataFrame) -> pd.Series:
    years = wind_df.index.year.unique()
    expected_hours = {}

    for year in years:
        start = f"{year}-01-01 00:00:00"
        end = f"{year}-12-31 23:00:00"
        year_hours = pd.date_range(start, end, freq="h")
        expected_hours[year] = len(year_hours)

    return pd.Series(expected_hours)

def get_data_quality_file_path(station_id, start_year, end_year) -> Path:
    directory = get_path(LOCAL_DATA_FOLDER, LOCAL_ANALYSED_DATA_FOLDER, station_id)
    filename = build_filename(ANALYSED_DATA_QUALITY_PREFIX, station_id, "annual", start_year, end_year)
    return directory / filename

def calculate_quality_statistics(wind_df: pd.DataFrame) -> pd.DataFrame:
    expected_hours_per_year = calculate_expected_hours_per_year(wind_df)

    speed_nan_count = wind_df.groupby(wind_df.index.year)[WindDataFrameFormat.WIND_SPEED].apply(count_nan_values)
    speed_total_values = wind_df.groupby(wind_df.index.year)[WindDataFrameFormat.WIND_SPEED].apply(count_total_values)
    speed_missing_values = calculate_missing_value_count(speed_nan_count, speed_total_values, expected_hours_per_year)
    speed_missing_data_ratio = calculate_data_missing_ratio(speed_missing_values, expected_hours_per_year)
    speed_data_quality = categorize_data_quality_for_series(speed_missing_data_ratio)

    direction_nan_count = wind_df.groupby(wind_df.index.year)[WindDataFrameFormat.WIND_DIRECTION].apply(count_nan_values)
    direction_total_values = wind_df.groupby(wind_df.index.year)[WindDataFrameFormat.WIND_DIRECTION].apply(
        count_total_values)
    direction_missing_values = calculate_missing_value_count(direction_nan_count, direction_total_values,
                                                             expected_hours_per_year)
    direction_missing_data_ratio = calculate_data_missing_ratio(direction_missing_values, expected_hours_per_year)
    direction_data_quality = categorize_data_quality_for_series(direction_missing_data_ratio)

    quality_stats = pd.DataFrame({
        DataQualityStatsDataFrame.EXPECTED_HOUR_COUNT: expected_hours_per_year,
        DataQualityStatsDataFrame.WIND_SPEED_NAN_COUNT: speed_nan_count,
        DataQualityStatsDataFrame.WIND_SPEED_MISSING_VALUES: speed_missing_values,
        DataQualityStatsDataFrame.WIND_SPEED_MISSING_RATIO: speed_missing_data_ratio.round(DataQualityStatsDataFrame.DECIMAL_PLACE),
        DataQualityStatsDataFrame.WIND_SPEED_DATA_QUALITY: speed_data_quality,
        DataQualityStatsDataFrame.WIND_DIRECTION_NAN_COUNT: direction_nan_count,
        DataQualityStatsDataFrame.WIND_DIRECTION_MISSING_VALUES: direction_missing_values,
        DataQualityStatsDataFrame.WIND_DIRECTION_MISSING_RATIO: direction_missing_data_ratio.round(DataQualityStatsDataFrame.DECIMAL_PLACE),
        DataQualityStatsDataFrame.WIND_DIRECTION_DATA_QUALITY: direction_data_quality
    })
    quality_stats.index.name = DataQualityStatsDataFrame.INDEX

    return quality_stats

def get_annual_data_quality_statistics(wind_df: pd.DataFrame, station_id: str) -> pd.DataFrame:
    start_year = wind_df.index.min().year
    end_year = wind_df.index.max().year
    file_path = get_data_quality_file_path(station_id=station_id, start_year=start_year, end_year=end_year)

    data_quality_statistics = calculate_quality_statistics(wind_df)

    save_as_csv(data_quality_statistics, file_path)

    return data_quality_statistics