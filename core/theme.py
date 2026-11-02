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
    "decor_1": 0.40, "decor_2": 0.50, "decor_soft": 0.85, "ribbon_fill": 1.0, "box_fill": 1.0,
}

# Palet per skin. SATU-SATUNYA tempat warna skin didefinisikan (skin tidak boleh punya hex sendiri).
# Hanya nama warna yang sudah ada yang boleh ditimpa. "classic" tidak menimpa apa pun.
SKIN_COLORS: Mapping[str, Mapping[str, str]] = {
    "garden": {"accent": "#2E7D32", "accent_soft": "#E8F5E9", "decor_1": "#43A047", "decor_2": "#F9A825",
               "decor_soft": "#CDE8C5", "ribbon_fill": "#E3F4D7", "box_fill": "#F4FAEF"},
    "space": {"accent": "#3F2B96", "accent_soft": "#ECE8FA", "decor_1": "#5B47C9", "decor_2": "#F2A900",
              "decor_soft": "#CFC8F2", "ribbon_fill": "#E9E5FA", "box_fill": "#F3F0FC"},
}
# Versi bw: hanya abu-abu; fill besar selalu 1.0 (putih), aksen berupa garis (outline).
SKIN_BW: Mapping[str, Mapping[str, float]] = {
    "garden": {"decor_1": 0.40, "decor_2": 0.50},
    "space": {"decor_1": 0.40, "decor_2": 0.50},
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
    skin: str = "classic"

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
def get_theme(mode: str, skin: str = "classic") -> Theme:
    """Ambil tema untuk mode 'color' | 'bw' dan skin tertentu (default classic = palet lama)."""
    if mode == "color":
        pal = {k: _hex_to_rgb(v) for k, v in config.BRAND_COLORS.items()}
        for k, v in SKIN_COLORS.get(skin, {}).items():
            if k not in pal:
                raise KeyError(f"Skin '{skin}' menimpa warna yang tidak ada: {k}")
            pal[k] = _hex_to_rgb(v)
        return Theme("color", pal, 1.0, skin)
    if mode == "bw":
        pal = {k: (v, v, v) for k, v in BW_PALETTE.items()}
        for k, v in SKIN_BW.get(skin, {}).items():
            if k not in pal:
                raise KeyError(f"Skin '{skin}' menimpa warna bw yang tidak ada: {k}")
            pal[k] = (v, v, v)
        return Theme("bw", pal, config.BW_LINE_SCALE, skin)
    raise ValueError(f"Mode tidak dikenal: {mode!r} (pakai 'color' atau 'bw')")
