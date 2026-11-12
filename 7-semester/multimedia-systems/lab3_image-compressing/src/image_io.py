import numpy as np
from PIL import Image


def load_grayscale(path: str, size: int = 512) -> np.ndarray:
    img = Image.open(path).convert("L")          # "L" = 8-bit grayscale
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    return np.asarray(img, dtype=np.float64)


def save_image(arr: np.ndarray, path: str) -> None:
    arr = np.clip(np.round(arr), 0, 255).astype(np.uint8)
    Image.fromarray(arr, mode="L").save(path)