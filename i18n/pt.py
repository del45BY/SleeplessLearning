"""Teks worksheet — Português (Brasil).

Semua teks yang tampil di PDF ada di sini (judul, instruksi, label, kata, footer).
Key harus identik di semua file bahasa (en.py adalah acuan; fallback ke en bila hilang).
Modul baru: tambahkan blok `STRINGS.update({...})` di bagian bawah file ini.
"""
STRINGS = {
    # --- common (header, identitas, footer) ---
    "common.name_label": 'Nome:',
    "common.date_label": 'Data:',
    "common.page": 'Página',
    "common.license": 'Apenas para uso pessoal e em sala de aula.',
    # --- bundle (cover + daftar isi) ---
    "bundle.default_title": 'Atividades pré-escolares',
    "bundle.cover_subtitle": 'Idades {age_min}–{age_max} anos',
    "bundle.toc_title": 'Sumário',
    "bundle.page_ref": 'pág. {n}',
}

# --- tracing_letters ---
STRINGS.update({
    "tracing_letters.title": 'Traçar letras',
    "tracing_letters.instruction": 'Cubra cada letra e depois escreva você mesmo.',
})
# (id gambar, kata) untuk huruf A..Z. Kata HARUS diawali huruf tersebut (dicek QC).
_LETTER_WORDS = [
    ('bee', 'Abelha'),  # A
    ('ball', 'Bola'),  # B
    ('house', 'Casa'),  # C
    ('dinosaur', 'Dinossauro'),  # D
    ('elephant', 'Elefante'),  # E
    ('flower', 'Flor'),  # F
    ('cat', 'Gato'),  # G
    ('helicopter', 'Helicóptero'),  # H
    ('island', 'Ilha'),  # I
    ('crocodile', 'Jacaré'),  # J
    ('kiwi', 'Kiwi'),  # K
    ('lion', 'Leão'),  # L
    ('apple', 'Maçã'),  # M
    ('ship', 'Navio'),  # N
    ('egg', 'Ovo'),  # O
    ('duck', 'Pato'),  # P
    ('cheese', 'Queijo'),  # Q
    ('mouse', 'Rato'),  # R
    ('sun', 'Sol'),  # S
    ('turtle', 'Tartaruga'),  # T
    ('grapes', 'Uva'),  # U
    ('cow', 'Vaca'),  # V
    ('waffle', 'Waffle'),  # W
    ('cup', 'Xícara'),  # X
    ('yoga', 'Yoga'),  # Y
    ('zebra', 'Zebra'),  # Z
]
for _L, (_img, _word) in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", _LETTER_WORDS):
    STRINGS[f"tracing_letters.img.{_L}"] = _img
    STRINGS[f"tracing_letters.word.{_L}"] = _word

# --- counting_1_10 ---
STRINGS.update({
    "counting_1_10.title": 'Contar de 1 a 10',
    "counting_1_10.instruction": 'Conte as figuras e cubra cada número.',
    "counting_1_10.num.1": 'um',
    "counting_1_10.num.2": 'dois',
    "counting_1_10.num.3": 'três',
    "counting_1_10.num.4": 'quatro',
    "counting_1_10.num.5": 'cinco',
    "counting_1_10.num.6": 'seis',
    "counting_1_10.num.7": 'sete',
    "counting_1_10.num.8": 'oito',
    "counting_1_10.num.9": 'nove',
    "counting_1_10.num.10": 'dez',
})

# --- vertical_lines ---
STRINGS.update({
    "vertical_lines.title": 'Linhas verticais',
    "vertical_lines.instruction.rain": 'Cubra a chuva de cima para baixo.',
    "vertical_lines.instruction.balloon": 'Cubra os fios dos balões para baixo.',
    "vertical_lines.instruction.candle": 'Cubra cada vela de cima para baixo.',
    "vertical_lines.instruction.fence": 'Cubra as estacas da cerca para baixo.',
    "vertical_lines.instruction.flower": 'Cubra os caules das flores para baixo.',
    "vertical_lines.instruction.tree": 'Cubra os troncos das árvores para baixo.',
    "vertical_lines.instruction.lollipop": 'Cubra os palitos dos pirulitos para baixo.',
    "vertical_lines.instruction.lamp": 'Cubra os postes de luz para baixo.',
    "vertical_lines.instruction.cloud_draw": 'Desenhe a chuva. Vá de círculo em círculo.',
    "vertical_lines.instruction.icicle": 'Desenhe os pingentes de gelo. Vá de cima para baixo.',
})

# --- horizontal_lines ---
STRINGS.update({
    "horizontal_lines.title": 'Linhas horizontais',
    "horizontal_lines.instruction.road": 'Cubra a estrada do carro até a casa.',
    "horizontal_lines.instruction.train": 'Cubra os trilhos do trem até a estação.',
    "horizontal_lines.instruction.bridge": 'Cubra a ponte da esquerda para a direita.',
    "horizontal_lines.instruction.clothesline": 'Cubra o varal de poste em poste.',
    "horizontal_lines.instruction.river": 'Cubra o rio do barco até a ilha.',
    "horizontal_lines.instruction.caterpillar": 'Cubra o caminho até a folha.',
    "horizontal_lines.instruction.wire": 'Cubra o fio do pássaro até o ninho.',
    "horizontal_lines.instruction.airplane": 'Cubra o voo do avião até a nuvem.',
    "horizontal_lines.instruction.snail": 'Desenhe o caminho até a folha, de círculo em círculo.',
    "horizontal_lines.instruction.ant": 'Desenhe o caminho até o biscoito, de círculo em círculo.',
})
