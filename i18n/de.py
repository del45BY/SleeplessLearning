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

# --- vertical_lines ---
STRINGS.update({
    "vertical_lines.title": 'Senkrechte Linien',
    "vertical_lines.instruction.rain": 'Fahre den Regen von oben nach unten nach.',
    "vertical_lines.instruction.balloon": 'Fahre die Ballonschnüre nach unten nach.',
    "vertical_lines.instruction.candle": 'Fahre jede Kerze von oben nach unten nach.',
    "vertical_lines.instruction.fence": 'Fahre die Zaunlatten nach unten nach.',
    "vertical_lines.instruction.flower": 'Fahre die Blumenstiele nach unten nach.',
    "vertical_lines.instruction.tree": 'Fahre die Baumstämme nach unten nach.',
    "vertical_lines.instruction.lollipop": 'Fahre die Lutscherstiele nach unten nach.',
    "vertical_lines.instruction.lamp": 'Fahre die Laternenpfähle nach unten nach.',
    "vertical_lines.instruction.cloud_draw": 'Zeichne den Regen. Gehe von Kreis zu Kreis.',
    "vertical_lines.instruction.icicle": 'Zeichne die Eiszapfen. Ziehe von oben nach unten.',
})

# --- horizontal_lines ---
STRINGS.update({
    "horizontal_lines.title": 'Waagerechte Linien',
    "horizontal_lines.instruction.road": 'Fahre die Straße vom Auto zum Haus nach.',
    "horizontal_lines.instruction.train": 'Fahre die Schienen vom Zug zum Bahnhof nach.',
    "horizontal_lines.instruction.bridge": 'Fahre die Brücke von links nach rechts nach.',
    "horizontal_lines.instruction.clothesline": 'Fahre die Wäscheleine von Pfosten zu Pfosten nach.',
    "horizontal_lines.instruction.river": 'Fahre den Fluss vom Boot zur Insel nach.',
    "horizontal_lines.instruction.caterpillar": 'Fahre den Weg zum Blatt nach.',
    "horizontal_lines.instruction.wire": 'Fahre den Draht vom Vogel zum Nest nach.',
    "horizontal_lines.instruction.airplane": 'Fahre den Flug vom Flugzeug zur Wolke nach.',
    "horizontal_lines.instruction.snail": 'Zeichne den Weg zum Blatt, von Kreis zu Kreis.',
    "horizontal_lines.instruction.ant": 'Zeichne den Weg zum Keks, von Kreis zu Kreis.',
})

# --- diagonal_lines ---
STRINGS.update({
    "diagonal_lines.title": 'Schräge Linien',
    "diagonal_lines.instruction.slide": 'Fahre die Rutsche von oben nach unten nach.',
    "diagonal_lines.instruction.ladder": 'Fahre die Leiter vom Fenster zum Boden nach.',
    "diagonal_lines.instruction.kite_string": 'Fahre die Drachenschnüre nach unten nach.',
    "diagonal_lines.instruction.roof": 'Fahre beide Seiten jedes Dachs nach.',
    "diagonal_lines.instruction.ice_cream": 'Fahre jede Eistüte nach.',
    "diagonal_lines.instruction.kite_frame": 'Fahre die Drachenstäbe nach. Zeichne ein X.',
    "diagonal_lines.instruction.tent": 'Fahre beide Seiten jedes Zelts nach.',
    "diagonal_lines.instruction.ski": 'Fahre die Skipiste den Berg hinunter nach.',
    "diagonal_lines.instruction.treasure": 'Zeichne ein X auf jede Karte, von Kreis zu Kreis.',
    "diagonal_lines.instruction.star": 'Zeichne die Sterne zum Mond, von Kreis zu Kreis.',
})

# --- zigzag_lines ---
STRINGS.update({
    "zigzag_lines.title": 'Zickzacklinien',
    "zigzag_lines.instruction.mountain_one": 'Fahre den Berg vom Wanderer zur Fahne nach.',
    "zigzag_lines.instruction.mountain_two": 'Fahre die zwei Berge nach.',
    "zigzag_lines.instruction.mountain_many": 'Fahre die Berge nach. Hoch und runter.',
    "zigzag_lines.instruction.lightning": 'Fahre den Blitz von der Wolke nach unten nach.',
    "zigzag_lines.instruction.fence": 'Fahre den Zackenzaun für die Katze nach.',
    "zigzag_lines.instruction.road": 'Fahre die Kurvenstraße vom Auto zum Haus nach.',
    "zigzag_lines.instruction.lightning_dots": 'Fahre den Blitz nach. Folge den Punkten.',
    "zigzag_lines.instruction.river": 'Fahre den kurvigen Fluss vom Boot zur Insel nach.',
    "zigzag_lines.instruction.lightning_draw": 'Zeichne den Blitz, von Kreis zu Kreis.',
    "zigzag_lines.instruction.mountain_draw": 'Zeichne die Berge, von Kreis zu Kreis.',
})

# --- curved_lines ---
STRINGS.update({
    "curved_lines.title": 'Gebogene Linien',
    "curved_lines.instruction.rainbow_one": 'Fahre den Regenbogen von Wolke zu Wolke nach.',
    "curved_lines.instruction.rainbow_three": 'Fahre alle drei Streifen jedes Regenbogens nach.',
    "curved_lines.instruction.smile": 'Fahre bei jedem Gesicht das Lächeln nach.',
    "curved_lines.instruction.rope": 'Fahre das Seil zwischen den Pfosten nach.',
    "curved_lines.instruction.umbrella": 'Fahre den Schirm und den Griff nach.',
    "curved_lines.instruction.caterpillar": 'Fahre die Hügel für die Raupe nach.',
    "curved_lines.instruction.hook": 'Fahre die Angelschnüre bis zu den Haken nach.',
    "curved_lines.instruction.lollipop": 'Fahre den Wirbel jedes Lutschers nach.',
    "curved_lines.instruction.rainbow_draw": 'Zeichne die Regenbogen, von Kreis zu Kreis.',
    "curved_lines.instruction.umbrella_draw": 'Zeichne die Schirme, von Kreis zu Kreis.',
})

# --- wavy_lines ---
STRINGS.update({
    "wavy_lines.title": 'Wellenlinien',
    "wavy_lines.instruction.sea_one": 'Fahre die großen Wellen vom Fisch zur Muschel nach.',
    "wavy_lines.instruction.sea_two": 'Fahre die Wellen nach. Rauf und runter.',
    "wavy_lines.instruction.snake": 'Fahre die Schlange bis zum Apfel nach.',
    "wavy_lines.instruction.river": 'Fahre den Flusslauf vom Berg zum See nach.',
    "wavy_lines.instruction.hair": 'Fahre die welligen Haare unter jeder Schleife nach.',
    "wavy_lines.instruction.sea_dots": 'Fahre die Meereswellen nach. Folge den Punkten.',
    "wavy_lines.instruction.snake_dots": 'Fahre die Schlangen nach. Folge den Punkten.',
    "wavy_lines.instruction.hair_dots": 'Fahre die welligen Haare nach. Folge den Punkten.',
    "wavy_lines.instruction.sea_draw": 'Zeichne die Wellen, von Kreis zu Kreis.',
    "wavy_lines.instruction.river_draw": 'Zeichne die Flüsse, von Kreis zu Kreis.',
})

# --- circles_spirals ---
STRINGS.update({
    "circles_spirals.title": 'Kreise und Spiralen',
    "circles_spirals.instruction.ball": 'Fahre den Ball nach. Fang oben an.',
    "circles_spirals.instruction.sun": 'Fahre die Sonne über jedem Haus nach.',
    "circles_spirals.instruction.wheel": 'Fahre die zwei Räder jedes Autos nach.',
    "circles_spirals.instruction.target": 'Fahre alle Kreise jeder Zielscheibe nach.',
    "circles_spirals.instruction.snail": 'Fahre das Schneckenhaus nach. Immer rundherum.',
    "circles_spirals.instruction.bubble": 'Fahre die Blasen über dem Fisch nach.',
    "circles_spirals.instruction.bike": 'Fahre die zwei Räder jedes Fahrrads nach.',
    "circles_spirals.instruction.snail_out": 'Fahre das Schneckenhaus von der Mitte nach außen nach.',
    "circles_spirals.instruction.target_draw": 'Zeichne die Zielscheiben, von Kreis zu Kreis.',
    "circles_spirals.instruction.snail_draw": 'Zeichne die Schneckenhäuser, von Kreis zu Kreis.',
})
