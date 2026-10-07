# Builds letterhead-concepts.html (images embedded) from concepts-template.html.
# For the PDF, run: node export_concepts_pdf.cjs  (prints the four letterheads as A4 pages)
import base64, io, os
from PIL import Image

here = os.path.dirname(os.path.abspath(__file__))


def uri(img, fmt, mime, **kw):
    b = io.BytesIO()
    img.save(b, fmt, **kw)
    return f"data:{mime};base64," + base64.b64encode(b.getvalue()).decode()


logo = Image.open(os.path.join(here, "..", "logos", "cec-logo-full-colour.png"))
logo.thumbnail((2400, 2400))
t = open(os.path.join(here, "concepts-template.html"), encoding="utf-8").read()
t = (t.replace("{{LOGO}}", uri(logo, "PNG", "image/png", optimize=True))
      .replace("{{LAMB}}", uri(Image.open(os.path.join(here, "lamb-small.png")), "PNG", "image/png", optimize=True))
      .replace("{{CURRENT}}", uri(Image.open(os.path.join(here, "current-letterhead.jpg")), "JPEG", "image/jpeg", quality=85)))
assert "{{" not in t
open(os.path.join(here, "letterhead-concepts.html"), "w", encoding="utf-8").write(t)
print("built", len(t))
