# Word downloads carry no build path: implementation plan

**Goal:** no built Word download holds the build machine's path: a drawn
figure's picture keeps its relative path, and `media-dir` is not a custom
document property.
**Architecture:** `tools/filters/media.lua` is the only reader of
`media-dir`. In Word, `figure_docx` gives the figure's PNG the source's own
relative path (`.svg` to `.png`), resolved through `--resource-path` like
every other picture, and the filter's `Meta` drops `media-dir` once read.
**Spec:** `docs/superpowers/specs/2026-11-13-docx-machine-path-design.md`;
ledger D-0177, the owner's three calls ruled "Leans as written" 2026-11-13.
**Verify:** with `PANDOC`, `QUARTO`, `CHROME`, `PDFTOTEXT` exported as in
CLAUDE.md "Which Pandoc": `python tools/check_em_dash.py`; the converted
files' `python tools/check_unchanged.py $files` and
`python tools/check_numbers.py $files` (the loop in
`.github/workflows/verify.yml`); `python tools/quarto_build.py`;
`python -m unittest discover -s tests`.

## Global constraints

- No source, original, wording or alt-text change (D-0168 not engaged).
- `wp:docPr descr` (Word's alt text) is byte-identical before and after.
- The lab page and the HTML download are unchanged: the `Meta` drop and the
  `src` change apply to `FORMAT == "docx"` only.
- The other six custom properties stay (call 1).
- Commit as hunterthelabguy with the noreply email, no trailer; subjects
  <=72 characters.

## Files

| File | Responsibility | Task |
|---|---|---|
| `tests/test_downloads.py` | `build_paths` helper; `MarkdownAndWord` and `MediaDownloads` tests; `--resource-path` in the label probe | T1, T2 |
| `tools/filters/media.lua` | relative PNG `src` in Word; `media-dir` dropped in Word; header comment | T2 |

## T1. Tests, red

Module level in `tests/test_downloads.py`, after `pdf_text` or near the
other helpers:

```python
ABSOLUTE = re.compile(r"[A-Za-z]:[\\/]|[\\/]")
DESCR = re.compile(r'\bdescr="([^"]*)"')


def build_paths(docx, *folders):
    """Each XML part of a Word file that holds one of the folders, in
    either slash form, and each descr that is an absolute path (D-0177)."""
    spellings = {str(f).replace("\\", "/").lower() for f in folders}
    found = []
    with zipfile.ZipFile(docx) as z:
        for name in z.namelist():
            if not name.endswith((".xml", ".rels")):
                continue
            text = z.read(name).decode("utf-8")
            flat = text.replace("\\", "/").lower()
            found += ["{} holds {}".format(name, s) for s in spellings if s in flat]
            found += ["{} descr {}".format(name, d) for d in DESCR.findall(text) if ABSOLUTE.match(d)]
    return found
```

`MarkdownAndWord`:

```python
    def test_word_carries_no_build_path(self):
        # D-0177: no Word download names the folder it was built in, in a
        # part (a figure's descr, a custom property) or as an absolute descr.
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                self.assertEqual(build_paths(self.docx(doc_id), ROOT, ROOT.resolve()), [])
```

`MediaDownloads` (its made-up lab builds in a temporary folder outside the
repo, which the site-wide test cannot see):

```python
    def test_word_carries_no_build_path(self):
        # D-0177, on a lab built outside the repo.
        root = Path(self.tmp.name)
        self.assertEqual(build_paths(self.docx, root, root.resolve(), ROOT), [])
```

Run both on the build of `main` in this worktree:
`python -m unittest tests.test_downloads.MarkdownAndWord.test_word_carries_no_build_path tests.test_downloads.MediaDownloads.test_word_carries_no_build_path`.
Expected: both FAIL. The site-wide test: 19 subtests fail, each on
`docProps/custom.xml`, and the three drawn-figure labs also on
`word/document.xml` and an absolute `descr`. The fixture test fails on
`docProps/custom.xml`, `word/document.xml` and its figure's `descr`.

Commit: `Tests: no Word download holds its build path (D-0177)`.

## T2. Fix, green

`tools/filters/media.lua`:

1. `figure_docx`: the image's `src` is `el.src:gsub("%.svg$", ".png")` in
   place of `figure_file(el, ".png")`; the SVG is still read through
   `figure_file(el)` (`media-dir`). If `figure_file`'s `ext` argument then
   has no caller, drop it.
2. The `Meta` function: after reading the three keys, for `FORMAT ==
   "docx"`, `meta["media-dir"] = nil` and return `meta`. The local `dir`
   keeps the value for the second filter table.
3. Header comment, "Metadata" paragraph: `media-dir` is read here and
   dropped from a Word file's metadata, since Pandoc would write it as a
   custom property (D-0177); a figure's PNG in Word keeps its relative
   path, found through `--resource-path`.

`tests/test_downloads.py`, `MediaDownloads.test_figure_label_names_the_group`:
its Word probe runs Pandoc with no `--resource-path`, so the relative PNG
would not be found (Pandoc warns, writes the alt text as words, and the
`descr` assertion fails). Add `"--resource-path", downloads.lab_dir(self.doc)`
to `args`. The HTML probe ignores it.

Run the two T1 tests after `python tools/quarto_build.py`; expected PASS.
Then the whole `tests.test_downloads` module.

Commit: `Word downloads drop the build path (D-0177)`.

## T3. Verify

The full verify sequence above, every step green, and the measurement:
every built `.docx`'s `wp:docPr descr` values identical to the `main`
baseline build (kept in this worktree's `build/` until T2's build replaces
it: copy `build/quarto-site/labs/*/*.docx` to the scratchpad first), and
`docProps/custom.xml` the same less `media-dir`. `document.xml` differs from
the baseline only in the three `pic:cNvPr descr` values.
