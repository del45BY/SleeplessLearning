"""Resolver gambar PNG + auto-placeholder + konversi bw (di-cache)."""
from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps
from PIL.PngImagePlugin import PngInfo

import config

log = logging.getLogger(__name__)
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_]*$")
PLACEHOLDER_TAG = "ws_placeholder"


class AssetError(RuntimeError):
    """Gambar tidak bisa disediakan."""


@dataclass(frozen=True)
class ImageInfo:
    image_id: str
    path: Path
    exists: bool
    placeholder: bool = False
    width: int = 0
    height: int = 0
    has_alpha: bool = False


def _load_font(size: int):
    p = config.find_font_file(config.FONT_CANDIDATES["bold"])
    if p:
        return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def make_placeholder(path: Path, image_id: str) -> None:
    """Buat PNG transparan 1000x1000: kotak abu-abu + nama objek (deterministik)."""
    n = config.PLACEHOLDER_PX
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    m = int(n * 0.06)
    d.rounded_rectangle((m, m, n - m, n - m), radius=int(n * 0.06),
                        fill=(232, 232, 232, 255), outline=(140, 140, 140, 255), width=10)
    lines = image_id.replace("_", " ").split()
    size = 150
    font = _load_font(size)
    while size > 24:
        font = _load_font(size)
        widths = [d.textlength(w, font=font) for w in lines]
        if max(widths) <= n * 0.74 and size * 1.25 * len(lines) <= n * 0.7:
            break
        size -= 6
    y = (n - size * 1.25 * len(lines)) / 2
    for w in lines:
        tw = d.textlength(w, font=font)
        d.text(((n - tw) / 2, y), w, font=font, fill=(90, 90, 90, 255))
        y += size * 1.25
    info = PngInfo()
    info.add_text(PLACEHOLDER_TAG, "1")
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, pnginfo=info)
    log.info("Placeholder dibuat: %s", path.name)


class AssetResolver:
    """Cari PNG berdasarkan id (mis. 'apple' -> assets/images/apple.png)."""

    def __init__(self, images_dir: Optional[Path] = None, cache_dir: Optional[Path] = None,
                 auto_placeholder: bool = True) -> None:
        self.images_dir = Path(images_dir or config.IMAGES_DIR)
        self.cache_dir = Path(cache_dir or config.CACHE_DIR) / "bw"
        self.auto_placeholder = auto_placeholder

    def source_path(self, image_id: str) -> Path:
        """Path PNG asli; membuat placeholder jika belum ada (kecuali dimatikan)."""
        if not SLUG_RE.match(image_id or ""):
            raise AssetError(f"Nama gambar tidak valid: {image_id!r} (huruf kecil, angka, underscore).")
        p = self.images_dir / f"{image_id}.png"
        if not p.is_file():
            if not self.auto_placeholder:
                raise AssetError(f"Gambar tidak ditemukan: {p}")
            make_placeholder(p, image_id)
        return p

    def path(self, image_id: str, mode: str) -> Path:
        """Path gambar siap pakai (bw = grayscale kontras tinggi, di-cache)."""
        src = self.source_path(image_id)
        if mode != "bw":
            return src
        st = src.stat()
        key = f"{src.resolve()}|{st.st_mtime_ns}|{st.st_size}|{config.BW_CONTRAST}|{config.BW_BRIGHTNESS}"
        out = self.cache_dir / f"{image_id}_{hashlib.sha1(key.encode()).hexdigest()[:10]}.png"
        if not out.is_file():
            self._to_bw(src, out)
        return out

    @staticmethod
    def _to_bw(src: Path, out: Path) -> None:
        im = Image.open(src).convert("RGBA")
        alpha = im.getchannel("A")
        gray = ImageOps.autocontrast(im.convert("L"), cutoff=2)
        gray = ImageEnhance.Contrast(gray).enhance(config.BW_CONTRAST)
        gray = ImageEnhance.Brightness(gray).enhance(config.BW_BRIGHTNESS)
        out.parent.mkdir(parents=True, exist_ok=True)
        Image.merge("RGBA", (gray, gray, gray, alpha)).save(out)

    def info(self, image_id: str) -> ImageInfo:
        """Metadata gambar untuk QC."""
        try:
            p = self.source_path(image_id)
        except AssetError:
            return ImageInfo(image_id, self.images_dir / f"{image_id}.png", False)
        with Image.open(p) as im:
            alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
            tagged = im.info.get(PLACEHOLDER_TAG) == "1"
            return ImageInfo(image_id, p, True, tagged, im.width, im.height, alpha)

    @staticmethod
    def is_gray_image(path: Path) -> bool:
        """True jika semua piksel R=G=B (dipakai QC mode bw)."""
        with Image.open(path) as im:
            r, g, b = im.convert("RGB").split()
            return ImageChops.difference(r, g).getbbox() is None and ImageChops.difference(g, b).getbbox() is None
