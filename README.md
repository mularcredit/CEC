# Christ Extension Church — Brand Book

Brand identity for Christ Extension Church Int'l. Tagline: *Prospering His pleasure on earth*.

## Deliverables

| File | What it is |
| --- | --- |
| `cec-brand-book.html` | The interactive brand book. One self-contained file; open it in any browser. |
| `CEC Brand Book.pdf` | The same book as a 20-page PDF, one page per chapter, with bookmarks. |
| `logos/` | Logo artwork: full colour, white and black logos, and versions without the tagline, as SVG, PDF and PNG. The mark (the cross with its tail) as SVG. |
| `letterhead/CEC Letterhead Concepts.pdf` | Four letterhead concepts (A4), with `letterhead-concepts.html` reviewing the current letterhead. |
| `merch/`, `digital/` | Merchandise, app and billboard concept visuals used in the book. |

## Editing

Edit `source/cec-template.html`, then rebuild:

```bash
python source/build_logo.py      # only if the logo artwork changes
python source/build.py           # rebuilds cec-brand-book.html
node source/export_pdf.cjs && python source/merge_pdf.py   # rebuilds the PDF
```

The letterhead concepts follow the same pattern: `letterhead/build_concepts.py`, then `node letterhead/export_concepts_pdf.cjs`.

### Requirements

- Python 3 with Pillow, NumPy and PyMuPDF.
- The logo fonts Baskerville Old Face (`BASKVILL.TTF`) and Rage Italic (`RAGE.TTF`), which ship with Microsoft Office on Windows.
- Node with Playwright and Google Chrome for the PDF exports. The export scripts currently load Playwright from a local path and use Chrome's default Windows install location. Update both paths at the top of each script on another machine.
