"""TEMPLATE modul baru. Salin file ini -> modules/<id>.py, lalu ubah. Diawali '_' jadi TIDAK ikut ter-registrasi.

Aturan:
  * Hanya boleh menaruh elemen lewat helper `ctx` (lihat core/layout.py, kelas Page).
  * Tidak ada teks hardcode: semua lewat ctx.t("<id>.<key>") + key di SEMUA file i18n/*.py.
  * Tidak ada warna/ukuran/angka desain acak: pakai token di config.py (ukuran slot "S"/"M"/"L"/"XL").
  * Semua PNG yang dipakai (termasuk ikon) WAJIB terdaftar di images().
  * Beri `group`/`value` pada item berurutan agar QC bisa cek urutan dan duplikasi.

Key i18n yang dibutuhkan contoh ini (tempel ke tiap i18n/<lang>.py, terjemahkan, jangan kosong/TODO):
    STRINGS.update({
        "match_shapes.title": "Match the Shapes",
        "match_shapes.instruction": "Draw a line to the matching shape.",
        "match_shapes.shape.circle": "circle",
        "match_shapes.shape.square": "square",
        "match_shapes.shape.triangle": "triangle",
    })
Perintah uji:  python main.py qc --module match_shapes
"""
from __future__ import annotations

from typing import List, Set, Tuple

from core.i18n import Translator
from core.layout import Page
from modules.base import BaseModule


class MatchShapes(BaseModule):
    # --- metadata (semua wajib) -------------------------------------------------
    id = "match_shapes"                  # snake_case, unik, = nama file
    title_key = "match_shapes.title"     # selalu "<id>.title"
    age_range = (3, 5)                   # (usia min, usia maks)
    category = "shapes"                  # dipakai oleh: build --category shapes
    pages = 1                            # jumlah halaman; render() dipanggil sebanyak ini
    series = "SHP"                       # kode di header kanan (opsional)
    sequences: dict = {}                 # contoh: {"number": (1, 10)} -> QC cek berurutan

    SHAPES = ["circle", "square", "triangle"]

    # --- kebutuhan gambar (nama file PNG di assets/images/, tanpa .png) ----------
    def images(self, lang: str) -> Set[str]:
        return {f"shape_{s}" for s in self.SHAPES} | {"icon_pencil"}

    # --- render satu halaman -----------------------------------------------------
    def render(self, page_index: int, ctx: Page) -> None:
        ctx.draw_instruction(ctx.t("match_shapes.instruction"), icon="icon_pencil")  # WAJIB, sekali
        for i, shape in enumerate(self.SHAPES):
            band = ctx.band(i, len(self.SHAPES), gap=6.0)       # pita horizontal ke-i
            ctx.draw_box(band)                                   # kontainer
            inner = band.inset(3.0)
            left, label, right = ctx.cell(inner, 0, 3), ctx.cell(inner, 3, 3), ctx.cell(inner, 9, 3)
            ctx.draw_image_slot(left, f"shape_{shape}", "M")     # token ukuran: S/M/L/XL
            ctx.draw_text(label, ctx.t(f"match_shapes.shape.{shape}"), bold=True)
            ctx.draw_image_slot(right, f"shape_{shape}", "M")

    # --- cek khusus modul (opsional) ---------------------------------------------
    def qc_extra(self, lang: str, tr: Translator) -> List[Tuple[str, str]]:
        return []                        # contoh: [("FAIL", "pesan")] bila ada aturan konten yang dilanggar
