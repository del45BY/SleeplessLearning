"""Pra-menulis: menebalkan garis datar (kiri -> kanan) dari gambar awal ke gambar tujuan. 10 halaman.

Kenaikan kesulitan: garis pendek & sedikit (3 baris) -> panjang & banyak (7 baris); garis putus ->
titik-titik -> hanya titik awal/akhir (anak menarik sendiri). 1 aktivitas per halaman, instruksi 1 baris.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Set

import config
from core.layout import Page
from modules.base import BaseModule


@dataclass(frozen=True)
class Level:
    theme: str      # kunci i18n instruksi: horizontal_lines.instruction.<theme>
    n: int          # jumlah baris
    img_cols: int   # lebar tiap gambar ujung (kolom grid); makin kecil = garis makin panjang
    style: str      # dashed | dotted | points
    start: str      # PNG di kiri (menghadap kanan)
    end: str        # PNG di kanan (tujuan)
    size: str       # token ukuran slot gambar: S | M | L


LEVELS = (
    Level("road",        3, 3, "dashed", "car_side",     "house",         "L"),
    Level("train",       3, 3, "dashed", "train",        "station",       "L"),
    Level("bridge",      4, 3, "dashed", "rabbit",       "carrot",        "M"),
    Level("clothesline", 4, 2, "dashed", "pole_left",    "pole_right",    "M"),
    Level("river",       4, 2, "dashed", "boat",         "island",        "M"),
    Level("caterpillar", 5, 2, "dotted", "caterpillar",  "leaf",          "M"),
    Level("wire",        5, 2, "dotted", "bird",         "nest",          "M"),
    Level("airplane",    5, 2, "dotted", "airplane_side", "cloud",        "M"),
    Level("snail",       6, 2, "points", "snail",        "leaf",          "S"),
    Level("ant",         7, 2, "points", "ant",          "cookie",        "S"),
)


class HorizontalLines(BaseModule):
    id = "horizontal_lines"
    title_key = "horizontal_lines.title"
    age_range = (4, 5)
    category = "pre_writing"
    pages = len(LEVELS)
    series = "HLN"

    def images(self, lang: str) -> Set[str]:
        out = {"icon_pencil"}
        for lv in LEVELS:
            out |= {lv.start, lv.end}
        return out

    def render(self, page_index: int, ctx: Page) -> None:
        lv = LEVELS[page_index]
        ctx.draw_instruction(ctx.t(f"horizontal_lines.instruction.{lv.theme}"), icon="icon_pencil")
        row_h = config.IMG_SIZES[lv.size] + config.VLINE_IMG_PAD_MM
        gap = config.HLINE_ROW_GAP_MM
        total = lv.n * row_h + (lv.n - 1) * gap              # komposisi diletakkan di tengah vertikal
        area = ctx.band(0, 1)
        region = area.take_top((area.h - total) / 2)[1].take_top(total)[0]
        for i, row in enumerate(region.split_rows(lv.n, gap)):
            ctx.draw_image_slot(ctx.cell(row, 0, lv.img_cols), lv.start, lv.size)
            ctx.draw_horizontal_line(ctx.cell(row, lv.img_cols, config.GRID_COLS - 2 * lv.img_cols),
                                     lv.style, group="line", value=str(i + 1))
            ctx.draw_image_slot(ctx.cell(row, config.GRID_COLS - lv.img_cols, lv.img_cols), lv.end, lv.size)
