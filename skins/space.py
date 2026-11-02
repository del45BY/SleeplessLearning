"""Skin 'space': bingkai bintang, header planet, latar bintang tipis, badge instruksi berbentuk roket.

PNG (assets/skins/space/): star_corner (sudut), star_edge (ubin bingkai), rocket_badge, planet (header).
Pola bintang latar memakai seed TETAP -> sama di setiap halaman satu seri.
"""
from __future__ import annotations

import random
from typing import List, Set, Tuple

import config
from core.layout import FONT_BOLD, Rect, text_width_mm
from skins.base import BaseSkin


class SpaceSkin(BaseSkin):
    name = "space"
    description = "Bingkai bintang putus-putus, header planet, latar bintang tipis, badge instruksi roket."

    def images(self) -> Set[str]:
        return {"star_corner", "star_edge", "rocket_badge", "planet"}

    def draw_page_background(self, page) -> None:
        for idx, strip in enumerate(page.margin_strips(outer=config.SKIN_FRAME_INSET_MM + 1.5, inner=1.0)):
            rng = random.Random(f"space-bg-{idx}")                 # seed tetap: pola sama di semua halaman
            n = int(strip.w * strip.h / 22)
            pts: List[Tuple[float, float, float]] = [
                (strip.x + rng.random() * strip.w, strip.y + rng.random() * strip.h, 0.2 + rng.random() * 0.3)
                for _ in range(n)]
            page.decor_dots(strip, color="decor_soft", points=pts)   # mode bw: dihilangkan otomatis

    def draw_page_frame(self, page) -> None:
        i = config.SKIN_FRAME_INSET_MM
        page.decor_rect(Rect(i, i, config.PAGE_W_MM - 2 * i, config.PAGE_H_MM - 2 * i), color="decor_1",
                        radius=4.0, dashed=True, hollow=True)
        for _, r in self.frame_tiles():
            page.decor_image(r, "star_edge")

    def draw_corner_decor(self, page) -> None:
        self.corner_images(page, "star_corner")

    def draw_header(self, page) -> None:
        hd, title = page.header_rect, page.spec.title
        p = config.SKIN_HEADER_ICON_MM
        page.decor_image(Rect(hd.x, hd.y, p, p), "planet")
        tw = text_width_mm(title, FONT_BOLD, config.FONT_TITLE)
        page.draw_text(Rect(hd.x + p + 3.0, hd.y, tw + 0.2, hd.h), title, size=config.FONT_TITLE, bold=True,
                       color="accent", zone="system", kind="header_title")
        self.draw_progress_marker(page)
        page.decor_line(hd.x, config.HEADER_TOP + config.HEADER_H, hd.right, config.HEADER_TOP + config.HEADER_H,
                        color="decor_1", line_w=1.6, dash=(0.01, 4.2), round_cap=True)

    def draw_progress_marker(self, page) -> None:
        self.progress_with_dots(page, "decor_1")

    def draw_reward_sticker_slot(self, page) -> None:
        self.sticker_circle(page, "decor_2")

    def draw_name_date_zone(self, page) -> None:
        self.boxed_name_date(page, dashed=True)

    def draw_instruction_badge(self, page, text: str, icon: str) -> None:
        self.badge_instruction(page, text, icon, "rocket_badge")

    def draw_section_title(self, page, rect: Rect, text: str, size: float) -> None:
        r = 1.6
        page.decor_circle(rect.x + r, rect.cy, r, color="decor_2", fill="decor_2", zone="content", kind="decor_bullet")
        page.draw_text(Rect(rect.x + 2 * r + 2.0, rect.y, rect.w - 2 * r - 2.0, rect.h), text, size=size,
                       bold=True, color="accent", kind="section_title")

    def draw_footer(self, page) -> None:
        y = config.FOOTER_TOP
        page.decor_line(config.MARGIN_MM, y, config.PAGE_W_MM - config.MARGIN_MM, y, color="decor_1",
                        line_w=1.4, dash=(0.01, 4.2), round_cap=True)
        self.footer_texts(page)
