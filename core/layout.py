"""Sistem layout tunggal: grid 12 kolom, header, zona identitas, footer, helper komponen.

Aturan emas: modul HANYA menaruh elemen lewat helper di kelas `Page` (yang di modul
disebut `ctx`). Jangan menyentuh canvas atau memakai koordinat bebas. Semua koordinat
dalam mm dari pojok kiri-atas. Setiap elemen dicatat (bbox, teks, gambar, warna) agar
QC bisa memeriksa tanpa membaca PDF.
"""
from __future__ import annotations

import logging
import math
import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional, Sequence, Set, Tuple

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

import config
from core import strokefont
from core.assets import AssetResolver
from core.i18n import Translator
from core.theme import Theme, relative_luminance

if TYPE_CHECKING:  # pragma: no cover
    from skins.base import BaseSkin

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
    skin_image: str = ""            # id PNG dekorasi skin (zone == "decor")


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
    warnings: List[str] = field(default_factory=list)


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
      draw_vertical_line(cell, style)       garis tegak atas->bawah (dashed|dotted|points)
      draw_horizontal_line(cell, style)     garis datar kiri->kanan (dashed|dotted|points)
      draw_diagonal_line(cell, direction, style)  garis miring: down_right|down_left|roof (A)|vee (V)|cross (X)
      draw_box(rect, ...)                   kotak/bingkai (kontainer)
      draw_text(rect, text, ...)            teks 1 baris
    """

    def __init__(self, canvas: Canvas, theme: Theme, tr: Translator, assets: AssetResolver,
                 spec: PageSpec, seed: Optional[int] = None, skin: Optional["BaseSkin"] = None) -> None:
        if skin is None:                      # tanpa skin = perilaku lama (classic)
            from skins.classic import ClassicSkin
            skin = ClassicSkin()
        self.skin = skin                     # skin aktif; modul tidak perlu tahu
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
        use_stroke = config.TRACE_STYLE == "stroke"
        if use_stroke and not all(strokefont.has_stroke_glyph(ch) for ch in text):
            missing = sorted({ch for ch in text if not strokefont.has_stroke_glyph(ch)})
            self.record.warnings.append(f"tracing '{text}': karakter {missing} tidak ada di stroke font, pakai outline")
            use_stroke = False
        for i in range(n):
            x0 = row.x + i * pitch
            if i == 0 and model:
                c.saveState()
                self._fill("model_fill")
                self._stroke("ink")
                c.setLineWidth(self._lw(config.LINE_NORMAL_PT))
                t = c.beginText()
                t.setTextOrigin(x0 * MM, self._y(y_base))
                t.setFont(FONT_TRACE, size)
                t.setTextRenderMode(2)
                t.textOut(text)
                c.drawText(t)
                c.restoreState()
            elif use_stroke:
                self._draw_center_strokes(text, x0, y_base, size)
            else:
                c.saveState()
                self._stroke("trace")
                c.setLineWidth(self._lw(config.TRACE_STROKE_PT))
                c.setDash(list(config.TRACE_DASH))
                t = c.beginText()
                t.setTextOrigin(x0 * MM, self._y(y_base))
                t.setFont(FONT_TRACE, size)
                t.setTextRenderMode(1)
                t.textOut(text)
                c.drawText(t)
                c.restoreState()

    def _draw_center_strokes(self, text: str, x0: float, y_base: float, size: float) -> None:
        """Satu garis putus di tengah tiap goresan huruf (stroke font), dipusatkan pada lebar font."""
        unit = (config.TRACE_BASE - config.TRACE_TOP) * config.TRACE_ROW_H_MM   # tinggi kapital (mm)
        c = self.c
        c.saveState()
        self._stroke("trace")
        c.setLineWidth(self._lw(config.TRACE_CENTER_STROKE_PT))
        c.setLineCap(1)
        c.setLineJoin(1)
        c.setDash(list(config.TRACE_CENTER_DASH))
        for k, ch in enumerate(text):
            w_ink, strokes = strokefont.GLYPHS[ch]
            adv = text_width_mm(ch, FONT_TRACE, size)
            gx = x0 + text_width_mm(text[:k], FONT_TRACE, size) + (adv - w_ink * unit) / 2
            for pts in strokes:
                p = c.beginPath()
                for j, (px, py) in enumerate(pts):
                    X, Y = (gx + px * unit) * MM, self._y(y_base) + py * unit * MM
                    p.moveTo(X, Y) if j == 0 else p.lineTo(X, Y)
                c.drawPath(p, stroke=1, fill=0)
        c.restoreState()

    def draw_vertical_line(self, cell: Rect, style: str = "dashed", *, group: str = "", value: str = "") -> None:
        """Satu garis tegak di tengah `cell`, dari atas ke bawah.

        style: "dashed" (garis putus), "dotted" (titik-titik), "points" (hanya lingkaran awal & akhir;
        anak menarik sendiri). Awal = lingkaran (accent), akhir = panah (atau lingkaran untuk "points").
        """
        if style not in ("dashed", "dotted", "points"):
            raise ValueError(f"style garis tegak tidak dikenal: {style!r}")
        R, A = config.VLINE_MARKER_R_MM, config.VLINE_ARROW_MM
        half = max(R, A)
        self._log(Element("vline", Rect(cell.cx - half, cell.y, 2 * half, cell.h), within=cell,
                          group=group, value=value))
        c, X = self.c, cell.cx * MM
        c.saveState()
        c.setLineWidth(self._lw(config.LINE_THICK_PT))
        self._stroke("accent")
        self._fill("paper")
        c.circle(X, self._y(cell.y + R), R * MM, stroke=1, fill=1)
        self._stroke("trace")
        if style == "points":
            c.circle(X, self._y(cell.bottom - R), R * MM, stroke=1, fill=1)
        else:
            c.setLineCap(1)
            c.setLineJoin(1)
            if style == "dashed":
                c.setLineWidth(self._lw(config.TRACE_CENTER_STROKE_PT))
                c.setDash(list(config.TRACE_CENTER_DASH))
            else:
                c.setLineWidth(self._lw(config.VLINE_DOTTED_PT))
                c.setDash(list(config.VLINE_DOTTED))
            c.line(X, self._y(cell.y + 2 * R + 1.0), X, self._y(cell.bottom - A))
            c.setDash([])
            c.setLineWidth(self._lw(config.LINE_THICK_PT))
            path = c.beginPath()
            path.moveTo(X - A * MM, self._y(cell.bottom - A))
            path.lineTo(X, self._y(cell.bottom))
            path.lineTo(X + A * MM, self._y(cell.bottom - A))
            c.drawPath(path, stroke=1, fill=0)
        c.restoreState()

    def draw_horizontal_line(self, cell: Rect, style: str = "dashed", *, group: str = "", value: str = "") -> None:
        """Satu garis datar di tengah `cell`, dari kiri ke kanan (arah dasar menulis).

        style: "dashed" | "dotted" | "points" (hanya lingkaran awal & akhir; anak menarik sendiri).
        Awal = lingkaran (accent) di kiri, akhir = panah (atau lingkaran untuk "points") di kanan.
        """
        if style not in ("dashed", "dotted", "points"):
            raise ValueError(f"style garis datar tidak dikenal: {style!r}")
        R, A = config.VLINE_MARKER_R_MM, config.VLINE_ARROW_MM
        half = max(R, A)
        self._log(Element("hline", Rect(cell.x, cell.cy - half, cell.w, 2 * half), within=cell,
                          group=group, value=value))
        c, Y = self.c, self._y(cell.cy)
        c.saveState()
        c.setLineWidth(self._lw(config.LINE_THICK_PT))
        self._stroke("accent")
        self._fill("paper")
        c.circle((cell.x + R) * MM, Y, R * MM, stroke=1, fill=1)
        self._stroke("trace")
        if style == "points":
            c.circle((cell.right - R) * MM, Y, R * MM, stroke=1, fill=1)
        else:
            c.setLineCap(1)
            c.setLineJoin(1)
            if style == "dashed":
                c.setLineWidth(self._lw(config.TRACE_CENTER_STROKE_PT))
                c.setDash(list(config.TRACE_CENTER_DASH))
            else:
                c.setLineWidth(self._lw(config.VLINE_DOTTED_PT))
                c.setDash(list(config.VLINE_DOTTED))
            c.line((cell.x + 2 * R + 1.0) * MM, Y, (cell.right - A) * MM, Y)
            c.setDash([])
            c.setLineWidth(self._lw(config.LINE_THICK_PT))
            path = c.beginPath()
            path.moveTo((cell.right - A) * MM, Y + A * MM)
            path.lineTo(cell.right * MM, Y)
            path.lineTo((cell.right - A) * MM, Y - A * MM)
            c.drawPath(path, stroke=1, fill=0)
        c.restoreState()

    def draw_diagonal_line(self, cell: Rect, direction: str = "down_right", style: str = "dashed", *,
                           group: str = "", value: str = "") -> None:
        """Garis miring di dalam `cell` (bounding box = seluruh cell; gambar lain harus di luar cell).

        direction: "down_right" (kiri-atas -> kanan-bawah), "down_left" (kanan-atas -> kiri-bawah),
                   "roof" (^, dua garis dari puncak tengah-atas turun ke kiri & kanan = bentuk A),
                   "vee" (V, dua garis dari sudut atas bertemu di tengah-bawah),
                   "cross" (X, dua garis bersilang).
        style: "dashed" | "dotted" | "points". Awal goresan = lingkaran (accent), akhir = panah
        (atau lingkaran untuk "points").
        """
        dirs = ("down_right", "down_left", "roof", "vee", "cross")
        if direction not in dirs:
            raise ValueError(f"direction garis miring tidak dikenal: {direction!r} (pilihan: {', '.join(dirs)})")
        if style not in ("dashed", "dotted", "points"):
            raise ValueError(f"style garis miring tidak dikenal: {style!r}")
        R, A = config.VLINE_MARKER_R_MM, config.VLINE_ARROW_MM
        h = max(R, A)
        x0, x1, y0, y1 = cell.x + h, cell.right - h, cell.y + h, cell.bottom - h
        xm = (x0 + x1) / 2
        strokes = {"down_right": [((x0, y0), (x1, y1))], "down_left": [((x1, y0), (x0, y1))],
                   "roof": [((xm, y0), (x0, y1)), ((xm, y0), (x1, y1))],
                   "vee": [((x0, y0), (xm, y1)), ((x1, y0), (xm, y1))],
                   "cross": [((x0, y0), (x1, y1)), ((x1, y0), (x0, y1))]}[direction]
        self._log(Element("dline", cell, within=cell, group=group, value=value))
        starts = list(dict.fromkeys((round(a[0], 2), round(a[1], 2)) for a, _ in strokes))
        ends = list(dict.fromkeys((round(b[0], 2), round(b[1], 2)) for _, b in strokes))
        c = self.c
        c.saveState()
        c.setLineWidth(self._lw(config.LINE_THICK_PT))
        self._stroke("accent")
        self._fill("paper")
        for sx, sy in starts:
            c.circle(sx * MM, self._y(sy), R * MM, stroke=1, fill=1)
        self._stroke("trace")
        if style == "points":
            for ex, ey in ends:
                c.circle(ex * MM, self._y(ey), R * MM, stroke=1, fill=1)
        else:
            c.setLineCap(1)
            c.setLineJoin(1)
            if style == "dashed":
                c.setLineWidth(self._lw(config.TRACE_CENTER_STROKE_PT))
                c.setDash(list(config.TRACE_CENTER_DASH))
            else:
                c.setLineWidth(self._lw(config.VLINE_DOTTED_PT))
                c.setDash(list(config.VLINE_DOTTED))
            units = []
            for (sx, sy), (ex, ey) in strokes:
                L = math.hypot(ex - sx, ey - sy)
                ux, uy = (ex - sx) / L, (ey - sy) / L
                units.append((ex, ey, ux, uy))
                c.line((sx + ux * (R + 1.0)) * MM, self._y(sy + uy * (R + 1.0)),
                       (ex - ux * A * 0.3) * MM, self._y(ey - uy * A * 0.3))
            c.setDash([])
            c.setLineWidth(self._lw(config.LINE_THICK_PT))
            for ex, ey, ux, uy in units:                       # panah (chevron) searah garis
                path = c.beginPath()
                wings = []
                for ang in (math.radians(35), math.radians(-35)):
                    rx, ry = ux * math.cos(ang) - uy * math.sin(ang), ux * math.sin(ang) + uy * math.cos(ang)
                    wings.append((ex - A * 1.15 * rx, ey - A * 1.15 * ry))
                path.moveTo(wings[0][0] * MM, self._y(wings[0][1]))
                path.lineTo(ex * MM, self._y(ey))
                path.lineTo(wings[1][0] * MM, self._y(wings[1][1]))
                c.drawPath(path, stroke=1, fill=0)
        c.restoreState()

    def draw_instruction(self, text: str, icon: str = "icon_pencil") -> None:
        """Satu gaya instruksi: ikon kecil + kalimat pendek 1 baris (zona tetap). Tampilan = hook skin."""
        if self.record.has_instruction:
            raise ValueError("draw_instruction hanya boleh dipanggil sekali per halaman.")
        self.record.has_instruction = True
        self.skin.draw_instruction_badge(self, text, icon)

    def draw_section_title(self, rect: Rect, text: str, *, size: float = config.FONT_LABEL) -> None:
        """Judul bagian (opsional untuk modul). Tampilan = hook skin; classic = teks tebal berwarna aksen."""
        self.skin.draw_section_title(self, rect, text, size)

    def _draw_icon(self, rect: Rect, icon: str) -> None:
        """Ikon instruksi (dipakai hook badge)."""
        self._log(Element("icon", rect, "system", image=icon))
        self.c.drawImage(str(self.assets.path(icon, self.mode)), rect.x * MM, self._y(rect.bottom),
                         rect.w * MM, rect.h * MM, mask="auto", preserveAspectRatio=True, anchor="c")

    # ---- chrome (header / identitas / footer) -------------------------------
    def _rule(self, y: float, color: str, width: float) -> None:
        self._log(Element("rule", Rect(config.MARGIN_MM, y, SAFE_AREA.w, 0.0), "system"))
        c = self.c
        c.saveState()
        self._stroke(color)
        c.setLineWidth(self._lw(width))
        c.line(config.MARGIN_MM * MM, self._y(y), (config.MARGIN_MM + SAFE_AREA.w) * MM, self._y(y))
        c.restoreState()

    # ---- zona tetap (dipakai skin; nilainya sama dengan perilaku lama) ----------
    @property
    def header_rect(self) -> Rect:
        return Rect(config.MARGIN_MM, config.HEADER_TOP, SAFE_AREA.w, config.HEADER_H - 1.5)

    @property
    def ident_rect(self) -> Rect:
        return Rect(config.MARGIN_MM, config.IDENT_TOP, SAFE_AREA.w, config.IDENT_H)

    @property
    def instr_zone(self) -> Rect:
        return Rect(config.MARGIN_MM, config.INSTR_TOP, SAFE_AREA.w, config.INSTR_H)

    @property
    def footer_rect(self) -> Rect:
        return Rect(config.MARGIN_MM, config.FOOTER_TOP + 1.0, SAFE_AREA.w, config.FOOTER_H - 1.0)

    def _draw_hline(self, x1: float, x2: float, y: float, color: str, width: float) -> None:
        """Garis horizontal sistem (mis. garis nama/tanggal). Tidak dicatat sebagai elemen."""
        c = self.c
        c.saveState()
        self._stroke(color)
        c.setLineWidth(self._lw(width))
        c.line(x1 * MM, self._y(y), x2 * MM, self._y(y))
        c.restoreState()

    def _draw_chrome(self) -> None:
        """Urutan tetap; tampilan tiap bagian ditentukan hook skin aktif."""
        k, s = self.spec.kind, self.skin
        s.draw_page_background(self)
        s.draw_page_frame(self)
        s.draw_corner_decor(self)
        if k in ("module", "toc"):
            s.draw_header(self)
        if k == "module":
            s.draw_name_date_zone(self)
        s.draw_footer(self)
        if k == "module":
            s.draw_reward_sticker_slot(self)

    # ---- primitif dekorasi (HANYA untuk skin; geometri sederhana + PNG skin) -----
    def _safe_fill(self, name: str) -> str:
        """Mode bw: fill gelap otomatis diganti kertas putih (hemat tinta)."""
        if self.theme.is_bw and relative_luminance(self.theme.rgb(name)) < 0.8:
            return "paper"
        return name

    def margin_strips(self, outer: float, inner: float = 0.0) -> List[Rect]:
        """4 strip margin (atas, bawah, kiri, kanan; tanpa tumpang tindih sudut) antara `outer` mm dari
        tepi kertas dan `inner` mm sebelum safe area."""
        W, H, M = config.PAGE_W_MM, config.PAGE_H_MM, config.MARGIN_MM
        t, lo = M - inner - outer, M - inner
        return [Rect(outer, outer, W - 2 * outer, t), Rect(outer, H - lo, W - 2 * outer, t),
                Rect(outer, lo, t, H - 2 * lo), Rect(W - lo, lo, t, H - 2 * lo)]

    def decor_rect(self, rect: Rect, *, color: str = "decor_1", fill: Optional[str] = None, radius: float = 0.0,
                   line_w: float = config.LINE_NORMAL_PT, dashed: bool = False, container: bool = False,
                   hollow: bool = False, zone: str = "decor", kind: str = "decor_box") -> None:
        """Kotak (bersudut bulat). hollow=True dicatat sebagai 4 strip tepi (untuk bingkai)."""
        if hollow:
            t = 0.5
            for r in (Rect(rect.x, rect.y, rect.w, t), Rect(rect.x, rect.bottom - t, rect.w, t),
                      Rect(rect.x, rect.y, t, rect.h), Rect(rect.right - t, rect.y, t, rect.h)):
                self._log(Element("decor_frame", r, zone))
        else:
            self._log(Element(kind, rect, zone, container=container))
        c = self.c
        c.saveState()
        self._stroke(color)
        c.setLineWidth(self._lw(line_w))
        if dashed:
            c.setDash(list(config.GUIDE_DASH))
        if fill:
            self._fill(self._safe_fill(fill))
        c.roundRect(rect.x * MM, self._y(rect.bottom), rect.w * MM, rect.h * MM, radius * MM,
                    stroke=1, fill=1 if fill else 0)
        c.restoreState()

    def decor_line(self, x1: float, y1: float, x2: float, y2: float, *, color: str = "decor_1",
                   line_w: float = config.LINE_NORMAL_PT, dash: Optional[Sequence[float]] = None,
                   round_cap: bool = False, zone: str = "decor") -> None:
        """Garis lurus (mm). dash=(on, off) dalam pt; round_cap + dash kecil = titik-titik."""
        pad = max(0.4, line_w * 0.3528)
        self._log(Element("decor_line", Rect(min(x1, x2) - pad / 2, min(y1, y2) - pad / 2,
                                              abs(x2 - x1) + pad, abs(y2 - y1) + pad), zone))
        c = self.c
        c.saveState()
        self._stroke(color)
        c.setLineWidth(self._lw(line_w))
        if round_cap:
            c.setLineCap(1)
        if dash:
            c.setDash(list(dash))
        c.line(x1 * MM, self._y(y1), x2 * MM, self._y(y2))
        c.restoreState()

    def decor_circle(self, cx: float, cy: float, r: float, *, color: str = "decor_1", fill: Optional[str] = None,
                     line_w: float = config.LINE_NORMAL_PT, dashed: bool = False, zone: str = "decor",
                     kind: str = "decor_circle") -> None:
        """Lingkaran (mm)."""
        self._log(Element(kind, Rect(cx - r, cy - r, 2 * r, 2 * r), zone))
        c = self.c
        c.saveState()
        self._stroke(color)
        c.setLineWidth(self._lw(line_w))
        if dashed:
            c.setDash(list(config.GUIDE_DASH))
        if fill:
            self._fill(self._safe_fill(fill))
        c.circle(cx * MM, self._y(cy), r * MM, stroke=1, fill=1 if fill else 0)
        c.restoreState()

    def decor_wave(self, rect: Rect, *, color: str = "decor_1", amp: float = 0.8, period: float = 8.0,
                   line_w: float = config.LINE_NORMAL_PT, zone: str = "decor") -> None:
        """Garis bergelombang sepanjang rect.w, berpusat di rect.cy."""
        self._log(Element("decor_wave", Rect(rect.x, rect.cy - amp - 0.2, rect.w, 2 * amp + 0.4), zone))
        c = self.c
        c.saveState()
        self._stroke(color)
        c.setLineWidth(self._lw(line_w))
        c.setLineJoin(1)
        path = c.beginPath()
        n = max(2, int(rect.w / 0.8))
        for i in range(n + 1):
            x = rect.x + rect.w * i / n
            y = rect.cy + amp * math.sin(2 * math.pi * (x - rect.x) / period)
            path.moveTo(x * MM, self._y(y)) if i == 0 else path.lineTo(x * MM, self._y(y))
        c.drawPath(path, stroke=1, fill=0)
        c.restoreState()

    def decor_dots(self, rect: Rect, *, step: float = config.SKIN_DOT_STEP_MM, r: float = config.SKIN_DOT_R_MM,
                   color: str = "decor_soft", points: Optional[Sequence[Tuple[float, float, float]]] = None) -> None:
        """Pola titik latar dalam rect (grid, atau `points` = [(x, y, r)] mutlak). Mode bw: DIHILANGKAN."""
        if self.theme.is_bw:
            return
        self._log(Element("decor_dots", rect, "decor"))
        c = self.c
        c.saveState()
        self._fill(color)
        if points is not None:
            for x, y, rr in points:
                c.circle(x * MM, self._y(y), rr * MM, stroke=0, fill=1)
        else:
            nx, ny = max(1, int(rect.w // step)), max(1, int(rect.h // step))
            for i in range(nx):
                for j in range(ny):
                    c.circle((rect.x + (i + 0.5) * rect.w / nx) * MM, self._y(rect.y + (j + 0.5) * rect.h / ny),
                             r * MM, stroke=0, fill=1)
        c.restoreState()

    def decor_image(self, rect: Rect, image_id: str, *, mirror_x: bool = False, mirror_y: bool = False,
                    rotate: int = 0, container: bool = False) -> None:
        """PNG dekorasi dari assets/skins/<skin>/<id>.png (placeholder otomatis), bisa dicerminkan/diputar."""
        self._log(Element("decor_image", rect, "decor", container=container, skin_image=image_id))
        path = self.assets.skin_path(self.skin.name, image_id, self.mode)
        c = self.c
        c.saveState()
        c.translate(rect.cx * MM, self._y(rect.cy))
        if rotate:
            c.rotate(-rotate)
        c.scale(-1 if mirror_x else 1, -1 if mirror_y else 1)
        c.drawImage(str(path), -rect.w * MM / 2, -rect.h * MM / 2, rect.w * MM, rect.h * MM,
                    mask="auto", preserveAspectRatio=True, anchor="c")
        c.restoreState()

    def finish(self) -> PageRecord:
        """Akhiri halaman (dipanggil renderer)."""
        self.c.showPage()
        return self.record
