"""Pra-menulis: menebalkan garis tegak (atas -> bawah) pada gambar. 10 halaman, mudah -> sulit.

Kenaikan tingkat kesulitan: garis jarang & sedikit (3) -> rapat & banyak (8); garis putus ->
titik-titik -> hanya titik awal/akhir (anak menarik sendiri). 1 aktivitas per halaman, instruksi 1 baris.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set

import config
from core.layout import Page
from modules.base import BaseModule


@dataclass(frozen=True)
class Level:
    theme: str                      # kunci i18n instruksi: vertical_lines.instruction.<theme>
    n: int                          # jumlah garis
    span: int                       # lebar area (kolom grid, genap): kecil = garis rapat
    length: str                     # token panjang: S | M | L  (config.VLINE_LENGTHS)
    style: str                      # dashed | dotted | points
    top: Optional[str] = None       # PNG di atas garis
    top_size: str = "M"
    top_each: bool = True           # True: 1 gambar per garis; False: 1 gambar untuk semua
    bottom: Optional[str] = None    # PNG di bawah garis (1 per garis)
    bottom_size: str = "S"


LEVELS = (
    Level("rain",       3,  6, "M", "dashed", top="cloud", top_size="XL", top_each=False),
    Level("balloon",    3, 12, "L", "dashed", top="balloon", top_size="L"),
    Level("candle",     4,  8, "S", "dashed", top="flame", top_size="S", bottom="cupcake", bottom_size="M"),
    Level("fence",      5, 12, "M", "dashed", top="picket_tip", top_size="M", bottom="grass_tuft"),
    Level("flower",     5, 12, "M", "dashed", top="flower_head", top_size="L"),
    Level("tree",       4, 12, "L", "dashed", top="tree_crown", top_size="L"),
    Level("lollipop",   6, 12, "L", "dotted", top="lollipop", top_size="M"),
    Level("lamp",       5, 12, "M", "dotted", top="lamp_head", top_size="L"),
    Level("cloud_draw", 6, 12, "M", "points", top="cloud", top_size="M"),
    Level("icicle",     8, 12, "M", "points", top="icicle", top_size="S"),
)


class VerticalLines(BaseModule):
    id = "vertical_lines"
    title_key = "vertical_lines.title"
    age_range = (4, 5)
    category = "pre_writing"
    pages = len(LEVELS)
    series = "VLN"

    def images(self, lang: str) -> Set[str]:
        out = {"icon_pencil"}
        for lv in LEVELS:
            out |= {i for i in (lv.top, lv.bottom) if i}
        return out

    def render(self, page_index: int, ctx: Page) -> None:
        lv = LEVELS[page_index]
        ctx.draw_instruction(ctx.t(f"vertical_lines.instruction.{lv.theme}"), icon="icon_pencil")
        pad = config.VLINE_IMG_PAD_MM
        top_h = config.IMG_SIZES[lv.top_size] + pad if lv.top else 0.0
        bot_h = config.IMG_SIZES[lv.bottom_size] + pad if lv.bottom else 0.0
        length = config.VLINE_LENGTHS[lv.length]
        area = ctx.band(0, 1)
        total = top_h + length + bot_h                       # komposisi diletakkan di tengah vertikal
        region = area.take_top((area.h - total) / 2)[1].take_top(total)[0]
        top_r, rest = region.take_top(top_h)
        lines_r, bot_r = rest.take_top(length)
        c0 = (config.GRID_COLS - lv.span) // 2
        if lv.top:
            if lv.top_each:
                for cell in ctx.cell(top_r, c0, lv.span).split_cols(lv.n):
                    ctx.draw_image_slot(cell, lv.top, lv.top_size)
            else:
                ctx.draw_image_slot(ctx.cell(top_r, c0, lv.span), lv.top, lv.top_size)
        for i, cell in enumerate(ctx.cell(lines_r, c0, lv.span).split_cols(lv.n)):
            ctx.draw_vertical_line(cell, lv.style, group="line", value=str(i + 1))
        if lv.bottom:
            for cell in ctx.cell(bot_r, c0, lv.span).split_cols(lv.n):
                ctx.draw_image_slot(cell, lv.bottom, lv.bottom_size)

