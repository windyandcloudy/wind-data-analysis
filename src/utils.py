# src/utils.py

from pathlib import Path
from typing import Union

from pandas import DataFrame


def ensure_dir_exists(path: Path) -> Path:
    """Create directory if it doesn't exist, return Path object"""
    path.mkdir(parents=True, exist_ok=True)
    return path

def build_filename(*parts: Union[str, Path], extension: str = "csv") -> Path:
    """Build filename from multiple parts with specified file extension."""
    str_parts = [str(part) for part in parts if str(part).strip()]

    filename_basis = "_".join(str_parts)

    filename = f"{filename_basis}.{extension}"

    return Path(filename)

def get_path(*folders: Union[str, Path]) -> Path:
    str_folders = [folder for folder in folders if str(folder).strip()]

    path = Path(*str_folders)

    return ensure_dir_exists(path)

def save_as_csv(df: DataFrame, file_path: Path) -> None:
    df.to_csv(file_path)
    print(f"Saved: {file_path}")