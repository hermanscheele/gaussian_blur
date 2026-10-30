"""Generate the README figures in docs/ from the images in imgs/.

Run from the repo root:  python scripts/make_figures.py
"""
import sys
import time
from multiprocessing import Pool, cpu_count
from pathlib import Path

import imageio.v3 as iio
import matplotlib.pyplot as plt
import numpy as np
from skimage import color, img_as_float, transform

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from blur import blur, g, kernel  # noqa: E402

DOCS = ROOT / "docs"
IMGS = ROOT / "imgs"
K_DIM, SIG = 3, 2.0
PASSES = 6  # repeated 3x3 passes ≈ one wider gaussian, so the effect is visible at README size

INK, MUTED, GRID, BLUE = "#1f2328", "#57606a", "#e1e0d9", "#2a78d6"
plt.rcParams.update({
    "font.family": ["Helvetica", "DejaVu Sans"], "font.size": 11, "text.color": INK,
    "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.edgecolor": GRID, "savefig.dpi": 150, "savefig.bbox": "tight",
})


def load_grey(name: str, width: int | None = None, rotate: int = 0) -> np.ndarray:
    img = img_as_float(color.rgb2gray(iio.imread(IMGS / name)[..., :3]))
    img = np.rot90(img, rotate)
    if width:
        img = transform.resize(img, (round(img.shape[0] * width / img.shape[1]), width), anti_aliasing=True)
    return img


def blur_n(img: np.ndarray, n: int) -> np.ndarray:
    for _ in range(n):
        img = blur(img, K_DIM, SIG)
    return img


def before_after(img: np.ndarray, out: str, crop: tuple[slice, slice]) -> None:
    blurred = blur_n(img, PASSES)
    top = img.shape[0] / img.shape[1]
    zoom = (crop[0].stop - crop[0].start) / (crop[1].stop - crop[1].start)
    fig, axes = plt.subplots(2, 2, figsize=(9, 4.5 * (top + zoom) + 0.9),
                             gridspec_kw={"height_ratios": [top, zoom]})
    for ax, im, title in [(axes[0, 0], img, "Before"), (axes[0, 1], blurred, "After")]:
        ax.imshow(im, cmap="gray", vmin=0, vmax=1)
        ax.set_title(title, loc="left", fontsize=12, fontweight="bold")
        ax.add_patch(plt.Rectangle((crop[1].start, crop[0].start), crop[1].stop - crop[1].start,
                                   crop[0].stop - crop[0].start, fill=False, ec=BLUE, lw=1.5))
    for ax, im in [(axes[1, 0], img), (axes[1, 1], blurred)]:
        ax.imshow(im[crop], cmap="gray", vmin=0, vmax=1, interpolation="nearest")
        ax.set_title("zoom", loc="left", fontsize=10, color=MUTED)
    for ax in axes.flat:
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
    fig.tight_layout()
    fig.savefig(DOCS / out)
    plt.close(fig)


def how_it_works() -> None:
    fig = plt.figure(figsize=(11, 4))

    # 1. the continuous 2D gaussian
    ax = fig.add_subplot(1, 3, 1, projection="3d")
    x, y = np.meshgrid(np.linspace(-3, 3, 60), np.linspace(-3, 3, 60))
    ax.plot_surface(x, y, g(x, y, 1.0), cmap="Blues", linewidth=0, antialiased=True, alpha=0.95)
    ax.set_title("1. 2D gaussian, σ = 1", loc="left", fontweight="bold")
    ax.set_xticks([-3, 0, 3]); ax.set_yticks([-3, 0, 3]); ax.set_zticks([0, 1])
    ax.set_xlabel("dx"); ax.set_ylabel("dy")
    ax.view_init(28, -55)

    # 2. sampled on a 3x3 grid and normalised -> kernel
    k = kernel(3, g, 1.0)
    ax = fig.add_subplot(1, 3, 2)
    ax.imshow(k, cmap="Blues", vmin=0, vmax=k.max() * 1.15)
    for (i, j), v in np.ndenumerate(k):
        ax.text(j, i, f"{v:.3f}", ha="center", va="center", color="white" if v > 0.12 else INK)
    ax.set_title("2. sampled → 3×3 kernel (sums to 1)", loc="left", fontweight="bold")
    ax.set_xticks([]); ax.set_yticks([])

    # 3. each output pixel = weighted sum of its neighbourhood
    patch = np.array([[0.9, 0.9, 0.2], [0.9, 0.9, 0.2], [0.9, 0.2, 0.2]])
    ax = fig.add_subplot(1, 3, 3)
    ax.imshow(patch, cmap="gray", vmin=0, vmax=1)
    for (i, j), v in np.ndenumerate(patch):
        ax.text(j, i, f"{v:.1f}", ha="center", va="center", color=INK if v > 0.5 else "white")
    ax.add_patch(plt.Rectangle((0.5, 0.5), 1, 1, fill=False, ec=BLUE, lw=2.5))
    ax.set_title("3. new centre = Σ pixel × weight", loc="left", fontweight="bold")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel(f"0.9  →  {float((patch * k).sum()):.2f}", fontsize=13, color=INK)

    fig.tight_layout()
    fig.savefig(DOCS / "how_it_works.png")
    plt.close(fig)


def blur_rows(rows: np.ndarray) -> np.ndarray:
    return blur(rows, K_DIM, SIG)


def benchmark(img: np.ndarray) -> None:
    workers = [w for w in (1, 2, 4, 8, cpu_count()) if w <= cpu_count()]
    times = []
    for w in workers:
        start = time.time()
        if w == 1:
            blur(img, K_DIM, SIG)
        else:
            with Pool(w) as p:
                np.vstack(p.map(blur_rows, np.array_split(img, w)))
        times.append(time.time() - start)
        print(f"{w:>2} processes: {times[-1]:.2f} s")

    fig, ax = plt.subplots(figsize=(7, 3.4))
    labels = ["sequential" if w == 1 else f"{w} processes" for w in workers]
    bars = ax.barh(labels, times, color=BLUE, height=0.6)
    for b, t in zip(bars, times):
        ax.text(b.get_width() + max(times) * 0.01, b.get_y() + b.get_height() / 2,
                f"{t:.1f} s   ({times[0] / t:.1f}×)", va="center", color=INK)
    ax.invert_yaxis()
    ax.set_xlim(0, max(times) * 1.25)
    ax.set_xlabel("seconds")
    ax.set_title(f"Blurring a {img.shape[1]}×{img.shape[0]} image ({cpu_count()}-core CPU)",
                 loc="left", fontweight="bold")
    ax.grid(axis="x", color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    fig.savefig(DOCS / "timing.png")
    plt.close(fig)


if __name__ == "__main__":
    DOCS.mkdir(exist_ok=True)
    how_it_works()
    before_after(load_grey("city.jpg"), "city.png", (slice(60, 140), slice(300, 460)))
    me = load_grey("me.png", width=480, rotate=-1)
    before_after(me, "me.png", (slice(220, 340), slice(160, 320)))
    benchmark(load_grey("me.png", width=1200, rotate=-1))
