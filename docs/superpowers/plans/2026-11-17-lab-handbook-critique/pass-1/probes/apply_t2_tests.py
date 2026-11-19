import re
plan=open('docs/superpowers/plans/2026-11-17-lab-handbook.md',encoding='utf-8').read()
t2=plan[plan.index('### T2:'):plan.index('### T3:')]
blocks=re.findall(r'```(?:python|)\n(.*?)```', t2, re.S)
p='hb/tests/test_check_numbers.py'
s=open(p,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1, old
    s=s.replace(old,new)
rep("    def __init__(self, body, labels):","    def __init__(self, body, labels, front=\"\"):")
rep(r"""self.md.write_text('---\nsource_file: "original.docx"\n---\n\n' + body,""",
    r"""self.md.write_text('---\nsource_file: "original.docx"\n' + front + '---\n\n' + body,""")
rep("""    def run_fixture(self, body, labels):
        f = Fixture(body, labels)""","""    def run_fixture(self, body, labels, front=""):
        f = Fixture(body, labels, front)""")
anchor="\n\nclass RealRecords(unittest.TestCase):"
rep(anchor, "\n"+blocks[1].rstrip("\n")+"\n"+anchor)
open(p,'w',encoding='utf-8',newline='\n').write(s)
open('probes/t2_impl.py','w',encoding='utf-8').write(blocks[2])
open('probes/t2_check.py','w',encoding='utf-8').write(blocks[3])
open('probes/t2_doc.txt','w',encoding='utf-8').write(blocks[4])
