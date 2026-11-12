import numpy as np
import matplotlib.pyplot as plt


def show_comparison(original, dct_rec, dwt_rec, dct_info, dwt_info, save_path=None):
    """dct_info / dwt_info: dict з ключами 'psnr', 'fraction', 'cr'."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.5))
    items = [
        (original, "Original", ""),
        (dct_rec, "DCT 8x8",
         f"PSNR={dct_info['psnr']:.2f} dB\nкоеф.: {dct_info['fraction']*100:.1f}%  CR≈{dct_info['cr']:.1f}"),
        (dwt_rec, "DWT Haar",
         f"PSNR={dwt_info['psnr']:.2f} dB\nкоеф.: {dwt_info['fraction']*100:.1f}%  CR≈{dwt_info['cr']:.1f}"),
    ]
    for ax, (img, title, sub) in zip(axes, items):
        ax.imshow(np.clip(img, 0, 255), cmap="gray", vmin=0, vmax=255)
        ax.set_title(title, fontsize=13)
        ax.set_xlabel(sub, fontsize=11)
        ax.set_xticks([]); ax.set_yticks([])
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()