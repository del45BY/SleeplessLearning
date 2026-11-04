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

# --- vertical_lines ---
STRINGS.update({
    "vertical_lines.title": 'Lignes verticales',
    "vertical_lines.instruction.rain": 'Repasse la pluie de haut en bas.',
    "vertical_lines.instruction.balloon": 'Repasse les ficelles des ballons vers le bas.',
    "vertical_lines.instruction.candle": 'Repasse chaque bougie de haut en bas.',
    "vertical_lines.instruction.fence": 'Repasse les piquets de la barrière vers le bas.',
    "vertical_lines.instruction.flower": 'Repasse les tiges des fleurs vers le bas.',
    "vertical_lines.instruction.tree": 'Repasse les troncs des arbres vers le bas.',
    "vertical_lines.instruction.lollipop": 'Repasse les bâtons des sucettes vers le bas.',
    "vertical_lines.instruction.lamp": 'Repasse les lampadaires vers le bas.',
    "vertical_lines.instruction.cloud_draw": 'Dessine la pluie. Va de rond en rond.',
    "vertical_lines.instruction.icicle": 'Dessine les glaçons. Va de haut en bas.',
})

# --- horizontal_lines ---
STRINGS.update({
    "horizontal_lines.title": 'Lignes horizontales',
    "horizontal_lines.instruction.road": 'Repasse la route de la voiture à la maison.',
    "horizontal_lines.instruction.train": 'Repasse les rails du train à la gare.',
    "horizontal_lines.instruction.bridge": 'Repasse le pont de gauche à droite.',
    "horizontal_lines.instruction.clothesline": 'Repasse le fil à linge de poteau en poteau.',
    "horizontal_lines.instruction.river": "Repasse la rivière du bateau à l'île.",
    "horizontal_lines.instruction.caterpillar": "Repasse le chemin jusqu'à la feuille.",
    "horizontal_lines.instruction.wire": "Repasse le fil de l'oiseau au nid.",
    "horizontal_lines.instruction.airplane": "Repasse le vol de l'avion au nuage.",
    "horizontal_lines.instruction.snail": "Dessine le chemin jusqu'à la feuille, de rond en rond.",
    "horizontal_lines.instruction.ant": "Dessine le chemin jusqu'au biscuit, de rond en rond.",
})

# --- diagonal_lines ---
STRINGS.update({
    "diagonal_lines.title": 'Lignes obliques',
    "diagonal_lines.instruction.slide": 'Repasse le toboggan de haut en bas.',
    "diagonal_lines.instruction.ladder": "Repasse l'échelle de la fenêtre au sol.",
    "diagonal_lines.instruction.kite_string": 'Repasse les ficelles des cerfs-volants vers le bas.',
    "diagonal_lines.instruction.roof": 'Repasse les deux côtés de chaque toit.',
    "diagonal_lines.instruction.ice_cream": 'Repasse chaque cornet de glace.',
    "diagonal_lines.instruction.kite_frame": 'Repasse les bâtons du cerf-volant. Fais un X.',
    "diagonal_lines.instruction.tent": 'Repasse les deux côtés de chaque tente.',
    "diagonal_lines.instruction.ski": 'Repasse la piste de ski sur la montagne.',
    "diagonal_lines.instruction.treasure": 'Dessine un X sur chaque carte, de rond en rond.',
    "diagonal_lines.instruction.star": 'Dessine les étoiles vers la lune, de rond en rond.',
})

# --- zigzag_lines ---
STRINGS.update({
    "zigzag_lines.title": 'Lignes en zigzag',
    "zigzag_lines.instruction.mountain_one": 'Repasse la montagne du randonneur au drapeau.',
    "zigzag_lines.instruction.mountain_two": 'Repasse les deux montagnes.',
    "zigzag_lines.instruction.mountain_many": 'Repasse les montagnes. Monte et descends.',
    "zigzag_lines.instruction.lightning": "Repasse l'éclair du nuage vers le bas.",
    "zigzag_lines.instruction.fence": 'Repasse la clôture en dents de scie pour le chat.',
    "zigzag_lines.instruction.road": 'Repasse la route sinueuse de la voiture à la maison.',
    "zigzag_lines.instruction.lightning_dots": "Repasse l'éclair. Suis les points.",
    "zigzag_lines.instruction.river": "Repasse la rivière sinueuse du bateau à l'île.",
    "zigzag_lines.instruction.lightning_draw": "Dessine l'éclair, de rond en rond.",
    "zigzag_lines.instruction.mountain_draw": 'Dessine les montagnes, de rond en rond.',
})

# --- curved_lines ---
STRINGS.update({
    "curved_lines.title": 'Lignes courbes',
    "curved_lines.instruction.rainbow_one": "Repasse l'arc-en-ciel de nuage en nuage.",
    "curved_lines.instruction.rainbow_three": 'Repasse les trois bandes de chaque arc-en-ciel.',
    "curved_lines.instruction.smile": 'Repasse un sourire sur chaque visage.',
    "curved_lines.instruction.rope": 'Repasse la corde entre les poteaux.',
    "curved_lines.instruction.umbrella": 'Repasse le parapluie et sa poignée.',
    "curved_lines.instruction.caterpillar": 'Repasse les collines de la chenille.',
    "curved_lines.instruction.hook": "Repasse les lignes de pêche jusqu'aux hameçons.",
    "curved_lines.instruction.lollipop": 'Repasse la spirale de chaque sucette.',
    "curved_lines.instruction.rainbow_draw": 'Dessine les arcs-en-ciel, de rond en rond.',
    "curved_lines.instruction.umbrella_draw": 'Dessine les parapluies, de rond en rond.',
})

# --- wavy_lines ---
STRINGS.update({
    "wavy_lines.title": 'Lignes ondulées',
    "wavy_lines.instruction.sea_one": 'Repasse les grandes vagues du poisson au coquillage.',
    "wavy_lines.instruction.sea_two": 'Repasse les vagues. Monte et descends.',
    "wavy_lines.instruction.snake": "Repasse le serpent ondulé jusqu'à la pomme.",
    "wavy_lines.instruction.river": 'Repasse la rivière sinueuse de la montagne au lac.',
    "wavy_lines.instruction.hair": 'Repasse les cheveux ondulés sous chaque nœud.',
    "wavy_lines.instruction.sea_dots": 'Repasse les vagues de la mer. Suis les points.',
    "wavy_lines.instruction.snake_dots": 'Repasse les serpents. Suis les points.',
    "wavy_lines.instruction.hair_dots": 'Repasse les cheveux ondulés. Suis les points.',
    "wavy_lines.instruction.sea_draw": 'Dessine les vagues, de rond en rond.',
    "wavy_lines.instruction.river_draw": 'Dessine les rivières, de rond en rond.',
})

# --- circles_spirals ---
STRINGS.update({
    "circles_spirals.title": 'Cercles et spirales',
    "circles_spirals.instruction.ball": 'Repasse le ballon. Commence en haut.',
    "circles_spirals.instruction.sun": 'Repasse le soleil au-dessus de chaque maison.',
    "circles_spirals.instruction.wheel": 'Repasse les deux roues de chaque voiture.',
    "circles_spirals.instruction.target": 'Repasse tous les cercles de chaque cible.',
    "circles_spirals.instruction.snail": "Repasse la coquille de l'escargot. Tourne, tourne.",
    "circles_spirals.instruction.bubble": 'Repasse les bulles au-dessus du poisson.',
    "circles_spirals.instruction.bike": 'Repasse les deux roues de chaque vélo.',
    "circles_spirals.instruction.snail_out": "Repasse la coquille de l'escargot du centre vers l'extérieur.",
    "circles_spirals.instruction.target_draw": 'Dessine les cibles, de rond en rond.',
    "circles_spirals.instruction.snail_draw": 'Dessine les coquilles, de rond en rond.',
})
