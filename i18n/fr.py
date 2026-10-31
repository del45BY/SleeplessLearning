"""Teks worksheet — Français.

Semua teks yang tampil di PDF ada di sini (judul, instruksi, label, kata, footer).
Key harus identik di semua file bahasa (en.py adalah acuan; fallback ke en bila hilang).
Modul baru: tambahkan blok `STRINGS.update({...})` di bagian bawah file ini.
"""
STRINGS = {
    # --- common (header, identitas, footer) ---
    "common.name_label": 'Nom :',
    "common.date_label": 'Date :',
    "common.page": 'Page',
    "common.license": 'Réservé à un usage personnel et en classe.',
    # --- bundle (cover + daftar isi) ---
    "bundle.default_title": 'Fiches de maternelle',
    "bundle.cover_subtitle": 'De {age_min} à {age_max} ans',
    "bundle.toc_title": 'Sommaire',
    "bundle.page_ref": 'p. {n}',
}

# --- tracing_letters ---
STRINGS.update({
    "tracing_letters.title": 'Tracer les lettres',
    "tracing_letters.instruction": 'Repasse chaque lettre, puis écris-la toi-même.',
})
# (id gambar, kata) untuk huruf A..Z. Kata HARUS diawali huruf tersebut (dicek QC).
_LETTER_WORDS = [
    ('airplane', 'Avion'),  # A
    ('balloon', 'Ballon'),  # B
    ('cat', 'Chat'),  # C
    ('dolphin', 'Dauphin'),  # D
    ('elephant', 'Éléphant'),  # E
    ('strawberry', 'Fraise'),  # F
    ('cake', 'Gâteau'),  # G
    ('owl', 'Hibou'),  # H
    ('igloo', 'Igloo'),  # I
    ('juice', 'Jus'),  # J
    ('kiwi', 'Kiwi'),  # K
    ('rabbit', 'Lapin'),  # L
    ('house', 'Maison'),  # M
    ('cloud', 'Nuage'),  # N
    ('bird', 'Oiseau'),  # O
    ('apple', 'Pomme'),  # P
    ('bowling_pin', 'Quille'),  # Q
    ('robot', 'Robot'),  # R
    ('sun', 'Soleil'),  # S
    ('turtle', 'Tortue'),  # T
    ('ukulele', 'Ukulélé'),  # U
    ('cow', 'Vache'),  # V
    ('wagon', 'Wagon'),  # W
    ('xylophone', 'Xylophone'),  # X
    ('yogurt', 'Yaourt'),  # Y
    ('zebra', 'Zèbre'),  # Z
]
for _L, (_img, _word) in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", _LETTER_WORDS):
    STRINGS[f"tracing_letters.img.{_L}"] = _img
    STRINGS[f"tracing_letters.word.{_L}"] = _word

# --- counting_1_10 ---
STRINGS.update({
    "counting_1_10.title": 'Compter de 1 à 10',
    "counting_1_10.instruction": 'Compte les images et repasse chaque chiffre.',
    "counting_1_10.num.1": 'un',
    "counting_1_10.num.2": 'deux',
    "counting_1_10.num.3": 'trois',
    "counting_1_10.num.4": 'quatre',
    "counting_1_10.num.5": 'cinq',
    "counting_1_10.num.6": 'six',
    "counting_1_10.num.7": 'sept',
    "counting_1_10.num.8": 'huit',
    "counting_1_10.num.9": 'neuf',
    "counting_1_10.num.10": 'dix',
})
