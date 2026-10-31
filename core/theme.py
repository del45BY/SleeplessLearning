"""Tema warna. SATU-SATUNYA tempat nilai warna didefinisikan.

Modul hanya boleh memakai NAMA warna (mis. "ink", "trace"), tidak pernah nilai.
Mode `bw`: semua warna abu-abu/hitam, tanpa fill gelap, garis lebih tegas.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Mapping, Tuple

from reportlab.lib.colors import Color

import config

RGB = Tuple[float, float, float]

# Palet hitam-putih ramah cetak (abu-abu 0..1). Garis >= 3:1 vs kertas putih.
BW_PALETTE: Mapping[str, float] = {
    "paper": 1.0, "ink": 0.0, "muted": 0.30, "line": 0.40, "guide": 0.45,
    "guide_soft": 0.55, "trace": 0.35, "accent": 0.0, "accent_soft": 1.0,
    "model_fill": 1.0,
}


def _hex_to_rgb(h: str) -> RGB:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))  # type: ignore[return-value]


def relative_luminance(rgb: RGB) -> float:
    """Luminansi relatif WCAG (0..1)."""
    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_vs_white(rgb: RGB) -> float:
    """Rasio kontras warna terhadap kertas putih."""
    return 1.05 / (relative_luminance(rgb) + 0.05)


def is_gray(rgb: RGB, tol: float = 1e-6) -> bool:
    return abs(rgb[0] - rgb[1]) <= tol and abs(rgb[1] - rgb[2]) <= tol


@dataclass(frozen=True)
class Theme:
    mode: str
    palette: Mapping[str, RGB]
    line_scale: float = 1.0

    @property
    def is_bw(self) -> bool:
        return self.mode == "bw"

    def rgb(self, name: str) -> RGB:
        try:
            return self.palette[name]
        except KeyError:
            raise KeyError(f"Warna '{name}' tidak ada di tema. Pilihan: {', '.join(sorted(self.palette))}")

    def color(self, name: str) -> Color:
        return Color(*self.rgb(name))


@lru_cache(maxsize=None)
def get_theme(mode: str) -> Theme:
    """Ambil tema untuk mode 'color' atau 'bw'."""
    if mode == "color":
        return Theme("color", {k: _hex_to_rgb(v) for k, v in config.BRAND_COLORS.items()})
    if mode == "bw":
        return Theme("bw", {k: (v, v, v) for k, v in BW_PALETTE.items()}, config.BW_LINE_SCALE)
    raise ValueError(f"Mode tidak dikenal: {mode!r} (pakai 'color' atau 'bw')")
