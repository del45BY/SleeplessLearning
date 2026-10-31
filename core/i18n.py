"""Loader bahasa + fallback ke `en` + pencatatan event untuk QC.

File bahasa: i18n/<lang>.py berisi dict `STRINGS` datar dengan key bertitik,
mis. "common.name_label", "tracing_letters.title".
"""
from __future__ import annotations

import importlib
import logging
from dataclasses import dataclass
from typing import Dict, List

import config

log = logging.getLogger(__name__)
_CACHE: Dict[str, Dict[str, str]] = {}


class I18nError(RuntimeError):
    """File bahasa tidak ada / rusak."""


@dataclass(frozen=True)
class I18nEvent:
    kind: str   # "fallback" | "missing" | "empty" | "format"
    key: str


def clear_cache() -> None:
    """Buang cache (dipakai tes / setelah file bahasa berubah)."""
    _CACHE.clear()


def load_language(lang: str) -> Dict[str, str]:
    """Muat dict string untuk satu bahasa."""
    if lang in _CACHE:
        return _CACHE[lang]
    if lang not in config.LANGS:
        raise I18nError(f"Bahasa '{lang}' tidak didukung. Pilihan: {', '.join(config.LANGS)}")
    try:
        mod = importlib.import_module(f"i18n.{lang}")
    except ModuleNotFoundError as exc:
        raise I18nError(f"File bahasa i18n/{lang}.py tidak ditemukan ({exc}).") from exc
    strings = getattr(mod, "STRINGS", None)
    if not isinstance(strings, dict):
        raise I18nError(f"i18n/{lang}.py harus punya dict bernama STRINGS.")
    _CACHE[lang] = dict(strings)
    return _CACHE[lang]


def lookup(lang: str, key: str) -> str:
    """Ambil string tanpa mencatat event (fallback ke en bila perlu). Dipakai module.images()."""
    s = load_language(lang).get(key)
    if s:
        return s
    return load_language(config.FALLBACK_LANG).get(key, "")


class Translator:
    """Penerjemah per bahasa; mencatat key yang dipakai/fallback agar QC bisa melapor."""

    def __init__(self, lang: str) -> None:
        self.lang = lang
        self.strings = load_language(lang)
        self.fallback = load_language(config.FALLBACK_LANG)
        self.events: List[I18nEvent] = []

    def has(self, key: str) -> bool:
        return bool(self.strings.get(key))

    def t(self, key: str, **fmt: object) -> str:
        text = self.strings.get(key)
        if text is None or text == "":
            if text == "":
                self.events.append(I18nEvent("empty", key))
            fb = self.fallback.get(key)
            if fb:
                if text is None:
                    self.events.append(I18nEvent("fallback", key))
                    log.warning("i18n: key '%s' tidak ada di '%s', pakai '%s'", key, self.lang, config.FALLBACK_LANG)
                text = fb
            else:
                self.events.append(I18nEvent("missing", key))
                log.warning("i18n: key '%s' tidak ada di bahasa mana pun", key)
                return f"[[{key}]]"
        if fmt:
            try:
                text = text.format(**fmt)
            except (KeyError, IndexError):
                self.events.append(I18nEvent("format", key))
        return text
