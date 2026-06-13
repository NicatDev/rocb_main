import pathlib

root = pathlib.Path(__file__).resolve().parents[1] / "templates"
needle = "<script src=\"{% static 'assets/js/navbar.js' %}\"></script>"
repl = (
    "{% include 'components/openai_translate_assets.html' %}\n"
    "        <script src=\"{% static 'assets/js/navbar.js' %}\"></script>"
)

for path in root.rglob("*.html"):
    text = path.read_text(encoding="utf-8")
    if "navbar.js" in text and "openai_translate_assets" not in text:
        new = text.replace(needle, repl)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print("updated", path.relative_to(root))
