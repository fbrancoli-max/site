#!/usr/bin/env python3
"""Generate A6 PDF with two-column music repertoire, filling the entire page."""

from reportlab.lib.pagesizes import A6
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

OUTPUT = "repertorio_2026.pdf"

WIDTH, HEIGHT = A6  # 105mm x 148mm

MARGIN_TOP = 3 * mm
MARGIN_BOTTOM = 3 * mm
MARGIN_LEFT = 3 * mm
MARGIN_RIGHT = 3 * mm
COL_GAP = 2.5 * mm

usable_width = WIDTH - MARGIN_LEFT - MARGIN_RIGHT - COL_GAP
COL_WIDTH = usable_width / 2
COL1_X = MARGIN_LEFT
COL2_X = MARGIN_LEFT + COL_WIDTH + COL_GAP
AVAILABLE_HEIGHT = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM

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


def max_font_for_col(items, font_name, col_width):
    """Find max font size so all text in items fits within col_width."""
    size = 12.0
    while size > 4.0:
        fits = True
        for text, typ in items:
            if typ == "blank":
                continue
            fn = font_name + "-Bold" if typ in ("title", "header", "section") else font_name
            w = stringWidth(text, fn, size)
            if w > col_width:
                fits = False
                break
        if fits:
            return size
        size -= 0.25
    return size


def compute_split_idx(items):
    """Split items into two roughly equal groups by count of non-blank lines."""
    total = sum(1 for _, t in items if t != "blank")
    count = 0
    for i, (_, t) in enumerate(items):
        if t != "blank":
            count += 1
        if count >= total / 2:
            return i + 1
    return len(items) // 2


def draw_column(c, items, x, start_y, end_y, font_size):
    """Draw items in a column, distributing them evenly between start_y and end_y."""
    # Count content lines and blanks
    content_lines = [(text, typ) for text, typ in items if typ != "blank"]
    blank_count = sum(1 for _, t in items if t == "blank")

    if not content_lines:
        return

    # Title and header get slightly more space
    weighted_lines = 0
    for text, typ in items:
        if typ == "blank":
            weighted_lines += 0.5
        elif typ == "title":
            weighted_lines += 1.6
        elif typ == "header":
            weighted_lines += 1.4
        elif typ == "section":
            weighted_lines += 1.2
        else:
            weighted_lines += 1.0

    total_space = start_y - end_y
    unit = total_space / weighted_lines

    y = start_y
    for text, typ in items:
        if typ == "blank":
            y -= unit * 0.5
            continue

        weight = {"title": 1.6, "header": 1.4, "section": 1.2, "song": 1.0}[typ]
        line_space = unit * weight

        # Draw text vertically centered in its allocated space
        text_y = y - line_space * 0.35  # position text in upper portion of space

        if typ == "title":
            fs = font_size * 1.5
            c.setFont("Helvetica-Bold", fs)
            c.setFillColorRGB(0, 0, 0)
            c.drawString(x, text_y, text)
        elif typ == "header":
            fs = font_size * 1.15
            c.setFont("Helvetica-Bold", fs)
            c.setFillColorRGB(0.15, 0.15, 0.15)
            c.drawString(x, text_y, text)
            c.setFillColorRGB(0, 0, 0)
        elif typ == "section":
            fs = font_size * 1.05
            c.setFont("Helvetica-Bold", fs)
            c.setFillColorRGB(0.3, 0.3, 0.3)
            c.drawString(x, text_y, text)
            c.setFillColorRGB(0, 0, 0)
        else:
            c.setFont("Helvetica", font_size)
            c.drawString(x, text_y, text)

        y -= line_space


def main():
    split = compute_split_idx(repertoire)
    col1_items = repertoire[:split]
    col2_items = repertoire[split:]

    # Find max font that fits both columns
    fs1 = max_font_for_col(col1_items, "Helvetica", COL_WIDTH)
    fs2 = max_font_for_col(col2_items, "Helvetica", COL_WIDTH)
    font_size = min(fs1, fs2)

    # Now check with the actual scaled sizes (title=1.5x, header=1.15x, section=1.05x)
    for text, typ in repertoire:
        if typ == "blank":
            continue
        scale = {"title": 1.5, "header": 1.15, "section": 1.05, "song": 1.0}[typ]
        fn = "Helvetica-Bold" if typ in ("title", "header", "section") else "Helvetica"
        while stringWidth(text, fn, font_size * scale) > COL_WIDTH and font_size > 4:
            font_size -= 0.25

    print(f"Font size: {font_size:.1f}pt")

    c = canvas.Canvas(OUTPUT, pagesize=A6)
    start_y = HEIGHT - MARGIN_TOP
    end_y = MARGIN_BOTTOM

    # Dividing line
    mid_x = MARGIN_LEFT + COL_WIDTH + COL_GAP / 2
    c.setStrokeColorRGB(0.75, 0.75, 0.75)
    c.setLineWidth(0.3)
    c.line(mid_x, start_y + 1 * mm, mid_x, end_y)

    draw_column(c, col1_items, COL1_X, start_y, end_y, font_size)
    draw_column(c, col2_items, COL2_X, start_y, end_y, font_size)

    c.save()
    print(f"PDF generated: {OUTPUT}")


if __name__ == "__main__":
    main()
