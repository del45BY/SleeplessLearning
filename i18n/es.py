"""Teks worksheet — Español neutro (Latinoamérica).

Semua teks yang tampil di PDF ada di sini (judul, instruksi, label, kata, footer).
Key harus identik di semua file bahasa (en.py adalah acuan; fallback ke en bila hilang).
Modul baru: tambahkan blok `STRINGS.update({...})` di bagian bawah file ini.
"""
STRINGS = {
    # --- common (header, identitas, footer) ---
    "common.name_label": 'Nombre:',
    "common.date_label": 'Fecha:',
    "common.page": 'Página',
    "common.license": 'Solo para uso personal y en el aula.',
    # --- bundle (cover + daftar isi) ---
    "bundle.default_title": 'Fichas de preescolar',
    "bundle.cover_subtitle": 'Edades {age_min}–{age_max} años',
    "bundle.toc_title": 'Contenido',
    "bundle.page_ref": 'pág. {n}',
}

# --- tracing_letters ---
STRINGS.update({
    "tracing_letters.title": 'Trazar letras',
    "tracing_letters.instruction": 'Repasa cada letra y escríbela tú.',
})
# (id gambar, kata) untuk huruf A..Z. Kata HARUS diawali huruf tersebut (dicek QC).
_LETTER_WORDS = [
    ('airplane', 'Avión'),  # A
    ('boat', 'Barco'),  # B
    ('house', 'Casa'),  # C
    ('dice', 'Dado'),  # D
    ('elephant', 'Elefante'),  # E
    ('flower', 'Flor'),  # F
    ('cat', 'Gato'),  # G
    ('ice_cream', 'Helado'),  # H
    ('island', 'Isla'),  # I
    ('giraffe', 'Jirafa'),  # J
    ('koala', 'Koala'),  # K
    ('lion', 'León'),  # L
    ('apple', 'Manzana'),  # M
    ('orange', 'Naranja'),  # N
    ('bear', 'Oso'),  # O
    ('duck', 'Pato'),  # P
    ('cheese', 'Queso'),  # Q
    ('mouse', 'Ratón'),  # R
    ('sun', 'Sol'),  # S
    ('turtle', 'Tortuga'),  # T
    ('grapes', 'Uvas'),  # U
    ('cow', 'Vaca'),  # V
    ('waffle', 'Waffle'),  # W
    ('xylophone', 'Xilófono'),  # X
    ('yoyo', 'Yoyó'),  # Y
    ('shoe', 'Zapato'),  # Z
]
for _L, (_img, _word) in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", _LETTER_WORDS):
    STRINGS[f"tracing_letters.img.{_L}"] = _img
    STRINGS[f"tracing_letters.word.{_L}"] = _word

# --- counting_1_10 ---
STRINGS.update({
    "counting_1_10.title": 'Contar del 1 al 10',
    "counting_1_10.instruction": 'Cuenta los dibujos y repasa cada número.',
    "counting_1_10.num.1": 'uno',
    "counting_1_10.num.2": 'dos',
    "counting_1_10.num.3": 'tres',
    "counting_1_10.num.4": 'cuatro',
    "counting_1_10.num.5": 'cinco',
    "counting_1_10.num.6": 'seis',
    "counting_1_10.num.7": 'siete',
    "counting_1_10.num.8": 'ocho',
    "counting_1_10.num.9": 'nueve',
    "counting_1_10.num.10": 'diez',
})
