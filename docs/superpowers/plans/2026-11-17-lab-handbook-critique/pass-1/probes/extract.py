import re, sys, json
plan=open('docs/superpowers/plans/2026-11-17-lab-handbook.md',encoding='utf-8').read()
a, b = sys.argv[1], sys.argv[2]
sec = plan[plan.index(a):plan.index(b) if b != 'END' else len(plan)]
blocks = re.findall(r'```[a-z]*\n(.*?)```', sec, re.S)
json.dump(blocks, open(sys.argv[3],'w',encoding='utf-8'))
for i,x in enumerate(blocks): print(i, repr(x.split('\n')[0][:80]))
