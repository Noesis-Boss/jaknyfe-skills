#!/usr/bin/env python3
import argparse
import json
import numpy as np
from PIL import Image
from scipy import ndimage


def prep(src, dst, pad=12):
    img = Image.open(src).convert("RGBA")
    a = np.asarray(img)[..., 3]
    ys, xs = np.where(a > 128)
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad + 1, a.shape[1])
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad + 1, a.shape[0])
    crop = img.crop((x0, y0, x1, y1))
    crop.save(dst)
    alpha = np.asarray(crop)[..., 3]
    h, w = alpha.shape
    solid = ndimage.binary_fill_holes(alpha > 128)
    dt = ndimage.distance_transform_edt(solid)
    hy, hx = np.unravel_index(dt.argmax(), dt.shape)
    rows = max(1, int(h * 0.035))
    fy, fx = np.where(alpha[h - rows:, :] > 128)
    feet_x = float(fx.mean()) if fx.size else w / 2
    return {
        "file": dst,
        "offset": [int(x0), int(y0)],
        "size": [int(w), int(h)],
        "head": {"x": int(hx), "y": int(hy), "r": round(float(dt[hy, hx]), 1)},
        "feet": {"x": round(feet_x, 1), "y": h},
    }


def main():
    p = argparse.ArgumentParser(description="Trim a keyed sprite and measure head and feet")
    p.add_argument("src")
    p.add_argument("dst")
    a = p.parse_args()
    print(json.dumps(prep(a.src, a.dst), indent=2))


if __name__ == "__main__":
    main()
