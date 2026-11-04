"""Pra-menulis: menebalkan garis bergelombang (gerakan berulang yang halus dan berirama). 10 halaman.

Memakai helper yang sudah ada: ctx.draw_zigzag_line(..., smooth=True, center_ends=True) = gelombang sinus mulus.
Dua jenis halaman (1 aktivitas per halaman):
  * "rows"    : gelombang HORIZONTAL (laut, ular): [gambar awal] ~~~~ [gambar tujuan]
  * "columns" : gelombang VERTIKAL (sungai, rambut): gambar di atas, gelombang turun ke bawah.
Kesulitan naik: gelombang besar & sedikit -> kecil & banyak, garis putus -> titik-titik -> hanya lingkaran
di puncak/lembah (anak menghubungkan sendiri).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set

import config
from core.layout import Page
from modules.base import BaseModule


@dataclass(frozen=True)
class Level:
    theme: str                      # kunci i18n: wavy_lines.instruction.<theme>
    kind: str                       # "rows" | "columns"
    style: str                      # dashed | dotted | points
    n: int                          # jumlah baris (rows) atau kolom (columns)
    segments: int                   # jumlah setengah gelombang (naik/turun)
    size: str                       # token ukuran slot gambar: S | M | L
    amp: float = 0.5                # simpangan relatif terhadap sel
    # rows
    img_cols: int = 3
    start: Optional[str] = None
    end: Optional[str] = None
    # columns
    span: int = 12
    length: str = "L"               # token panjang (config.VLINE_LENGTHS)
    top: Optional[str] = None
    bottom: Optional[str] = None


LEVELS = (
    Level("sea_one",    "rows",    "dashed", 3, 4, "L", amp=0.5, img_cols=3, start="fish", end="shell"),
    Level("sea_two",    "rows",    "dashed", 3, 6, "L", amp=0.5, img_cols=3, start="fish", end="shell"),
    Level("snake",      "rows",    "dashed", 4, 6, "M", amp=0.6, img_cols=2, start="snake", end="apple"),
    Level("river",      "columns", "dashed", 2, 6, "M", amp=0.6, span=8, top="mountain", bottom="lake"),
    Level("hair",       "columns", "dashed", 4, 6, "M", amp=0.4, top="bow"),
    Level("sea_dots",   "rows",    "dotted", 4, 8, "M", amp=0.45, img_cols=2, start="fish", end="shell"),
    Level("snake_dots", "rows",    "dotted", 4, 8, "M", amp=0.6, img_cols=2, start="snake", end="apple"),
    Level("hair_dots",  "columns", "dotted", 5, 8, "M", amp=0.35, top="bow"),
    Level("sea_draw",   "rows",    "points", 5, 8, "S", amp=0.45, img_cols=2, start="fish", end="shell"),
    Level("river_draw", "columns", "points", 3, 8, "M", amp=0.5, top="mountain", bottom="lake"),
)


class WavyLines(BaseModule):
    id = "wavy_lines"
    title_key = "wavy_lines.title"
    age_range = (4, 5)
    category = "pre_writing"
    pages = len(LEVELS)
    series = "WAV"

    def images(self, lang: str) -> Set[str]:
        out = {"icon_pencil"}
        for lv in LEVELS:
            out |= {i for i in (lv.start, lv.end, lv.top, lv.bottom) if i}
        return out

    def render(self, page_index: int, ctx: Page) -> None:
        lv = LEVELS[page_index]
        ctx.draw_instruction(ctx.t(f"wavy_lines.instruction.{lv.theme}"), icon="icon_pencil")
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
        cell_h, gap = config.DLINE_ROW_H_MM[lv.size], config.HLINE_ROW_GAP_MM
        region = self._centered(ctx, lv.n * cell_h + (lv.n - 1) * gap)
        for i, row in enumerate(region.split_rows(lv.n, gap)):
            # gelombang mulai & berakhir di garis tengah baris -> gambar ujung diletakkan di tengah baris
            ctx.draw_image_slot(ctx.cell(row, 0, lv.img_cols), lv.start, lv.size)
            ctx.draw_zigzag_line(ctx.cell(row, lv.img_cols, config.GRID_COLS - 2 * lv.img_cols), lv.segments,
                                 "horizontal", lv.style, smooth=True, center_ends=True, amp=lv.amp,
                                 group="wave", value=str(i + 1))
            ctx.draw_image_slot(ctx.cell(row, config.GRID_COLS - lv.img_cols, lv.img_cols), lv.end, lv.size)

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
            ctx.draw_zigzag_line(cell, lv.segments, "vertical", lv.style, smooth=True, center_ends=True,
                                 amp=lv.amp, group="wave", value=str(i + 1))
        if lv.bottom:
            for cell in ctx.cell(bot_r, c0, lv.span).split_cols(lv.n):
                ctx.draw_image_slot(cell, lv.bottom, lv.size)
