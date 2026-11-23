import json
b = json.load(open('probes/t1_blocks.json', encoding='utf-8'))
p = 'hb/tools/check_unchanged.py'
s = open(p, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:60], s.count(old))
    s = s.replace(old, new)

# paragraph_text and body_spans after without_fallbacks
anchor = '''            if child.tag == MC_FALLBACK:
                parent.remove(child)
    return root
'''
rep(anchor, anchor + "\n\n" + b[1].rstrip("\n") + "\n")
rep("def docx_content(path):", "def docx_content(path, spans=()):")
rep("    blocks(root)\n    return sink[\"out\"]", b[2].rstrip("\n") + "\n    return sink[\"out\"]")
# word_tables
start = s.index("def word_tables(path):")
end = s.index("def word_table_shares(path):")
s = s[:start] + b[3].rstrip("\n") + "\n\n\n" + s[end:]
rep("    meta = {k: meta_value(v) for k, v in doc[\"meta\"].items()}\n",
    "    meta = {k: meta_value(v) for k, v in doc[\"meta\"].items()}\n" + b[4])
rep("    src = os.path.join(repo_root, meta[\"source_file\"])\n",
    "    src = os.path.join(repo_root, meta[\"source_file\"])\n" + b[5])
rep("docx_content(src)", "docx_content(src, spans)")
rep("word_tables(src)", "word_tables(src, spans)")
old = '''        for item in meta.get(key, []) or []:
            if not item.get("ledger"):
                problems.append(f"{key} entry lacks a ledger reference: {item.get('text')!r}")
            passage = [w for w, _ in tokens([(ch, False) for ch in item["text"]])]
'''
rep(old, b[6])
# docstring after ruled_equations example block
old = '''        converted: "x2=x×x"     # the converted text, as it prints it
        ledger: "D-0167"
'''
rep(old, old + b[7])
open(p, 'w', encoding='utf-8', newline='\n').write(s)
