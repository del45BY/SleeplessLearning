# ADD_MODULE_GUIDE — aturan untuk AI saat diminta menambah modul

Perintah pengguna: `Tambahkan modul: <judul>, usia <x-y>, <jumlah> halaman`.
Turunkan sendiri: `id` (snake_case dari judul, mis. "Match the Shapes" → `match_shapes`), `category`
(pakai yang sudah ada di `python main.py list` bila cocok: literacy, math, shapes, …), isi halaman, dan teks.
**Jangan mengubah `core/` atau `config.py`.** Bila butuh token baru (mis. ukuran slot), tanyakan dulu.

## Alur wajib
1. **Baca** `modules/_template.py` dan `core/layout.py` (kelas `Page` + docstring helper). Lihat juga satu modul contoh.
2. **Buat** `modules/<id>.py` dari template: metadata (`id`, `title_key="<id>.title"`, `age_range`, `category`, `pages`, `series`).
   `render(page_index, ctx)` harus memanggil `ctx.draw_instruction(...)` tepat sekali, lalu menaruh elemen **hanya** lewat
   `ctx.band / ctx.cell / draw_image_slot / draw_trace_line / draw_vertical_line / draw_horizontal_line / draw_diagonal_line / draw_zigzag_line / draw_curved_line / draw_writing_lines / draw_box / draw_text`.
3. **Tambah key i18n ke SEMUA** `i18n/{en,id,es,de,fr,pt}.py` sebagai blok `STRINGS.update({...})` di bawah file.
   Key wajib: `<id>.title`, `<id>.instruction` (1 baris, pendek), plus semua label/kata. Terjemahan harus nyata
   (bukan kosong, bukan TODO). Inggris = US, Spanyol = netral. Kata bergantung bahasa (kata contoh, huruf awal,
   nama angka) disimpan di i18n, bukan di modul. Jerman/Spanyol/Prancis lebih panjang: jaga teks tetap pendek.
4. **Daftarkan gambar** di `images(lang)`: set id PNG (tanpa `.png`, huruf kecil/angka/underscore), termasuk ikon.
   Jangan menggambar ilustrasi lewat kode. Placeholder dibuat otomatis (QC: WARN, itu wajar).
5. **Jalankan** `python main.py qc --module <id>` (semua bahasa & mode).
6. **Perbaiki sampai tidak ada FAIL.** Panduan cepat:
   * "Teks … melebihi kotak" → persingkat teks di bahasa itu atau beri sel lebih lebar (`span` lebih besar).
   * "lebih besar dari selnya" → sel lebih kecil dari token (mis. slot `L` = 34 mm, baris tracing = 22 mm); perbesar sel/band.
   * "saling menimpa" → rapikan pembagian sel; kotak `draw_box` boleh membungkus anak yang sepenuhnya di dalamnya.
   * "tidak dideklarasikan di images()" → tambahkan id gambar ke `images()`.
   * Urutan/duplikasi → beri `group=` dan `value=` pada item berurutan dan isi `sequences = {"group": (awal, akhir)}`.
   * Aturan konten khusus → override `qc_extra(lang, tr)` mengembalikan `[("FAIL"|"WARN", pesan)]`.
7. **Catat** di `MODULES_LOG.md`: entri ditambahkan otomatis saat QC modul lulus tanpa FAIL; periksa barisnya benar
   (tambahkan catatan manual di bawahnya bila perlu).

## Larangan
Tidak ada warna/hex atau angka ukuran/font/garis acak di modul; tidak menyentuh `ctx.c` (canvas); tidak ada teks hardcode;
tidak ada koordinat bebas (pakai `band`/`cell`/`Rect.split_*`/`take_top`/`inset`); tidak mengubah modul lain.

## Skin
Modul netral terhadap skin: jangan memeriksa/menyebut skin dan jangan menggambar dekorasi margin/bingkai.
Setelah QC modul lulus untuk `classic`, jalankan juga `python main.py qc --module <id> --skin all` (dekorasi otomatis ikut).
Modul baru tidak ada di `baseline/classic_layout.json` (QC: WARN) sampai `python main.py baseline` dijalankan.
