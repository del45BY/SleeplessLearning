"""Pra-menulis: menebalkan zigzag (perubahan arah pensil bertahap). 10 halaman, mudah -> sulit.

Dua jenis halaman (1 aktivitas per halaman):
  * "rows"    : zigzag HORIZONTAL (gunung, pagar bergerigi, sungai berliku): [gambar awal] zigzag [gambar tujuan]
  * "columns" : zigzag VERTIKAL (kilat, jalan berliku): gambar di atas, garis turun ke bawah.
Kesulitan naik: belokan sedikit -> banyak, garis putus -> titik-titik -> hanya lingkaran di tiap belokan
(anak menghubungkan sendiri), bentuk tajam -> melengkung mulus.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set

import config
from core.layout import Page
from modules.base import BaseModule


@dataclass(frozen=True)
class Level:
    theme: str                      # kunci i18n: zigzag_lines.instruction.<theme>
    kind: str                       # "rows" | "columns"
    style: str                      # dashed | dotted | points
    n: int                          # jumlah baris (rows) atau kolom (columns)
    segments: int                   # jumlah ruas/belokan (rows: genap agar berakhir di bawah)
    size: str                       # token ukuran slot gambar: S | M | L
    smooth: bool = False
    amp: float = 1.0
    # rows
    img_cols: int = 3
    start: Optional[str] = None
    end: Optional[str] = None
    # columns
    span: int = 12
    length: str = "L"               # token panjang (config.VLINE_LENGTHS)
    top: Optional[str] = None
    bottom: Optional[str] = None
    center_ends: bool = False


LEVELS = (
    Level("mountain_one",  "rows",    "dashed", 3, 2, "L", img_cols=3, start="hiker", end="flag"),
    Level("mountain_two",  "rows",    "dashed", 3, 4, "L", img_cols=3, start="hiker", end="flag"),
    Level("mountain_many", "rows",    "dashed", 4, 6, "M", img_cols=2, start="hiker", end="flag"),
    Level("lightning",     "columns", "dashed", 3, 4, "L", amp=0.45, center_ends=True, top="storm_cloud"),
    Level("fence",         "rows",    "dashed", 4, 8, "M", amp=0.6, img_cols=2, start="cat", end="fish"),
    Level("road",          "columns", "dashed", 2, 4, "M", smooth=True, amp=0.7, span=8, center_ends=True,
          top="car_side", bottom="house"),
    Level("lightning_dots", "columns", "dotted", 4, 6, "M", amp=0.5, center_ends=True, top="storm_cloud"),
    Level("river",         "rows",    "dotted", 4, 6, "M", smooth=True, amp=0.8, img_cols=2, start="boat", end="island"),
    Level("lightning_draw", "columns", "points", 3, 6, "M", amp=0.5, center_ends=True, top="storm_cloud"),
    Level("mountain_draw", "rows",    "points", 5, 8, "S", img_cols=2, start="hiker", end="flag"),
)


class ZigzagLines(BaseModule):
    id = "zigzag_lines"
    title_key = "zigzag_lines.title"
    age_range = (4, 5)
    category = "pre_writing"
    pages = len(LEVELS)
    series = "ZIG"

    def images(self, lang: str) -> Set[str]:
        out = {"icon_pencil"}
        for lv in LEVELS:
            out |= {i for i in (lv.start, lv.end, lv.top, lv.bottom) if i}
        return out

    def render(self, page_index: int, ctx: Page) -> None:
        lv = LEVELS[page_index]
        ctx.draw_instruction(ctx.t(f"zigzag_lines.instruction.{lv.theme}"), icon="icon_pencil")
        if lv.kind == "rows":
            self._rows(ctx, lv)
        else:
            self._columns(ctx, lv)

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
            left, right = ctx.cell(row, 0, lv.img_cols), ctx.cell(row, config.GRID_COLS - lv.img_cols, lv.img_cols)
            mid = ctx.cell(row, lv.img_cols, config.GRID_COLS - 2 * lv.img_cols)
            ground = img + pad                                   # zigzag mulai & berakhir di bawah -> gambar rata bawah
            ctx.draw_image_slot(left.take_top(row.h - ground)[1], lv.start, lv.size)
            ctx.draw_image_slot(right.take_top(row.h - ground)[1], lv.end, lv.size)
            ctx.draw_zigzag_line(mid, lv.segments, "horizontal", lv.style, smooth=lv.smooth, amp=lv.amp,
                                 group="line", value=str(i + 1))

    def _columns(self, ctx: Page, lv: Level) -> None:
        pad = config.VLINE_IMG_PAD_MM
        top_h = config.IMG_SIZES[lv.size] + pad if lv.top else 0.0
        bot_h = config.IMG_SIZES[lv.size] + pad if lv.bottom else 0.0
        length = config.VLINE_LENGTHS[lv.length]
        region = self._centered(ctx, top_h + length + bot_h)
        top_r, rest = region.take_top(top_h)
        lines_r, bot_r = rest.take_top(length)
        c0 = (config.GRID_COLS - lv.span) // 2
        if lv.top:
            for cell in ctx.cell(top_r, c0, lv.span).split_cols(lv.n):
                ctx.draw_image_slot(cell, lv.top, lv.size)
        for i, cell in enumerate(ctx.cell(lines_r, c0, lv.span).split_cols(lv.n)):
            ctx.draw_zigzag_line(cell, lv.segments, "vertical", lv.style, smooth=lv.smooth, amp=lv.amp,
                                 center_ends=lv.center_ends, group="line", value=str(i + 1))
        if lv.bottom:
            for cell in ctx.cell(bot_r, c0, lv.span).split_cols(lv.n):
                ctx.draw_image_slot(cell, lv.bottom, lv.size)
