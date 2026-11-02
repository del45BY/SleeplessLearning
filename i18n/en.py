"""Teks worksheet — Inggris (US). Key baru modul ditambahkan sebagai blok STRINGS.update({...}) di bagian bawah.

Semua teks yang tampil di PDF ada di sini (judul, instruksi, label, kata, footer).
Key harus identik di semua file bahasa (en.py adalah acuan; fallback ke en bila hilang).
Modul baru: tambahkan blok `STRINGS.update({...})` di bagian bawah file ini.
"""
STRINGS = {
    # --- common (header, identitas, footer) ---
    "common.name_label": 'Name:',
    "common.date_label": 'Date:',
    "common.page": 'Page',
    "common.license": 'For personal and classroom use only.',
    # --- bundle (cover + daftar isi) ---
    "bundle.default_title": 'Preschool Worksheets',
    "bundle.cover_subtitle": 'Ages {age_min}–{age_max}',
    "bundle.toc_title": 'Contents',
    "bundle.page_ref": 'p. {n}',
}

# --- tracing_letters ---
STRINGS.update({
    "tracing_letters.title": 'Tracing Letters',
    "tracing_letters.instruction": 'Trace each letter, then write it yourself.',
})
# (id gambar, kata) untuk huruf A..Z. Kata HARUS diawali huruf tersebut (dicek QC).
_LETTER_WORDS = [
    ('apple', 'Apple'),  # A
    ('ball', 'Ball'),  # B
    ('cat', 'Cat'),  # C
    ('dog', 'Dog'),  # D
    ('egg', 'Egg'),  # E
    ('fish', 'Fish'),  # F
    ('grapes', 'Grapes'),  # G
    ('hat', 'Hat'),  # H
    ('ice_cream', 'Ice cream'),  # I
    ('juice', 'Juice'),  # J
    ('kite', 'Kite'),  # K
    ('lion', 'Lion'),  # L
    ('moon', 'Moon'),  # M
    ('nest', 'Nest'),  # N
    ('orange', 'Orange'),  # O
    ('pig', 'Pig'),  # P
    ('queen', 'Queen'),  # Q
    ('rabbit', 'Rabbit'),  # R
    ('sun', 'Sun'),  # S
    ('tree', 'Tree'),  # T
    ('umbrella', 'Umbrella'),  # U
    ('violin', 'Violin'),  # V
    ('whale', 'Whale'),  # W
    ('xylophone', 'Xylophone'),  # X
    ('yoyo', 'Yo-yo'),  # Y
    ('zebra', 'Zebra'),  # Z
]
for _L, (_img, _word) in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", _LETTER_WORDS):
    STRINGS[f"tracing_letters.img.{_L}"] = _img
    STRINGS[f"tracing_letters.word.{_L}"] = _word

# --- counting_1_10 ---
STRINGS.update({
    "counting_1_10.title": 'Counting 1–10',
    "counting_1_10.instruction": 'Count the pictures and trace each number.',
    "counting_1_10.num.1": 'one',
    "counting_1_10.num.2": 'two',
    "counting_1_10.num.3": 'three',
    "counting_1_10.num.4": 'four',
    "counting_1_10.num.5": 'five',
    "counting_1_10.num.6": 'six',
    "counting_1_10.num.7": 'seven',
    "counting_1_10.num.8": 'eight',
    "counting_1_10.num.9": 'nine',
    "counting_1_10.num.10": 'ten',
})

# --- vertical_lines ---
STRINGS.update({
    "vertical_lines.title": 'Vertical Lines',
    "vertical_lines.instruction.rain": 'Trace the rain from top to bottom.',
    "vertical_lines.instruction.balloon": 'Trace the balloon strings down.',
    "vertical_lines.instruction.candle": 'Trace each candle from top to bottom.',
    "vertical_lines.instruction.fence": 'Trace the fence posts down.',
    "vertical_lines.instruction.flower": 'Trace the flower stems down.',
    "vertical_lines.instruction.tree": 'Trace the tree trunks down.',
    "vertical_lines.instruction.lollipop": 'Trace the lollipop sticks down.',
    "vertical_lines.instruction.lamp": 'Trace the lamp posts down.',
    "vertical_lines.instruction.cloud_draw": 'Draw the rain. Go from circle to circle.',
    "vertical_lines.instruction.icicle": 'Draw the icicles. Go from top to bottom.',
})
