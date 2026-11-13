"""mutate_one.py IN.docx OUT.docx: copy IN to OUT with one change: the first
label paragraph loses its direct <w:spacing w:before="0" w:after="0"/> (so
the style's 79 twips after applies). Prints the label before and after."""
import re, sys, zipfile

src, dst = sys.argv[1], sys.argv[2]
P = re.compile(r'<w:p><w:pPr><w:pStyle w:val="QuestionLabel\d"/>.*?</w:p>', re.S)
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "word/document.xml":
            x = data.decode("utf-8")
            m = P.search(x)
            new = m.group(0).replace('<w:spacing w:before="0" w:after="0"/>', "", 1)
            assert new != m.group(0)
            print("before:", m.group(0)); print("after: ", new)
            data = (x[:m.start()] + new + x[m.end():]).encode("utf-8")
        zout.writestr(item, data)
