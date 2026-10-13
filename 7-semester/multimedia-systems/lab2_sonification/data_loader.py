import csv

import numpy as np
import pandas as pd

# --- Constants (no "magic numbers" in the code) ---
MIN_ROWS = 8               # fewer rows than this cannot make a melody
MIN_NUMERIC_COLS = 2       # lab requirement: at least two indicators
NUMERIC_SHARE = 0.8        # share of values that must parse as numbers
DEFAULT_MAX_NOTES = 96     # maximum number of notes in the melody
TREND_FRACTION = 0.1       # trend window = 10% of the series length


class DataError(Exception):

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def load_csv(path: str) -> pd.DataFrame:
    """Read a CSV file and return a DataFrame with usable numeric columns only."""
    try:
        df = pd.read_csv(path, sep=None, engine="python")
    except FileNotFoundError:
        raise DataError(f"File not found: {path}")
    except pd.errors.EmptyDataError:
        raise DataError("The file is empty.")
    except csv.Error:
        raise DataError("The file is empty or does not look like a CSV table.")
    except Exception as e:
        raise DataError(f"Could not read the file as CSV: {e}")

    numeric = _extract_numeric_columns(df)

    if len(numeric.columns) < MIN_NUMERIC_COLS:
        raise DataError(
            f"Numeric columns found: {len(numeric.columns)}. "
            f"At least {MIN_NUMERIC_COLS} are required."
        )
    if len(numeric) < MIN_ROWS:
        raise DataError(
            f"Too few rows: {len(numeric)}. At least {MIN_ROWS} are required."
        )
    return numeric.reset_index(drop=True)


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


# ------------------------------------------------------------ preparation
def clean(series: pd.Series) -> pd.Series:
    # Fill gaps using linear interpolation.
    return series.interpolate().bfill().ffill()


def downsample(df: pd.DataFrame, max_notes: int = DEFAULT_MAX_NOTES) -> pd.DataFrame:
    # Reduce the number of rows to max_notes by averaging blocks of rows.
    n = len(df)
    if n <= max_notes:
        return df.reset_index(drop=True)
    blocks = np.arange(n) * max_notes // n  # block number for every row
    return df.groupby(blocks).mean().reset_index(drop=True)


def normalize(series: pd.Series, method: str = "rank") -> pd.Series:
    s = clean(series)
    if s.nunique() < 2:
        return pd.Series(0.5, index=s.index)  # guard against division by zero
    if method == "rank":
        return (s.rank(method="average") - 1) / (len(s) - 1)
    lo, hi = s.quantile(0.05), s.quantile(0.95)
    if hi == lo:
        return pd.Series(0.5, index=s.index)
    return ((s - lo) / (hi - lo)).clip(0, 1)


def split_trend(series: pd.Series, fraction: float = TREND_FRACTION):
    # Split a series into a slow trend and small fluctuations around it
    s = clean(series)
    window = max(3, int(len(s) * fraction))
    trend = s.rolling(window, center=True, min_periods=1).mean()
    return trend, s - trend


def prepare(df: pd.DataFrame, max_notes: int = DEFAULT_MAX_NOTES) -> pd.DataFrame:
    cleaned = df.apply(clean)
    small = downsample(cleaned, max_notes)
    return small.apply(normalize)