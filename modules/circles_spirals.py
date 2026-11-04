"""Pra-menulis: menebalkan lingkaran dan spiral (bentuk bulat dan gerak memutar). 10 halaman.

Memakai ctx.draw_curved_line(shape="circle" | "spiral" | "spiral_out"). Dua jenis halaman (1 aktivitas/halaman):
  * "plain"  : grid bentuk (bola, matahari, sasaran, gelembung, cangkang keong) + gambar pendamping di bawah
  * "wheels" : badan kendaraan (mobil, sepeda) di atas + dua lingkaran (roda) tepat di bawahnya
Kesulitan naik: lingkaran tunggal -> bersarang (3 lingkaran) -> spiral ke dalam -> spiral dari pusat ke luar,
garis putus -> titik-titik -> hanya lingkaran penanda (anak menarik sendiri).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set

import config
from core.layout import Page
from modules.base import BaseModule


@dataclass(frozen=True)
class Level:
    theme: str                      # kunci i18n: circles_spirals.instruction.<theme>
    kind: str                       # "plain" | "wheels"
    shape: str                      # circle | spiral | spiral_out
    style: str                      # dashed | dotted | points
    per_row: int                    # jumlah unit per baris (membagi 12 kolom)
    rows: int                       # jumlah baris unit
    cell: str = "M"                 # token tinggi sel bentuk (config.DLINE_SHAPE_H_MM)
    rings: int = 1                  # lingkaran bersarang (circle)
    bottom: Optional[str] = None    # gambar pendamping di bawah (plain)
    bottom_size: str = "S"
    body: Optional[str] = None      # badan kendaraan di atas (wheels)
    body_size: str = "XL"
    pair: int = 2                   # jumlah roda (wheels)


LEVELS = (
    Level("ball",        "plain",  "circle",     "dashed", 2, 2, cell="L", bottom="grass_patch"),
    Level("sun",         "plain",  "circle",     "dashed", 3, 2, cell="M", bottom="house"),
    Level("wheel",       "wheels", "circle",     "dashed", 2, 2, body="car_body"),
    Level("target",      "plain",  "circle",     "dashed", 2, 2, cell="L", rings=3, bottom="target_stand"),
    Level("snail",       "plain",  "spiral",     "dashed", 3, 2, cell="M", bottom="snail_body", bottom_size="M"),
    Level("bubble",      "plain",  "circle",     "dotted", 4, 3, cell="S", bottom="fish"),
    Level("bike",        "wheels", "circle",     "dotted", 2, 2, body="bike_frame"),
    Level("snail_out",   "plain",  "spiral_out", "dotted", 3, 2, cell="M", bottom="snail_body", bottom_size="M"),
    Level("target_draw", "plain",  "circle",     "points", 2, 2, cell="L", rings=3, bottom="target_stand"),
    Level("snail_draw",  "plain",  "spiral_out", "points", 3, 2, cell="M", bottom="snail_body", bottom_size="M"),
)


class CirclesSpirals(BaseModule):
    id = "circles_spirals"
    title_key = "circles_spirals.title"
    age_range = (4, 5)
    category = "pre_writing"
    pages = len(LEVELS)
    series = "CIR"

    def images(self, lang: str) -> Set[str]:
        out = {"icon_pencil"}
        for lv in LEVELS:
            out |= {i for i in (lv.bottom, lv.body) if i}
        return out

    def render(self, page_index: int, ctx: Page) -> None:
        lv = LEVELS[page_index]
        ctx.draw_instruction(ctx.t(f"circles_spirals.instruction.{lv.theme}"), icon="icon_pencil")
        (self._wheels if lv.kind == "wheels" else self._plain)(ctx, lv)

    @staticmethod
    def _centered(ctx: Page, total: float):
        """Blok setinggi `total` di tengah vertikal area konten."""
        area = ctx.band(0, 1)
        return area.take_top((area.h - total) / 2)[1].take_top(total)[0]

    def _plain(self, ctx: Page, lv: Level) -> None:
        pad, gap = config.VLINE_IMG_PAD_MM, config.HLINE_ROW_GAP_MM
        cell_h = config.DLINE_SHAPE_H_MM[lv.cell]
        bot_h = config.IMG_SIZES[lv.bottom_size] + pad if lv.bottom else 0.0
        unit_h = cell_h + bot_h
        region = self._centered(ctx, lv.rows * unit_h + (lv.rows - 1) * gap)
        span, k = config.GRID_COLS // lv.per_row, 0
        for row in region.split_rows(lv.rows, gap):
            for j in range(lv.per_row):
                k += 1
                shape_r, bot_r = ctx.cell(row, j * span, span).take_top(cell_h)
                ctx.draw_curved_line(shape_r, lv.shape, lv.style, rings=lv.rings, group="shape", value=str(k))
                if lv.bottom:
                    ctx.draw_image_slot(bot_r, lv.bottom, lv.bottom_size)

    def _wheels(self, ctx: Page, lv: Level) -> None:
        pad, gap = config.VLINE_IMG_PAD_MM, config.HLINE_ROW_GAP_MM
        body_h = config.IMG_SIZES[lv.body_size] + pad
        wheel_h = config.DLINE_ROW_H_MM["S"]
        region = self._centered(ctx, lv.rows * (body_h + wheel_h) + (lv.rows - 1) * gap)
        span, k = config.GRID_COLS // lv.per_row, 0
        for row in region.split_rows(lv.rows, gap):
            for j in range(lv.per_row):
                unit = ctx.cell(row, j * span, span)
                body_r, wheel_z = unit.take_top(body_h)
                ctx.draw_image_slot(body_r, lv.body, lv.body_size)
                # roda berada tepat di bawah badan: lebar zona roda = 4 dari span kolom unit (~ lebar badan XL)
                for wheel in ctx.cell(wheel_z, 1, span - 2, cols=span).split_cols(lv.pair):
                    k += 1
                    ctx.draw_curved_line(wheel, "circle", lv.style, group="shape", value=str(k))
