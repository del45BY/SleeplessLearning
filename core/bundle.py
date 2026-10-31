"""Gabungkan beberapa modul menjadi satu PDF (cover + daftar isi opsional)."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import config
from core import registry
from core.layout import Page, Rect
from core.renderer import FrontMatter, RenderResult, Renderer, TOC_ROWS_PER_PAGE
from modules.base import BaseModule


def draw_cover(page: Page, front: Optional[FrontMatter], modules: Sequence[BaseModule]) -> None:
    """Halaman cover: judul, rentang usia, gambar, nama bahasa."""
    title = (front.title if front and front.title else None) or page.t("bundle.default_title")
    a, b = min(m.age_range[0] for m in modules), max(m.age_range[1] for m in modules)
    top = page.band(0, 3, gap=6)
    t_rect, s_rect = top.split_rows(2)
    page.draw_text(t_rect, title, size=config.FONT_COVER_TITLE, bold=True,
                   align="center", color="accent", kind="cover_title")
    page.draw_text(s_rect, page.t("bundle.cover_subtitle", age_min=a, age_max=b), size=config.FONT_COVER_SUB,
                   align="center", color="muted", kind="cover_subtitle")
    mid = page.band(1, 3, gap=6)
    page.draw_image_slot(page.cell(mid, 0, 12), "cover_art", "XL")
    low = page.band(2, 3, gap=6)
    page.draw_text(low.take_top(10)[0], config.LANG_NAMES.get(page.lang, page.lang),
                   size=config.FONT_LABEL, align="center", color="muted", kind="cover_lang")


def draw_toc(page: Page, modules: Sequence[BaseModule], start: Dict[str, int], toc_index: int) -> None:
    """Daftar isi dengan nomor halaman berurutan (dipaginasi per TOC_ROWS_PER_PAGE)."""
    chunk = modules[toc_index * TOC_ROWS_PER_PAGE:(toc_index + 1) * TOC_ROWS_PER_PAGE]
    for i, m in enumerate(chunk):
        band = page.band(i, TOC_ROWS_PER_PAGE, gap=2.0)
        page.draw_text(page.cell(band, 0, 10), page.t(m.title_key), size=config.FONT_LABEL, kind="toc_title")
        page.draw_text(page.cell(band, 10, 2), page.t("bundle.page_ref", n=start[m.id]),
                       size=config.FONT_LABEL, align="right", color="muted", kind="toc_page")


def default_name(ids: Sequence[str]) -> str:
    name = "-".join(ids)
    return name if len(name) <= 60 else f"{len(ids)}modules-{ids[0]}"


def build_bundle(module_ids: Sequence[str], lang: str, mode: str, *, name: Optional[str] = None,
                 title: Optional[str] = None, cover: bool = True, toc: bool = True,
                 seed: Optional[int] = None, out_dir: Optional[Path] = None) -> RenderResult:
    """Render beberapa modul menjadi 1 PDF: output/{lang}/{mode}/bundle_<name>.pdf."""
    mods: List[BaseModule] = [registry.get_module(i) for i in module_ids]
    name = name or default_name(list(module_ids))
    path = Path(out_dir or config.OUTPUT_DIR) / lang / mode / f"bundle_{name}.pdf"
    r = Renderer(lang, mode, seed)
    return r.render(mods, path, scope=f"bundle:{name}", front=FrontMatter(title, cover, toc))
