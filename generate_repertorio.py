#!/usr/bin/env python3
"""Generate A6 PDF with two-column music repertoire."""

from reportlab.lib.pagesizes import A6
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

OUTPUT = "repertorio_2026.pdf"

# A6 dimensions
WIDTH, HEIGHT = A6  # 105mm x 148mm approx

# Margins
MARGIN_TOP = 6 * mm
MARGIN_BOTTOM = 4 * mm
MARGIN_LEFT = 4 * mm
MARGIN_RIGHT = 4 * mm
COL_GAP = 3 * mm

# Column widths
usable_width = WIDTH - MARGIN_LEFT - MARGIN_RIGHT - COL_GAP
COL_WIDTH = usable_width / 2

# Column x positions
COL1_X = MARGIN_LEFT
COL2_X = MARGIN_LEFT + COL_WIDTH + COL_GAP

# Font sizes
TITLE_SIZE = 8
SECTION_SIZE = 6
SONG_SIZE = 5.5
HEADER_SIZE = 5

LINE_HEIGHT = 2.2 * mm


def draw_text(c, x, y, text, size, bold=False):
    font = "Helvetica-Bold" if bold else "Helvetica"
    c.setFont(font, size)
    c.drawString(x, y, text)
    return y


# Define the repertoire as structured data
# Each item: (text, type) where type is 'title', 'section', 'header', 'song', 'blank'
repertoire = [
    ("Repertorio 2026", "title"),
    ("", "blank"),
    ("Esquenta bateria", "header"),
    ("-Samba", "section"),
    ("Vou partir", "song"),
    ("Sol nascera", "song"),
    ("Tristeza", "song"),
    ("Imperio do samba", "song"),
    ("", "blank"),
    ("-Marchinhas", "section"),
    ("Abre alas", "song"),
    ("Mascara negra (acelera 2a volta)", "song"),
    ("Anda luzia", "song"),
    ("Turma do funil", "song"),
    ("Alla la oh", "song"),
    ("Balance", "song"),
    ("Quem sabe sabe", "song"),
    ("Ta-ih", "song"),
    ("", "blank"),
    ("-6/8", "section"),
    ("Coisa 5 / Preciso me encontrar", "song"),
    # --- Column 2 starts around here ---
    ("DIPLOMATA", "header"),
    ("-Samba", "section"),
    ("De volta ao samba", "song"),
    ("Sonho de um carnaval", "song"),
    ("Barracao/Lata dagua/Me deixa em paz", "song"),
    ("", "blank"),
    ("-Marchinha", "section"),
    ("Pastorinhas", "song"),
    ("Bandeira branca", "song"),
    ("Cachaca", "song"),
    ("Pierrot apaixonado", "song"),
    ("Aurora", "song"),
    ("Mamae eu quero", "song"),
    ("Jardineira", "song"),
    ("", "blank"),
    ("-Ijexa", "section"),
    ("Refazenda", "song"),
    ("Filhos de Gandhi", "song"),
    ("Emorio", "song"),
    ("", "blank"),
    ("-6/8", "section"),
    ("Luz negra", "song"),
    ("", "blank"),
    ("-Samba", "section"),
    ("Sorri de mim", "song"),
    ("Agora e cinza", "song"),
    ("A alegria continua", "song"),
    ("Agua de chuva/Pagodes da vida", "song"),
    ("", "blank"),
    ("Tem capoeira", "song"),
    ("E baiana", "song"),
    ("Caciqueando", "song"),
]


def get_line_height(item_type):
    if item_type == "title":
        return 3.2 * mm
    elif item_type == "blank":
        return 1.5 * mm
    elif item_type == "header":
        return 2.8 * mm
    elif item_type == "section":
        return 2.5 * mm
    else:
        return LINE_HEIGHT


def compute_split():
    """Find the best split point so both columns are roughly equal height."""
    total_h = sum(get_line_height(t) for _, t in repertoire)
    target = total_h / 2
    cumulative = 0
    best_idx = 0
    best_diff = float("inf")
    for i, (text, item_type) in enumerate(repertoire):
        cumulative += get_line_height(item_type)
        diff = abs(cumulative - target)
        if diff < best_diff:
            best_diff = diff
            best_idx = i + 1
    return best_idx


def draw_column(c, items, x, start_y):
    y = start_y
    for text, item_type in items:
        if item_type == "blank":
            y -= 1.5 * mm
            continue
        if item_type == "title":
            draw_text(c, x, y, text, TITLE_SIZE, bold=True)
            y -= 3.2 * mm
        elif item_type == "header":
            c.setFillColorRGB(0.15, 0.15, 0.15)
            draw_text(c, x, y, text, SECTION_SIZE + 0.5, bold=True)
            c.setFillColorRGB(0, 0, 0)
            y -= 2.8 * mm
        elif item_type == "section":
            c.setFillColorRGB(0.3, 0.3, 0.3)
            draw_text(c, x, y, text, SECTION_SIZE, bold=True)
            c.setFillColorRGB(0, 0, 0)
            y -= 2.5 * mm
        else:
            draw_text(c, x, y, text, SONG_SIZE)
            y -= LINE_HEIGHT
    return y


def main():
    split = compute_split()
    col1_items = repertoire[:split]
    col2_items = repertoire[split:]

    c = canvas.Canvas(OUTPUT, pagesize=A6)
    start_y = HEIGHT - MARGIN_TOP

    # Draw thin dividing line
    mid_x = MARGIN_LEFT + COL_WIDTH + COL_GAP / 2
    c.setStrokeColorRGB(0.7, 0.7, 0.7)
    c.setLineWidth(0.3)
    c.line(mid_x, HEIGHT - MARGIN_TOP + 2 * mm, mid_x, MARGIN_BOTTOM)

    draw_column(c, col1_items, COL1_X, start_y)
    draw_column(c, col2_items, COL2_X, start_y)

    c.save()
    print(f"PDF generated: {OUTPUT}")


if __name__ == "__main__":
    main()
