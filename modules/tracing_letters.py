"""Modul contoh 1: menebalkan huruf A-Z (huruf besar + kecil) dengan gambar dan kata awal."""
from __future__ import annotations

import string
import unicodedata
from typing import List, Set, Tuple

from core.i18n import Translator, lookup
from core.layout import Page
from modules.base import BaseModule


def _initial(word: str) -> str:
    """Huruf pertama tanpa aksen, huruf besar (Éléphant -> E)."""
    first = unicodedata.normalize("NFD", word.strip())[:1]
    return first.upper()


class TracingLetters(BaseModule):
    id = "tracing_letters"
    title_key = "tracing_letters.title"
    age_range = (4, 6)
    category = "literacy"
    pages = 7
    series = "TRC"
    sequences = {"letter": ("A", "Z")}      # QC: A..Z berurutan, tanpa lompat/duplikat

    PER_PAGE = 4
    LETTERS = string.ascii_uppercase

    def _img(self, lang: str, letter: str) -> str:
        return lookup(lang, f"tracing_letters.img.{letter}")

    def images(self, lang: str) -> Set[str]:
        return {self._img(lang, L) for L in self.LETTERS} | {"icon_pencil"}

    def render(self, page_index: int, ctx: Page) -> None:
        ctx.draw_instruction(ctx.t("tracing_letters.instruction"), icon="icon_pencil")
        start = page_index * self.PER_PAGE
        for i, L in enumerate(self.LETTERS[start:start + self.PER_PAGE]):
            band = ctx.band(i, self.PER_PAGE, gap=4.0)
            left, right = ctx.cell(band, 0, 3), ctx.cell(band, 3, 9)
            pic, label = left.take_top(left.h - 9.0)
            ctx.draw_box(pic)
            ctx.draw_image_slot(pic, self._img(ctx.lang, L), "L")
            ctx.draw_text(label, ctx.t(f"tracing_letters.word.{L}"), bold=True, align="center")
            upper, lower = right.split_rows(2)
            ctx.draw_trace_line(upper, L, group="letter", value=L)
            ctx.draw_trace_line(lower, L.lower(), group="letter_lower", value=L.lower())

    def qc_extra(self, lang: str, tr: Translator) -> List[Tuple[str, str]]:
        """Kata contoh harus diawali huruf yang dilatih (berbeda tiap bahasa)."""
        out = []
        for L in self.LETTERS:
            word = tr.strings.get(f"tracing_letters.word.{L}", "")
            if _initial(word) != L:
                out.append(("FAIL", f"kata '{word}' tidak diawali huruf {L}"))
        return out
