#!/usr/bin/env python3
import argparse
import numpy as np
from PIL import Image
from scipy import ndimage


def key(src, dst, tol=60.0):
    im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    border = np.concatenate([im[0], im[-1], im[:, 0], im[:, -1]])
    bgc = np.median(border, axis=0)
    dist = np.sqrt(((im - bgc) ** 2).sum(2))
    labels, _ = ndimage.label(dist < tol)
    edge = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    bg = np.isin(labels, edge[edge > 0])
    band = ndimage.binary_dilation(bg, iterations=3) & ~bg
    ink = np.array([20.0, 20.0, 20.0])
    d_ink = np.sqrt(((ink - bgc) ** 2).sum())
    alpha = np.ones(im.shape[:2], np.float32)
    alpha[bg] = 0.0
    alpha[band] = np.clip(dist[band] / d_ink, 0.0, 1.0)
    out = np.dstack([im, alpha * 255.0]).astype(np.uint8)
    Image.fromarray(out, "RGBA").save(dst)
    return bgc, int(bg.sum()), int(im.shape[0] * im.shape[1])


def main():
    p = argparse.ArgumentParser(description="Key a flat background to transparency")
    p.add_argument("src")
    p.add_argument("dst")
    p.add_argument("--tol", type=float, default=60.0)
    a = p.parse_args()
    bgc, removed, total = key(a.src, a.dst, a.tol)
    print(f"bg={bgc.round().astype(int).tolist()} removed={removed}/{total} px -> {a.dst}")


if __name__ == "__main__":
    main()
