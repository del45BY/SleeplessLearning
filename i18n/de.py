"""Teks worksheet — Deutsch.

Semua teks yang tampil di PDF ada di sini (judul, instruksi, label, kata, footer).
Key harus identik di semua file bahasa (en.py adalah acuan; fallback ke en bila hilang).
Modul baru: tambahkan blok `STRINGS.update({...})` di bagian bawah file ini.
"""
STRINGS = {
    # --- common (header, identitas, footer) ---
    "common.name_label": 'Name:',
    "common.date_label": 'Datum:',
    "common.page": 'Seite',
    "common.license": 'Nur für den privaten Gebrauch und den Unterricht.',
    # --- bundle (cover + daftar isi) ---
    "bundle.default_title": 'Vorschul-Arbeitsblätter',
    "bundle.cover_subtitle": 'Alter {age_min}–{age_max} Jahre',
    "bundle.toc_title": 'Inhalt',
    "bundle.page_ref": 'S. {n}',
}

# --- tracing_letters ---
STRINGS.update({
    "tracing_letters.title": 'Buchstaben nachspuren',
    "tracing_letters.instruction": 'Fahre jeden Buchstaben nach und schreibe ihn selbst.',
})
# (id gambar, kata) untuk huruf A..Z. Kata HARUS diawali huruf tersebut (dicek QC).
_LETTER_WORDS = [
    ('apple', 'Apfel'),  # A
    ('ball', 'Ball'),  # B
    ('clown', 'Clown'),  # C
    ('dolphin', 'Delfin'),  # D
    ('duck', 'Ente'),  # E
    ('fish', 'Fisch'),  # F
    ('giraffe', 'Giraffe'),  # G
    ('dog', 'Hund'),  # H
    ('hedgehog', 'Igel'),  # I
    ('jacket', 'Jacke'),  # J
    ('cat', 'Katze'),  # K
    ('lion', 'Löwe'),  # L
    ('moon', 'Mond'),  # M
    ('nest', 'Nest'),  # N
    ('orange', 'Orange'),  # O
    ('mushroom', 'Pilz'),  # P
    ('jellyfish', 'Qualle'),  # Q
    ('rocket', 'Rakete'),  # R
    ('sun', 'Sonne'),  # S
    ('tiger', 'Tiger'),  # T
    ('clock', 'Uhr'),  # U
    ('bird', 'Vogel'),  # V
    ('whale', 'Wal'),  # W
    ('xylophone', 'Xylophon'),  # X
    ('yak', 'Yak'),  # Y
    ('zebra', 'Zebra'),  # Z
]
for _L, (_img, _word) in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", _LETTER_WORDS):
    STRINGS[f"tracing_letters.img.{_L}"] = _img
    STRINGS[f"tracing_letters.word.{_L}"] = _word

# --- counting_1_10 ---
STRINGS.update({
    "counting_1_10.title": 'Zählen von 1 bis 10',
    "counting_1_10.instruction": 'Zähle die Bilder und fahre die Zahlen nach.',
    "counting_1_10.num.1": 'eins',
    "counting_1_10.num.2": 'zwei',
    "counting_1_10.num.3": 'drei',
    "counting_1_10.num.4": 'vier',
    "counting_1_10.num.5": 'fünf',
    "counting_1_10.num.6": 'sechs',
    "counting_1_10.num.7": 'sieben',
    "counting_1_10.num.8": 'acht',
    "counting_1_10.num.9": 'neun',
    "counting_1_10.num.10": 'zehn',
})
