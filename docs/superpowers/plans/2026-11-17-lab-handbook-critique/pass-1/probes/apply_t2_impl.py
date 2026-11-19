p='hb/tools/check_numbers.py'
s=open(p,encoding='utf-8').read()
impl=open('probes/t2_impl.py',encoding='utf-8').read()
chk=open('probes/t2_check.py',encoding='utf-8').read()
doc=open('probes/t2_doc.txt',encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1, old
    s=s.replace(old,new)
anchor='''        return plain(node.get("c"))
    return ""
'''
rep(anchor, anchor+"\n\n"+impl.rstrip("\n")+"\n")
rep('''    items = rendered_items(md_path)
    return items, compare(record["labels"], items)
''', chk)
rep("\nAn anchor no rule places fails.", "\n"+doc.rstrip("\n")+"\n\nAn anchor no rule places fails.")
open(p,'w',encoding='utf-8',newline='\n').write(s)
