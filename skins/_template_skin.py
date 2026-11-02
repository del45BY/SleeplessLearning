"""TEMPLATE skin baru. Salin -> skins/<nama>.py, ubah `name` (HARUS = nama file, snake_case). File berawalan '_'
tidak ikut ter-registrasi.

ATURAN (lihat SKIN_GUIDE.md):
  * Hanya override hook yang perlu; hook yang tidak di-override = perilaku classic (tanpa dekorasi).
  * Gambar HANYA lewat PNG (page.decor_image) di assets/skins/<name>/<id>.png; placeholder dibuat otomatis.
    Bentuk geometris sederhana (garis, kotak rounded, lingkaran, gelombang, titik) boleh lewat primitif Page.
  * Warna = NAMA dari core/theme.py. Palet skin ditambahkan di core/theme.py (SKIN_COLORS dan SKIN_BW), BUKAN di sini.
    Nama tersedia: paper ink muted line guide guide_soft trace accent accent_soft model_fill
                   decor_1 decor_2 decor_soft ribbon_fill box_fill
  * Teks hanya lewat i18n (page.t) / data halaman (page.spec.title). Jangan hardcode kalimat.
  * Dekorasi hanya di margin, header, footer, latar, sudut. JANGAN menyentuh page.content (area konten modul).
    Elemen yang menutupi teks sistem (mis. pita di belakang judul) harus container=True dan memuat teksnya.
  * Mode bw: pola latar hilang otomatis (decor_dots), fill gelap otomatis jadi putih; buat aksen sebagai OUTLINE.
  * Pola harus sama di semua halaman satu seri (jangan pakai nomor halaman untuk posisi dekorasi;
    satu-satunya yang boleh berubah = penanda progres, kind="decor_progress").
  * Jangan mengubah posisi/ukuran zona (page.header_rect, ident_rect, instr_zone, footer_rect) di luar yang
    diperlukan; teks harus tetap muat untuk 6 bahasa (QC memeriksa).
Perintah uji: python main.py qc --module <id> --skin <nama> --lang all --mode both
"""
from __future__ import annotations

from typing import Set

import config
from core.layout import Rect
from skins.base import BaseSkin


class MySkin(BaseSkin):
    name = "my_skin"                       # = nama file tanpa .py
    description = "Satu kalimat tentang gaya skin ini."

    def images(self) -> Set[str]:          # semua PNG dekorasi yang dipakai (assets/skins/my_skin/<id>.png)
        return {"corner_art"}

    # Latar: titik/pola di margin saja. page.margin_strips(outer, inner) -> 4 strip margin.
    def draw_page_background(self, page) -> None:
        for strip in page.margin_strips(outer=config.SKIN_FRAME_INSET_MM + 1.5, inner=1.0):
            page.decor_dots(strip, color="decor_soft")

    # Bingkai: garis di margin (hollow=True agar QC mengecek tepinya, bukan kotak penuh).
    def draw_page_frame(self, page) -> None:
        i = config.SKIN_FRAME_INSET_MM
        page.decor_rect(Rect(i, i, config.PAGE_W_MM - 2 * i, config.PAGE_H_MM - 2 * i),
                        color="decor_1", radius=4.0, hollow=True)

    # Sudut: PNG di 4 pojok (dicerminkan otomatis).
    def draw_corner_decor(self, page) -> None:
        self.corner_images(page, "corner_art")

    # Hook lain yang bisa di-override (bawaan = classic):
    #   draw_header, draw_progress_marker, draw_footer, draw_name_date_zone,
    #   draw_instruction_badge, draw_section_title, draw_reward_sticker_slot
    # Helper siap pakai di BaseSkin: progress_with_dots, sticker_circle, boxed_name_date,
    #   badge_instruction, frame_tiles, corner_images, footer_texts.
