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

# --- horizontal_lines ---
STRINGS.update({
    "horizontal_lines.title": 'Horizontal Lines',
    "horizontal_lines.instruction.road": 'Trace the road from the car to the house.',
    "horizontal_lines.instruction.train": 'Trace the track from the train to the station.',
    "horizontal_lines.instruction.bridge": 'Trace the bridge from left to right.',
    "horizontal_lines.instruction.clothesline": 'Trace the clothesline from pole to pole.',
    "horizontal_lines.instruction.river": 'Trace the river from the boat to the island.',
    "horizontal_lines.instruction.caterpillar": 'Trace the path to the leaf.',
    "horizontal_lines.instruction.wire": 'Trace the wire from the bird to the nest.',
    "horizontal_lines.instruction.airplane": 'Trace the flight from the plane to the cloud.',
    "horizontal_lines.instruction.snail": 'Draw the path to the leaf, circle to circle.',
    "horizontal_lines.instruction.ant": 'Draw the path to the cookie, circle to circle.',
})

# --- diagonal_lines ---
STRINGS.update({
    "diagonal_lines.title": 'Diagonal Lines',
    "diagonal_lines.instruction.slide": 'Trace the slide from the top to the bottom.',
    "diagonal_lines.instruction.ladder": 'Trace the ladder from the window to the ground.',
    "diagonal_lines.instruction.kite_string": 'Trace the kite strings down to the hands.',
    "diagonal_lines.instruction.roof": 'Trace both sides of each roof.',
    "diagonal_lines.instruction.ice_cream": 'Trace each ice cream cone.',
    "diagonal_lines.instruction.kite_frame": 'Trace the kite sticks. Make an X.',
    "diagonal_lines.instruction.tent": 'Trace both sides of each tent.',
    "diagonal_lines.instruction.ski": 'Trace the ski path down the mountain.',
    "diagonal_lines.instruction.treasure": 'Draw an X on each map, circle to circle.',
    "diagonal_lines.instruction.star": 'Draw the stars falling to the moon, circle to circle.',
})

# --- zigzag_lines ---
STRINGS.update({
    "zigzag_lines.title": 'Zigzag Lines',
    "zigzag_lines.instruction.mountain_one": 'Trace the mountain from the hiker to the flag.',
    "zigzag_lines.instruction.mountain_two": 'Trace the two mountains.',
    "zigzag_lines.instruction.mountain_many": 'Trace the mountains. Go up and down.',
    "zigzag_lines.instruction.lightning": 'Trace the lightning from the cloud down.',
    "zigzag_lines.instruction.fence": 'Trace the zigzag fence for the cat.',
    "zigzag_lines.instruction.road": 'Trace the winding road from the car to the house.',
    "zigzag_lines.instruction.lightning_dots": 'Trace the lightning. Follow the dots.',
    "zigzag_lines.instruction.river": 'Trace the winding river from the boat to the island.',
    "zigzag_lines.instruction.lightning_draw": 'Draw the lightning, circle to circle.',
    "zigzag_lines.instruction.mountain_draw": 'Draw the mountains, circle to circle.',
})

# --- curved_lines ---
STRINGS.update({
    "curved_lines.title": 'Curved Lines',
    "curved_lines.instruction.rainbow_one": 'Trace the rainbow from cloud to cloud.',
    "curved_lines.instruction.rainbow_three": 'Trace all three bands of each rainbow.',
    "curved_lines.instruction.smile": 'Trace a smile on each face.',
    "curved_lines.instruction.rope": 'Trace the rope between the poles.',
    "curved_lines.instruction.umbrella": 'Trace the umbrella top and the handle.',
    "curved_lines.instruction.caterpillar": 'Trace the hills for the caterpillar.',
    "curved_lines.instruction.hook": 'Trace the fishing lines down to the hooks.',
    "curved_lines.instruction.lollipop": 'Trace the swirl on each lollipop.',
    "curved_lines.instruction.rainbow_draw": 'Draw the rainbows, circle to circle.',
    "curved_lines.instruction.umbrella_draw": 'Draw the umbrellas, circle to circle.',
})

# --- wavy_lines ---
STRINGS.update({
    "wavy_lines.title": 'Wavy Lines',
    "wavy_lines.instruction.sea_one": 'Trace the big waves from the fish to the shell.',
    "wavy_lines.instruction.sea_two": 'Trace the waves. Up and down, up and down.',
    "wavy_lines.instruction.snake": 'Trace the wavy snake to the apple.',
    "wavy_lines.instruction.river": 'Trace the wavy river from the mountain to the lake.',
    "wavy_lines.instruction.hair": 'Trace the wavy hair under each bow.',
    "wavy_lines.instruction.sea_dots": 'Trace the sea waves. Follow the dots.',
    "wavy_lines.instruction.snake_dots": 'Trace the wavy snakes. Follow the dots.',
    "wavy_lines.instruction.hair_dots": 'Trace the wavy hair. Follow the dots.',
    "wavy_lines.instruction.sea_draw": 'Draw the waves, circle to circle.',
    "wavy_lines.instruction.river_draw": 'Draw the rivers, circle to circle.',
})

# --- circles_spirals ---
STRINGS.update({
    "circles_spirals.title": 'Circles & Spirals',
    "circles_spirals.instruction.ball": 'Trace the ball. Start at the top.',
    "circles_spirals.instruction.sun": 'Trace the sun above each house.',
    "circles_spirals.instruction.wheel": 'Trace the two wheels of each car.',
    "circles_spirals.instruction.target": 'Trace all the circles on each target.',
    "circles_spirals.instruction.snail": "Trace the snail's shell. Go round and round.",
    "circles_spirals.instruction.bubble": 'Trace the bubbles above the fish.',
    "circles_spirals.instruction.bike": 'Trace the two wheels of each bike.',
    "circles_spirals.instruction.snail_out": "Trace the snail's shell from the middle out.",
    "circles_spirals.instruction.target_draw": 'Draw the targets, circle to circle.',
    "circles_spirals.instruction.snail_draw": 'Draw the shells from the middle, circle to circle.',
})
