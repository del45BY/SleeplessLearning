"""Render modul -> PDF Letter. Satu fungsi inti dipakai build, bundle, dan QC."""
from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Set

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas

import config
from core.assets import AssetResolver
from core.i18n import I18nEvent, Translator
from core.layout import Page, PageRecord, PageSpec, register_fonts
from core.theme import get_theme
from modules.base import BaseModule

log = logging.getLogger(__name__)
TOC_ROWS_PER_PAGE = 16


@dataclass
class FrontMatter:
    """Konfigurasi cover + daftar isi untuk bundle."""
    title: Optional[str] = None
    cover: bool = True
    toc: bool = True


@dataclass
class RenderResult:
    scope: str
    lang: str
    mode: str
    path: Path
    modules: List[BaseModule]
    expected_pages: int
    records: List[PageRecord] = field(default_factory=list)
    i18n_events: List[I18nEvent] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    extra_images: Set[str] = field(default_factory=set)


class Renderer:
    """Render satu atau beberapa modul ke satu PDF untuk (lang, mode)."""

    def __init__(self, lang: str, mode: str, seed: Optional[int] = None,
                 assets: Optional[AssetResolver] = None) -> None:
        register_fonts()
        self.lang, self.mode, self.seed = lang, mode, seed
        self.theme = get_theme(mode)
        self.assets = assets or AssetResolver()

    def render(self, modules: Sequence[BaseModule], out_path: Path, *, scope: Optional[str] = None,
               front: Optional[FrontMatter] = None) -> RenderResult:
        from core.bundle import draw_cover, draw_toc  # impor lambat: bundle memakai renderer
        tr = Translator(self.lang)
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        plan: List[tuple] = []
        if front and front.cover:
            plan.append(("cover", None, 0))
        n_toc = math.ceil(len(modules) / TOC_ROWS_PER_PAGE) if front and front.toc else 0
        plan += [("toc", None, i) for i in range(n_toc)]
        start: Dict[str, int] = {}
        for m in modules:
            start[m.id] = len(plan) + 1
            plan += [("module", m, p) for p in range(m.pages)]
        total = len(plan)

        res = RenderResult(scope or (modules[0].id if len(modules) == 1 else "bundle"), self.lang, self.mode,
                           out_path, list(modules), total)
        if front and front.cover:
            res.extra_images.add("cover_art")
        c = Canvas(str(out_path), pagesize=letter, invariant=1, pageCompression=1,
                   initialFontName="WS-Regular", initialFontSize=12)
        c.setAuthor(config.BRAND_NAME)
        c.setTitle(front.title if front and front.title else tr.t(modules[0].title_key) if len(modules) == 1
                   else tr.t("bundle.default_title"))
        c.setSubject(f"{self.lang}/{self.mode}")

        for n, (kind, m, idx) in enumerate(plan, start=1):
            if kind == "module":
                spec = PageSpec("module", tr.t(m.title_key), f"{m.series_code} {idx + 1}/{m.pages}", n, total,
                                m.id, idx, m.pages)
            elif kind == "toc":
                spec = PageSpec("toc", tr.t("bundle.toc_title"), "", n, total)
            else:
                spec = PageSpec("cover", "", "", n, total)
            page = Page(c, self.theme, tr, self.assets, spec, self.seed)
            try:
                if kind == "module":
                    if idx == 0:
                        key = f"mod_{m.id}"
                        c.bookmarkPage(key)
                        c.addOutlineEntry(tr.t(m.title_key), key, level=0)
                    m.render(idx, page)
                elif kind == "toc":
                    draw_toc(page, modules, start, idx)
                else:
                    draw_cover(page, front, modules)
            except Exception as exc:  # satu halaman rusak tidak mematikan sisanya; QC akan FAIL
                log.exception("Render gagal: %s halaman %d", getattr(m, "id", kind), idx + 1)
                res.errors.append(f"{getattr(m, 'id', kind)} halaman {idx + 1}: {exc!r}")
            res.records.append(page.finish())
        c.save()
        res.i18n_events = tr.events
        log.info("PDF ditulis: %s (%d halaman)", out_path, total)
        return res
