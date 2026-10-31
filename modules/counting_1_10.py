"""Modul contoh 2: berhitung 1-10 (hitung gambar + tebalkan angka)."""
from __future__ import annotations

from typing import Set

from core.layout import Page
from modules.base import BaseModule


class Counting1To10(BaseModule):
    id = "counting_1_10"
    title_key = "counting_1_10.title"
    age_range = (3, 5)
    category = "math"
    pages = 2
    series = "CNT"
    sequences = {"number": (1, 10)}

    PER_PAGE = 5
    POOL = ["apple", "fish", "star", "ball", "flower", "car", "duck", "heart", "sun", "cat"]

    def images(self, lang: str) -> Set[str]:
        return set(self.POOL) | {"icon_count"}

    def render(self, page_index: int, ctx: Page) -> None:
        ctx.draw_instruction(ctx.t("counting_1_10.instruction"), icon="icon_count")
        objects = ctx.order(self.POOL)          # urutan tetap; diacak deterministik jika --seed
        for i in range(self.PER_PAGE):
            n = page_index * self.PER_PAGE + i + 1
            band = ctx.band(i, self.PER_PAGE, gap=3.0)
            ctx.draw_box(band)
            inner = band.inset(2.0)
            left, right = ctx.cell(inner, 0, 5), ctx.cell(inner, 5, 7)
            trace, word = left.take_top(22.0)
            ctx.draw_trace_line(trace, str(n), group="number", value=str(n))
            ctx.draw_text(word, ctx.t(f"counting_1_10.num.{n}"), bold=True, align="center")
            for slot in right.grid(2, 5, gap=1.0)[:n]:
                ctx.draw_image_slot(slot, objects[n - 1], "S")
