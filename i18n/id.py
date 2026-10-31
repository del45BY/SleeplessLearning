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
