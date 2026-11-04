"""Pra-menulis: menebalkan garis lengkung (kelenturan pergelangan untuk huruf melengkung). 10 halaman.

Tiga jenis halaman (1 aktivitas per halaman):
  * "rows"     : [gambar awal] lengkung [gambar tujuan]  (pelangi, tali, bukit-bukit ulat)
  * "units"    : grid unit dengan gambar di atas/bawah (senyum di wajah, kail pancing, permen spiral)
  * "umbrella" : payung = busur (kanopi) + kait J (gagang) yang bertemu di tengah
Kesulitan naik: 1 lengkung -> 3 lengkung bersarang, busur -> senyum -> tali -> kait -> spiral,
garis putus -> titik-titik -> hanya lingkaran di awal/puncak/akhir (anak menarik sendiri).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set

import config
from core.layout import Page, Rect
from modules.base import BaseModule

# tinggi sel kurva untuk jenis "units" (token config; XL = panjang garis baku L)
CURVE_H = {**config.DLINE_SHAPE_H_MM, "XL": config.VLINE_LENGTHS["L"]}
# proporsi payung terhadap lebar unit (kanopi) dan lebar gagang terhadap kanopi
UMBRELLA_CANOPY_W, UMBRELLA_HANDLE_W = 0.8, 0.5
# proporsi area senyum di dalam gambar wajah (x, y, lebar, tinggi relatif terhadap slot)
FACE_MOUTH = (0.2, 0.58, 0.6, 0.3)


@dataclass(frozen=True)
class Level:
    theme: str                        # kunci i18n: curved_lines.instruction.<theme>
    kind: str                         # "rows" | "units" | "umbrella"
    shape: str                        # arch | smile | sag | hook | spiral
    style: str                        # dashed | dotted | points
    size: str                         # token ukuran slot gambar
    rings: int = 1                    # lengkung bersarang (pelangi)
    depth: float = 1.0
    # rows
    n: int = 3
    img_cols: int = 3
    start: Optional[str] = None
    end: Optional[str] = None
    align: str = "bottom"             # gambar ujung rata "bottom" | "top"
    parts: int = 1                    # jumlah lengkung berjajar dalam satu baris (bukit-bukit)
    # units / umbrella
    per_row: int = 2
    rows: int = 2
    top: Optional[str] = None
    bottom: Optional[str] = None
    line_h: str = "M"
    overlay: bool = False             # lengkung digambar DI DALAM gambar latar (wajah)


LEVELS = (
    Level("rainbow_one",   "rows", "arch",  "dashed", "L", n=3, img_cols=3, start="cloud", end="cloud"),
    Level("rainbow_three", "rows", "arch",  "dashed", "L", rings=3, n=3, img_cols=3, start="cloud", end="cloud"),
    Level("smile",         "units", "smile", "dashed", "XL", per_row=2, rows=2, top="face_blank", overlay=True),
    Level("rope",          "rows", "sag",   "dashed", "M", depth=0.6, n=4, img_cols=2, start="pole_left",
          end="pole_right", align="top"),
    Level("umbrella",      "umbrella", "arch", "dashed", "S", per_row=2, rows=2, top="raindrops"),
    Level("caterpillar",   "rows", "arch",  "dotted", "M", depth=0.6, n=4, img_cols=2, start="caterpillar",
          end="leaf", parts=4),
    Level("hook",          "units", "hook", "dotted", "M", per_row=4, rows=1, top="boat", bottom="fish", line_h="XL"),
    Level("lollipop",      "units", "spiral", "dotted", "S", per_row=3, rows=2, bottom="lollipop_stick", line_h="M"),
    Level("rainbow_draw",  "rows", "arch",  "points", "L", rings=3, n=3, img_cols=3, start="cloud", end="cloud"),
    Level("umbrella_draw", "umbrella", "arch", "points", "S", per_row=2, rows=2, top="raindrops"),
)


class CurvedLines(BaseModule):
    id = "curved_lines"
    title_key = "curved_lines.title"
    age_range = (4, 5)
    category = "pre_writing"
    pages = len(LEVELS)
    series = "CRV"

    def images(self, lang: str) -> Set[str]:
        out = {"icon_pencil"}
        for lv in LEVELS:
            out |= {i for i in (lv.start, lv.end, lv.top, lv.bottom) if i}
        return out

    def render(self, page_index: int, ctx: Page) -> None:
        lv = LEVELS[page_index]
        ctx.draw_instruction(ctx.t(f"curved_lines.instruction.{lv.theme}"), icon="icon_pencil")
        {"rows": self._rows, "units": self._units, "umbrella": self._umbrella}[lv.kind](ctx, lv)

    @staticmethod
    def _centered(ctx: Page, total: float):
        """Blok setinggi `total` di tengah vertikal area konten."""
        area = ctx.band(0, 1)
        return area.take_top((area.h - total) / 2)[1].take_top(total)[0]

    def _rows(self, ctx: Page, lv: Level) -> None:
        img, pad = config.IMG_SIZES[lv.size], config.VLINE_IMG_PAD_MM
        cell_h, gap = config.DLINE_ROW_H_MM[lv.size], config.HLINE_ROW_GAP_MM
        region = self._centered(ctx, lv.n * cell_h + (lv.n - 1) * gap)
        k = 0
        for row in region.split_rows(lv.n, gap):
            left, right = ctx.cell(row, 0, lv.img_cols), ctx.cell(row, config.GRID_COLS - lv.img_cols, lv.img_cols)
            mid = ctx.cell(row, lv.img_cols, config.GRID_COLS - 2 * lv.img_cols)
            band = img + pad
            pick = (lambda c: c.take_top(row.h - band)[1]) if lv.align == "bottom" else (lambda c: c.take_top(band)[0])
            ctx.draw_image_slot(pick(left), lv.start, lv.size)
            ctx.draw_image_slot(pick(right), lv.end, lv.size)
            for part in (mid.split_cols(lv.parts, 2.0) if lv.parts > 1 else [mid]):
                k += 1
                ctx.draw_curved_line(part, lv.shape, lv.style, rings=lv.rings, depth=lv.depth,
                                     group="curve", value=str(k))

    def _units(self, ctx: Page, lv: Level) -> None:
        img, pad, gap = config.IMG_SIZES[lv.size], config.VLINE_IMG_PAD_MM, config.HLINE_ROW_GAP_MM
        span = config.GRID_COLS // lv.per_row
        if lv.overlay:                                   # wajah: lengkung di dalam gambar (container)
            unit_h = img + pad
        else:
            unit_h = (img + pad if lv.top else 0) + CURVE_H[lv.line_h] + (img + pad if lv.bottom else 0)
        region = self._centered(ctx, lv.rows * unit_h + (lv.rows - 1) * gap)
        k = 0
        for row in region.split_rows(lv.rows, gap):
            for j in range(lv.per_row):
                k += 1
                unit = ctx.cell(row, j * span, span)
                if lv.overlay:
                    ctx.draw_image_slot(unit, lv.top, lv.size, container=True)
                    sq = unit.center_square(config.IMG_SIZES[lv.size])
                    fx, fy, fw, fh = FACE_MOUTH
                    mouth = Rect(sq.x + sq.w * fx, sq.y + sq.h * fy, sq.w * fw, sq.h * fh)
                    ctx.draw_curved_line(mouth, lv.shape, lv.style, depth=lv.depth, group="curve", value=str(k))
                    continue
                top_r, rest = unit.take_top(img + pad if lv.top else 0.0)
                line_r, bot_r = rest.take_top(CURVE_H[lv.line_h])
                if lv.top:
                    ctx.draw_image_slot(top_r, lv.top, lv.size)
                ctx.draw_curved_line(line_r, lv.shape, lv.style, rings=lv.rings, depth=lv.depth,
                                     group="curve", value=str(k))
                if lv.bottom:
                    ctx.draw_image_slot(bot_r, lv.bottom, lv.size)

    def _umbrella(self, ctx: Page, lv: Level) -> None:
        img, pad, gap = config.IMG_SIZES[lv.size], config.VLINE_IMG_PAD_MM, config.HLINE_ROW_GAP_MM
        canopy_h, handle_h = config.DLINE_SHAPE_H_MM["S"], config.DLINE_ROW_H_MM["S"]
        top_h = img + pad if lv.top else 0.0
        region = self._centered(ctx, lv.rows * (top_h + canopy_h + handle_h) + (lv.rows - 1) * gap)
        span, k = config.GRID_COLS // lv.per_row, 0
        for row in region.split_rows(lv.rows, gap):
            for j in range(lv.per_row):
                k += 1
                unit = ctx.cell(row, j * span, span)
                top_r, rest = unit.take_top(top_h)
                canopy_z, handle_z = rest.take_top(canopy_h)
                cw = canopy_z.w * UMBRELLA_CANOPY_W
                canopy = Rect(canopy_z.cx - cw / 2, canopy_z.y, cw, canopy_z.h)
                hw = cw * UMBRELLA_HANDLE_W
                handle = Rect(canopy_z.cx - hw / 2, handle_z.y, hw, handle_z.h)
                if lv.top:
                    ctx.draw_image_slot(top_r, lv.top, lv.size)
                ctx.draw_curved_line(canopy, "arch", lv.style, group="canopy", value=str(k))
                ctx.draw_curved_line(handle, "hook", lv.style, group="handle", value=str(k))
