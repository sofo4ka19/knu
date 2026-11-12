import numpy as np


def mse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean((a.astype(np.float64) - b.astype(np.float64)) ** 2))


def psnr(original: np.ndarray, restored: np.ndarray, max_val: float = 255.0) -> float:
    restored = np.clip(np.round(restored), 0, 255)
    m = mse(original, restored)
    if m == 0:
        return float("inf")
    return 10.0 * np.log10(max_val ** 2 / m)


def estimated_compression_ratio(nonzero_fraction: float) -> float:
    """Ідеалізований CR = всього коефіцієнтів / ненульових"""
    return 1.0 / nonzero_fraction if nonzero_fraction > 0 else float("inf")