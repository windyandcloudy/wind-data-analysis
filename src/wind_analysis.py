# src/analyze_data.py
from typing import Optional

import numpy as np
import pandas as pd

from src.constants import DataFrameFormat, AnnualStatsDataFrame, LOCAL_DATA_FOLDER, FILE_NAME_ANNUAL_STATISTICS


def calculate_annual_average_wind_speed(wind_df: pd.DataFrame) -> pd.Series:
    return wind_df.groupby(wind_df.index.year)[DataFrameFormat.WIND_SPEED].mean()


def calculate_annual_median_wind_speed(wind_df: pd.DataFrame) -> pd.Series:
    return wind_df.groupby(wind_df.index.year)[DataFrameFormat.WIND_SPEED].median()


def calculate_annual_minimum_wind_speed(wind_df: pd.DataFrame) -> pd.Series:
    return wind_df.groupby(wind_df.index.year)[DataFrameFormat.WIND_SPEED].min()


def calculate_annual_maximum_wind_speed(wind_df: pd.DataFrame) -> pd.Series:
    return wind_df.groupby(wind_df.index.year)[DataFrameFormat.WIND_SPEED].max()


def calculate_annual_standard_deviation_wind_speed(wind_df: pd.DataFrame) -> pd.Series:
    return wind_df.groupby(wind_df.index.year)[DataFrameFormat.WIND_SPEED].std()


def calculate_circular_mean(wind_directions: pd.Series) -> float:
    wind_radians = np.radians(wind_directions)
    u_mean = np.cos(wind_radians).mean()
    v_mean = np.sin(wind_radians).mean()
    wind_average_direction_radian = np.arctan2(u_mean, v_mean)

    return np.degrees(wind_average_direction_radian) % 360


def calculate_annual_circular_average_direction(wind_df: pd.DataFrame) -> Optional[pd.Series]:
    clean_wind_df = wind_df.dropna(subset=DataFrameFormat.WIND_DIRECTION)

    if len(clean_wind_df) == 0:
        return None

    return clean_wind_df.groupby(clean_wind_df.index.year)[DataFrameFormat.WIND_DIRECTION].apply(
        calculate_circular_mean)


def count_nan_values(series: pd.Series) -> int:
    return series.isna().sum()


def count_both_nan_values(df: pd.DataFrame) -> int:
    speed_nan = df[DataFrameFormat.WIND_SPEED].isna()
    direction_nan = df[DataFrameFormat.WIND_DIRECTION].isna()
    both_nan = speed_nan & direction_nan
    return both_nan.sum()


def count_total_values(series: pd.Series) -> int:
    return len(series)


def calculate_expected_hours_per_year(wind_df: pd.DataFrame) -> pd.Series:
    years = wind_df.index.year.unique()
    expected_hours = {}

    for year in years:
        start = f"{year}-01-01 00:00:00"
        end = f"{year}-12-31 23:00:00"
        year_hours = pd.date_range(start, end, freq="h")
        expected_hours[year] = len(year_hours)

    return pd.Series(expected_hours)


def get_annual_wind_statistics(wind_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate comprehensive annual wind statistics"""
    expected_hours_per_year = calculate_expected_hours_per_year(wind_df)
    nan_count_speed = wind_df.groupby(wind_df.index.year)[DataFrameFormat.WIND_SPEED].apply(count_nan_values)
    total_values_speed = wind_df.groupby(wind_df.index.year)[DataFrameFormat.WIND_SPEED].apply(count_total_values)
    nan_count_direction = wind_df.groupby(wind_df.index.year)[DataFrameFormat.WIND_DIRECTION].apply(count_nan_values)
    total_values_direction = wind_df.groupby(wind_df.index.year)[DataFrameFormat.WIND_DIRECTION].apply(
        count_total_values)

    annual_stats = pd.DataFrame({
        # AnnualStatsDataFrame.EXPECTED_HOUR_COUNT: expected_hours_per_year,
        # AnnualStatsDataFrame.WIND_SPEED_NAN_COUNT: nan_count_speed,
        AnnualStatsDataFrame.WIND_SPEED_MISSING_VALUES: (expected_hours_per_year - total_values_speed) + nan_count_speed,
        # AnnualStatsDataFrame.WIND_DIRECTION_NAN_COUNT: nan_count_direction,
        AnnualStatsDataFrame.WIND_DIRECTION_MISSING_VALUES: (expected_hours_per_year - total_values_direction) + nan_count_direction,
        AnnualStatsDataFrame.WIND_DATA_BOTH_NAN_COUNT: wind_df.groupby(wind_df.index.year).apply(count_both_nan_values),
        AnnualStatsDataFrame.WIND_SPEED_MEAN: calculate_annual_average_wind_speed(wind_df),
        AnnualStatsDataFrame.WIND_SPEED_MEDIAN: calculate_annual_median_wind_speed(wind_df),
        AnnualStatsDataFrame.WIND_SPEED_MINIMUM: calculate_annual_minimum_wind_speed(wind_df),
        AnnualStatsDataFrame.WIND_SPEED_MAXIMUM: calculate_annual_maximum_wind_speed(wind_df),
        AnnualStatsDataFrame.WIND_SPEED_STANDARD_DEVIATION: calculate_annual_standard_deviation_wind_speed(wind_df),
        AnnualStatsDataFrame.WIND_DIRECTION_AVERAGE: calculate_annual_circular_average_direction(wind_df)
    })
    annual_stats.index.name = AnnualStatsDataFrame.INDEX

    annual_stats = annual_stats.round(AnnualStatsDataFrame.DECIMAL_PLACE)
    print(annual_stats)
    annual_stats.to_csv(LOCAL_DATA_FOLDER + "/" + FILE_NAME_ANNUAL_STATISTICS)
    return annual_stats


def get_monthly_wind_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze wind patterns by month"""
    pass
