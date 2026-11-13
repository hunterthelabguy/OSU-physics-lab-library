"""Compare two builds of build/quarto-site (base, T1): every file byte for
byte; for a differing .docx, part by part, and document.xml after taking out
the label paragraphs and restoring the cell top margin; for a differing PDF,
with its dates and ID taken out. Counts the T1 labels per level and checks
each is directly followed by <w:tbl>. Usage: compare_builds.py BASE T1"""
import collections, hashlib, pathlib, re, sys, zipfile

base, new = (pathlib.Path(a) for a in sys.argv[1:3])
files_b = {p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file()}
files_n = {p.relative_to(new).as_posix() for p in new.rglob("*") if p.is_file()}
print("only in base:", sorted(files_b - files_n))
print("only in T1:", sorted(files_n - files_b))

BASE_LABEL = re.compile(r'<w:p><w:pPr><w:pStyle w:val="QuestionLabel(\d)" /></w:pPr>(.*?)</w:p>', re.S)
NEW_LABEL = re.compile(r'<w:p><w:pPr><w:pStyle w:val="QuestionLabel(\d)"/>.*?</w:pPr>(.*?)</w:p>', re.S)
TEXT = re.compile(r"<w:t[^>]*>([^<]*)</w:t>")
PDF_VOLATILE = re.compile(rb"/(CreationDate|ModDate) \([^)]*\)|/ID \[<[0-9a-fA-F]+> <[0-9a-fA-F]+>\]")

levels = collections.Counter()
diff_kinds = collections.Counter()
for rel in sorted(files_b & files_n):
    a, b = (base / rel).read_bytes(), (new / rel).read_bytes()
    if a == b:
        continue
    if rel.endswith(".docx"):
        za, zb = zipfile.ZipFile(base / rel), zipfile.ZipFile(new / rel)
        na, nb = set(za.namelist()), set(zb.namelist())
        if na != nb:
            print(rel, "parts differ", na ^ nb)
        for part in sorted(na & nb):
            pa, pb = za.read(part), zb.read(part)
            if pa == pb:
                continue
            if part != "word/document.xml":
                print(rel, "part differs:", part)
                diff_kinds["other part " + part] += 1
                continue
            da, db = pa.decode(), pb.decode()
            la = [(m.group(1), "".join(TEXT.findall(m.group(2)))) for m in BASE_LABEL.finditer(da)]
            lb = [(m.group(1), "".join(TEXT.findall(m.group(2)))) for m in NEW_LABEL.finditer(db)]
            for m in NEW_LABEL.finditer(db):
                levels[m.group(1)] += 1
                if not db[m.end():].lstrip().startswith("<w:tbl>"):
                    print(rel, "label not followed by a table:", m.group(0)[:120])
            ra = BASE_LABEL.sub("", da).replace('<w:top w:w="203" w:type="dxa"/>', '<w:top w:w="92" w:type="dxa"/>')
            rb = NEW_LABEL.sub("", db)
            # Whitespace between tags only (Pandoc puts each raw block on its own line).
            ra, rb = (re.sub(r">\s+<", "><", x) for x in (ra, rb))
            # The tree's own path (in a picture's descr) and, counted apart,
            # a box stem's Body Text turned First Paragraph.
            ra = ra.replace(str(base.parent.parent.name), "TREE")
            rb = rb.replace(str(new.parent.parent.name), "TREE")
            fp = len(re.findall("FirstParagraph", rb)) - len(re.findall("FirstParagraph", ra))
            if fp:
                print(rel, "stems now First Paragraph:", fp)
                diff_kinds["stems First Paragraph"] += fp
            pat = re.compile(r'(</w:tcPr><w:p><w:pPr><w:pStyle w:val=")FirstParagraph(")')
            rb = pat.sub(lambda m: m.group(1) + "BodyText" + m.group(2), rb)
            ok = la == lb and ra == rb
            print(rel, "document.xml: labels", len(la), "->", len(lb), "same labels" if la == lb else "LABELS DIFFER",
                  "| rest identical" if ra == rb else "| REST DIFFERS")
            if ra != rb:
                i = next(k for k in range(min(len(ra), len(rb))) if ra[k] != rb[k])
                print("   first difference:", ra[i - 80:i + 120], "\n   vs", rb[i - 80:i + 120])
            diff_kinds["docx document.xml " + ("ok" if ok else "BAD")] += 1
    elif rel.endswith(".pdf"):
        same = PDF_VOLATILE.sub(b"", a) == PDF_VOLATILE.sub(b"", b)
        print(rel, "PDF differs", "only in dates/ID" if same else "IN CONTENT")
        diff_kinds["pdf " + ("dates only" if same else "CONTENT")] += 1
    else:
        print(rel, "DIFFERS", len(a), len(b))
        diff_kinds["other " + rel.rsplit(".", 1)[-1]] += 1
print("T1 labels per level:", dict(sorted(levels.items())), "total", sum(levels.values()))
print("differences:", dict(diff_kinds))
