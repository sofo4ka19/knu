import numpy as np


# 1 рівень, 1D по рядках
def _rows(a: np.ndarray) -> np.ndarray:
    """x[2i] = (s + d) / 2, x[2i+1] = (s - d) / 2. - слайд 43"""
    even, odd = a[:, 0::2], a[:, 1::2]
    return np.hstack([(even + odd) / 2, (even - odd) / 2])


def _irows(a: np.ndarray) -> np.ndarray:
    """Обернене: x[2i] = s + d, x[2i+1] = s - d. - слайд 46"""
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

# повна обробка зображення (3 рівні)
def dwt_image(img: np.ndarray, levels: int = 3) -> np.ndarray:
    out = img.astype(np.float64).copy()
    size = out.shape[0]
    for _ in range(levels):
        out[:size, :size] = haar2d_level(out[:size, :size])
        size //= 2
    return out


def idwt_image(coeffs: np.ndarray, levels: int = 3) -> np.ndarray:
    out = coeffs.astype(np.float64).copy()
    size = out.shape[0] // (2 ** (levels - 1))   # розмір LL найглибшого рівня
    for _ in range(levels):
        out[:size, :size] = ihaar2d_level(out[:size, :size])
        size *= 2
    return out