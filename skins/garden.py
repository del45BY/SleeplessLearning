"""Skin 'garden': bingkai daun, header berpita, latar titik lembut, badge instruksi berbentuk bunga.

PNG (assets/skins/garden/): leaf_corner (sudut), leaf_edge (ubin bingkai), flower_badge (badge instruksi).
Dekorasi hanya di margin/header/footer/sudut; area konten modul tidak disentuh.
"""
from __future__ import annotations

from typing import Set

import config
from core.layout import FONT_BOLD, Rect, text_width_mm
from skins.base import BaseSkin

_ROT = {"top": 0, "right": 90, "bottom": 180, "left": 270}


class GardenSkin(BaseSkin):
    name = "garden"
    description = "Bingkai daun, header berpita, latar titik lembut, badge instruksi bunga, footer bergelombang."

    def images(self) -> Set[str]:
        return {"leaf_corner", "leaf_edge", "flower_badge"}

    def draw_page_background(self, page) -> None:
        for strip in page.margin_strips(outer=config.SKIN_FRAME_INSET_MM + 1.5, inner=1.0):
            page.decor_dots(strip, color="decor_soft")          # mode bw: dihilangkan otomatis

    def draw_page_frame(self, page) -> None:
        i = config.SKIN_FRAME_INSET_MM
        page.decor_rect(Rect(i, i, config.PAGE_W_MM - 2 * i, config.PAGE_H_MM - 2 * i), color="decor_1",
                        radius=4.0, hollow=True)
        for side, r in self.frame_tiles():
            page.decor_image(r, "leaf_edge", rotate=_ROT[side])

    def draw_corner_decor(self, page) -> None:
        self.corner_images(page, "leaf_corner")

    def draw_header(self, page) -> None:
        hd, title = page.header_rect, page.spec.title
        tw = text_width_mm(title, FONT_BOLD, config.FONT_TITLE)
        ribbon = Rect(hd.x, hd.y, tw + 10.0, hd.h)
        page.decor_rect(ribbon, color="decor_1", fill="ribbon_fill", radius=2.0, container=True, kind="decor_ribbon")
        page.draw_text(Rect(ribbon.x + 5.0, ribbon.y, tw + 0.2, ribbon.h), title, size=config.FONT_TITLE, bold=True,
                       color="accent", zone="system", kind="header_title")
        self.draw_progress_marker(page)
        page.decor_wave(Rect(hd.x, config.HEADER_TOP + config.HEADER_H, hd.w, 0.0), color="decor_1",
                        amp=0.7, period=7.0)

    def draw_progress_marker(self, page) -> None:
        self.progress_with_dots(page, "decor_1")

    def draw_reward_sticker_slot(self, page) -> None:
        self.sticker_circle(page, "decor_2")

    def draw_name_date_zone(self, page) -> None:
        self.boxed_name_date(page)

    def draw_instruction_badge(self, page, text: str, icon: str) -> None:
        self.badge_instruction(page, text, icon, "flower_badge")

    def draw_section_title(self, page, rect: Rect, text: str, size: float) -> None:
        r = 1.6                                    # bullet bulat di dalam rect milik modul (dianggap konten)
        page.decor_circle(rect.x + r, rect.cy, r, color="decor_2", fill="decor_2", zone="content", kind="decor_bullet")
        page.draw_text(Rect(rect.x + 2 * r + 2.0, rect.y, rect.w - 2 * r - 2.0, rect.h), text, size=size,
                       bold=True, color="accent", kind="section_title")

    def draw_footer(self, page) -> None:
        page.decor_wave(Rect(config.MARGIN_MM, config.FOOTER_TOP, config.PAGE_W_MM - 2 * config.MARGIN_MM, 0.0),
                        color="decor_1", amp=0.7, period=7.0, line_w=config.LINE_THIN_PT)
        self.footer_texts(page)
