# Builds cec-brand-book.html from source/cec-template.html, embedding logos, logo SVGs and merch photos once as a JSON map.
# Run build_logo.py first if the logo artwork changes.
import base64, json, os
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)


def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


logos = {"full": "cec-logo-full-colour", "white": "cec-logo-white", "black": "cec-logo-black",
         "wordmark": "cec-wordmark-full-colour", "wordmarkWhite": "cec-wordmark-white", "markRed": "cec-mark-red"}
img = {k: data_uri(os.path.join(root, "logos", f + ".png"), "image/png") for k, f in logos.items()}
merch = ["mugs", "lapel-pins", "caps", "umbrella", "bottles", "book-cover", "stationery", "business-cards",
         "lanyards", "tote-notebook", "polos", "pull-up-banner"]
for m in merch:
    img["m_" + m.replace("-", "_")] = data_uri(os.path.join(root, "merch", m + ".webp"), "image/webp")
for k, f in {"d_app": "app-screens", "d_rooted": "billboard-rooted", "d_welcome": "billboard-welcome"}.items():
    img[k] = data_uri(os.path.join(root, "digital", f + ".webp"), "image/webp")
img["svgFull"] = open(os.path.join(root, "logos", "cec-logo-full-colour.svg"), encoding="utf-8").read()
img["svgWhite"] = open(os.path.join(root, "logos", "cec-logo-white.svg"), encoding="utf-8").read()

t = open(os.path.join(here, "cec-template.html"), encoding="utf-8").read()
assert "{{IMG_JSON}}" in t
t = t.replace("{{IMG_JSON}}", json.dumps(img).replace("</", "<\\/"))
open(os.path.join(root, "cec-brand-book.html"), "w", encoding="utf-8").write(t)
print("built", len(t))
