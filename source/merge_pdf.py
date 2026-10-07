# Merges the per-chapter captures from export_pdf.cjs into "CEC Brand Book.pdf" with bookmarks.
import glob, io, os
import pymupdf
from PIL import Image

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
NAMES = ["Cover", "Our Affirmation", "Contents", "01 Who We Are", "02 Our Foundation", "03 The Logo",
         "04 Clear Space & Size", "05 Logo Versions", "06 The Mark", "07 The Extension Line", "08 Logo Misuse",
         "09 Colour", "10 Typography", "11 Voice & Tone", "12 In Practice", "13 On Screen & Outdoor", "14 Merchandise",
         "15 Post Studio", "16 Downloads", "Back cover"]

parts = sorted(glob.glob(os.path.join(here, "pdf-parts", "*.png")))
assert len(parts) == len(NAMES), (len(parts), len(NAMES))
out = pymupdf.open()
for f in parts:
    im = Image.open(f).convert("RGB")
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=88, optimize=True)
    # captured at 2x, so 1 CSS px = 0.75 pt at full size
    w, h = im.size[0] / 2 * 0.75, im.size[1] / 2 * 0.75
    out.new_page(width=w, height=h).insert_image(pymupdf.Rect(0, 0, w, h), stream=buf.getvalue())
out.set_metadata({"title": "Christ Extension Church — Brand Book", "author": "Figbloom Digital",
                  "subject": "Brand identity guidelines, Edition 1.0, 2026"})
out.set_toc([[1, n, i + 1] for i, n in enumerate(NAMES)])
dest = os.path.join(root, "CEC Brand Book.pdf")
out.save(dest, garbage=4, deflate=True)
print(out.page_count, "pages,", os.path.getsize(dest), "bytes")
