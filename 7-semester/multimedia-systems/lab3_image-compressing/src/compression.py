import numpy as np


def keep_top_fraction(coeffs: np.ndarray, fraction: float) -> np.ndarray:
    if not 0 < fraction <= 1:
        raise ValueError("fraction must be in (0, 1]")
    flat = np.abs(coeffs).ravel()
    k = max(1, int(round(fraction * flat.size)))        # скільки залишити
    # k-те за величиною значення = поріг
    threshold = np.partition(flat, flat.size - k)[flat.size - k]
    out = coeffs.copy()
    out[np.abs(out) < threshold] = 0.0
    return out


def count_nonzero_fraction(coeffs: np.ndarray) -> float:
    return np.count_nonzero(coeffs) / coeffs.size