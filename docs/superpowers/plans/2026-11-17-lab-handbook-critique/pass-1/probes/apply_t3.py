import json
b=json.load(open('probes/t3.json',encoding='utf-8'))
p='hb/tools/check_em_dash.py'
s=open(p,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1, old
    s=s.replace(old,new)
rep("import os\nimport sys\n", "import os\nimport re\nimport sys\n")
anchor='''        if line.startswith("source_file:"):
            return True
    return False
'''
rep(anchor, anchor+"\n\n"+b[1].rstrip("\n")+"\n")
rep(b[2], b[3])
rep("skipped. Exit code 1 and the files listed when any other file has one.\n",
    "skipped. Exit code 1 and the files listed when any other file has one.\nA converted file's `ruled_additions` text is scanned: it is new public wording (Lab Handbook spec 4.7).\n")
open(p,'w',encoding='utf-8',newline='\n').write(s)
