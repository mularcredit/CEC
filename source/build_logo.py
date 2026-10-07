# Rebuilds the CEC logo as vector artwork from the layout of "CEC logo.pdf" (Publisher),
# with the confirmed tagline "Prospering His pleasure on earth".
# Outputs PDF, SVG (text converted to outlines) and high-res PNGs into ../logos.
import os
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "logos")
BASK = r"C:\Windows\Fonts\BASKVILL.TTF"   # Baskerville Old Face
RAGE = r"C:\Windows\Fonts\RAGE.TTF"       # Rage Italic

# Publisher widened the space after "Chris" (+10.9 pt) to make room for the cross, so set the two runs separately.
WORDMARK = [("Chris", (49.7, 331.0)), ("Extension Church", (175.3, 331.0))]
WORDMARK_SIZE = 48.0
TAGLINE = ("Prospering His pleasure on earth", 27.96, (176.7, 371.8))

# The red mark was placed in the PDF as a 2172x724 image stretched into this box (points).
IMG_BOX = (115.1, 217.7, 561.9, 396.3)
SX = (IMG_BOX[2] - IMG_BOX[0]) / 2172
SY = (IMG_BOX[3] - IMG_BOX[1]) / 724
# Mark geometry in image pixels: crossbar, stem, tail (x0, y0, x1, y1).
MARK_PX = [(141, 254, 320, 278), (218, 172, 242, 514), (218, 490, 2036, 514)]
MARK = [pymupdf.Rect(IMG_BOX[0] + a * SX, IMG_BOX[1] + b * SY, IMG_BOX[0] + c * SX, IMG_BOX[1] + d * SY) for a, b, c, d in MARK_PX]

RED = (181 / 255, 0, 0)
INK = (0, 0, 0)
WHITE = (1, 1, 1)


def render(text_col, mark_col, tagline=True):
    doc = pymupdf.open()
    page = doc.new_page(width=595.32, height=841.92)
    for r in MARK:
        page.draw_rect(r, color=None, fill=mark_col, width=0)
    tw = pymupdf.TextWriter(page.rect)
    bask = pymupdf.Font(fontfile=BASK)
    rage = pymupdf.Font(fontfile=RAGE)
    for text, origin in WORDMARK:
        tw.append(origin, text, font=bask, fontsize=WORDMARK_SIZE)
    if tagline:
        tw.append(TAGLINE[2], TAGLINE[0], font=rage, fontsize=TAGLINE[1])
    tw.write_text(page, color=text_col)
    # crop to the artwork with a small margin
    box = pymupdf.Rect(MARK[0])
    for r in MARK:
        box |= r
    box |= tw.text_rect
    box = pymupdf.Rect(box.x0 - 3, box.y0 - 3, box.x1 + 3, box.y1 + 3)
    page.set_cropbox(box)
    return doc, page


VARIANTS = {
    "cec-logo-full-colour": (INK, RED, True),
    "cec-logo-white": (WHITE, WHITE, True),
    "cec-logo-black": (INK, INK, True),
    "cec-wordmark-full-colour": (INK, RED, False),
    "cec-wordmark-white": (WHITE, WHITE, False),
}

for name, (tc, mc, tag) in VARIANTS.items():
    doc, page = render(tc, mc, tag)
    doc.save(os.path.join(OUT, name + ".pdf"))
    with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8") as f:
        f.write(page.get_svg_image(text_as_path=True))
    page.get_pixmap(dpi=600, alpha=True).save(os.path.join(OUT, name + ".png"))
    print(name, "ok")
