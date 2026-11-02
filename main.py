#!/usr/bin/env python3
"""CLI generator worksheet preschool.

  python main.py list                      daftar modul
  python main.py skins                     daftar skin (tema visual)
  python main.py build --module tracing_letters --lang id --mode both [--skin garden|space|classic|all]
  python main.py build --all --lang all --mode both --skin all
  python main.py bundle --modules tracing_letters,counting_1_10 --lang id --mode both --skin garden
  python main.py qc [--module ID | --all] [--lang xx|all] [--mode color|bw|both] [--skin NAMA|all]
  python main.py baseline                  simpan baseline tata letak skin classic (untuk cek regresi QC)
  python main.py assets                    buat placeholder PNG (modul + skin) yang belum ada

Output: output/{lang}/{skin}/{color|bw}/<id>.pdf
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

import config
from core import registry
from core.assets import AssetResolver
from core.bundle import build_bundle
from core.i18n import I18nError, lookup
from core.qc import QCReport, run_qc, write_baseline
from core.renderer import RenderResult, Renderer
from modules.base import BaseModule

log = logging.getLogger("worksheet")


def _langs(v: str) -> List[str]:
    if v == "all":
        return list(config.LANGS)
    bad = [x for x in v.split(",") if x not in config.LANGS]
    if bad:
        raise SystemExit(f"Bahasa tidak dikenal: {bad}. Pilihan: {', '.join(config.LANGS)}, all")
    return v.split(",")


def _modes(v: str) -> List[str]:
    if v == "both":
        return list(config.MODES)
    if v not in config.MODES:
        raise SystemExit(f"Mode tidak dikenal: {v!r}. Pilihan: color, bw, both")
    return [v]


def _skins(v: str) -> List[str]:
    if v == "all":
        return [s.name for s in registry.all_skins()]
    return [registry.get_skin(n).name for n in v.split(",")]


def _select(args: argparse.Namespace) -> List[BaseModule]:
    if getattr(args, "all", False):
        mods = registry.all_modules()
    elif getattr(args, "category", None):
        mods = registry.by_category(args.category)
    elif getattr(args, "module", None):
        mods = [registry.get_module(i) for i in args.module.split(",")]
    else:
        raise SystemExit("Pilih salah satu: --module <id>, --all, atau --category <nama>")
    if not mods:
        raise SystemExit("Tidak ada modul. Tambahkan file di modules/ (lihat ADD_MODULE_GUIDE.md).")
    return mods


def _finish_qc(rep: QCReport, mods: List[BaseModule]) -> int:
    md, _ = rep.write(config.OUTPUT_DIR)
    print(rep.console())
    print(f"Laporan: {md}")
    if rep.exit_code == 0:
        added = registry.sync_log([m for m in mods if rep.status(m.id) != "FAIL"])
        if added:
            print(f"MODULES_LOG.md diperbarui: {', '.join(added)}")
    return rep.exit_code


def cmd_list(args: argparse.Namespace) -> int:
    print(f"{'ID':<22}{'KATEGORI':<12}{'USIA':<7}{'HAL':<5}JUDUL (en)")
    for m in registry.all_modules():
        print(f"{m.id:<22}{m.category:<12}{m.age_range[0]}-{m.age_range[1]:<5}{m.pages:<5}{lookup('en', m.title_key)}")
    for e in registry.errors():
        print(f"! {e}", file=sys.stderr)
    return 0


def cmd_skins(args: argparse.Namespace) -> int:
    a = AssetResolver()
    print(f"{'SKIN':<12}{'PNG':<5}{'PLACEHOLDER':<13}DESKRIPSI")
    for s in registry.all_skins():
        ph = sum(1 for i in s.images() if a.skin_info(s.name, i).placeholder) if (config.SKINS_DIR / s.name).is_dir() else "-"
        mark = " (default)" if s.name == config.DEFAULT_SKIN else ""
        print(f"{s.name:<12}{len(s.images()):<5}{ph!s:<13}{s.description}{mark}")
    for e in registry.skin_errors():
        print(f"! {e}", file=sys.stderr)
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    mods, langs, modes, skins = _select(args), _langs(args.lang), _modes(args.mode), _skins(args.skin)
    out = Path(args.out or config.OUTPUT_DIR)
    results: List[RenderResult] = []
    for m in mods:
        for skin in skins:
            for lang in langs:
                for mode in modes:
                    r = Renderer(lang, mode, args.seed, skin=skin).render([m], out / lang / skin / mode / f"{m.id}.pdf")
                    results.append(r)
                    print(f"OK  {r.path}  ({r.expected_pages} hal)")
    if args.no_qc:
        return 1 if any(r.errors for r in results) else 0
    return _finish_qc(run_qc(mods, langs, modes, results=results, out_dir=out, write=False, skins=skins), mods)


def cmd_bundle(args: argparse.Namespace) -> int:
    ids = [i.strip() for i in args.modules.split(",") if i.strip()]
    langs, modes, skins = _langs(args.lang), _modes(args.mode), _skins(args.skin)
    out = Path(args.out or config.OUTPUT_DIR)
    results = []
    for skin in skins:
        for lang in langs:
            for mode in modes:
                r = build_bundle(ids, lang, mode, name=args.name, title=args.title, cover=not args.no_cover,
                                 toc=not args.no_toc, seed=args.seed, out_dir=out, skin=skin)
                results.append(r)
                print(f"OK  {r.path}  ({r.expected_pages} hal)")
    if args.no_qc:
        return 0
    return _finish_qc(run_qc([registry.get_module(i) for i in ids], langs, modes, results=results,
                             out_dir=out, write=False, skins=skins), [])


def cmd_qc(args: argparse.Namespace) -> int:
    mods = _select(args) if (args.module or args.all or args.category) else registry.all_modules()
    rep = run_qc(mods, _langs(args.lang), _modes(args.mode), seed=args.seed, write=False, skins=_skins(args.skin))
    return _finish_qc(rep, mods)


def cmd_baseline(args: argparse.Namespace) -> int:
    results = [Renderer(lang, "color", skin=config.DEFAULT_SKIN).render([m], config.OUTPUT_DIR / "_baseline_tmp" / f"{m.id}_{lang}.pdf")
               for m in registry.all_modules() for lang in config.LANGS]
    path = write_baseline(results)
    import shutil
    shutil.rmtree(config.OUTPUT_DIR / "_baseline_tmp", ignore_errors=True)
    print(f"Baseline classic ditulis: {path} ({len(results)} entri)")
    return 0


def cmd_assets(args: argparse.Namespace) -> int:
    a, n = AssetResolver(), 0
    for m in registry.all_modules():
        for lang in config.LANGS:
            for img in sorted(m.images(lang)):
                if not (a.images_dir / f"{img}.png").is_file():
                    a.source_path(img)
                    n += 1
    for s in registry.all_skins():
        for img in sorted(s.images()):
            if not (a.skins_dir / s.name / f"{img}.png").is_file():
                a.skin_source(s.name, img)
                n += 1
    print(f"{n} placeholder dibuat di {a.images_dir} dan {a.skins_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="main.py", description="Generator worksheet preschool (PDF Letter).")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--lang", default="en", help="en|id|es|de|fr|pt|all atau daftar dipisah koma")
        sp.add_argument("--mode", default="both", help="color|bw|both")
        sp.add_argument("--skin", default=config.DEFAULT_SKIN, help="nama skin | daftar dipisah koma | all")
        sp.add_argument("--seed", type=int, default=None, help="seed variasi konten (tanpa seed = tetap)")
        sp.add_argument("--out", default=None, help="folder output (default: output/)")

    sub.add_parser("list", help="daftar modul").set_defaults(fn=cmd_list)
    sub.add_parser("skins", help="daftar skin").set_defaults(fn=cmd_skins)
    b = sub.add_parser("build", help="build modul ke PDF")
    b.add_argument("--module", help="id modul (boleh dipisah koma)")
    b.add_argument("--all", action="store_true")
    b.add_argument("--category")
    b.add_argument("--no-qc", action="store_true")
    common(b)
    b.set_defaults(fn=cmd_build)

    g = sub.add_parser("bundle", help="gabung modul jadi 1 PDF")
    g.add_argument("--modules", required=True, help="a,b,c")
    g.add_argument("--name"), g.add_argument("--title")
    g.add_argument("--no-cover", action="store_true"), g.add_argument("--no-toc", action="store_true")
    g.add_argument("--no-qc", action="store_true")
    common(g)
    g.set_defaults(fn=cmd_bundle)

    q = sub.add_parser("qc", help="quality control")
    q.add_argument("--module"), q.add_argument("--all", action="store_true"), q.add_argument("--category")
    common(q)
    q.set_defaults(fn=cmd_qc)
    sub.add_parser("baseline", help="simpan baseline tata letak classic").set_defaults(fn=cmd_baseline)
    sub.add_parser("assets", help="buat placeholder PNG").set_defaults(fn=cmd_assets)
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING,
                        format="%(levelname)s %(name)s: %(message)s")
    try:
        return args.fn(args)
    except (registry.ModuleNotFound, I18nError) as exc:
        print(f"Error: {exc.args[0] if exc.args else exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
