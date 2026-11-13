"""cmp_builds.py BASE_DIR T1_DIR: compare each lab's word/document.xml, base
build against the T1 build, after removing the known, designed differences:
the label paragraph (inside the table at base, before it at T1), the cell top
margin 203 -> 92, whitespace, and the stems' FirstParagraph style. Prints per
file: label counts, label (style, text) lists equal, every T1 label XML equal
to the expected raw paragraph, stems restyled, and whether the rest is equal.
"""
import glob, os, re, sys, zipfile

base_dir, t1_dir = sys.argv[1], sys.argv[2]
LBL = re.compile(r'<w:p><w:pPr><w:pStyle w:val="(QuestionLabel\d)" ?/>(?:(?!</w:p>).)*</w:p>', re.S)
TXT = re.compile(r"<w:t[^>]*>([^<]*)</w:t>")


def doc(p):
    return zipfile.ZipFile(p).read("word/document.xml").decode("utf-8")


def labels(x):
    return [(m.group(1), "".join(TXT.findall(m.group(0)))) for m in LBL.finditer(x)]


def expected(style, text, rule, fill):
    return ('<w:p><w:pPr><w:pStyle w:val="' + style + '"/>'
            '<w:pBdr><w:top w:val="single" w:sz="4" w:space="9" w:color="' + fill + '"/>'
            '<w:left w:val="single" w:sz="24" w:space="9" w:color="' + rule + '"/>'
            '<w:right w:val="single" w:sz="4" w:space="11" w:color="' + fill + '"/></w:pBdr>'
            '<w:shd w:val="clear" w:color="auto" w:fill="' + fill + '"/>'
            '<w:spacing w:before="0" w:after="0"/><w:ind w:left="238" w:right="258" w:firstLine="10"/></w:pPr>'
            '<w:r><w:t xml:space="preserve">' + text + '</w:t></w:r></w:p>')


def norm(x):
    x = LBL.sub("", x)
    x = x.replace('<w:tblCellMar><w:top w:w="203"', '<w:tblCellMar><w:top w:w="92"')
    x = x.replace('w:val="FirstParagraph"', 'w:val="BodyText"')
    return re.sub(r"\s+", "", x)


total = {"labels": 0, "restyled": 0, "bad": 0}
for b in sorted(glob.glob(os.path.join(base_dir, "*.docx"))):
    name = os.path.basename(b)
    t = os.path.join(t1_dir, name)
    xb, xt = doc(b), doc(t)
    lb, lt = labels(xb), labels(xt)
    # each T1 label must be the expected raw XML, directly followed by <w:tbl>
    ok_xml = True
    for m in LBL.finditer(xt):
        tbl = xt[m.end():m.end() + 2000]
        rule = re.search(r'<w:left w:val="single" w:sz="24" w:space="0" w:color="([0-9A-F]{6})"', tbl).group(1)
        fill = re.search(r'<w:shd w:val="clear" w:color="auto" w:fill="([0-9A-F]{6})"', tbl).group(1)
        want = expected(m.group(1), "".join(TXT.findall(m.group(0))), rule, fill)
        if m.group(0) != want or not tbl.lstrip().startswith("<w:tbl>"):
            ok_xml = False
    restyled = xt.count('w:val="FirstParagraph"') - xb.count('w:val="FirstParagraph"')
    same = norm(xb) == norm(xt)
    total["labels"] += len(lt); total["restyled"] += restyled
    if not (lb == lt and ok_xml and same): total["bad"] += 1
    print("{:45s} labels {:3d}/{:3d} same={} xml_ok={} restyled={:3d} rest_equal={}".format(
        name, len(lb), len(lt), lb == lt, ok_xml, restyled, same))
    if not same:
        a, c = norm(xb), norm(xt)
        i = next(k for k in range(min(len(a), len(c))) if a[k] != c[k])
        print("   first diff:", a[max(0, i - 150):i + 150]); print("   vs        :", c[max(0, i - 150):i + 150])
print(total)
