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

# --- diagonal_lines ---
STRINGS.update({
    "diagonal_lines.title": 'Linhas inclinadas',
    "diagonal_lines.instruction.slide": 'Cubra o escorregador de cima para baixo.',
    "diagonal_lines.instruction.ladder": 'Cubra a escada da janela até o chão.',
    "diagonal_lines.instruction.kite_string": 'Cubra as linhas das pipas para baixo.',
    "diagonal_lines.instruction.roof": 'Cubra os dois lados de cada telhado.',
    "diagonal_lines.instruction.ice_cream": 'Cubra cada casquinha de sorvete.',
    "diagonal_lines.instruction.kite_frame": 'Cubra as varetas da pipa. Faça um X.',
    "diagonal_lines.instruction.tent": 'Cubra os dois lados de cada barraca.',
    "diagonal_lines.instruction.ski": 'Cubra a pista de esqui na montanha.',
    "diagonal_lines.instruction.treasure": 'Desenhe um X em cada mapa, de círculo em círculo.',
    "diagonal_lines.instruction.star": 'Desenhe as estrelas até a lua, de círculo em círculo.',
})

# --- zigzag_lines ---
STRINGS.update({
    "zigzag_lines.title": 'Linhas em zigue-zague',
    "zigzag_lines.instruction.mountain_one": 'Cubra a montanha do alpinista até a bandeira.',
    "zigzag_lines.instruction.mountain_two": 'Cubra as duas montanhas.',
    "zigzag_lines.instruction.mountain_many": 'Cubra as montanhas. Suba e desça.',
    "zigzag_lines.instruction.lightning": 'Cubra o raio da nuvem para baixo.',
    "zigzag_lines.instruction.fence": 'Cubra a cerca de pontas para o gato.',
    "zigzag_lines.instruction.road": 'Cubra a estrada com curvas do carro até a casa.',
    "zigzag_lines.instruction.lightning_dots": 'Cubra o raio. Siga os pontinhos.',
    "zigzag_lines.instruction.river": 'Cubra o rio com curvas do barco até a ilha.',
    "zigzag_lines.instruction.lightning_draw": 'Desenhe o raio, de círculo em círculo.',
    "zigzag_lines.instruction.mountain_draw": 'Desenhe as montanhas, de círculo em círculo.',
})

# --- curved_lines ---
STRINGS.update({
    "curved_lines.title": 'Linhas curvas',
    "curved_lines.instruction.rainbow_one": 'Cubra o arco-íris de nuvem em nuvem.',
    "curved_lines.instruction.rainbow_three": 'Cubra as três faixas de cada arco-íris.',
    "curved_lines.instruction.smile": 'Cubra um sorriso em cada rosto.',
    "curved_lines.instruction.rope": 'Cubra a corda entre os postes.',
    "curved_lines.instruction.umbrella": 'Cubra o guarda-chuva e o cabo.',
    "curved_lines.instruction.caterpillar": 'Cubra os morros da lagarta.',
    "curved_lines.instruction.hook": 'Cubra as linhas de pesca até os anzóis.',
    "curved_lines.instruction.lollipop": 'Cubra o redemoinho de cada pirulito.',
    "curved_lines.instruction.rainbow_draw": 'Desenhe os arco-íris, de círculo em círculo.',
    "curved_lines.instruction.umbrella_draw": 'Desenhe os guarda-chuvas, de círculo em círculo.',
})

# --- wavy_lines ---
STRINGS.update({
    "wavy_lines.title": 'Linhas onduladas',
    "wavy_lines.instruction.sea_one": 'Cubra as ondas grandes do peixe até a concha.',
    "wavy_lines.instruction.sea_two": 'Cubra as ondas. Sobe e desce, sobe e desce.',
    "wavy_lines.instruction.snake": 'Cubra a cobra ondulada até a maçã.',
    "wavy_lines.instruction.river": 'Cubra o rio com curvas da montanha até o lago.',
    "wavy_lines.instruction.hair": 'Cubra o cabelo ondulado embaixo de cada laço.',
    "wavy_lines.instruction.sea_dots": 'Cubra as ondas do mar. Siga os pontinhos.',
    "wavy_lines.instruction.snake_dots": 'Cubra as cobras. Siga os pontinhos.',
    "wavy_lines.instruction.hair_dots": 'Cubra o cabelo ondulado. Siga os pontinhos.',
    "wavy_lines.instruction.sea_draw": 'Desenhe as ondas, de círculo em círculo.',
    "wavy_lines.instruction.river_draw": 'Desenhe os rios, de círculo em círculo.',
})

# --- circles_spirals ---
STRINGS.update({
    "circles_spirals.title": 'Círculos e espirais',
    "circles_spirals.instruction.ball": 'Cubra a bola. Comece em cima.',
    "circles_spirals.instruction.sun": 'Cubra o sol em cima de cada casa.',
    "circles_spirals.instruction.wheel": 'Cubra as duas rodas de cada carro.',
    "circles_spirals.instruction.target": 'Cubra todos os círculos de cada alvo.',
    "circles_spirals.instruction.snail": 'Cubra a concha do caracol. Gire e gire.',
    "circles_spirals.instruction.bubble": 'Cubra as bolhas em cima do peixe.',
    "circles_spirals.instruction.bike": 'Cubra as duas rodas de cada bicicleta.',
    "circles_spirals.instruction.snail_out": 'Cubra a concha do caracol do meio para fora.',
    "circles_spirals.instruction.target_draw": 'Desenhe os alvos, de círculo em círculo.',
    "circles_spirals.instruction.snail_draw": 'Desenhe as conchas, de círculo em círculo.',
})
