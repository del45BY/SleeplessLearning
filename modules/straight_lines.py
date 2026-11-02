"""Tracing Straight Lines: Roads, Rain & Rockets. Pra-menulis / motorik halus, usia 4-5, 6 halaman.

Urutan mudah -> sulit: mendatar, tegak, miring naik, miring turun, zigzag, campuran.
Garis lurus digambar lewat draw_trace_line memakai glyph garis dari i18n (kunci "<id>.line.*"),
jadi tidak ada koordinat atau teks hardcode di modul ini.
"""
from __future__ import annotations

from typing import List, Set, Tuple

import config
from core.i18n import Translator
from core.layout import Page
from modules.base import BaseModule

# (kunci glyph di i18n, gambar awal, gambar akhir)
_ROAD = ("h", "car", "flag_finish")
_RAIN = ("v", "cloud", "umbrella")
_ROCKET = ("up", "rocket", "star")
_RAMP = ("down", "ball", "flag_finish")
_ZIGZAG = ("zig", "bus", "flag_finish")

LINES_PER_PAGE = 4


class StraightLines(BaseModule):
    # --- metadata ---------------------------------------------------------------
    id = "straight_lines"
    title_key = "straight_lines.title"
    age_range = (4, 5)
    category = "prewriting"
    pages = 6
    series = "LIN"
    sequences: dict = {}

    # satu jenis garis per halaman, kecuali halaman 6 (campuran)
    PAGES: List[List[Tuple[str, str, str]]] = [
        [_ROAD] * LINES_PER_PAGE,
        [_RAIN] * LINES_PER_PAGE,
        [_ROCKET] * LINES_PER_PAGE,
        [_RAMP] * LINES_PER_PAGE,
        [_ZIGZAG] * LINES_PER_PAGE,
        [_ROAD, _RAIN, _ROCKET, _RAMP],
    ]

    # --- kebutuhan gambar ---------------------------------------------------------
    def images(self, lang: str) -> Set[str]:
        used = {"icon_pencil"}
        for page in self.PAGES:
            for _, start, finish in page:
                used |= {start, finish}
        return used

    # --- render satu halaman --------------------------------------------------------
    def render(self, page_index: int, ctx: Page) -> None:
        ctx.draw_instruction(ctx.t("straight_lines.instruction"), icon="icon_pencil")  # WAJIB, sekali

        head, body = ctx.content.take_top(config.HEADER_H)
        ctx.draw_text(head, ctx.t(f"straight_lines.page.{page_index + 1}"), bold=True)

        rows = body.split_rows(LINES_PER_PAGE, gap=config.TRACE_GAP_MM)
        for row, (line_key, start_img, finish_img) in zip(rows, self.PAGES[page_index]):
            line_area, label_area = row.take_top(config.IMG_SIZES["L"])
            # kiri: gambar awal + label; tengah: garis tracing; kanan: gambar akhir + label
            ctx.draw_image_slot(ctx.cell(line_area, 0, 2), start_img, "M")
            ctx.draw_trace_line(ctx.cell(line_area, 2, 8), ctx.t(f"straight_lines.line.{line_key}"))
            ctx.draw_image_slot(ctx.cell(line_area, 10, 2), finish_img, "M")
            ctx.draw_text(ctx.cell(label_area, 0, 2), ctx.t("straight_lines.start"),
                          size=config.FONT_BODY, align="center")
            ctx.draw_text(ctx.cell(label_area, 10, 2), ctx.t("straight_lines.finish"),
                          size=config.FONT_BODY, align="center")

    # --- cek khusus modul ---------------------------------------------------------
    def qc_extra(self, lang: str, tr: Translator) -> List[Tuple[str, str]]:
        issues: List[Tuple[str, str]] = []
        if len(self.PAGES) != self.pages:
            issues.append(("FAIL", f"jumlah definisi halaman {len(self.PAGES)} != pages={self.pages}"))
        for key in ("h", "v", "up", "down", "zig"):
            if not tr.t(f"straight_lines.line.{key}").strip():
                issues.append(("FAIL", f"glyph garis '{key}' kosong"))
        return issues
