"""Probe copies of one built Word download, each changing one thing about
where or how the question label is written, so the Navigation pane shows
which change makes the labels appear. Writes into argv[2]."""
import pathlib, re, shutil, sys, zipfile

src = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
doc = zipfile.ZipFile(src).read("word/document.xml").decode("utf-8")
LABEL = re.compile(r'<w:p><w:pPr><w:pStyle w:val="QuestionLabel(\d)" /></w:pPr>.*?</w:p>', re.S)


def write(name, xml):
    dest = out / name
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = xml.encode("utf-8") if item.filename == "word/document.xml" else zin.read(item.filename)
            zout.writestr(item, data)
    print(dest.name, "labels:", len(LABEL.findall(xml)) or len(re.findall(r'w:val="Heading\d" /></w:pPr><w:r><w:t xml:space="preserve">(?:Question|Checkpoint) ', xml)))


# A: as built (labels in the box's table cell, Question Label N).
shutil.copyfile(src, out / "A-as-built.docx")
print("A-as-built.docx")

# B: each label moved out of its box, to just before the box's table.
xml, moved = doc, 0
for m in reversed(list(LABEL.finditer(doc))):
    para = m.group(0)
    start = xml.rfind("<w:tbl>", 0, m.start())
    xml = xml[:m.start()] + xml[m.end():]
    xml = xml[:start] + para + xml[start:]
    moved += 1
assert moved == len(LABEL.findall(doc))
write("B-label-above-box.docx", xml)

# C: labels left in the box, styled with Word's built-in Heading N.
write("C-builtin-heading-in-box.docx", LABEL.sub(lambda m: m.group(0).replace(
    f'QuestionLabel{m.group(1)}', f'Heading{m.group(1)}'), doc))

# D: the label above the box, drawn as the box's top line: the box's rule
# and tint on the label paragraph, its top padding as a border in the tint,
# and the cell's top margin cut to the label's old space below it.
def top_line(space_left="9", space_right="12", space_top="10", cell_top="79"):
    xml = doc
    for m in reversed(list(LABEL.finditer(doc))):
        para = m.group(0)
        start = xml.rfind("<w:tbl>", 0, m.start())
        tblpr = xml[start:xml.find("</w:tblPr>", start)]
        rule = re.search(r'<w:left w:val="single" w:sz="24" w:space="0" w:color="([0-9A-F]{6})"', tblpr).group(1)
        fill = re.search(r'w:fill="([0-9A-F]{6})"', xml[start:m.start()]).group(1)
        ppr = (f'<w:pPr><w:pStyle w:val="QuestionLabel{m.group(1)}" /><w:pBdr>'
               f'<w:top w:val="single" w:sz="4" w:space="{space_top}" w:color="{fill}"/>'
               f'<w:left w:val="single" w:sz="24" w:space="{space_left}" w:color="{rule}"/>'
               f'<w:right w:val="single" w:sz="4" w:space="{space_right}" w:color="{fill}"/></w:pBdr>'
               f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>'
               f'<w:spacing w:before="0" w:after="0"/><w:ind w:left="248" w:right="248"/></w:pPr>')
        para = re.sub(r"<w:pPr>.*?</w:pPr>", ppr, para, count=1)
        xml = xml[:m.start()] + xml[m.end():]
        head = xml[start:].replace('<w:top w:w="203" w:type="dxa"/>', f'<w:top w:w="{cell_top}" w:type="dxa"/>', 1)
        xml = xml[:start] + para + head
    return xml

write("D-label-as-top-line.docx", top_line())

# D2: height equal to the box as built (top border 0.5 pt + 9 pt space +
# 92 twips cell margin = 203 + 79 twips), rule and tint edges nudged.
if len(sys.argv) > 3:
    sl, sr, st, ct = sys.argv[3:7]
    write(f"D2-{sl}-{sr}-{st}-{ct}.docx", top_line(sl, sr, st, ct))
