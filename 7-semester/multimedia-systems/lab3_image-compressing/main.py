import argparse
import numpy as np

from src.image_io import load_grayscale, save_image
from src.dct import dct_image, idct_image
from src.dwt import dwt_image, idwt_image
from src.compression import keep_top_fraction, count_nonzero_fraction
from src.metrics import psnr, estimated_compression_ratio
from src.visualize import show_comparison

LEVELS = 3


def run_dct(img, fraction):
    coeffs = dct_image(img)
    kept = keep_top_fraction(coeffs, fraction)
    rec = idct_image(kept)
    frac = count_nonzero_fraction(kept)
    return rec, {"psnr": psnr(img, rec), "fraction": frac,
                 "cr": estimated_compression_ratio(frac)}


def run_dwt(img, fraction):
    coeffs = dwt_image(img, LEVELS)
    kept = keep_top_fraction(coeffs, fraction)
    rec = idwt_image(kept, LEVELS)
    frac = count_nonzero_fraction(kept)
    return rec, {"psnr": psnr(img, rec), "fraction": frac,
                 "cr": estimated_compression_ratio(frac)}


def experiments(img, fractions=(0.25, 0.10, 0.05, 0.02)):
    print(f"{'Метод':<6}{'Частка':>9}{'Збер.коеф':>11}{'CR~':>8}{'PSNR,дБ':>10}")
    for f in fractions:
        for name, fn in (("DCT", run_dct), ("DWT", run_dwt)):
            rec, info = fn(img, f)
            print(f"{name:<6}{f*100:>8.1f}%{info['fraction']*100:>10.2f}%"
                  f"{info['cr']:>8.1f}{info['psnr']:>10.2f}")
            save_image(rec, f"results/{name.lower()}_{int(f*100)}pct.png")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--fraction", type=float, default=0.10)
    ap.add_argument("--experiments", action="store_true")
    args = ap.parse_args()

    img = load_grayscale(args.image, 512)
    if args.experiments:
        experiments(img)
    else:
        dct_rec, dct_info = run_dct(img, args.fraction)
        dwt_rec, dwt_info = run_dwt(img, args.fraction)
        show_comparison(img, dct_rec, dwt_rec, dct_info, dwt_info,
                        save_path="results/comparison.png")