"""Kelas abstrak BaseModule. Semua modul worksheet mewarisi kelas ini."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar, Dict, List, Set, Tuple

from core.i18n import Translator
from core.layout import Page


class BaseModule(ABC):
    """Metadata + render satu modul worksheet.

    Atribut wajib (ClassVar): id, title_key, age_range, category, pages.
    Opsional: series (kode pendek di header), sequences (aturan urutan untuk QC).
    """

    id: ClassVar[str]
    title_key: ClassVar[str]            # selalu "<id>.title"
    age_range: ClassVar[Tuple[int, int]]
    category: ClassVar[str]
    pages: ClassVar[int]
    series: ClassVar[str] = ""
    # QC: {"group": (awal, akhir)} -> nilai `group` yang digambar harus berurutan awal..akhir
    sequences: ClassVar[Dict[str, Tuple[Any, Any]]] = {}

    @property
    def series_code(self) -> str:
        return self.series or self.id[:3].upper()

    @abstractmethod
    def images(self, lang: str) -> Set[str]:
        """Semua id PNG (tanpa .png) yang dipakai modul untuk bahasa ini, termasuk ikon."""

    @abstractmethod
    def render(self, page_index: int, ctx: Page) -> None:
        """Gambar halaman ke-`page_index` (0-based) hanya lewat helper `ctx`."""

    def qc_extra(self, lang: str, tr: Translator) -> List[Tuple[str, str]]:
        """Cek khusus modul -> daftar (level 'WARN'|'FAIL', pesan). Default: tidak ada."""
        return []
