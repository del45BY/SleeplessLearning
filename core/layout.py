"""Sistem layout tunggal: grid 12 kolom, header, zona identitas, footer, helper komponen.

Aturan emas: modul HANYA menaruh elemen lewat helper di kelas `Page` (yang di modul
disebut `ctx`). Jangan menyentuh canvas atau memakai koordinat bebas. Semua koordinat
dalam mm dari pojok kiri-atas. Setiap elemen dicatat (bbox, teks, gambar, warna) agar
QC bisa memeriksa tanpa membaca PDF.
"""
from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Set, Tuple

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

import config
from core.assets import AssetResolver
from core.i18n import Translator
from core.theme import Theme

log = logging.getLogger(__name__)
MM = config.MM_TO_PT
FONT_REGULAR, FONT_BOLD, FONT_TRACE = "WS-Regular", "WS-Bold", "WS-Trace"


# ----------------------------------------------------------------------------
# Font
# ----------------------------------------------------------------------------
class FontError(RuntimeError):
    """Font TTF Unicode tidak ditemukan."""


_FONTS_READY = False


def register_fonts() -> None:
    """Daftarkan font TTF (di-embed otomatis oleh ReportLab). Aman dipanggil berulang."""
    global _FONTS_READY
    if _FONTS_READY:
        return
    for role, name in (("regular", FONT_REGULAR), ("bold", FONT_BOLD), ("trace", FONT_TRACE)):
        path = config.find_font_file(config.FONT_CANDIDATES[role])
        if path is None:
            raise FontError(
                f"Font '{role}' tidak ditemukan. Salin DejaVuSans.ttf dan DejaVuSans-Bold.ttf "
                f"ke folder {config.FONTS_DIR} (lihat README)."
            )
        pdfmetrics.registerFont(TTFont(name, str(path)))
    _FONTS_READY = True


def text_width_mm(text: str, font: str, size: float) -> float:
    """Lebar teks dalam mm."""
    return stringWidth(text, font, size) / MM


def has_glyph(font: str, ch: str) -> bool:
    """Apakah font punya glyph untuk karakter ini."""
    return ord(ch) in pdfmetrics.getFont(font).face.charToGlyph


# ----------------------------------------------------------------------------
# Geometri
# ----------------------------------------------------------------------------
@dataclass(frozen=True)
class Rect:
    """Persegi panjang dalam mm; (x, y) = pojok kiri-atas."""
    x: float
    y: float
    w: float
    h: float

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def bottom(self) -> float:
        return self.y + self.h

    @property
    def cx(self) -> float:
        return self.x + self.w / 2

    @property
    def cy(self) -> float:
        return self.y + self.h / 2

    def inset(self, d: float) -> "Rect":
        return Rect(self.x + d, self.y + d, self.w - 2 * d, self.h - 2 * d)

    def split_cols(self, n: int, gap: float = 0.0) -> List["Rect"]:
        w = (self.w - gap * (n - 1)) / n
        return [Rect(self.x + i * (w + gap), self.y, w, self.h) for i in range(n)]

    def split_rows(self, n: int, gap: float = 0.0) -> List["Rect"]:
        h = (self.h - gap * (n - 1)) / n
        return [Rect(self.x, self.y + i * (h + gap), self.w, h) for i in range(n)]

    def grid(self, rows: int, cols: int, gap: float = 0.0) -> List["Rect"]:
        """Sel-sel grid berurutan baris demi baris."""
        return [c for r in self.split_rows(rows, gap) for c in r.split_cols(cols, gap)]

    def take_top(self, h: float) -> Tuple["Rect", "Rect"]:
        """Potong bagian atas setinggi h -> (atas, sisa)."""
        return Rect(self.x, self.y, self.w, h), Rect(self.x, self.y + h, self.w, self.h - h)

    def center_square(self, side: float) -> "Rect":
        return Rect(self.cx - side / 2, self.cy - side / 2, side, side)

    def contains(self, o: "Rect", tol: float = 0.01) -> bool:
        return (o.x >= self.x - tol and o.y >= self.y - tol
                and o.right <= self.right + tol and o.bottom <= self.bottom + tol)

    def overlap_area(self, o: "Rect") -> float:
        dx = min(self.right, o.right) - max(self.x, o.x)
        dy = min(self.bottom, o.bottom) - max(self.y, o.y)
        return dx * dy if dx > 0 and dy > 0 else 0.0

    def as_list(self) -> List[float]:
        return [round(v, 2) for v in (self.x, self.y, self.w, self.h)]


SAFE_AREA = Rect(config.MARGIN_MM, config.MARGIN_MM,
                 config.PAGE_W_MM - 2 * config.MARGIN_MM, config.PAGE_H_MM - 2 * config.MARGIN_MM)


@dataclass
class Element:
    """Catatan satu elemen yang digambar (untuk QC)."""
    kind: str
    rect: Rect
    zone: str = "content"            # "content" | "system"
    container: bool = False          # kotak pembungkus: anak boleh ada di dalamnya
    within: Optional[Rect] = None    # sel tempat elemen harus berada
    text: str = ""
    font: str = ""
    size: float = 0.0
    check_height: bool = True
    image: str = ""
    group: str = ""
    value: str = ""


@dataclass
class PageSpec:
    kind: str                         # "module" | "toc" | "cover"
    title: str
    series_label: str
    page_number: int
    total_pages: int
    module_id: str = ""
    page_index: int = 0
    module_pages: int = 0


@dataclass
class PageRecord:
    spec: PageSpec
    content_rect: Rect
    elements: List[Element] = field(default_factory=list)
    colors: Set[Tuple[str, Tuple[float, float, float], str]] = field(default_factory=set)
    has_instruction: bool = False


# ----------------------------------------------------------------------------
# Page (= ctx di modul)
# ----------------------------------------------------------------------------
class Page:
    """Satu halaman PDF. Modul memanggil helper `draw_*`, `band`, `cell`, `t`.

    Helper publik untuk modul:
      t(key, **fmt)                         terjemahan
      order(seq)                            urutan tetap, atau diacak deterministik jika --seed
      band(i, n, gap)                       pita horizontal ke-i dari n di area konten
      cell(rect, col, span)                 sel grid 12 kolom di dalam rect
      draw_instruction(text, icon)          instruksi 1 baris (WAJIB 1x per halaman modul)
      draw_image_slot(cell, image_id, size) gambar PNG dalam slot token S/M/L/XL
      draw_trace_line(cell, text, ...)      baris tracing dengan garis panduan
      draw_writing_lines(cell, rows)        baris menulis kosong
      draw_box(rect, ...)                   kotak/bingkai (kontainer)
      draw_text(rect, text, ...)            teks 1 baris
    """

    def __init__(self, canvas: Canvas, theme: Theme, tr: Translator, assets: AssetResolver,
                 spec: PageSpec, seed: Optional[int] = None) -> None:
        self.c = canvas                      # internal: jangan dipakai modul
        self.theme, self.tr, self.assets, self.spec = theme, tr, assets, spec
        self.lang, self.mode = tr.lang, theme.mode
        self.page_index, self.module_pages = spec.page_index, spec.module_pages
        self.rng = random.Random(f"{seed}|{spec.module_id}|{spec.page_index}") if seed is not None else None
        top = {"module": config.CONTENT_TOP, "toc": config.TOC_CONTENT_TOP, "cover": config.MARGIN_MM}[spec.kind]
        self.content = Rect(config.MARGIN_MM, top, SAFE_AREA.w, config.CONTENT_BOTTOM - top)
        self.record = PageRecord(spec, self.content)
        self._draw_chrome()

    # ---- util ---------------------------------------------------------------
    def t(self, key: str, **fmt: object) -> str:
        return self.tr.t(key, **fmt)

    def order(self, seq: Sequence) -> list:
        items = list(seq)
        if self.rng is not None:
            self.rng.shuffle(items)
        return items

    def _y(self, y_mm: float) -> float:
        return (config.PAGE_H_MM - y_mm) * MM

    def _log(self, el: Element) -> Element:
        self.record.elements.append(el)
        return el

    def _use(self, name: str, usage: str):
        rgb = self.theme.rgb(name)
        self.record.colors.add((name, rgb, usage))
        return self.theme.color(name)

    def _stroke(self, name: str) -> None:
        self.c.setStrokeColor(self._use(name, "stroke"))

    def _fill(self, name: str, usage: str = "fill") -> None:
        self.c.setFillColor(self._use(name, usage))

    def _lw(self, pt: float) -> float:
        return pt * self.theme.line_scale

    # ---- grid ---------------------------------------------------------------
    def band(self, i: int, n: int, gap: float = 4.0) -> Rect:
        """Pita ke-i (0-based) dari n pita setinggi sama di area konten."""
        if not 0 <= i < n:
            raise ValueError(f"band index {i} di luar 0..{n - 1}")
        return self.content.split_rows(n, gap)[i]

    def cell(self, rect: Rect, col: int, span: int = 1, cols: int = config.GRID_COLS) -> Rect:
        """Sel grid (default 12 kolom, gutter dari config) di dalam rect."""
        if col < 0 or span < 1 or col + span > cols:
            raise ValueError(f"cell(col={col}, span={span}) di luar grid {cols} kolom")
        g = config.GRID_GUTTER_MM
        cw = (rect.w - g * (cols - 1)) / cols
        return Rect(rect.x + col * (cw + g), rect.y, span * cw + (span - 1) * g, rect.h)

    # ---- helper komponen ----------------------------------------------------
    def draw_text(self, rect: Rect, text: str, *, size: float = config.FONT_LABEL, bold: bool = False,
                  align: str = "left", color: str = "ink", group: str = "", value: str = "",
                  zone: str = "content", kind: str = "text") -> None:
        """Teks satu baris, rata kiri/tengah/kanan, tegak lurus di tengah rect."""
        font = FONT_BOLD if bold else FONT_REGULAR
        self._log(Element(kind, rect, zone, text=text, font=font, size=size, group=group, value=value))
        if not text:
            return
        c = self.c
        c.setFont(font, size)
        self._fill(color, "text")
        base = self._y(rect.cy) - 0.35 * size
        if align == "left":
            c.drawString(rect.x * MM, base, text)
        elif align == "right":
            c.drawRightString(rect.right * MM, base, text)
        else:
            c.drawCentredString(rect.cx * MM, base, text)

    def draw_image_slot(self, cell: Rect, image_id: str, size: str = "M", *, group: str = "",
                        value: str = "", zone: str = "content", kind: str = "image") -> None:
        """Gambar PNG di slot persegi ukuran token (S/M/L/XL), rata tengah sel."""
        side = config.IMG_SIZES[size]
        sq = cell.center_square(side)
        self._log(Element(kind, sq, zone, within=cell, image=image_id, group=group, value=value))
        path = self.assets.path(image_id, self.mode)
        self.c.drawImage(str(path), sq.x * MM, self._y(sq.bottom), side * MM, side * MM,
                         mask="auto", preserveAspectRatio=True, anchor="c")

    def draw_box(self, rect: Rect, *, dashed: bool = False, color: str = "line",
                 fill: Optional[str] = None, radius: float = config.BOX_RADIUS_MM) -> None:
        """Kotak bersudut bulat; berfungsi sebagai kontainer (anak boleh di dalamnya)."""
        self._log(Element("box", rect, container=True))
        c = self.c
        c.saveState()
        self._stroke(color)
        c.setLineWidth(self._lw(config.LINE_NORMAL_PT))
        if dashed:
            c.setDash(list(config.GUIDE_DASH))
        if fill:
            self._fill(fill)
        c.roundRect(rect.x * MM, self._y(rect.bottom), rect.w * MM, rect.h * MM,
                    radius * MM, stroke=1, fill=1 if fill else 0)
        c.restoreState()

    def draw_writing_lines(self, rect: Rect, rows: Optional[int] = None) -> None:
        """Baris menulis kosong setinggi WRITE_ROW_H_MM."""
        rh = config.WRITE_ROW_H_MM
        n = rows if rows is not None else max(1, int(rect.h // rh))
        used = Rect(rect.x, rect.y, rect.w, n * rh)
        self._log(Element("writing", used, within=rect))
        c = self.c
        c.saveState()
        self._stroke("guide")
        c.setLineWidth(self._lw(config.LINE_THIN_PT))
        for i in range(n):
            y = self._y(used.y + (i + 1) * rh)
            c.line(used.x * MM, y, used.right * MM, y)
        c.restoreState()

    def draw_trace_line(self, rect: Rect, text: str, *, group: str = "", value: str = "",
                        model: bool = True, max_reps: Optional[int] = None) -> None:
        """Baris tracing: 3 garis panduan + contoh (garis tegas) + pengulangan putus-putus."""
        H = config.TRACE_ROW_H_MM
        row = Rect(rect.x, rect.y + (rect.h - H) / 2, rect.w, H)
        size = config.TRACE_FONT_PT
        gw = text_width_mm(text, FONT_TRACE, size)
        self._log(Element("trace", row, within=rect, text=text, font=FONT_TRACE, size=size,
                          check_height=False, group=group, value=value))
        # lebar 1 glyph harus muat di baris (QC memeriksa lewat Element.text vs rect.w)
        c = self.c
        y_top, y_mid, y_base = (row.y + f * H for f in (config.TRACE_TOP, config.TRACE_MID, config.TRACE_BASE))
        c.saveState()
        c.setLineWidth(self._lw(config.LINE_THIN_PT))
        self._stroke("guide")
        for y in (y_top, y_base):
            c.line(row.x * MM, self._y(y), row.right * MM, self._y(y))
        self._stroke("guide_soft")
        c.setDash(list(config.GUIDE_DASH))
        c.line(row.x * MM, self._y(y_mid), row.right * MM, self._y(y_mid))
        c.restoreState()
        pitch = gw + config.TRACE_GAP_MM
        n = max(1, int((row.w + config.TRACE_GAP_MM) // pitch))
        if max_reps:
            n = min(n, max_reps)
        for i in range(n):
            c.saveState()
            if i == 0 and model:
                self._fill("model_fill")
                self._stroke("ink")
                c.setLineWidth(self._lw(config.LINE_NORMAL_PT))
                mode = 2
            else:
                self._stroke("trace")
                c.setLineWidth(self._lw(config.TRACE_STROKE_PT))
                c.setDash(list(config.TRACE_DASH))
                mode = 1
            t = c.beginText()
            t.setTextOrigin((row.x + i * pitch) * MM, self._y(y_base))
            t.setFont(FONT_TRACE, size)
            t.setTextRenderMode(mode)
            t.textOut(text)
            c.drawText(t)
            c.restoreState()

    def draw_instruction(self, text: str, icon: str = "icon_pencil") -> None:
        """Satu gaya instruksi: ikon kecil + kalimat pendek 1 baris (zona tetap)."""
        if self.record.has_instruction:
            raise ValueError("draw_instruction hanya boleh dipanggil sekali per halaman.")
        self.record.has_instruction = True
        z = Rect(config.MARGIN_MM, config.INSTR_TOP, SAFE_AREA.w, config.INSTR_H)
        ic = Rect(z.x, z.y + (z.h - config.ICON_MM) / 2, config.ICON_MM, config.ICON_MM)
        self._log(Element("icon", ic, "system", image=icon))
        self.c.drawImage(str(self.assets.path(icon, self.mode)), ic.x * MM, self._y(ic.bottom),
                         ic.w * MM, ic.h * MM, mask="auto", preserveAspectRatio=True, anchor="c")
        gap = 3.0
        tr = Rect(ic.right + gap, z.y, z.w - config.ICON_MM - gap, z.h)
        self.draw_text(tr, text, size=config.FONT_INSTRUCTION, bold=True, zone="system", kind="instruction")

    # ---- chrome (header / identitas / footer) -------------------------------
    def _rule(self, y: float, color: str, width: float) -> None:
        self._log(Element("rule", Rect(config.MARGIN_MM, y, SAFE_AREA.w, 0.0), "system"))
        c = self.c
        c.saveState()
        self._stroke(color)
        c.setLineWidth(self._lw(width))
        c.line(config.MARGIN_MM * MM, self._y(y), (config.MARGIN_MM + SAFE_AREA.w) * MM, self._y(y))
        c.restoreState()

    def _draw_chrome(self) -> None:
        k = self.spec.kind
        if k in ("module", "toc"):
            hd = Rect(config.MARGIN_MM, config.HEADER_TOP, SAFE_AREA.w, config.HEADER_H - 1.5)
            self.draw_text(self.cell(hd, 0, 9), self.spec.title, size=config.FONT_TITLE, bold=True,
                           color="accent", zone="system", kind="header_title")
            self.draw_text(self.cell(hd, 9, 3), self.spec.series_label, size=config.FONT_HEADER_SIDE,
                           align="right", color="muted", zone="system", kind="header_side")
            self._rule(config.HEADER_TOP + config.HEADER_H, "accent", config.LINE_THICK_PT)
        if k == "module":
            ir = Rect(config.MARGIN_MM, config.IDENT_TOP, SAFE_AREA.w, config.IDENT_H)
            for cell, key in ((self.cell(ir, 0, 8), "common.name_label"), (self.cell(ir, 8, 4), "common.date_label")):
                label = self.t(key)
                lab_rect = Rect(cell.x, cell.y, cell.w - config.MIN_WRITE_LINE_MM, cell.h)
                self.draw_text(lab_rect, label, size=config.FONT_IDENT, bold=True, zone="system", kind="identity_label")
                lw = text_width_mm(label, FONT_BOLD, config.FONT_IDENT)
                c = self.c
                c.saveState()
                self._stroke("line")
                c.setLineWidth(self._lw(config.LINE_NORMAL_PT))
                y = self._y(cell.bottom - 1.0)
                c.line((cell.x + lw + 2) * MM, y, (cell.right - 1) * MM, y)
                c.restoreState()
        # footer
        self._rule(config.FOOTER_TOP, "line", config.LINE_THIN_PT)
        fr = Rect(config.MARGIN_MM, config.FOOTER_TOP + 1.0, SAFE_AREA.w, config.FOOTER_H - 1.0)
        self.draw_text(self.cell(fr, 0, 3), config.BRAND_NAME, size=config.FONT_FOOTER, bold=True,
                       color="muted", zone="system", kind="footer_brand")
        self.draw_text(self.cell(fr, 3, 7), self.t("common.license"), size=config.FONT_FOOTER,
                       align="center", color="muted", zone="system", kind="footer_license")
        self.draw_text(self.cell(fr, 10, 2), f"{self.t('common.page')} {self.spec.page_number}",
                       size=config.FONT_FOOTER, bold=True, align="right", color="muted",
                       zone="system", kind="footer_page")

    def finish(self) -> PageRecord:
        """Akhiri halaman (dipanggil renderer)."""
        self.c.showPage()
        return self.record
