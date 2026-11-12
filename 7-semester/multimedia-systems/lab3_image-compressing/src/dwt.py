import numpy as np


# 1 рівень, 1D по рядках (лекція 10, слайди 43-45)
def _rows(a: np.ndarray) -> np.ndarray:
    even, odd = a[:, 0::2], a[:, 1::2]
    return np.hstack([(even + odd) / 2, (even - odd) / 2])


def _irows(a: np.ndarray) -> np.ndarray:
    """Обернене: x[2i] = s + d, x[2i+1] = s - d."""
    half = a.shape[1] // 2
    s, d = a[:, :half], a[:, half:]
    out = np.empty_like(a)
    out[:, 0::2] = s + d
    out[:, 1::2] = s - d
    return out


# 1 рівень, 2D (лекція 10, слайди 47-49)
def haar2d_level(x: np.ndarray) -> np.ndarray:
    return _rows(_rows(x).T).T


def ihaar2d_level(y: np.ndarray) -> np.ndarray:
    return _irows(_irows(y.T).T)