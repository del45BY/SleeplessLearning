"""BaseSkin: kelas abstrak skin (tema visual). Setiap hook punya implementasi bawaan = perilaku lama (classic).

Skin hanya boleh:
  * menggambar di margin, header, footer, latar, dan sudut (BUKAN area konten modul);
  * memakai primitif dekorasi milik Page: decor_rect/line/circle/wave/dots/image, margin_strips;
  * memakai NAMA warna dari core/theme.py (tidak ada hex di skin) dan teks dari i18n;
  * memakai PNG di assets/skins/<name>/ (placeholder otomatis) untuk ilustrasi.
Hook dipanggil oleh core/layout.py (Page). Modul tidak tahu skin apa yang aktif.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar, List, Set, Tuple

import config
from core.layout import FONT_BOLD, FONT_REGULAR, Rect, text_width_mm


class BaseSkin(ABC):
    name: ClassVar[str]                  # slug = nama file skin (mis. "garden")
    description: ClassVar[str] = ""

    @abstractmethod
    def images(self) -> Set[str]:
        """Semua id PNG dekorasi yang dipakai skin (tanpa .png), di assets/skins/<name>/."""

    # ---- latar / bingkai / sudut (bawaan: tidak ada) -----------------------------
    def draw_page_background(self, page) -> None:
        """Latar halaman (mis. pola titik di margin). Bawaan: kosong."""

    def draw_page_frame(self, page) -> None:
        """Bingkai halaman di margin. Bawaan: kosong."""

    def draw_corner_decor(self, page) -> None:
        """Hiasan sudut halaman. Bawaan: kosong."""

    # ---- header -----------------------------------------------------------------
    def draw_header(self, page) -> None:
        """Header: judul (kiri), penanda progres (kanan), garis pemisah."""
        hd = page.header_rect
        page.draw_text(page.cell(hd, 0, 9), page.spec.title, size=config.FONT_TITLE, bold=True,
                       color="accent", zone="system", kind="header_title")
        self.draw_progress_marker(page)
        page._rule(config.HEADER_TOP + config.HEADER_H, "accent", config.LINE_THICK_PT)

    def draw_progress_marker(self, page) -> None:
        """Penanda progres/seri di header kanan (bawaan: teks 'KODE n/total')."""
        page.draw_text(page.cell(page.header_rect, 9, 3), page.spec.series_label, size=config.FONT_HEADER_SIDE,
                       align="right", color="muted", zone="system", kind="header_side")

    def draw_reward_sticker_slot(self, page) -> None:
        """Slot stiker/stempel hadiah (hanya halaman modul). Bawaan: tidak ada."""

    # ---- zona identitas ----------------------------------------------------------
    def draw_name_date_zone(self, page) -> None:
        """Nama ____ Tanggal ____ di posisi tetap."""
        ir = page.ident_rect
        for cell, key in ((page.cell(ir, 0, 8), "common.name_label"), (page.cell(ir, 8, 4), "common.date_label")):
            label = page.t(key)
            lab_rect = Rect(cell.x, cell.y, cell.w - config.MIN_WRITE_LINE_MM, cell.h)
            page.draw_text(lab_rect, label, size=config.FONT_IDENT, bold=True, zone="system", kind="identity_label")
            lw = text_width_mm(label, FONT_BOLD, config.FONT_IDENT)
            page._draw_hline(cell.x + lw + 2, cell.right - 1, cell.bottom - 1.0, "line", config.LINE_NORMAL_PT)

    # ---- instruksi & judul bagian ------------------------------------------------
    def draw_instruction_badge(self, page, text: str, icon: str) -> None:
        """Instruksi: ikon kecil + kalimat 1 baris di zona instruksi."""
        z = page.instr_zone
        ic = Rect(z.x, z.y + (z.h - config.ICON_MM) / 2, config.ICON_MM, config.ICON_MM)
        page._draw_icon(ic, icon)
        gap = 3.0
        tr = Rect(ic.right + gap, z.y, z.w - config.ICON_MM - gap, z.h)
        page.draw_text(tr, text, size=config.FONT_INSTRUCTION, bold=True, zone="system", kind="instruction")

    def draw_section_title(self, page, rect: Rect, text: str, size: float) -> None:
        """Judul bagian di dalam rect milik modul. Skin hanya boleh menata gaya teks (+ bullet di dalam rect)."""
        page.draw_text(rect, text, size=size, bold=True, color="accent", kind="section_title")

    # ---- footer -----------------------------------------------------------------
    def draw_footer(self, page) -> None:
        """Footer: garis, brand, lisensi, nomor halaman."""
        page._rule(config.FOOTER_TOP, "line", config.LINE_THIN_PT)
        self.footer_texts(page)

    def footer_texts(self, page) -> None:
        """3 teks footer pada posisi tetap (dipakai skin lain agar posisi teks tetap sama)."""
        fr = page.footer_rect
        page.draw_text(page.cell(fr, 0, 3), config.BRAND_NAME, size=config.FONT_FOOTER, bold=True,
                       color="muted", zone="system", kind="footer_brand")
        page.draw_text(page.cell(fr, 3, 7), page.t("common.license"), size=config.FONT_FOOTER,
                       align="center", color="muted", zone="system", kind="footer_license")
        page.draw_text(page.cell(fr, 10, 2), f"{page.t('common.page')} {page.spec.page_number}",
                       size=config.FONT_FOOTER, bold=True, align="right", color="muted",
                       zone="system", kind="footer_page")

    # ======================================================================
    # Helper bersama untuk skin dekoratif (tidak dipakai classic)
    # ======================================================================
    def frame_tiles(self, clear: float = 0.0) -> List[Tuple[str, Rect]]:
        """Posisi ubin PNG di sepanjang bingkai: [(sisi, Rect)], sisi = top|bottom|left|right.
        Ubin berada di margin (antara bingkai dan safe area) dan sama di semua halaman."""
        W, H = config.PAGE_W_MM, config.PAGE_H_MM
        i, t = config.SKIN_FRAME_INSET_MM, config.SKIN_TILE_MM
        c = i + 2.0 + t / 2                              # jarak pusat ubin dari tepi kertas
        corner = config.SKIN_CORNER_MM + 3.0 + clear
        out: List[Tuple[str, Rect]] = []
        x0, x1 = i + corner, W - i - corner
        n = max(1, int((x1 - x0) // config.SKIN_TILE_STEP_MM))
        for k in range(n):
            x = x0 + (k + 0.5) * (x1 - x0) / n
            out.append(("top", Rect(x - t / 2, c - t / 2, t, t)))
            out.append(("bottom", Rect(x - t / 2, H - c - t / 2, t, t)))
        y0, y1 = i + corner, H - i - corner
        n = max(1, int((y1 - y0) // config.SKIN_TILE_STEP_MM))
        for k in range(n):
            y = y0 + (k + 0.5) * (y1 - y0) / n
            out.append(("left", Rect(c - t / 2, y - t / 2, t, t)))
            out.append(("right", Rect(W - c - t / 2, y - t / 2, t, t)))
        return out

    def corner_images(self, page, image_id: str) -> None:
        """PNG sudut di 4 pojok (dicerminkan), di dalam margin."""
        W, H = config.PAGE_W_MM, config.PAGE_H_MM
        i, c = config.SKIN_FRAME_INSET_MM, config.SKIN_CORNER_MM
        for x, y, mx, my in ((i, i, False, False), (W - i - c, i, True, False),
                             (i, H - i - c, False, True), (W - i - c, H - i - c, True, True)):
            page.decor_image(Rect(x, y, c, c), image_id, mirror_x=mx, mirror_y=my)

    def progress_with_dots(self, page, color: str = "decor_1") -> None:
        """Penanda progres: teks seri + deretan titik (terisi = halaman yang sudah/sedang dikerjakan).
        Menyisakan tempat untuk slot stiker di ujung kanan header (halaman modul)."""
        hd = page.header_rect
        right = hd.right - (config.SKIN_STICKER_MM + 3.0 if page.spec.kind == "module" else 0.0)
        label = page.spec.series_label
        tw = text_width_mm(label, FONT_REGULAR, config.FONT_HEADER_SIDE)
        tr = Rect(right - tw - 0.2, hd.y, tw + 0.2, hd.h)
        page.draw_text(tr, label, size=config.FONT_HEADER_SIDE, align="right", color="muted",
                       zone="system", kind="header_side")
        n = page.module_pages if page.spec.kind == "module" else 0
        if 1 <= n <= 12:
            step, r = config.SKIN_PROGRESS_STEP_MM, config.SKIN_PROGRESS_R_MM
            for i in range(n):
                done = i <= page.page_index
                page.decor_circle(tr.x - 3.0 - r - (n - 1 - i) * step, hd.cy, r, color=color,
                                  fill=color if done else None,
                                  line_w=config.LINE_THICK_PT if done else config.LINE_THIN_PT,
                                  kind="decor_progress")

    def sticker_circle(self, page, color: str = "decor_2") -> None:
        """Slot stiker/stempel hadiah: lingkaran putus-putus di ujung kanan header."""
        hd, d = page.header_rect, config.SKIN_STICKER_MM
        page.decor_circle(hd.right - d / 2, hd.cy, d / 2 - 0.3, color=color, dashed=True,
                          line_w=config.LINE_THICK_PT, kind="decor_sticker")

    def boxed_name_date(self, page, dashed: bool = False) -> None:
        """Zona Nama/Tanggal di dalam kotak rounded (posisi sama dengan classic)."""
        ir = page.ident_rect
        for cell, key in ((page.cell(ir, 0, 8), "common.name_label"), (page.cell(ir, 8, 4), "common.date_label")):
            page.decor_rect(cell, color="decor_1", fill="box_fill", radius=2.0, dashed=dashed, container=True)
            inner = Rect(cell.x + 2.5, cell.y, cell.w - 4.0, cell.h)
            label = page.t(key)
            page.draw_text(Rect(inner.x, inner.y, inner.w - config.MIN_WRITE_LINE_MM, inner.h), label,
                           size=config.FONT_IDENT, bold=True, zone="system", kind="identity_label")
            lw = text_width_mm(label, FONT_BOLD, config.FONT_IDENT)
            page._draw_hline(inner.x + lw + 2, inner.right, cell.bottom - 1.5, "line", config.LINE_NORMAL_PT)

    def badge_instruction(self, page, text: str, icon: str, badge_id: str) -> None:
        """Instruksi dengan badge PNG (ikon modul diletakkan di tengah badge)."""
        z, b_mm = page.instr_zone, config.SKIN_BADGE_MM
        b = Rect(z.x, z.y + (z.h - b_mm) / 2, b_mm, b_mm)
        page.decor_image(b, badge_id, container=True)
        page._draw_icon(b.center_square(config.ICON_MM), icon)
        page.draw_text(Rect(b.right + 3.0, z.y, z.w - b_mm - 3.0, z.h), text, size=config.FONT_INSTRUCTION,
                       bold=True, zone="system", kind="instruction")
