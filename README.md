# worksheet_tool — generator worksheet preschool (usia 3–6)

PDF US Letter (215.9 × 279.4 mm), 6 bahasa (en, id, es, de, fr, pt), mode `color` dan `bw`,
QC otomatis, modul ditambah dengan 1 file + key i18n (core tidak diubah).

## Instal
```bash
python3 -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
Font: salin `DejaVuSans.ttf` dan `DejaVuSans-Bold.ttf` ke `fonts/` agar hasil identik di semua mesin
(jika tidak ada, tool mencari DejaVu/Liberation/Arial di folder font sistem). Opsional: `fonts/Trace.ttf`
untuk font tracing khusus.

## Perintah
```bash
python main.py list                                              # daftar modul
python main.py skins                                             # daftar skin (classic, garden, space)
python main.py build --module tracing_letters --lang id --mode both
python main.py build --all --lang all --mode both               # semua modul x 6 bahasa x 2 mode
python main.py build --category literacy --lang en,id
python main.py bundle --modules tracing_letters,counting_1_10 --lang id --mode both   # cover + daftar isi
python main.py bundle --modules a,b --lang all --no-cover --no-toc --name paket1
python main.py qc                                                # semua modul, semua bahasa, semua mode
python main.py qc --module counting_1_10 --lang id,de --mode bw
python main.py build --module vertical_lines --lang id --mode both --skin garden
python main.py build --all --lang all --mode both --skin all     # semua modul x bahasa x mode x skin
python main.py bundle --modules tracing_letters,counting_1_10 --lang id --skin space
python main.py qc --all --lang all --mode both --skin all
python main.py baseline                                          # rekam ulang baseline classic (hanya bila tata letak sengaja diubah)
python main.py assets                                            # buat placeholder PNG (modul + skin) yang belum ada
```
Opsi umum: `--seed N` (variasi konten deterministik; tanpa seed hasil selalu identik), `--out DIR`, `--no-qc`, `-v`.

Output: `output/{lang}/{skin}/{color|bw}/<id>.pdf`, bundle `bundle_<nama>.pdf`, laporan `output/qc_report.md|json`.
Exit code `1` jika ada FAIL (aman untuk pipeline), `2` untuk salah pemakaian.

## Gambar
Semua gambar = PNG di `assets/images/<id>.png` (ikon juga: `icon_pencil.png`). Jika belum ada, dibuat placeholder
otomatis (kotak abu-abu + nama objek, ditandai di metadata PNG) dan QC melapor WARN. Timpa saja dengan PNG asli
(disarankan RGBA, sisi terpendek ≥ 300 px). Versi bw dibuat otomatis (grayscale + kontras) dan di-cache di `.cache/bw/`.

## Tracing: satu garis putus di tengah goresan
Baris tracing (`ctx.draw_trace_line`, juga untuk kata utuh) memakai stroke font garis-tengah di `core/strokefont.py`
(A–Z, a–z, 0–9). Huruf contoh pertama tetap outline tebal; pengulangan berikutnya = SATU garis putus di tengah goresan.
Atur lewat `config.py`: `TRACE_STYLE` (`"stroke"` | `"outline"` = cara lama), `TRACE_CENTER_STROKE_PT`, `TRACE_CENTER_DASH`.
Karakter di luar set (mis. é, ñ) otomatis memakai outline untuk baris itu dan QC memberi WARN.
Jika memakai font tracing sendiri (`fonts/Trace.ttf`), sesuaikan bentuk di `strokefont.py` atau pakai `"outline"`.

## Skin (tema visual)
`--skin <nama>` (default `classic` = tampilan asli, output identik byte-per-byte dengan sebelum ada skin).
Skin bawaan: `garden` (bingkai daun, header berpita, latar titik lembut, badge bunga) dan `space` (bingkai bintang,
header planet, latar bintang, badge roket). Dekorasi hanya di margin/header/footer/latar/sudut; area konten modul
tidak berubah. Modul lama dan baru otomatis ikut. PNG dekorasi: `assets/skins/<skin>/<id>.png` (placeholder otomatis).
Mode bw: pola latar hilang, aksen jadi outline. Menambah skin: lihat `SKIN_GUIDE.md`. Folder `output/{lang}/{skin}/{mode}/`
menggantikan `output/{lang}/{mode}/` (isi PDF classic tidak berubah).

## Struktur
`config.py` token desain · `core/layout.py` satu-satunya sistem layout · `core/theme.py` semua warna ·
`core/qc.py` QC · `skins/` satu file per skin · `modules/` satu file per modul · `i18n/<lang>.py` semua teks · `MODULES_LOG.md` otomatis.
Menambah modul: lihat `ADD_MODULE_GUIDE.md`.

## Catatan desain
* Layout dalam mm dari kiri-atas, grid 12 kolom, margin 15 mm. Modul hanya memakai helper `ctx.*`.
* QC bekerja dari log elemen yang dicatat helper (bbox, teks, gambar, warna) + pemeriksaan PDF lewat `pypdf`.
* Key i18n yang hilang di bahasa target: runtime fallback ke `en` + warning, tetapi QC menandainya **FAIL**.
* Tanpa jaringan: tidak ada layanan online.
