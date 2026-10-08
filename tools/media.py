"""A converted lab's pictures and drawn figures (four-items call 4.3; D-0117).

Usage, at conversion:
  python tools/media.py list ORIGINAL.docx
      Each picture in the original, in the word check's reading order: its
      part, Word's size, crop and alt text; and each drawing that is not a
      picture, with its docPr id, for a figure's `drawings`.
  python tools/media.py extract ORIGINAL.docx FOLDER NAME [NAME ...]
      Copies each picture of its own, in order, into FOLDER under the name
      given for it, byte for byte, and prints the front matter `images:`
      entries and each image's Markdown. Names are the converter's
      descriptors (ledger 14); this tool invents none.

The build calls build(): it copies a lab's pictures from beside its source
into the folder the site publishes, `labs/<id>/<id>-media/`, and makes each
drawn figure's SVG (tools/figures.py) and the PNG the Word download embeds.
Pictures sit beside the source as `curriculum/<course>/<id>-media/<name>`,
named in front matter `images:` (file, source_part, sha256); a figure is an
image with class `drawn` whose file is made, never committed (D-0101).
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile

import check_unchanged
import figures
import render


def folder_name(doc_id):
    return doc_id + "-media"


def lab_media(doc):
    """{"images": front matter entries, "figures": [{"file", "drawings",
    "alt"}]} for a converted document; every file under <id>-media/."""
    ast = json.loads(subprocess.run(
        [render.PANDOC, "-f", render.FROM, "-t", "json", doc["path"]],
        check=True, capture_output=True, encoding="utf-8").stdout)
    prefix = folder_name(doc["meta"]["id"]) + "/"
    found = []

    def walk(node):
        if isinstance(node, list):
            for n in node:
                walk(n)
        elif isinstance(node, dict):
            if node.get("t") == "Image":
                (_, classes, attrs), _, (target, _) = node["c"]
                found.append((target, "drawn" in classes, dict(attrs)))
            walk(node.get("c"))

    walk(ast["blocks"])
    images = doc["meta"].get("images") or []
    # Word's crop of each image in document order, figures None; the Word
    # download writes them (tools/downloads.py).
    crops = [None if drawn else attrs.get("crop") for _, drawn, attrs in found]
    out = {"images": images, "figures": [], "crops": crops}
    for target, drawn, attrs in found:
        if not target.startswith(prefix) or "/" in target[len(prefix):]:
            raise SystemExit("{}: {} is not in {}".format(doc["path"], target, prefix))
        if drawn:
            if not target.endswith(".svg"):
                raise SystemExit("{}: a drawn figure's file ends .svg: {}".format(doc["path"], target))
            out["figures"].append({"file": target[len(prefix):], "drawings": attrs.get("drawings", "").split()})
    for e in images:
        if "/" in e["file"][len(prefix):] or not e["file"].startswith(prefix):
            raise SystemExit("{}: image {} is not in {}".format(doc["path"], e["file"], prefix))
    return out


def build(doc, dest, chrome):
    """Fill dest (a lab's media folder) and return the files to publish."""
    media = lab_media(doc)
    if not media["images"] and not media["figures"]:
        return []
    os.makedirs(dest, exist_ok=True)
    source_dir = os.path.dirname(doc["path"])
    original = os.path.join(render.ROOT, doc["meta"]["source_file"])
    published = []
    for e in media["images"]:
        src = os.path.join(source_dir, e["file"])
        name = os.path.basename(e["file"])
        shutil.copyfile(src, os.path.join(dest, name))
        published.append(name)
    for f in media["figures"]:
        text, _ = figures.svg(original, f["drawings"])
        svg_path = os.path.join(dest, f["file"])
        with open(svg_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        figures.png(svg_path, svg_path[:-4] + ".png", chrome)
        published.append(f["file"])
    return published


def pictures(original):
    _, _, pics, drawings = check_unchanged.docx_content(original)
    return pics, drawings


def size_attrs(pic):
    attrs = 'width="{:.4f}in" height="{:.4f}in"'.format(*(v / 914400 for v in pic["extent"]))
    if pic["crop"]:
        attrs += ' crop="{}"'.format(" ".join(str(v) for v in pic["crop"]))
    return attrs


def main(argv):
    if argv[:1] == ["list"] and len(argv) == 2:
        pics, drawings = pictures(argv[1])
        for i, p in enumerate(pics, 1):
            where = "in a drawn figure" if p["in_figure"] else "{{{}}}".format(size_attrs(p))
            print("picture {}: {} {} alt {!r}".format(i, p["part"], where, p["descr"]))
        for d in drawings:
            print("drawing {}: {}alt {!r}".format(d["id"], "lone text box; " if d["lone_text_box"] else "",
                                                 d["descr"]))
        return 0
    if argv[:1] == ["extract"] and len(argv) >= 4:
        original, folder, names = argv[1], argv[2], argv[3:]
        own = [p for p in pictures(original)[0] if not p["in_figure"]]
        if len(names) != len(own):
            raise SystemExit("{} pictures of their own, {} names".format(len(own), len(names)))
        os.makedirs(folder, exist_ok=True)
        prefix = os.path.basename(os.path.normpath(folder))
        entries, seen = [], {}
        with zipfile.ZipFile(original) as z:
            for p, name in zip(own, names):
                data = z.read(p["part"])
                if name in seen and seen[name] != data:
                    raise SystemExit("{} is given to two different pictures".format(name))
                seen[name] = data
                with open(os.path.join(folder, name), "wb") as fh:
                    fh.write(data)
                if not any(e["file"] == prefix + "/" + name for e in entries):
                    entries.append({"file": prefix + "/" + name, "source_part": p["part"],
                                    "sha256": hashlib.sha256(data).hexdigest()})
        print("images:")
        for e in entries:
            print('  - file: "{file}"\n    source_part: "{source_part}"\n    sha256: "{sha256}"'.format(**e))
        print()
        for p, name in zip(own, names):
            print("![{}]({}/{}){{{}}}".format(p["descr"], prefix, name, size_attrs(p)))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
