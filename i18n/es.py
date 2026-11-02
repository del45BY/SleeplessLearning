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

# --- vertical_lines ---
STRINGS.update({
    "vertical_lines.title": 'Líneas verticales',
    "vertical_lines.instruction.rain": 'Repasa la lluvia de arriba hacia abajo.',
    "vertical_lines.instruction.balloon": 'Repasa los hilos de los globos hacia abajo.',
    "vertical_lines.instruction.candle": 'Repasa cada vela de arriba hacia abajo.',
    "vertical_lines.instruction.fence": 'Repasa los palos de la cerca hacia abajo.',
    "vertical_lines.instruction.flower": 'Repasa los tallos de las flores hacia abajo.',
    "vertical_lines.instruction.tree": 'Repasa los troncos de los árboles hacia abajo.',
    "vertical_lines.instruction.lollipop": 'Repasa los palitos de las paletas hacia abajo.',
    "vertical_lines.instruction.lamp": 'Repasa los postes de luz hacia abajo.',
    "vertical_lines.instruction.cloud_draw": 'Dibuja la lluvia. Ve de círculo en círculo.',
    "vertical_lines.instruction.icicle": 'Dibuja los carámbanos. Ve de arriba hacia abajo.',
})

# --- horizontal_lines ---
STRINGS.update({
    "horizontal_lines.title": 'Líneas horizontales',
    "horizontal_lines.instruction.road": 'Repasa el camino del auto a la casa.',
    "horizontal_lines.instruction.train": 'Repasa las vías del tren a la estación.',
    "horizontal_lines.instruction.bridge": 'Repasa el puente de izquierda a derecha.',
    "horizontal_lines.instruction.clothesline": 'Repasa la cuerda de la ropa de poste a poste.',
    "horizontal_lines.instruction.river": 'Repasa el río del bote a la isla.',
    "horizontal_lines.instruction.caterpillar": 'Repasa el camino hasta la hoja.',
    "horizontal_lines.instruction.wire": 'Repasa el cable del pájaro al nido.',
    "horizontal_lines.instruction.airplane": 'Repasa el vuelo del avión a la nube.',
    "horizontal_lines.instruction.snail": 'Dibuja el camino a la hoja, de círculo en círculo.',
    "horizontal_lines.instruction.ant": 'Dibuja el camino a la galleta, de círculo en círculo.',
})
