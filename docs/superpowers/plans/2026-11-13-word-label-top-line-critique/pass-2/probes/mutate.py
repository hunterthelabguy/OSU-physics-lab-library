"""mutate.py MODE: rewrite label paragraphs in every built .docx (backup first with MODE=backup, MODE=restore)."""
import glob, re, shutil, sys, zipfile, os
mode = sys.argv[1]
root = sys.argv[2]
bak = sys.argv[3]
files = sorted(glob.glob(root + '/labs/*/*.docx'))
os.makedirs(bak, exist_ok=True)
P = re.compile(r'(<w:p><w:pPr><w:pStyle w:val="QuestionLabel\d"/>.*?</w:p>)', re.S)
MUT = {
    'space_after': lambda p: p.replace('<w:spacing w:before="0" w:after="0"/>', '<w:spacing w:before="0" w:after="200"/>'),
    'no_spacing': lambda p: p.replace('<w:spacing w:before="0" w:after="0"/>', ''),
    'indent': lambda p: p.replace('w:left="238" w:right="258" w:firstLine="10"', 'w:left="400" w:right="100" w:firstLine="0"'),
    'bdr_space': lambda p: p.replace('w:space="9" w:color', 'w:space="3" w:color'),
}
for f in files:
    b = os.path.join(bak, os.path.basename(f))
    if mode == 'backup':
        shutil.copyfile(f, b)
    elif mode == 'restore':
        shutil.copyfile(b, f)
    else:
        with zipfile.ZipFile(b) as zin, zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == 'word/document.xml':
                    x = data.decode('utf-8')
                    x2 = P.sub(lambda m: MUT[mode](m.group(1)), x)
                    assert x2 != x or "problem-solving" in f, f
                    data = x2.encode('utf-8')
                zout.writestr(item, data)
