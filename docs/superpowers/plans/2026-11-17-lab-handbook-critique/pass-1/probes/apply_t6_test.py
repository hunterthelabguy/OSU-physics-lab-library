import json
b=json.load(open('probes/t6.json',encoding='utf-8'))
p='hb/tests/test_quarto_site.py'; s=open(p,encoding='utf-8').read()
anchor="        self.assertEqual(found, self.ADDRESSES)\n"
assert s.count(anchor)==1, 'anchor'
s=s.replace(anchor, anchor+'\n'+b[0])
open(p,'w',encoding='utf-8',newline='\n').write(s)
