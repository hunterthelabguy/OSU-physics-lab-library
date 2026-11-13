import re, zipfile, sys
a = zipfile.ZipFile(sys.argv[1]).read("word/document.xml").decode()
b = zipfile.ZipFile(sys.argv[2]).read("word/document.xml").decode()
P = re.compile(r'<w:p><w:pPr><w:pStyle w:val="QuestionLabel\d" ?/>.*?</w:p>', re.S)
la, lb = P.findall(a), P.findall(b)
print(len(la), len(lb))
norm = lambda x: x.replace(' />', '/>')
print("exact equal:", la == lb, " equal ignoring ' />' spacing:", [norm(x) for x in la] == [norm(x) for x in lb])
for x, y in zip(la, lb):
    if norm(x) != norm(y): print(x); print(y); break
# the table opening/cell margin
Ta = re.findall(r'<w:tblCellMar><w:top w:w="(\d+)"', a); Tb = re.findall(r'<w:tblCellMar><w:top w:w="(\d+)"', b)
print("cell tops", set(Ta), set(Tb))
# whole-document equality after normalising
def strip(x): return re.sub(r'\s+', '', norm(x))
print("whole doc equal (ws,/> normalised):", strip(a) == strip(b))
