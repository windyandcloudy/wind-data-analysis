# station ids
STATION_ID_HELGOLAND = "02115"

# remote paths
URL_DWD_WIND_DATA = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/wind/"
REMOTE_PATH_DWD_HISTORICAL = "historical/"
REMOTE_PATH_DWD_RECENT = "recent/"
WIND_DATA_FILE_PREFIX = "produkt_ff_stunde"
# zip folder name schema: stundenwerte_FF_[station id]_[start time]_[end time]_hist.zip
# wind data file name schema: produkt_ff_stunde_[start time]_[end time]_[station id].txt

# local paths
LOCAL_DATA_FOLDER = "data"
LOCAL_HISTORICAL_FOLDER = "historical"
LOCAL_RECENT_FOLDER = "recent"
FILE_NAME_ANNUAL_STATISTICS = "annual_wind_statistics.csv"


# DWD data format constants
class DWDFormat:
    DATE_FORMAT = "%Y%m%d%H"
    ERROR_VALUE = "-999"
    END_OF_ROW = "eor"
    SEPARATOR = ";"


class DWDColumnNames:
    MEASURE_DATE = "MESS_DATUM"
    STATION_ID = "STATIONS_ID"
    WIND_SPEED = "F"
    WIND_DIRECTION = "D"


class DataFrameFormat:
    INDEX = "datetime"
    STATION_ID = "station_id"
    MEASURE_DATE = "measure_date"
    WIND_SPEED = "wind_speed"
    WIND_DIRECTION = "wind_direction"

class AnnualStatsDataFrame:
    INDEX = "year"
    EXPECTED_HOUR_COUNT = "expected_hours"
    WIND_SPEED_NAN_COUNT = "speed_nans"
    WIND_SPEED_MISSING_VALUES = "speed_missing_values"
    WIND_DIRECTION_NAN_COUNT = "direction_nans"
    WIND_DIRECTION_MISSING_VALUES = "direction_missing_values"
    WIND_DATA_BOTH_NAN_COUNT = "both_nans"
    WIND_SPEED_MEAN = "speed_mean"
    WIND_SPEED_MEDIAN = "speed_median"
    WIND_SPEED_MINIMUM = "speed_min"
    WIND_SPEED_MAXIMUM = "speed_max"
    WIND_SPEED_STANDARD_DEVIATION = "speed_standard_deviation"
    WIND_DIRECTION_AVERAGE = "direction_average"
    DECIMAL_PLACE = 2