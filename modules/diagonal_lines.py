"""Pra-menulis: menebalkan garis miring (dasar huruf A, V, X). 10 halaman, mudah -> sulit.

Dua jenis halaman (1 aktivitas per halaman):
  * "rows"  : baris [gambar awal] -- garis miring --> [gambar tujuan] (perosotan, tangga, tali layang-layang, ...)
  * "shape" : bentuk A (atap/tenda), V (kerucut es krim), X (rangka layang-layang/peta harta) + 1 gambar pendamping.
Kesulitan naik: arah satu jenis -> arah berganti; garis putus -> titik-titik -> hanya titik awal/akhir.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set, Tuple

import config
from core.layout import Page
from modules.base import BaseModule


@dataclass(frozen=True)
class Level:
    theme: str                          # kunci i18n: diagonal_lines.instruction.<theme>
    kind: str                           # "rows" | "shape"
    style: str                          # dashed | dotted | points
    size: str                           # token ukuran slot gambar: S | M | L
    # kind == "rows"
    n: int = 0                          # jumlah baris
    img_cols: int = 3                   # lebar kolom gambar ujung (kolom grid)
    dirs: Tuple[str, ...] = ("down_right",)   # arah per baris (diulang bergantian)
    start: Optional[str] = None
    end: Optional[str] = None
    # kind == "shape"
    shape: str = "roof"                 # roof (A) | vee (V) | cross (X)
    per_row: int = 2                    # jumlah bentuk per baris (membagi 12 kolom)
    rows: int = 2                       # jumlah baris bentuk
    image: Optional[str] = None         # gambar pendamping (di bawah roof/cross, di atas vee)
    line_h: str = "M"                   # token tinggi area garis (config.DLINE_SHAPE_H_MM)


LEVELS = (
    Level("slide",       "rows",  "dashed", "L", n=3, img_cols=3, dirs=("down_right",), start="slide_top", end="kid_sit"),
    Level("ladder",      "rows",  "dashed", "L", n=3, img_cols=3, dirs=("down_left",), start="window", end="grass_patch"),
    Level("kite_string", "rows",  "dashed", "L", n=3, img_cols=3, dirs=("down_right", "down_left"), start="kite", end="kid_kite"),
    Level("roof",        "shape", "dashed", "M", shape="roof", per_row=2, rows=2, image="house_body"),
    Level("ice_cream",   "shape", "dashed", "M", shape="vee",  per_row=3, rows=2, image="ice_scoop"),
    Level("kite_frame",  "shape", "dashed", "M", shape="cross", per_row=3, rows=2, image="kite_tail"),
    Level("tent",        "shape", "dotted", "S", shape="roof", per_row=3, rows=2, image="tent_door"),
    Level("ski",         "rows",  "dotted", "M", n=4, img_cols=2, dirs=("down_right", "down_left"), start="skier", end="cabin"),
    Level("treasure",    "shape", "points", "S", shape="cross", per_row=3, rows=2, image="treasure_chest"),
    Level("star",        "rows",  "points", "S", n=5, img_cols=2, dirs=("down_right", "down_left"), start="star", end="moon"),
)


class DiagonalLines(BaseModule):
    id = "diagonal_lines"
    title_key = "diagonal_lines.title"
    age_range = (4, 5)
    category = "pre_writing"
    pages = len(LEVELS)
    series = "DGL"

    def images(self, lang: str) -> Set[str]:
        out = {"icon_pencil"}
        for lv in LEVELS:
            out |= {i for i in (lv.start, lv.end, lv.image) if i}
        return out

    def render(self, page_index: int, ctx: Page) -> None:
        lv = LEVELS[page_index]
        ctx.draw_instruction(ctx.t(f"diagonal_lines.instruction.{lv.theme}"), icon="icon_pencil")
        if lv.kind == "rows":
            self._rows(ctx, lv)
        else:
            self._shapes(ctx, lv)

    @staticmethod
    def _centered(ctx: Page, total: float):
        """Blok setinggi `total` di tengah vertikal area konten."""
        area = ctx.band(0, 1)
        return area.take_top((area.h - total) / 2)[1].take_top(total)[0]

    def _rows(self, ctx: Page, lv: Level) -> None:
        img, pad = config.IMG_SIZES[lv.size], config.VLINE_IMG_PAD_MM
        cell_h, gap = config.DLINE_ROW_H_MM[lv.size], config.HLINE_ROW_GAP_MM
        region = self._centered(ctx, lv.n * cell_h + (lv.n - 1) * gap)
        for i, row in enumerate(region.split_rows(lv.n, gap)):
            d = lv.dirs[i % len(lv.dirs)]
            left, right = ctx.cell(row, 0, lv.img_cols), ctx.cell(row, config.GRID_COLS - lv.img_cols, lv.img_cols)
            mid = ctx.cell(row, lv.img_cols, config.GRID_COLS - 2 * lv.img_cols)
            top_h = img + pad
            if d == "down_right":           # awal kiri-atas, tujuan kanan-bawah
                s_cell, e_cell = left.take_top(top_h)[0], right.take_top(row.h - top_h)[1]
            else:                           # awal kanan-atas, tujuan kiri-bawah
                s_cell, e_cell = right.take_top(top_h)[0], left.take_top(row.h - top_h)[1]
            ctx.draw_image_slot(s_cell, lv.start, lv.size)
            ctx.draw_image_slot(e_cell, lv.end, lv.size)
            ctx.draw_diagonal_line(mid, d, lv.style, group="line", value=str(i + 1))

    def _shapes(self, ctx: Page, lv: Level) -> None:
        img, pad = config.IMG_SIZES[lv.size], config.VLINE_IMG_PAD_MM
        line_h, gap = config.DLINE_SHAPE_H_MM[lv.line_h], config.HLINE_ROW_GAP_MM
        unit_h = line_h + img + pad
        region = self._centered(ctx, lv.rows * unit_h + (lv.rows - 1) * gap)
        span = config.GRID_COLS // lv.per_row
        for r, row in enumerate(region.split_rows(lv.rows, gap)):
            for k in range(lv.per_row):
                unit = ctx.cell(row, k * span, span)
                if lv.shape == "vee":       # gambar di atas, garis V di bawahnya
                    pic, lines = unit.take_top(img + pad)
                else:                       # garis di atas, gambar di bawahnya (rumah, tenda, ekor layang-layang)
                    lines, pic = unit.take_top(line_h)
                ctx.draw_image_slot(pic, lv.image, lv.size)
                ctx.draw_diagonal_line(lines, lv.shape, lv.style, group="shape", value=str(r * lv.per_row + k + 1))
