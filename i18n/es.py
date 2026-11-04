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

# --- diagonal_lines ---
STRINGS.update({
    "diagonal_lines.title": 'Líneas diagonales',
    "diagonal_lines.instruction.slide": 'Repasa el tobogán de arriba hacia abajo.',
    "diagonal_lines.instruction.ladder": 'Repasa la escalera de la ventana al suelo.',
    "diagonal_lines.instruction.kite_string": 'Repasa los hilos de las cometas hacia abajo.',
    "diagonal_lines.instruction.roof": 'Repasa los dos lados de cada techo.',
    "diagonal_lines.instruction.ice_cream": 'Repasa cada cono de helado.',
    "diagonal_lines.instruction.kite_frame": 'Repasa los palos de la cometa. Haz una X.',
    "diagonal_lines.instruction.tent": 'Repasa los dos lados de cada carpa.',
    "diagonal_lines.instruction.ski": 'Repasa el camino de esquí por la montaña.',
    "diagonal_lines.instruction.treasure": 'Dibuja una X en cada mapa, de círculo en círculo.',
    "diagonal_lines.instruction.star": 'Dibuja las estrellas que caen a la luna, de círculo en círculo.',
})

# --- zigzag_lines ---
STRINGS.update({
    "zigzag_lines.title": 'Líneas en zigzag',
    "zigzag_lines.instruction.mountain_one": 'Repasa la montaña del excursionista a la bandera.',
    "zigzag_lines.instruction.mountain_two": 'Repasa las dos montañas.',
    "zigzag_lines.instruction.mountain_many": 'Repasa las montañas. Sube y baja.',
    "zigzag_lines.instruction.lightning": 'Repasa el rayo de la nube hacia abajo.',
    "zigzag_lines.instruction.fence": 'Repasa la cerca de picos para el gato.',
    "zigzag_lines.instruction.road": 'Repasa el camino con curvas del auto a la casa.',
    "zigzag_lines.instruction.lightning_dots": 'Repasa el rayo. Sigue los puntos.',
    "zigzag_lines.instruction.river": 'Repasa el río con curvas del bote a la isla.',
    "zigzag_lines.instruction.lightning_draw": 'Dibuja el rayo, de círculo en círculo.',
    "zigzag_lines.instruction.mountain_draw": 'Dibuja las montañas, de círculo en círculo.',
})

# --- curved_lines ---
STRINGS.update({
    "curved_lines.title": 'Líneas curvas',
    "curved_lines.instruction.rainbow_one": 'Repasa el arcoíris de nube a nube.',
    "curved_lines.instruction.rainbow_three": 'Repasa las tres franjas de cada arcoíris.',
    "curved_lines.instruction.smile": 'Repasa una sonrisa en cada cara.',
    "curved_lines.instruction.rope": 'Repasa la cuerda entre los postes.',
    "curved_lines.instruction.umbrella": 'Repasa el paraguas y su mango.',
    "curved_lines.instruction.caterpillar": 'Repasa las colinas de la oruga.',
    "curved_lines.instruction.hook": 'Repasa las cañas de pescar hasta los anzuelos.',
    "curved_lines.instruction.lollipop": 'Repasa el remolino de cada paleta.',
    "curved_lines.instruction.rainbow_draw": 'Dibuja los arcoíris, de círculo en círculo.',
    "curved_lines.instruction.umbrella_draw": 'Dibuja los paraguas, de círculo en círculo.',
})

# --- wavy_lines ---
STRINGS.update({
    "wavy_lines.title": 'Líneas onduladas',
    "wavy_lines.instruction.sea_one": 'Repasa las olas grandes del pez a la concha.',
    "wavy_lines.instruction.sea_two": 'Repasa las olas. Sube y baja, sube y baja.',
    "wavy_lines.instruction.snake": 'Repasa la serpiente ondulada hasta la manzana.',
    "wavy_lines.instruction.river": 'Repasa el río con curvas de la montaña al lago.',
    "wavy_lines.instruction.hair": 'Repasa el pelo ondulado bajo cada moño.',
    "wavy_lines.instruction.sea_dots": 'Repasa las olas del mar. Sigue los puntos.',
    "wavy_lines.instruction.snake_dots": 'Repasa las serpientes. Sigue los puntos.',
    "wavy_lines.instruction.hair_dots": 'Repasa el pelo ondulado. Sigue los puntos.',
    "wavy_lines.instruction.sea_draw": 'Dibuja las olas, de círculo en círculo.',
    "wavy_lines.instruction.river_draw": 'Dibuja los ríos, de círculo en círculo.',
})

# --- circles_spirals ---
STRINGS.update({
    "circles_spirals.title": 'Círculos y espirales',
    "circles_spirals.instruction.ball": 'Repasa la pelota. Empieza arriba.',
    "circles_spirals.instruction.sun": 'Repasa el sol sobre cada casa.',
    "circles_spirals.instruction.wheel": 'Repasa las dos ruedas de cada auto.',
    "circles_spirals.instruction.target": 'Repasa todos los círculos de cada diana.',
    "circles_spirals.instruction.snail": 'Repasa la concha del caracol. Da vueltas y vueltas.',
    "circles_spirals.instruction.bubble": 'Repasa las burbujas sobre el pez.',
    "circles_spirals.instruction.bike": 'Repasa las dos ruedas de cada bicicleta.',
    "circles_spirals.instruction.snail_out": 'Repasa la concha del caracol desde el centro.',
    "circles_spirals.instruction.target_draw": 'Dibuja las dianas, de círculo en círculo.',
    "circles_spirals.instruction.snail_draw": 'Dibuja las conchas desde el centro, de círculo en círculo.',
})
