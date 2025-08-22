from pathlib import Path

DOM_EXTRACTOR_PATH = (Path(__file__).resolve().parent.parent.parent / "dom_extractor.js").resolve()

if not DOM_EXTRACTOR_PATH.exists():
    raise FileNotFoundError(f"dom_extractor.js not found at {DOM_EXTRACTOR_PATH}")

with open(DOM_EXTRACTOR_PATH, "r", encoding="utf-8") as f:
    BUILD_TREE_JS = f.read()
