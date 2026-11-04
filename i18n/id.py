"""Teks worksheet — Bahasa Indonesia.

Semua teks yang tampil di PDF ada di sini (judul, instruksi, label, kata, footer).
Key harus identik di semua file bahasa (en.py adalah acuan; fallback ke en bila hilang).
Modul baru: tambahkan blok `STRINGS.update({...})` di bagian bawah file ini.
"""
STRINGS = {
    # --- common (header, identitas, footer) ---
    "common.name_label": 'Nama:',
    "common.date_label": 'Tanggal:',
    "common.page": 'Halaman',
    "common.license": 'Hanya untuk penggunaan pribadi dan kelas.',
    # --- bundle (cover + daftar isi) ---
    "bundle.default_title": 'Worksheet Prasekolah',
    "bundle.cover_subtitle": 'Usia {age_min}–{age_max} tahun',
    "bundle.toc_title": 'Daftar Isi',
    "bundle.page_ref": 'hlm. {n}',
}

# --- tracing_letters ---
STRINGS.update({
    "tracing_letters.title": 'Menebalkan Huruf',
    "tracing_letters.instruction": 'Tebalkan setiap huruf, lalu tulis sendiri.',
})
# (id gambar, kata) untuk huruf A..Z. Kata HARUS diawali huruf tersebut (dicek QC).
_LETTER_WORDS = [
    ('apel', 'Apel'),  # A
    ('bola', 'Bola'),  # B
    ('cangkir', 'Cangkir'),  # C
    ('domba', 'Domba'),  # D
    ('es_krim', 'Es krim'),  # E
    ('flamingo', 'Flamingo'),  # F
    ('gajah', 'Gajah'),  # G
    ('harimau', 'Harimau'),  # H
    ('ikan', 'Ikan'),  # I
    ('jeruk', 'Jeruk'),  # J
    ('kucing', 'Kucing'),  # K
    ('lebah', 'Lebah'),  # L
    ('mobil', 'Mobil'),  # M
    ('nanas', 'Nanas'),  # N
    ('orangutan', 'Orangutan'),  # O
    ('pisang', 'Pisang'),  # P
    ('quokka', 'Quokka'),  # Q
    ('rumah', 'Rumah'),  # R
    ('sapi', 'Sapi'),  # S
    ('topi', 'Topi'),  # T
    ('ular', 'Ular'),  # U
    ('vas', 'Vas'),  # V
    ('wortel', 'Wortel'),  # W
    ('xilofon', 'Xilofon'),  # X
    ('yoyo', 'Yoyo'),  # Y
    ('zebra', 'Zebra'),  # Z
]
for _L, (_img, _word) in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", _LETTER_WORDS):
    STRINGS[f"tracing_letters.img.{_L}"] = _img
    STRINGS[f"tracing_letters.word.{_L}"] = _word

# --- counting_1_10 ---
STRINGS.update({
    "counting_1_10.title": 'Berhitung 1–10',
    "counting_1_10.instruction": 'Hitung gambarnya dan tebalkan angkanya.',
    "counting_1_10.num.1": 'satu',
    "counting_1_10.num.2": 'dua',
    "counting_1_10.num.3": 'tiga',
    "counting_1_10.num.4": 'empat',
    "counting_1_10.num.5": 'lima',
    "counting_1_10.num.6": 'enam',
    "counting_1_10.num.7": 'tujuh',
    "counting_1_10.num.8": 'delapan',
    "counting_1_10.num.9": 'sembilan',
    "counting_1_10.num.10": 'sepuluh',
})

# --- vertical_lines ---
STRINGS.update({
    "vertical_lines.title": 'Garis Tegak',
    "vertical_lines.instruction.rain": 'Tebalkan hujan dari atas ke bawah.',
    "vertical_lines.instruction.balloon": 'Tebalkan tali balon ke bawah.',
    "vertical_lines.instruction.candle": 'Tebalkan setiap lilin dari atas ke bawah.',
    "vertical_lines.instruction.fence": 'Tebalkan tiang pagar ke bawah.',
    "vertical_lines.instruction.flower": 'Tebalkan batang bunga ke bawah.',
    "vertical_lines.instruction.tree": 'Tebalkan batang pohon ke bawah.',
    "vertical_lines.instruction.lollipop": 'Tebalkan tangkai permen ke bawah.',
    "vertical_lines.instruction.lamp": 'Tebalkan tiang lampu ke bawah.',
    "vertical_lines.instruction.cloud_draw": 'Gambar hujannya. Tarik dari lingkaran ke lingkaran.',
    "vertical_lines.instruction.icicle": 'Gambar es yang menggantung. Tarik dari atas ke bawah.',
})

# --- horizontal_lines ---
STRINGS.update({
    "horizontal_lines.title": 'Garis Datar',
    "horizontal_lines.instruction.road": 'Tebalkan jalan dari mobil ke rumah.',
    "horizontal_lines.instruction.train": 'Tebalkan rel dari kereta ke stasiun.',
    "horizontal_lines.instruction.bridge": 'Tebalkan jembatan dari kiri ke kanan.',
    "horizontal_lines.instruction.clothesline": 'Tebalkan tali jemuran dari tiang ke tiang.',
    "horizontal_lines.instruction.river": 'Tebalkan sungai dari perahu ke pulau.',
    "horizontal_lines.instruction.caterpillar": 'Tebalkan jalan ke daun.',
    "horizontal_lines.instruction.wire": 'Tebalkan kawat dari burung ke sarang.',
    "horizontal_lines.instruction.airplane": 'Tebalkan jalur dari pesawat ke awan.',
    "horizontal_lines.instruction.snail": 'Gambar jalan ke daun, dari lingkaran ke lingkaran.',
    "horizontal_lines.instruction.ant": 'Gambar jalan ke kue, dari lingkaran ke lingkaran.',
})

# --- diagonal_lines ---
STRINGS.update({
    "diagonal_lines.title": 'Garis Miring',
    "diagonal_lines.instruction.slide": 'Tebalkan perosotan dari atas ke bawah.',
    "diagonal_lines.instruction.ladder": 'Tebalkan tangga dari jendela ke tanah.',
    "diagonal_lines.instruction.kite_string": 'Tebalkan tali layang-layang ke bawah.',
    "diagonal_lines.instruction.roof": 'Tebalkan kedua sisi atap.',
    "diagonal_lines.instruction.ice_cream": 'Tebalkan kerucut es krim.',
    "diagonal_lines.instruction.kite_frame": 'Tebalkan rangka layang-layang. Buat huruf X.',
    "diagonal_lines.instruction.tent": 'Tebalkan kedua sisi tenda.',
    "diagonal_lines.instruction.ski": 'Tebalkan jalur ski menuruni gunung.',
    "diagonal_lines.instruction.treasure": 'Gambar X di setiap peta, dari lingkaran ke lingkaran.',
    "diagonal_lines.instruction.star": 'Gambar bintang jatuh ke bulan, dari lingkaran ke lingkaran.',
})

# --- zigzag_lines ---
STRINGS.update({
    "zigzag_lines.title": 'Garis Zigzag',
    "zigzag_lines.instruction.mountain_one": 'Tebalkan gunung dari pendaki ke bendera.',
    "zigzag_lines.instruction.mountain_two": 'Tebalkan dua gunung.',
    "zigzag_lines.instruction.mountain_many": 'Tebalkan gunung-gunung. Naik dan turun.',
    "zigzag_lines.instruction.lightning": 'Tebalkan kilat dari awan ke bawah.',
    "zigzag_lines.instruction.fence": 'Tebalkan pagar bergerigi untuk si kucing.',
    "zigzag_lines.instruction.road": 'Tebalkan jalan berliku dari mobil ke rumah.',
    "zigzag_lines.instruction.lightning_dots": 'Tebalkan kilat. Ikuti titik-titiknya.',
    "zigzag_lines.instruction.river": 'Tebalkan sungai berliku dari perahu ke pulau.',
    "zigzag_lines.instruction.lightning_draw": 'Gambar kilat, dari lingkaran ke lingkaran.',
    "zigzag_lines.instruction.mountain_draw": 'Gambar gunung, dari lingkaran ke lingkaran.',
})

# --- curved_lines ---
STRINGS.update({
    "curved_lines.title": 'Garis Lengkung',
    "curved_lines.instruction.rainbow_one": 'Tebalkan pelangi dari awan ke awan.',
    "curved_lines.instruction.rainbow_three": 'Tebalkan ketiga lengkung setiap pelangi.',
    "curved_lines.instruction.smile": 'Tebalkan senyum di setiap wajah.',
    "curved_lines.instruction.rope": 'Tebalkan tali di antara kedua tiang.',
    "curved_lines.instruction.umbrella": 'Tebalkan atas payung dan gagangnya.',
    "curved_lines.instruction.caterpillar": 'Tebalkan bukit-bukit untuk ulat.',
    "curved_lines.instruction.hook": 'Tebalkan tali pancing ke bawah sampai kail.',
    "curved_lines.instruction.lollipop": 'Tebalkan pusaran di setiap permen.',
    "curved_lines.instruction.rainbow_draw": 'Gambar pelangi, dari lingkaran ke lingkaran.',
    "curved_lines.instruction.umbrella_draw": 'Gambar payung, dari lingkaran ke lingkaran.',
})

# --- wavy_lines ---
STRINGS.update({
    "wavy_lines.title": 'Garis Bergelombang',
    "wavy_lines.instruction.sea_one": 'Tebalkan ombak besar dari ikan ke kerang.',
    "wavy_lines.instruction.sea_two": 'Tebalkan ombaknya. Naik turun, naik turun.',
    "wavy_lines.instruction.snake": 'Tebalkan ular yang berlekuk sampai apel.',
    "wavy_lines.instruction.river": 'Tebalkan sungai berkelok dari gunung ke danau.',
    "wavy_lines.instruction.hair": 'Tebalkan rambut bergelombang di bawah setiap pita.',
    "wavy_lines.instruction.sea_dots": 'Tebalkan ombak laut. Ikuti titik-titiknya.',
    "wavy_lines.instruction.snake_dots": 'Tebalkan ular-ular itu. Ikuti titik-titiknya.',
    "wavy_lines.instruction.hair_dots": 'Tebalkan rambut bergelombang. Ikuti titik-titiknya.',
    "wavy_lines.instruction.sea_draw": 'Gambar ombak, dari lingkaran ke lingkaran.',
    "wavy_lines.instruction.river_draw": 'Gambar sungai, dari lingkaran ke lingkaran.',
})

# --- circles_spirals ---
STRINGS.update({
    "circles_spirals.title": 'Lingkaran & Spiral',
    "circles_spirals.instruction.ball": 'Tebalkan bola. Mulai dari atas.',
    "circles_spirals.instruction.sun": 'Tebalkan matahari di atas setiap rumah.',
    "circles_spirals.instruction.wheel": 'Tebalkan kedua roda setiap mobil.',
    "circles_spirals.instruction.target": 'Tebalkan semua lingkaran pada setiap sasaran.',
    "circles_spirals.instruction.snail": 'Tebalkan cangkang keong. Putar dan putar.',
    "circles_spirals.instruction.bubble": 'Tebalkan gelembung di atas ikan.',
    "circles_spirals.instruction.bike": 'Tebalkan kedua roda setiap sepeda.',
    "circles_spirals.instruction.snail_out": 'Tebalkan cangkang keong dari tengah ke luar.',
    "circles_spirals.instruction.target_draw": 'Gambar sasaran, dari lingkaran ke lingkaran.',
    "circles_spirals.instruction.snail_draw": 'Gambar cangkang dari tengah, dari lingkaran ke lingkaran.',
})
