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
