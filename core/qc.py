"""Quality control otomatis: i18n, layout, gambar, PDF, mode bw, konten.

Level: PASS < WARN < FAIL. Laporan ditulis ke output/qc_report.md dan qc_report.json.
`run_qc` mengembalikan QCReport; `report.exit_code` bernilai 1 bila ada FAIL.
"""
from __future__ import annotations

import json
import logging
import re
import shutil
import string
import unicodedata
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

import config
from core import registry
from core.assets import AssetResolver
from core.i18n import I18nError, Translator, load_language
from core.layout import SAFE_AREA, Rect, has_glyph, register_fonts, text_width_mm
from core.renderer import Renderer, RenderResult
from core.theme import BW_PALETTE, contrast_vs_white, get_theme, is_gray, relative_luminance
from modules.base import BaseModule

log = logging.getLogger(__name__)
RANK = {"PASS": 0, "WARN": 1, "FAIL": 2}
AREAS = ("i18n", "layout", "images", "pdf", "mode", "content")
TODO_RE = re.compile(r"\b(TODO|TBD|FIXME|XXX|lorem ipsum)\b|\[\[", re.I)
GLOBAL = "_global"


@dataclass(frozen=True)
class Finding:
    level: str
    area: str
    scope: str
    message: str
    lang: str = ""
    mode: str = ""


class QCReport:
    """Kumpulan temuan + ringkasan per scope (modul / bundle / _global)."""

    def __init__(self) -> None:
        self.findings: List[Finding] = []
        self.scopes: "OrderedDict[str, None]" = OrderedDict()

    def add(self, level: str, area: str, scope: str, message: str, lang: str = "", mode: str = "") -> None:
        self.scopes.setdefault(scope, None)
        self.findings.append(Finding(level, area, scope, message, lang, mode))

    def touch(self, scope: str) -> None:
        self.scopes.setdefault(scope, None)

    def status(self, scope: str, area: Optional[str] = None) -> str:
        worst = "PASS"
        for f in self.findings:
            if f.scope == scope and (area is None or f.area == area) and RANK[f.level] > RANK[worst]:
                worst = f.level
        return worst

    def count(self, level: str) -> int:
        return sum(1 for f in self.findings if f.level == level)

    @property
    def exit_code(self) -> int:
        return 1 if self.count("FAIL") else 0

    def _grouped(self, scope: str, area: str) -> List[Tuple[str, str, List[str]]]:
        groups: "OrderedDict[Tuple[str, str], Set[str]]" = OrderedDict()
        for f in self.findings:
            if f.scope == scope and f.area == area:
                ctx = "/".join(x for x in (f.lang, f.mode) if x)
                groups.setdefault((f.level, f.message), set()).add(ctx)
        out = []
        for (lvl, msg), ctxs in groups.items():
            out.append((lvl, msg, sorted(c for c in ctxs if c)))
        out.sort(key=lambda t: -RANK[t[0]])
        return out

    def to_json(self) -> dict:
        data = {"summary": {"scopes": len(self.scopes), "fail": self.count("FAIL"), "warn": self.count("WARN")},
                "scopes": {}}
        for s in self.scopes:
            data["scopes"][s] = {"status": self.status(s), "areas": {
                a: {"status": self.status(s, a),
                    "findings": [{"level": l, "message": m, "context": c} for l, m, c in self._grouped(s, a)]}
                for a in AREAS}}
        return data

    def to_markdown(self) -> str:
        L = ["# QC Report", "", f"**FAIL: {self.count('FAIL')} · WARN: {self.count('WARN')}**", "",
             "| Scope | Status | " + " | ".join(AREAS) + " |", "|---|---|" + "---|" * len(AREAS)]
        for s in self.scopes:
            L.append(f"| `{s}` | **{self.status(s)}** | " + " | ".join(self.status(s, a) for a in AREAS) + " |")
        for s in self.scopes:
            L += ["", f"## `{s}` — {self.status(s)}"]
            for a in AREAS:
                items = self._grouped(s, a)
                L.append(f"- **{a}**: {self.status(s, a)}")
                for lvl, msg, ctxs in items:
                    ctx = f" _(…{', '.join(ctxs)})_" if ctxs and len(ctxs) <= 6 else (f" _({len(ctxs)} kombinasi)_" if ctxs else "")
                    L.append(f"  - [{lvl}] {msg}{ctx}")
        return "\n".join(L) + "\n"

    def write(self, out_dir: Path) -> Tuple[Path, Path]:
        out_dir.mkdir(parents=True, exist_ok=True)
        md, js = out_dir / "qc_report.md", out_dir / "qc_report.json"
        md.write_text(self.to_markdown(), encoding="utf-8")
        js.write_text(json.dumps(self.to_json(), indent=2, ensure_ascii=False), encoding="utf-8")
        return md, js

    def console(self) -> str:
        lines = []
        for s in self.scopes:
            parts = " ".join(f"{a}:{self.status(s, a)}" for a in AREAS)
            lines.append(f"[{self.status(s):4}] {s:<28} {parts}")
        lines.append(f"TOTAL FAIL={self.count('FAIL')} WARN={self.count('WARN')}")
        return "\n".join(lines)


# ----------------------------------------------------------------------------
# Cek global (sekali jalan)
# ----------------------------------------------------------------------------
def _scope_for_key(key: str, ids: Set[str]) -> str:
    head = key.split(".", 1)[0]
    return head if head in ids else GLOBAL


def check_global(rep: QCReport, module_ids: Set[str]) -> None:
    rep.touch(GLOBAL)
    for e in registry.errors():
        rep.add("FAIL", "content", GLOBAL, f"Registry: {e}")
    try:
        register_fonts()
    except Exception as exc:
        rep.add("FAIL", "layout", GLOBAL, f"Font: {exc}")
    for name in ("color", "bw"):
        th = get_theme(name)
        missing = set(BW_PALETTE) - set(th.palette)
        if missing:
            rep.add("FAIL", "mode", GLOBAL, f"Tema {name} kehilangan warna: {sorted(missing)}")
    if not all(is_gray(get_theme("bw").rgb(n)) for n in BW_PALETTE):
        rep.add("FAIL", "mode", GLOBAL, "Palet bw mengandung warna non-abu-abu")
    try:
        en = load_language("en")
    except I18nError as exc:
        rep.add("FAIL", "i18n", GLOBAL, str(exc))
        return
    for lang in config.LANGS:
        try:
            s = load_language(lang)
        except I18nError as exc:
            rep.add("FAIL", "i18n", GLOBAL, str(exc), lang)
            continue
        for key in en:
            if key not in s:
                rep.add("FAIL", "i18n", _scope_for_key(key, module_ids), f"Key '{key}' tidak ada (fallback ke en)", lang)
        for key, val in s.items():
            sc = _scope_for_key(key, module_ids)
            if key not in en:
                rep.add("WARN", "i18n", sc, f"Key '{key}' tidak ada di en", lang)
            if not isinstance(val, str) or not val.strip():
                rep.add("FAIL", "i18n", sc, f"String kosong: '{key}'", lang)
            elif TODO_RE.search(val):
                rep.add("FAIL", "i18n", sc, f"Placeholder TODO di '{key}': {val!r}", lang)
            elif lang != "en" and val == en.get(key) and len(val) > 12 and ".img." not in key:
                rep.add("WARN", "i18n", sc, f"'{key}' identik dengan en (belum diterjemahkan?)", lang)


# ----------------------------------------------------------------------------
# Cek per hasil render
# ----------------------------------------------------------------------------
def _check_render_i18n(rep: QCReport, res: RenderResult) -> None:
    seen: Set[Tuple[str, str]] = set()
    for ev in res.i18n_events:
        if (ev.kind, ev.key) in seen:
            continue
        seen.add((ev.kind, ev.key))
        msg = {"fallback": f"Key '{ev.key}' tidak ada di bahasa target; dipakai teks en",
               "missing": f"Key '{ev.key}' tidak ada di bahasa mana pun",
               "empty": f"Key '{ev.key}' kosong", "format": f"Format gagal di '{ev.key}'"}[ev.kind]
        rep.add("FAIL", "i18n", res.scope, msg, res.lang, res.mode)


def _check_layout(rep: QCReport, res: RenderResult) -> None:
    S = res.scope
    ctx = (res.lang, res.mode)
    for rec in res.records:
        pg = rec.spec.page_number
        els = rec.elements
        for el in els:
            r = el.rect
            if not SAFE_AREA.contains(r):
                rep.add("FAIL", "layout", S, f"hal.{pg}: {el.kind} keluar dari safe area {r.as_list()}", *ctx)
            if el.zone == "content" and not rec.content_rect.contains(r):
                rep.add("FAIL", "layout", S, f"hal.{pg}: {el.kind} keluar dari area konten {r.as_list()}", *ctx)
            if el.within is not None and not el.within.contains(r):
                rep.add("FAIL", "layout", S, f"hal.{pg}: {el.kind} '{el.text or el.image}' lebih besar dari selnya "
                        f"({r.w:.1f}x{r.h:.1f} mm vs {el.within.w:.1f}x{el.within.h:.1f} mm)", *ctx)
            if el.font:
                if el.size < config.MIN_FONT_PT:
                    rep.add("FAIL", "layout", S, f"hal.{pg}: font {el.size}pt < minimum {config.MIN_FONT_PT}pt", *ctx)
                w = text_width_mm(el.text, el.font, el.size)
                if el.text and w > r.w + 0.05:
                    rep.add("FAIL", "i18n", S, f"Teks '{el.text}' ({w:.1f} mm) melebihi kotak {r.w:.1f} mm [{el.kind}]", *ctx)
                if el.check_height and el.text and el.size * 25.4 / 72 > r.h + 0.05:
                    rep.add("FAIL", "layout", S, f"hal.{pg}: teks '{el.text}' lebih tinggi dari kotaknya", *ctx)
                bad = sorted({ch for ch in el.text if not ch.isspace() and not has_glyph(el.font, ch)})
                if bad:
                    rep.add("FAIL", "i18n", S, f"Glyph tidak ada di font untuk {bad} pada '{el.text}'", *ctx)
        flat = [e for e in els if e.kind != "rule"]
        for i, a in enumerate(flat):
            for b in flat[i + 1:]:
                if a.rect.overlap_area(b.rect) <= 0.25:
                    continue
                if (a.container and a.rect.contains(b.rect)) or (b.container and b.rect.contains(a.rect)):
                    continue
                rep.add("FAIL", "layout", S, f"hal.{pg}: {a.kind} saling menimpa {b.kind} "
                        f"({a.text or a.image} / {b.text or b.image})", *ctx)
        for w in rec.warnings:
            rep.add("WARN", "layout", S, f"hal.{pg}: {w}", *ctx)
        if rec.spec.kind == "module":
            if not rec.has_instruction:
                rep.add("FAIL", "layout", S, f"hal.{pg}: tidak ada draw_instruction()", *ctx)
            if not any(e.zone == "content" for e in els):
                rep.add("FAIL", "pdf", S, f"hal.{pg}: halaman kosong (tidak ada konten)", *ctx)
    for e in res.errors:
        rep.add("FAIL", "layout", S, f"Error render: {e}", *ctx)


def _check_images(rep: QCReport, res: RenderResult, assets: AssetResolver) -> None:
    S, ctx = res.scope, (res.lang, res.mode)
    used = {e.image for r in res.records for e in r.elements if e.image}
    declared: Set[str] = set(res.extra_images)
    for m in res.modules:
        try:
            declared |= set(m.images(res.lang))
        except Exception as exc:
            rep.add("FAIL", "images", S, f"{m.id}.images() error: {exc!r}", *ctx)
    if used - declared:
        rep.add("FAIL", "images", S, f"Gambar dipakai tapi tidak dideklarasikan di images(): {sorted(used - declared)}", *ctx)
    if declared - used:
        rep.add("WARN", "images", S, f"Gambar dideklarasikan tapi tidak dipakai: {sorted(declared - used)}", *ctx)
    placeholders, small, noalpha = [], [], []
    for iid in sorted(used | declared):
        info = assets.info(iid)
        if not info.exists:
            rep.add("FAIL", "images", S, f"Gambar '{iid}.png' tidak ada", *ctx)
            continue
        if info.placeholder:
            placeholders.append(iid)
            continue
        m = min(info.width, info.height)
        if m < config.HARD_MIN_IMAGE_PX:
            rep.add("FAIL", "images", S, f"'{iid}.png' resolusi {info.width}x{info.height} terlalu kecil", *ctx)
        elif m < config.MIN_IMAGE_PX:
            small.append(f"{iid} ({info.width}x{info.height})")
        if not info.has_alpha:
            noalpha.append(iid)
    if placeholders:
        shown = ", ".join(placeholders[:6]) + (f", … (+{len(placeholders) - 6})" if len(placeholders) > 6 else "")
        rep.add("WARN", "images", S, f"{len(placeholders)} gambar masih placeholder: {shown}", *ctx)
    if small:
        rep.add("WARN", "images", S, f"Resolusi < {config.MIN_IMAGE_PX}px: {', '.join(small)}", *ctx)
    if noalpha:
        rep.add("WARN", "images", S, f"PNG tanpa alpha channel: {', '.join(noalpha)}", *ctx)


def _check_pdf(rep: QCReport, res: RenderResult) -> None:
    S, ctx = res.scope, (res.lang, res.mode)
    p = res.path
    if not p.is_file() or p.stat().st_size == 0:
        rep.add("FAIL", "pdf", S, f"File PDF tidak ada/kosong: {p}", *ctx)
        return
    mb = p.stat().st_size / 1e6
    if mb > config.MAX_PDF_FAIL_MB:
        rep.add("FAIL", "pdf", S, f"Ukuran file {mb:.1f} MB terlalu besar", *ctx)
    elif mb > config.MAX_PDF_WARN_MB:
        rep.add("WARN", "pdf", S, f"Ukuran file {mb:.1f} MB cukup besar", *ctx)
    try:
        from pypdf import PdfReader
    except ImportError:
        rep.add("WARN", "pdf", S, "pypdf tidak terpasang: cek mendalam PDF dilewati", *ctx)
        return
    rd = PdfReader(str(p))
    if len(rd.pages) != res.expected_pages:
        rep.add("FAIL", "pdf", S, f"Jumlah halaman {len(rd.pages)} != metadata {res.expected_pages}", *ctx)
    unembedded: Set[str] = set()
    for i, pg in enumerate(rd.pages, start=1):
        w, h = float(pg.mediabox.width), float(pg.mediabox.height)
        if abs(w - 612) > 0.5 or abs(h - 792) > 0.5:
            rep.add("FAIL", "pdf", S, f"Hal.{i} ukuran {w:.0f}x{h:.0f} pt, bukan Letter 612x792", *ctx)
        fonts = (pg.get("/Resources") or {}).get("/Font") or {}
        for _, ref in fonts.items():
            f = ref.get_object()
            desc = f.get("/FontDescriptor")
            if desc is None and "/DescendantFonts" in f:
                desc = f["/DescendantFonts"][0].get_object().get("/FontDescriptor")
            d = desc.get_object() if desc is not None else {}
            if not any(k in d for k in ("/FontFile", "/FontFile2", "/FontFile3")):
                unembedded.add(str(f.get("/BaseFont")))
    if unembedded:
        rep.add("FAIL", "pdf", S, f"Font tidak ter-embed: {sorted(unembedded)}", *ctx)


def _lum_contrast(rgb) -> float:
    return contrast_vs_white(rgb)


def _check_mode(rep: QCReport, res: RenderResult, assets: AssetResolver) -> None:
    if res.mode != "bw":
        return
    S, ctx = res.scope, (res.lang, res.mode)
    bad_color: Set[str] = set()
    dark_fill: Set[str] = set()
    weak: Set[str] = set()
    for rec in res.records:
        for name, rgb, usage in rec.colors:
            if not is_gray(rgb):
                bad_color.add(name)
            if usage == "fill" and relative_luminance(rgb) < 0.8:
                dark_fill.add(name)
            if usage in ("stroke", "text") and _lum_contrast(rgb) < 3.0:
                weak.add(name)
    if bad_color:
        rep.add("FAIL", "mode", S, f"Warna non-abu-abu di mode bw: {sorted(bad_color)}", *ctx)
    if dark_fill:
        rep.add("FAIL", "mode", S, f"Fill gelap di mode bw (boros tinta): {sorted(dark_fill)}", *ctx)
    if weak:
        rep.add("FAIL", "mode", S, f"Kontras garis/teks < 3:1 di mode bw: {sorted(weak)}", *ctx)
    for iid in sorted({e.image for r in res.records for e in r.elements if e.image}):
        if not assets.is_gray_image(assets.path(iid, "bw")):
            rep.add("FAIL", "mode", S, f"Gambar bw '{iid}' bukan grayscale", *ctx)


def _expected(spec: Tuple) -> List:
    a, b = spec
    if isinstance(a, int):
        return list(range(a, b + 1))
    return [chr(c) for c in range(ord(a), ord(b) + 1)]


def _check_content(rep: QCReport, res: RenderResult) -> None:
    S, ctx = res.scope, (res.lang, res.mode)
    for rec in res.records:
        seen: Set[Tuple[str, str]] = set()
        for e in rec.elements:
            if e.group and e.value != "":
                k = (e.group, e.value)
                if k in seen:
                    rep.add("FAIL", "content", S, f"hal.{rec.spec.page_number}: duplikasi item {e.group}={e.value}", *ctx)
                seen.add(k)
    for m in res.modules:
        for group, spec in m.sequences.items():
            vals = [e.value for r in res.records if r.spec.module_id == m.id for e in r.elements if e.group == group]
            exp = [str(x) for x in _expected(spec)]
            if vals != exp:
                rep.add("FAIL", "content", S, f"{m.id}: urutan '{group}' salah. Seharusnya {exp[0]}…{exp[-1]}, "
                        f"didapat {vals[:12]}", *ctx)
        try:
            for lvl, msg in m.qc_extra(res.lang, Translator(res.lang)):
                rep.add(lvl, "content", S, f"{m.id}: {msg}", *ctx)
        except Exception as exc:
            rep.add("FAIL", "content", S, f"{m.id}.qc_extra() error: {exc!r}", *ctx)


def check_result(rep: QCReport, res: RenderResult, assets: Optional[AssetResolver] = None) -> None:
    """Jalankan semua cek untuk satu hasil render."""
    assets = assets or AssetResolver()
    rep.touch(res.scope)
    _check_render_i18n(rep, res)
    _check_layout(rep, res)
    _check_images(rep, res, assets)
    _check_pdf(rep, res)
    _check_mode(rep, res, assets)
    _check_content(rep, res)


def run_qc(modules: Sequence[BaseModule], langs: Sequence[str], modes: Sequence[str], *,
           results: Optional[Iterable[RenderResult]] = None, out_dir: Optional[Path] = None,
           seed: Optional[int] = None, write: bool = True) -> QCReport:
    """Jalankan QC. Tanpa `results`, modul dirender dulu ke folder sementara."""
    out_dir = Path(out_dir or config.OUTPUT_DIR)
    rep = QCReport()
    ids = {m.id for m in registry.all_modules()}
    check_global(rep, ids)
    for m in modules:
        rep.touch(m.id)
    tmp: Optional[Path] = None
    if results is None:
        tmp = out_dir / "_qc_tmp"
        res_list: List[RenderResult] = []
        for m in modules:
            for lang in langs:
                for mode in modes:
                    res_list.append(Renderer(lang, mode, seed).render([m], tmp / lang / mode / f"{m.id}.pdf"))
    else:
        res_list = list(results)
    assets = AssetResolver()
    for res in res_list:
        check_result(rep, res, assets)
    if tmp is not None:
        shutil.rmtree(tmp, ignore_errors=True)
    # saring temuan global i18n agar hanya yang relevan dengan modul terpilih + _global
    keep = {m.id for m in modules} | {GLOBAL} | {r.scope for r in res_list}
    rep.findings = [f for f in rep.findings if f.scope in keep and (not f.lang or f.lang in langs)]
    rep.scopes = OrderedDict((s, None) for s in rep.scopes if s in keep)
    if write:
        rep.write(out_dir)
    return rep
