import csv

import numpy as np
import pandas as pd

# --- Constants ---
MIN_ROWS = 8
MIN_NUMERIC_COLS = 2
NUMERIC_SHARE = 0.8
DEFAULT_MAX_NOTES = 96
FLAG_MAX_VALUES = 5


class DataError(Exception):
    """Raised when there is a problem with initial file"""


def load_csv(path: str) -> pd.DataFrame:
    """Read a CSV file and return a ready to converting DataFrame"""
    df = _read_csv(path)
    numeric = _extract_numeric_columns(df)

    if len(numeric.columns) < MIN_NUMERIC_COLS:
        raise DataError(
            f"Number of found numeric columns {len(numeric.columns)}. "
            f"At least {MIN_NUMERIC_COLS} are required."
        )
    if len(numeric) < MIN_ROWS:
        raise DataError(
            f"Too few rows: {len(numeric)}. At least {MIN_ROWS} are required."
        )
    table = numeric[_order_columns(numeric)].apply(_fill_gaps)
    table = _average_blocks(table)
    table.attrs["source_rows"] = len(numeric)
    return table

def _read_csv(path: str) -> pd.DataFrame:
    """Read the file; turn every reading problem into a DataError."""
    try:
        return pd.read_csv(path, sep=None, engine="python")
    except FileNotFoundError:
        raise DataError(f"File not found: {path}")
    except pd.errors.EmptyDataError:
        raise DataError("The file is empty.")
    except csv.Error:
        raise DataError("The file is empty or does not look like a CSV table.")
    except Exception as e:
        raise DataError(f"Could not read the file as CSV: {e}")

def _extract_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Keep numeric columns; drop empty and constant ones."""
    columns = {}
    for name in df.columns:
        col = df[name]
        if not pd.api.types.is_numeric_dtype(col):
            # Try to read text such as "12,5" as a number
            col = pd.to_numeric(
                col.astype(str).str.replace(",", ".", regex=False),
                errors="coerce",
            )
            if col.notna().mean() < NUMERIC_SHARE:
                continue  # not a numeric column
        col = col.replace([np.inf, -np.inf], np.nan)
        if col.nunique(dropna=True) < 2:
            continue # Constant or empty column
        columns[name] = col
    return pd.DataFrame(columns)


def _order_columns(numeric: pd.DataFrame) -> list:
    """Column names in file order, but "flag" columns (few distinct values) last."""
    flags = [c for c in numeric.columns if numeric[c].nunique() <= FLAG_MAX_VALUES]
    return [c for c in numeric.columns if c not in flags] + flags

def _fill_gaps(series: pd.Series) -> pd.Series:
    # Fill gaps using linear interpolation.
    return series.interpolate().bfill().ffill()


def _average_blocks(df: pd.DataFrame, max_notes: int = DEFAULT_MAX_NOTES) -> pd.DataFrame:
    """Reduce the number of rows to max_notes by averaging blocks of rows."""
    n = len(df)
    if n <= max_notes:
        return df.reset_index(drop=True)
    blocks = np.arange(n) * max_notes // n  # block number for every row
    return df.groupby(blocks).mean().reset_index(drop=True)
