"""Skin 'classic' = tampilan asli. Semua hook memakai implementasi bawaan BaseSkin (tanpa dekorasi)."""
from __future__ import annotations

from typing import Set

from skins.base import BaseSkin


class ClassicSkin(BaseSkin):
    name = "classic"
    description = "Tampilan asli: bersih, tanpa dekorasi (default; output identik dengan versi sebelum skin)."

    def images(self) -> Set[str]:
        return set()
