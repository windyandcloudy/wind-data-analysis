# data_loader.py

import zipfile
from pathlib import Path
from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.constants import URL_DWD_WIND_DATA, REMOTE_PATH_DWD_HISTORICAL, LOCAL_DATA_FOLDER, LOCAL_HISTORICAL_FOLDER, \
    WIND_DATA_FILE_PREFIX, DWDFormat, DWDColumnNames, DataFrameFormat, STATION_ID_HELGOLAND


# Version 1: Web scraping
def find_station_file_url_web_scraping(station_id: str, base_url: str = URL_DWD_WIND_DATA) -> str | None:
    """Finds station file URL via web scraping"""
    try:
        base_url_historical = base_url + REMOTE_PATH_DWD_HISTORICAL
        response_historical = requests.get(base_url_historical)
        response_historical.raise_for_status()

        soup_historical = BeautifulSoup(response_historical.content, "html.parser")
        links_historical = soup_historical.find_all("a")

        for link in links_historical:
            href = link.get("href", "")
            if station_id in href and href.endswith(".zip"):
                return base_url_historical + href

        print(f"No file found for station {station_id}")
        return None

    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


def download_station_data_web_scraping(url: str) -> Path:
    """Downloads zip file if not already present. Creates folder structure."""
    local_historical_path = Path(LOCAL_DATA_FOLDER) / LOCAL_HISTORICAL_FOLDER
    local_historical_path.mkdir(parents=True, exist_ok=True)

    zip_name = url.split("/")[-1]
    zip_path = local_historical_path / zip_name

    if zip_path.exists():
        print(f"File already exists: {zip_path}")
        return zip_path

    response = requests.get(url)
    with open(zip_path, "wb") as file:
        file.write(response.content)

    print(f"Downloaded: {zip_path}")
    return zip_path


# Version 2: Wetterdienst Package
def find_station_file_url_wetterdienst(station_id):
    # TODO: Implement function that use the wetterdienst package
    pass


def extract_txt_files_from_zip(zip_path: Path) -> list[Path] | None:
    """Extract zip data with txt ending und returns a list of local txt path"""
    zip_path = Path(zip_path)
    extract_to_folder = zip_path.with_suffix("")
    print(extract_to_folder)
    extract_to_folder.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, mode="r") as zip_file:
        txt_file_list = [file for file in zip_file.namelist() if file.endswith(".txt")]

        if txt_file_list:
            zip_file.extractall(path=extract_to_folder, members=txt_file_list)
            return [extract_to_folder / txt_file for txt_file in txt_file_list]
        else:
            print("No txt data found!")
            return None


def find_wind_data_file(txt_file_list: list[Path]) -> Path | None:
    """Find the wind data txt in all extracted txt files"""
    if not txt_file_list:
        return None

    for file_path in txt_file_list:
        if WIND_DATA_FILE_PREFIX in file_path.name:
            return file_path

    print(f"No file with '{WIND_DATA_FILE_PREFIX}' found!")
    return None


def parse_wind_data_txt_to_dataframe(txt_file_path: Path) -> pd.DataFrame:
    """
    Parse DWD wind data file to pandas DataFrame.

    Args:
        txt_file_path: Path to the wind data txt file

    Returns:
        DataFrame with datetime index and renamed columns

    Raises:
        FileNotFoundError: If file doesn't exist
        pd.errors.EmptyDataError: If file is empty
    """
    df = pd.read_csv(
        txt_file_path,
        sep=DWDFormat.SEPARATOR,
        na_values=DWDFormat.ERROR_VALUE,
        usecols=lambda x: x != DWDFormat.END_OF_ROW,
        skipinitialspace=True
    )
    df[DataFrameFormat.INDEX] = pd.to_datetime(df[DWDColumnNames.MEASURE_DATE], format=DWDFormat.DATE_FORMAT)
    df = df.set_index(DataFrameFormat.INDEX)
    df.rename(columns={
        DWDColumnNames.STATION_ID: DataFrameFormat.STATION_ID,
        DWDColumnNames.MEASURE_DATE: DataFrameFormat.MEASURE_DATE,
        DWDColumnNames.WIND_SPEED: DataFrameFormat.WIND_SPEED,
        DWDColumnNames.WIND_DIRECTION: DataFrameFormat.WIND_DIRECTION
    }, inplace=True)
    print(f"Wind data loaded: {len(df)} Measured values between {df.index.min()} and {df.index.max()}")
    print(df.head())
    return df


def load_single_station_data(station_id: str, method="scraping") -> Optional[pd.DataFrame]:
    """
    Orchestrates the data loading process for a single station id.

    Args:
        station_id: station id
        method: scraping or wetterdienst

    Returns:
        DataFrame of wind data for station id

    Raises:
        ValueError: If method is unknown
    """
    print(f"Loading data for station: {station_id}")

    if method == "scraping":
        print("Find zip file for station...")
        url_dwd_data = find_station_file_url_web_scraping(station_id)
        if not url_dwd_data:
            return None

        print("Download zip file for station...")
        zip_path = download_station_data_web_scraping(url_dwd_data)
        if not zip_path:
            return None

        print("Extract txt files from zip for station...")
        txt_files = extract_txt_files_from_zip(zip_path)
        if not txt_files:
            return None

        print("Find wind data file in extracted txt files...")
        wind_data_file = find_wind_data_file(txt_files)
        if not wind_data_file:
            return None

        print("Parse and return wind data file to DataFrame...")
        return parse_wind_data_txt_to_dataframe(wind_data_file)

    if method == "wetterdienst":
        # TODO: Implement wetterdienst method in load_single_station_data
        raise NotImplementedError("Wetterdienst method not yet implemented")

    else:
        raise ValueError(f"Unknown method: {method}")


def load_station_wind_data(station_ids: list[str] = None, method="scraping") -> dict[str, pd.DataFrame]:
    """
    Load wind data for one or multiple weather stations.

    Args:
        station_ids: List of DWD station IDs. Defaults to Helgoland (02115)
        method: Data loading method - 'scraping' or 'wetterdienst'

    Returns:
        Dictionary mapping station IDs to their wind data DataFrames

    Raises:
        ValueError: If unknown method is specified
    """

    if station_ids is None:
        station_ids = [STATION_ID_HELGOLAND]

    wind_data_results = {}

    for station_id in station_ids:
        try:
            data = load_single_station_data(station_id, method)
            if data is not None:
                wind_data_results[station_id] = data
            else:
                print(f"Failed to load data for station {station_id}")
        except Exception as e:
            print(f"Error loading station {station_id}: {e}")

    return wind_data_results
