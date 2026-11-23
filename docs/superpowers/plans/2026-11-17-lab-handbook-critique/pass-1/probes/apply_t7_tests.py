import json
b=json.load(open('probes/t7.json',encoding='utf-8'))
p='hb/tests/test_quarto_site.py'; s=open(p,encoding='utf-8').read()
anchor="\n\nclass NoThirdParty(unittest.TestCase):"
assert s.count(anchor)==1
s=s.replace(anchor, "\n"+b[0].rstrip("\n")+"\n"+anchor)
open(p,'w',encoding='utf-8',newline='\n').write(s)
p='hb/tests/test_downloads.py'; s=open(p,encoding='utf-8').read()
anchor='''    def docx(self, doc_id):
        return QSITE / "labs" / doc_id / (doc_id + ".docx")
'''
assert s.count(anchor)==1
s=s.replace(anchor, anchor+"\n"+b[1])
open(p,'w',encoding='utf-8',newline='\n').write(s)
