import numpy as np

N = 8

def C(u):
    return np.sqrt(2) / 2 if u == 0 else 1.0

def dct_matrix(n: int = N) -> np.ndarray:
    """Будує ортонормовану матрицю DCT розміру n x n. Формула з лекції 10 слайд 34"""
    T = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == 0:
                T[i, j] = 1.0 / np.sqrt(n)
            else:
                T[i, j] = np.sqrt(2.0 / n) * np.cos((2 * j + 1) * i * np.pi / (2 * n))
    return T

T = dct_matrix(N)


def dct2_block(f: np.ndarray) -> np.ndarray:
    return T @ f @ T.T


def idct2_block(F: np.ndarray) -> np.ndarray:
    return T.T @ F @ T

def dct_image(img: np.ndarray) -> np.ndarray:
    h, w = img.shape
    assert h % N == 0 and w % N == 0, "Розмір має бути кратним 8"
    out = np.zeros_like(img, dtype=np.float64)
    for i in range(0, h, N):
        for j in range(0, w, N):
            out[i:i+N, j:j+N] = dct2_block(img[i:i+N, j:j+N] - 128.0)
    return out


def idct_image(coeffs: np.ndarray) -> np.ndarray:
    h, w = coeffs.shape
    out = np.zeros_like(coeffs, dtype=np.float64)
    for i in range(0, h, N):
        for j in range(0, w, N):
            out[i:i+N, j:j+N] = idct2_block(coeffs[i:i+N, j:j+N]) + 128.0
    return out