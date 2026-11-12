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
