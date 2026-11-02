"""Teks worksheet — Bahasa Indonesia.

Semua teks yang tampil di PDF ada di sini (judul, instruksi, label, kata, footer).
Key harus identik di semua file bahasa (en.py adalah acuan; fallback ke en bila hilang).
Modul baru: tambahkan blok `STRINGS.update({...})` di bagian bawah file ini.
"""
STRINGS = {
    # --- common (header, identitas, footer) ---
    "common.name_label": 'Nama:',
    "common.date_label": 'Tanggal:',
    "common.page": 'Halaman',
    "common.license": 'Hanya untuk penggunaan pribadi dan kelas.',
    # --- bundle (cover + daftar isi) ---
    "bundle.default_title": 'Worksheet Prasekolah',
    "bundle.cover_subtitle": 'Usia {age_min}–{age_max} tahun',
    "bundle.toc_title": 'Daftar Isi',
    "bundle.page_ref": 'hlm. {n}',
}

# --- tracing_letters ---
STRINGS.update({
    "tracing_letters.title": 'Menebalkan Huruf',
    "tracing_letters.instruction": 'Tebalkan setiap huruf, lalu tulis sendiri.',
})
# (id gambar, kata) untuk huruf A..Z. Kata HARUS diawali huruf tersebut (dicek QC).
_LETTER_WORDS = [
    ('apel', 'Apel'),  # A
    ('bola', 'Bola'),  # B
    ('cangkir', 'Cangkir'),  # C
    ('domba', 'Domba'),  # D
    ('es_krim', 'Es krim'),  # E
    ('flamingo', 'Flamingo'),  # F
    ('gajah', 'Gajah'),  # G
    ('harimau', 'Harimau'),  # H
    ('ikan', 'Ikan'),  # I
    ('jeruk', 'Jeruk'),  # J
    ('kucing', 'Kucing'),  # K
    ('lebah', 'Lebah'),  # L
    ('mobil', 'Mobil'),  # M
    ('nanas', 'Nanas'),  # N
    ('orangutan', 'Orangutan'),  # O
    ('pisang', 'Pisang'),  # P
    ('quokka', 'Quokka'),  # Q
    ('rumah', 'Rumah'),  # R
    ('sapi', 'Sapi'),  # S
    ('topi', 'Topi'),  # T
    ('ular', 'Ular'),  # U
    ('vas', 'Vas'),  # V
    ('wortel', 'Wortel'),  # W
    ('xilofon', 'Xilofon'),  # X
    ('yoyo', 'Yoyo'),  # Y
    ('zebra', 'Zebra'),  # Z
]
for _L, (_img, _word) in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", _LETTER_WORDS):
    STRINGS[f"tracing_letters.img.{_L}"] = _img
    STRINGS[f"tracing_letters.word.{_L}"] = _word

# --- counting_1_10 ---
STRINGS.update({
    "counting_1_10.title": 'Berhitung 1–10',
    "counting_1_10.instruction": 'Hitung gambarnya dan tebalkan angkanya.',
    "counting_1_10.num.1": 'satu',
    "counting_1_10.num.2": 'dua',
    "counting_1_10.num.3": 'tiga',
    "counting_1_10.num.4": 'empat',
    "counting_1_10.num.5": 'lima',
    "counting_1_10.num.6": 'enam',
    "counting_1_10.num.7": 'tujuh',
    "counting_1_10.num.8": 'delapan',
    "counting_1_10.num.9": 'sembilan',
    "counting_1_10.num.10": 'sepuluh',
})

# --- vertical_lines ---
STRINGS.update({
    "vertical_lines.title": 'Garis Tegak',
    "vertical_lines.instruction.rain": 'Tebalkan hujan dari atas ke bawah.',
    "vertical_lines.instruction.balloon": 'Tebalkan tali balon ke bawah.',
    "vertical_lines.instruction.candle": 'Tebalkan setiap lilin dari atas ke bawah.',
    "vertical_lines.instruction.fence": 'Tebalkan tiang pagar ke bawah.',
    "vertical_lines.instruction.flower": 'Tebalkan batang bunga ke bawah.',
    "vertical_lines.instruction.tree": 'Tebalkan batang pohon ke bawah.',
    "vertical_lines.instruction.lollipop": 'Tebalkan tangkai permen ke bawah.',
    "vertical_lines.instruction.lamp": 'Tebalkan tiang lampu ke bawah.',
    "vertical_lines.instruction.cloud_draw": 'Gambar hujannya. Tarik dari lingkaran ke lingkaran.',
    "vertical_lines.instruction.icicle": 'Gambar es yang menggantung. Tarik dari atas ke bawah.',
})

# --- horizontal_lines ---
STRINGS.update({
    "horizontal_lines.title": 'Garis Datar',
    "horizontal_lines.instruction.road": 'Tebalkan jalan dari mobil ke rumah.',
    "horizontal_lines.instruction.train": 'Tebalkan rel dari kereta ke stasiun.',
    "horizontal_lines.instruction.bridge": 'Tebalkan jembatan dari kiri ke kanan.',
    "horizontal_lines.instruction.clothesline": 'Tebalkan tali jemuran dari tiang ke tiang.',
    "horizontal_lines.instruction.river": 'Tebalkan sungai dari perahu ke pulau.',
    "horizontal_lines.instruction.caterpillar": 'Tebalkan jalan ke daun.',
    "horizontal_lines.instruction.wire": 'Tebalkan kawat dari burung ke sarang.',
    "horizontal_lines.instruction.airplane": 'Tebalkan jalur dari pesawat ke awan.',
    "horizontal_lines.instruction.snail": 'Gambar jalan ke daun, dari lingkaran ke lingkaran.',
    "horizontal_lines.instruction.ant": 'Gambar jalan ke kue, dari lingkaran ke lingkaran.',
})
