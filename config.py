"""Konfigurasi global + design tokens.

SEMUA angka desain (ukuran font, tebal garis, tinggi baris, ukuran slot gambar)
didefinisikan di sini. Modul TIDAK boleh memakai angka acak; pakai token ini
lewat helper di core/layout.py.

Unit: milimeter (mm) untuk layout, point (pt) untuk font dan tebal garis.
Koordinat layout dihitung dari pojok KIRI-ATAS halaman.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence

# --------------------------------------------------------------------------
# Path
# --------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
IMAGES_DIR = ROOT / "assets" / "images"
CACHE_DIR = ROOT / ".cache"
FONTS_DIR = ROOT / "fonts"
OUTPUT_DIR = ROOT / "output"
LOG_FILE = ROOT / "MODULES_LOG.md"

# --------------------------------------------------------------------------
# Brand, bahasa, mode
# --------------------------------------------------------------------------
BRAND_NAME = "Sleepless Learning"
LANGS = ("en", "id", "es", "de", "fr", "pt")
DEFAULT_LANG = "en"
FALLBACK_LANG = "en"
LANG_NAMES = {
    "en": "English (US)", "id": "Bahasa Indonesia", "es": "Español",
    "de": "Deutsch", "fr": "Français", "pt": "Português",
}
MODES = ("color", "bw")

# Warna brand (mode color). Mode bw dibuat di core/theme.py.
BRAND_COLORS = {
    "paper": "#FFFFFF",
    "ink": "#1F2937",
    "muted": "#6B7280",
    "line": "#94A3B8",
    "guide": "#7FA6E8",
    "guide_soft": "#A9C3F0",
    "trace": "#E8590C",
    "accent": "#2F6FDE",
    "accent_soft": "#E6EEFC",
    "model_fill": "#FFF1E6",
}

# --------------------------------------------------------------------------
# Halaman (US Letter portrait) dan grid
# --------------------------------------------------------------------------
PAGE_W_MM = 215.9
PAGE_H_MM = 279.4
MM_TO_PT = 72.0 / 25.4
MARGIN_MM = 15.0
GRID_COLS = 12
GRID_GUTTER_MM = 4.0

# Zona vertikal (mm dari atas halaman)
HEADER_TOP = MARGIN_MM
HEADER_H = 9.0
IDENT_TOP = 27.0
IDENT_H = 8.0
INSTR_TOP = 38.0
INSTR_H = 10.0
CONTENT_TOP = 52.0
FOOTER_H = 9.0
FOOTER_TOP = PAGE_H_MM - MARGIN_MM - FOOTER_H      # 255.4
CONTENT_BOTTOM = FOOTER_TOP - 3.0                  # 252.4
TOC_CONTENT_TOP = 32.0

# --------------------------------------------------------------------------
# Token font (pt)
# --------------------------------------------------------------------------
FONT_TITLE = 17.0
FONT_HEADER_SIDE = 10.0
FONT_IDENT = 11.0
FONT_INSTRUCTION = 12.0
FONT_LABEL = 14.0
FONT_BODY = 11.0
FONT_FOOTER = 8.0
FONT_COVER_TITLE = 22.0
FONT_COVER_SUB = 14.0
MIN_FONT_PT = 8.0                                  # QC: tidak boleh lebih kecil

# --------------------------------------------------------------------------
# Token garis dan baris (pt / mm)
# --------------------------------------------------------------------------
LINE_THIN_PT = 0.5
LINE_NORMAL_PT = 0.8
LINE_THICK_PT = 1.2
TRACE_STROKE_PT = 0.9
TRACE_DASH = (2.2, 2.2)
GUIDE_DASH = (1.5, 2.0)
BOX_RADIUS_MM = 3.0
MIN_WRITE_LINE_MM = 20.0                           # sisa garis minimal di zona identitas

TRACE_ROW_H_MM = 22.0                              # tinggi 1 baris tracing
TRACE_TOP, TRACE_MID, TRACE_BASE = 0.12, 0.31, 0.88  # posisi garis panduan (rasio tinggi baris)
TRACE_CAP_RATIO = 0.729                            # cap-height font trace / em (DejaVu Sans)
TRACE_GAP_MM = 6.0
# ukuran font tracing diturunkan dari tinggi baris supaya huruf pas di antara garis
TRACE_FONT_PT = (TRACE_BASE - TRACE_TOP) * TRACE_ROW_H_MM / TRACE_CAP_RATIO * MM_TO_PT
WRITE_ROW_H_MM = 14.0                              # tinggi baris menulis kosong

# --------------------------------------------------------------------------
# Token ukuran slot gambar (mm, persegi) dan ikon
# --------------------------------------------------------------------------
IMG_SIZES = {"S": 16.0, "M": 26.0, "L": 34.0, "XL": 60.0}
ICON_MM = 7.0
MIN_IMAGE_PX = 300                                 # di bawah ini: WARN
HARD_MIN_IMAGE_PX = 100                            # di bawah ini: FAIL
PLACEHOLDER_PX = 1000

# Mode hitam-putih
BW_CONTRAST = 1.35
BW_BRIGHTNESS = 1.0
BW_LINE_SCALE = 1.25                               # garis lebih tegas di mode bw

# QC
MAX_PDF_WARN_MB = 8.0
MAX_PDF_FAIL_MB = 30.0

# --------------------------------------------------------------------------
# Font (TTF Unicode). Letakkan file di fonts/ agar hasil identik di semua mesin.
# --------------------------------------------------------------------------
FONT_SEARCH_DIRS: Sequence[Path] = (
    FONTS_DIR,
    Path("/usr/share/fonts/truetype/dejavu"),
    Path("/usr/share/fonts/dejavu"),
    Path("/usr/share/fonts/TTF"),
    Path("/usr/share/fonts/truetype/liberation"),
    Path("/Library/Fonts"),
    Path("/System/Library/Fonts/Supplemental"),
    Path("C:/Windows/Fonts"),
    Path.home() / ".fonts",
)
FONT_CANDIDATES = {
    "regular": ["DejaVuSans.ttf", "LiberationSans-Regular.ttf", "Arial.ttf", "arial.ttf"],
    "bold": ["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf"],
    # font khusus tracing (mis. font sekolah bertitik). Jika tidak ada, pakai regular.
    "trace": ["Trace.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf", "Arial.ttf", "arial.ttf"],
}


def find_font_file(names: Sequence[str]) -> Optional[Path]:
    """Cari file font pertama yang ada di FONT_SEARCH_DIRS."""
    for name in names:
        for d in FONT_SEARCH_DIRS:
            p = Path(d) / name
            if p.is_file():
                return p
    return None


# --------------------------------------------------------------------------
# Override opsional lewat worksheet.yaml (butuh PyYAML)
# --------------------------------------------------------------------------
def _apply_yaml_overrides() -> None:
    path = ROOT / "worksheet.yaml"
    if not path.is_file():
        return
    try:
        import yaml  # type: ignore
    except ImportError:
        return
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    g = globals()
    if "brand_name" in data:
        g["BRAND_NAME"] = str(data["brand_name"])
    if isinstance(data.get("brand_colors"), dict):
        BRAND_COLORS.update({k: str(v) for k, v in data["brand_colors"].items() if k in BRAND_COLORS})


_apply_yaml_overrides()
