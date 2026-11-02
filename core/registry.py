"""Auto-discover modul di folder modules/ (tanpa daftar manual)."""
from __future__ import annotations

import difflib
import importlib
import inspect
import logging
import pkgutil
import re
from datetime import date
from typing import Dict, List, Optional

import config
from core.i18n import lookup
from modules.base import BaseModule
from skins.base import BaseSkin

log = logging.getLogger(__name__)
_REGISTRY: Optional[Dict[str, BaseModule]] = None
_ERRORS: List[str] = []
ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")


class ModuleNotFound(KeyError):
    pass


def validate(m: BaseModule) -> List[str]:
    """Periksa metadata modul; kembalikan daftar masalah."""
    p: List[str] = []
    cls = type(m).__name__
    for attr in ("id", "title_key", "age_range", "category", "pages"):
        if not hasattr(m, attr):
            p.append(f"{cls}: atribut '{attr}' belum didefinisikan")
    if p:
        return p
    if not ID_RE.match(m.id):
        p.append(f"{cls}: id '{m.id}' harus snake_case huruf kecil")
    if m.title_key != f"{m.id}.title":
        p.append(f"{cls}: title_key harus '{m.id}.title'")
    if not (isinstance(m.pages, int) and m.pages >= 1):
        p.append(f"{cls}: pages harus integer >= 1")
    a = m.age_range
    if not (isinstance(a, tuple) and len(a) == 2 and 2 <= a[0] <= a[1] <= 8):
        p.append(f"{cls}: age_range harus tuple (min, max) dalam 2..8")
    if not m.category or not re.match(r"^[a-z][a-z0-9_]*$", m.category):
        p.append(f"{cls}: category harus snake_case")
    return p


def discover(reload: bool = False) -> Dict[str, BaseModule]:
    """Impor semua file modules/*.py (kecuali base & yang diawali '_') dan daftarkan subclass-nya."""
    global _REGISTRY
    if _REGISTRY is not None and not reload:
        return _REGISTRY
    import modules as pkg
    reg: Dict[str, BaseModule] = {}
    _ERRORS.clear()
    for info in sorted(pkgutil.iter_modules(pkg.__path__), key=lambda i: i.name):
        if info.name.startswith("_") or info.name == "base":
            continue
        try:
            mod = importlib.reload(importlib.import_module(f"modules.{info.name}")) if reload \
                else importlib.import_module(f"modules.{info.name}")
        except Exception as exc:  # modul rusak tidak boleh mematikan seluruh tool
            _ERRORS.append(f"modules/{info.name}.py gagal diimpor: {exc!r}")
            continue
        found = [c for _, c in inspect.getmembers(mod, inspect.isclass)
                 if issubclass(c, BaseModule) and c is not BaseModule
                 and c.__module__ == mod.__name__ and not inspect.isabstract(c)]
        if not found:
            _ERRORS.append(f"modules/{info.name}.py tidak berisi subclass BaseModule yang lengkap")
        for cls in found:
            inst = cls()
            problems = validate(inst)
            if problems:
                _ERRORS.extend(problems)
                continue
            if inst.id in reg:
                _ERRORS.append(f"id ganda '{inst.id}' di modules/{info.name}.py")
                continue
            reg[inst.id] = inst
    _REGISTRY = reg
    return reg


def errors() -> List[str]:
    discover()
    return list(_ERRORS)


def all_modules() -> List[BaseModule]:
    return [m for _, m in sorted(discover().items())]


def categories() -> List[str]:
    return sorted({m.category for m in all_modules()})


def by_category(name: str) -> List[BaseModule]:
    mods = [m for m in all_modules() if m.category == name]
    if not mods:
        raise ModuleNotFound(f"Kategori '{name}' tidak ada. Pilihan: {', '.join(categories()) or '(kosong)'}")
    return mods


def get_module(module_id: str) -> BaseModule:
    reg = discover()
    if module_id not in reg:
        hint = difflib.get_close_matches(module_id, list(reg), n=3)
        extra = f" Maksud Anda: {', '.join(hint)}?" if hint else ""
        raise ModuleNotFound(f"Modul '{module_id}' tidak ditemukan.{extra} Jalankan `python main.py list`.")
    return reg[module_id]


def sync_log(modules: List[BaseModule]) -> List[str]:
    """Tambahkan entri ke MODULES_LOG.md untuk modul yang belum tercatat. Return id yang ditambahkan."""
    path = config.LOG_FILE
    text = path.read_text(encoding="utf-8") if path.is_file() else (
        "# MODULES_LOG\n\nCatatan modul worksheet. Entri ditambahkan otomatis saat QC modul lulus.\n\n")
    added: List[str] = []
    for m in modules:
        if f"`{m.id}`" in text:
            continue
        title = lookup("en", m.title_key) or m.id
        text += (f"- `{m.id}` — {title} · {m.category} · usia {m.age_range[0]}–{m.age_range[1]} · "
                 f"{m.pages} halaman · ditambahkan {date.today().isoformat()}\n")
        added.append(m.id)
    if added:
        path.write_text(text, encoding="utf-8")
    return added


# ---------------------------------------------------------------------------
# Skin (auto-discover dari skins/*.py, kecuali base dan yang diawali '_')
# ---------------------------------------------------------------------------
_SKINS: Optional[Dict[str, BaseSkin]] = None
_SKIN_ERRORS: List[str] = []


def discover_skins(reload: bool = False) -> Dict[str, BaseSkin]:
    """Impor semua skins/*.py dan daftarkan subclass BaseSkin yang lengkap."""
    global _SKINS
    if _SKINS is not None and not reload:
        return _SKINS
    import skins as pkg
    reg: Dict[str, BaseSkin] = {}
    _SKIN_ERRORS.clear()
    for info in sorted(pkgutil.iter_modules(pkg.__path__), key=lambda i: i.name):
        if info.name.startswith("_") or info.name == "base":
            continue
        try:
            mod = importlib.import_module(f"skins.{info.name}")
            if reload:
                mod = importlib.reload(mod)
        except Exception as exc:
            _SKIN_ERRORS.append(f"skins/{info.name}.py gagal diimpor: {exc!r}")
            continue
        found = [c for _, c in inspect.getmembers(mod, inspect.isclass)
                 if issubclass(c, BaseSkin) and c is not BaseSkin and c.__module__ == mod.__name__
                 and not inspect.isabstract(c)]
        if not found:
            _SKIN_ERRORS.append(f"skins/{info.name}.py tidak berisi subclass BaseSkin yang lengkap")
        for cls in found:
            inst = cls()
            name = getattr(inst, "name", "")
            if not ID_RE.match(name or ""):
                _SKIN_ERRORS.append(f"{cls.__name__}: name '{name}' harus snake_case huruf kecil")
            elif name != info.name:
                _SKIN_ERRORS.append(f"{cls.__name__}: name '{name}' harus sama dengan nama file '{info.name}'")
            elif name in reg:
                _SKIN_ERRORS.append(f"nama skin ganda '{name}'")
            else:
                reg[name] = inst
    if config.DEFAULT_SKIN not in reg:
        _SKIN_ERRORS.append(f"skin default '{config.DEFAULT_SKIN}' tidak ditemukan di skins/")
    _SKINS = reg
    return reg


def skin_errors() -> List[str]:
    discover_skins()
    return list(_SKIN_ERRORS)


def all_skins() -> List[BaseSkin]:
    return [s for _, s in sorted(discover_skins().items())]


def get_skin(name: str) -> BaseSkin:
    reg = discover_skins()
    if name not in reg:
        hint = difflib.get_close_matches(name, list(reg), n=3)
        extra = f" Maksud Anda: {', '.join(hint)}?" if hint else ""
        raise ModuleNotFound(f"Skin '{name}' tidak ditemukan.{extra} Jalankan `python main.py skins`.")
    return reg[name]
