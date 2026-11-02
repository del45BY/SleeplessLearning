# SKIN_GUIDE — aturan untuk AI saat diminta menambah skin

Perintah pengguna contoh: `Tambahkan skin: <nama/tema>, gaya <deskripsi>`.
Skin = lapisan dekorasi visual. Modul tidak tahu skin apa yang aktif; **jangan mengubah `modules/*.py`**.
Jika sebuah modul tampak harus diubah agar cocok dengan skin, BERHENTI dan laporkan dulu.

## Alur wajib
1. **Baca** `skins/base.py` (semua hook + helper), `skins/_template_skin.py`, lalu `skins/garden.py` atau `skins/space.py`
   sebagai contoh. Baca juga bagian "primitif dekorasi" di `core/layout.py` (`decor_*`, `margin_strips`).
2. **Buat** `skins/<nama>.py` (nama file = `name` kelas, snake_case). Override hanya hook yang perlu;
   hook yang tidak di-override = perilaku classic.
3. **Palet warna** di `core/theme.py`: tambahkan `SKIN_COLORS["<nama>"]` (hex, mode color) dan `SKIN_BW["<nama>"]`
   (abu-abu 0..1, mode bw). Hanya nama warna yang sudah ada yang boleh ditimpa
   (`accent, accent_soft, decor_1, decor_2, decor_soft, ribbon_fill, box_fill`, dst.). Skin TIDAK boleh berisi hex.
4. **PNG dekorasi**: daftarkan id di `images()`. File di `assets/skins/<nama>/<id>.png` (RGBA, ≥ 300 px sisi terpendek);
   placeholder dibuat otomatis saat build atau `python main.py assets` (QC: WARN, wajar).
5. **Jalankan** `python main.py qc --all --lang all --mode both --skin <nama>`.
6. **Perbaiki sampai tidak ada FAIL**, lalu buat PDF contoh: `python main.py build --all --lang id --mode both --skin <nama>`
   dan periksa visual (warna dan bw).

## Hook (semua opsional; bawaan = classic)
`draw_page_background`, `draw_page_frame`, `draw_corner_decor`, `draw_header`, `draw_progress_marker`,
`draw_footer`, `draw_name_date_zone`, `draw_instruction_badge`, `draw_section_title`, `draw_reward_sticker_slot`.
Helper siap pakai di `BaseSkin`: `progress_with_dots`, `sticker_circle`, `boxed_name_date`, `badge_instruction`,
`frame_tiles`, `corner_images`, `footer_texts`.

## Aturan keras
* **Area konten tidak boleh menyempit/tertimpa.** Dekorasi hanya di margin, header, footer, latar, sudut. Jangan
  menyentuh `page.content`. Dekorasi yang menutupi teks sistem (pita di belakang judul, kotak nama/tanggal, badge + ikon)
  harus `container=True` dan memuat teksnya sepenuhnya. QC memeriksa bounding box.
* **Ilustrasi = PNG.** Dilarang menggambar ilustrasi lewat kode; hanya bentuk geometris sederhana: garis, kotak
  rounded, lingkaran, gelombang, titik (lewat `decor_*`).
* **Tidak ada warna atau teks hardcode.** Warna = nama dari theme; teks = i18n/`page.t(...)`.
* **Konsisten satu seri.** Posisi dekorasi tidak boleh bergantung pada nomor halaman. Satu-satunya yang boleh berubah:
  penanda progres (`kind="decor_progress"`). Pola acak harus memakai seed TETAP.
* **Jangan ubah ukuran zona** (`header_rect`, `ident_rect`, `instr_zone`, `footer_rect`) kecuali perlu. Teks harus tetap muat
  di 6 bahasa; geser teks hanya dengan menyempitkan rect-nya (QC mengukur per bahasa).
* **Mode bw wajib ramah cetak.** Pola latar (`decor_dots`) hilang otomatis di bw; fill gelap otomatis jadi putih.
  Rancang aksen sebagai OUTLINE (garis), bukan area gelap. Garis dekor di bw ≥ 3:1 terhadap kertas.
* **Jaga margin cetak.** Printer rumahan kerap memotong < 5 mm dari tepi; QC memberi WARN bila dekorasi lebih dekat.
* **Slot stiker** kecil (±7,5 mm) karena hanya muat di header; untuk stiker besar buat skin dengan zona khusus lewat diskusi.
* Skin `classic` jangan diubah: output wajib identik dengan baseline (`python main.py baseline` hanya dijalankan
  bila perubahan tata letak modul/core MEMANG disengaja).

## Cek QC khusus skin
Dekorasi tidak menimpa konten/elemen sistem · PNG skin ada/placeholder (WARN) dan bw grayscale · classic = baseline ·
elemen konten identik di semua skin · pola dekorasi sama antar halaman · tidak ada non-abu-abu di bw ·
teks header/badge muat di semua bahasa.
