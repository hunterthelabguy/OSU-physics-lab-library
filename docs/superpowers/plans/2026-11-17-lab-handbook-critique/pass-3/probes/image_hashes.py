"""Hash every declared image against its front-matter sha256 (D-0198 (4)).

Run from the repo root: python -X utf8 image_hashes.py
"""
import hashlib
import os
import sys

sys.path.insert(0, "tools")
import render  # noqa: E402

total = bad = missing = 0
for doc_id, doc in render.converted_documents().items():
    for e in doc["meta"].get("images") or []:
        total += 1
        path = os.path.join(os.path.dirname(doc["path"]), e["file"])
        digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
        if "sha256" not in e:
            missing += 1
            print("no sha256:", doc_id, e["file"])
        elif digest != e["sha256"]:
            bad += 1
            print("differs:", doc_id, e["file"])
print("images", total, "differ", bad, "without sha256", missing)
