# Question labels as headings implementation plan

**Goal:** every question's and checkpoint's label is a heading one level
below its section on the lab page, the HTML download and (by outline level)
the Word download, with the box drawn as it is today.
**Architecture:** `tools/filters/questions.lua` already writes every label;
it switches to top-down traversal so it meets headings and questions in
document order, tracks the last section level, and writes the label as a
`Header` (Word: a "Question Label N" paragraph style with an outline level).
CSS undoes what a heading brings; tests read the rendered headings.
**Spec:** `docs/superpowers/specs/2026-11-12-question-headings-design.md`
(sections 3 to 7, 10); ledger D-0176, ruled "Leans as written" 2026-11-12.
**Verify:** with `PANDOC`, `QUARTO`, `CHROME`, `PDFTOTEXT` exported as in
CLAUDE.md "Which Pandoc": `python tools/check_em_dash.py`; the converted
files' `python tools/check_unchanged.py $files` and
`python tools/check_numbers.py $files` (the loop in
`.github/workflows/verify.yml` lines 53 to 58); `python tools/quarto_build.py`;
`python -m unittest discover -s tests`.

## Global constraints

- Label level = level of the last heading before it in document order,
  outside any question box, plus one; the page's H1 makes the floor H2. A
  label past H6 fails the render.
- The heading's text is the label alone, "Question N" / "Checkpoint N"; the
  heading has no id.
- No source wording changes (D-0168). Only two source lines change, heading
  level only (T3).
- The box looks as it does today on screen at desktop and 375 px; print
  differs only where a page break moves without stranding anything.
- Word: styles "Question Label 2" to "Question Label 6", each
  `basedOn` "Question Label" plus `<w:outlineLvl w:val="level-1"/>` and
  nothing else.
- Commit as hunterthelabguy with the noreply email, no trailer; subjects
  <=72 characters.

## Files

| File | Responsibility | Task |
|---|---|---|
| `tools/filters/questions.lua` | label as heading, level by section; Word style by level | T1, T2 |
| `themes/modern.css` | label look on a heading; print rule names the label | T1 |
| `tests/test_check_numbers.py` (class `Filter`) | filter unit tests on small bodies | T1 |
| `tests/test_headings.py` | rendered heading reading: no skip, label level, box headings | T1, T3 |
| `tests/test_downloads.py` | label form in the print-split check; no duplicate ids; Word styles | T1, T2 |
| `tools/make_reference_docx.py`, `tools/reference.docx` | the five level styles | T2 |
| `curriculum/ph212/ph212-data-analysis-handout.md:111`, `curriculum/ph212/ph212-extending-a-model-handout.md:122` | box heading `###` to `####` | T3 |
| `docs/accessibility/2026-11-05-nvda-ph212.md:7` | "Fixes since" names D-0176 | T3 |

`tools/check_numbers.py` is not changed: it reads the label as the plain
text of the box's first block, which a `Header` gives as "Question N".

### T1: Labels become headings on the page and the HTML download

**Depends on:** none
**Files:** modify `tools/filters/questions.lua`, `themes/modern.css:111-117`
and `:187-188`; test `tests/test_check_numbers.py` (class `Filter`),
`tests/test_headings.py`, `tests/test_downloads.py:877` and class `Html`
**Seams:** the filter's HTML output for a Markdown body; the rendered AST
of each source (`check_numbers.FROM`, `check_numbers.FILTER`,
`-M theme-name=modern`); the built page `build/quarto-site/labs/<id>/modern/index.html`
**Interfaces:** produces the module-level `section` in `questions.lua`
and the label element `pandoc.Header(level, {Str text}, Attr("", {kind.."-label"}))`
for non-Word output; T2 reads `level` in the Word branch.
**Verify:** `python -m unittest tests.test_check_numbers.Filter tests.test_headings -v`,
then the build and `python -m unittest tests.test_downloads -v`

- [ ] Failing tests in `tests/test_check_numbers.py`, class `Filter`:

```python
    def test_label_is_a_heading_one_below_its_section(self):
        # D-0176: the label is a heading one level below the last heading
        # before it; a body with none sits under the page's H1.
        body = "\n".join([q("z"), "## Week 1\n", q("a"), "### Part A\n", q("b"),
                          "#### Deep\n", q("c"), "## Week 2\n", q("d", cls="checkpoint")])
        out = self.render(body, "-t", "html").stdout
        for tag in ('<h2 class="question-label">Question 1</h2>',
                    '<h3 class="question-label">Question 2</h3>',
                    '<h4 class="question-label">Question 3</h4>',
                    '<h5 class="question-label">Question 4</h5>',
                    '<h3 class="checkpoint-label">Checkpoint 1</h3>'):
            self.assertIn(tag, out)
        self.assertNotIn("<p>Question", out)

    def test_heading_in_a_box_is_not_a_section(self):
        # D-0176: a heading inside a question's box leaves the section as
        # it was, so the next question's label keeps the same level.
        body = "\n".join(["## Week 1\n", q("a", "::: box\n#### Box title\n\nWords.\n:::"), q("b")])
        out = self.render(body, "-t", "html").stdout
        self.assertIn('<h3 class="question-label">Question 1</h3>', out)
        self.assertIn('<h3 class="question-label">Question 2</h3>', out)

    def test_label_past_h6_fails(self):
        out = self.render("###### Six\n\n" + q("a"), "-t", "html")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("h7", out.stderr)
```

- [ ] Run `python -m unittest tests.test_check_numbers.Filter -v`;
  expected: the three fail (`<p>Question 1</p>` found, no `<h2 class=`;
  the h6 body renders with code 0).
- [ ] Replace `tests/test_headings.py` with the rendered reading
  (`skips` now takes a list of levels; the source-text reading goes, since
  the rendered one holds every source heading too):

```python
"""Heading levels never skip (D-0166; WCAG 1.3.1, from the NVDA test of
2026-11-05), and each question's label is a heading one level below its
section (D-0176). Reads each source as the lab page renders it: through
tools/filters/questions.lua, so the labels are there.

KNOWN_SKIPS is a ratchet: the labs not yet fixed. A lab leaves the list
when its headings are fixed, and a lab on the list that no longer skips
fails, so the list only shrinks.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import check_numbers  # noqa: E402

KNOWN_SKIPS = {
    "ph211-capstone-handout",
    "ph211-uncertainty-handout",
    "ph213-data-analysis-handout",
}
LABELS = ("question-label", "checkpoint-label")


def headings(path):
    """[(level, kind, box)] in document order: kind "label" for a
    question's or checkpoint's label, "box" for a heading inside a question
    (box: its label's level), "section" otherwise."""
    doc = json.loads(subprocess.run(
        [check_numbers.PANDOC, str(path), "-f", check_numbers.FROM, "-t", "json",
         "--lua-filter", check_numbers.FILTER, "-M", "theme-name=modern"],
        capture_output=True, check=True, encoding="utf-8").stdout)
    found = []

    def walk(blocks, box):
        for b in blocks:
            if b["t"] == "Header":
                found.append((b["c"][0], "box" if box is not None else "section", box))
            elif b["t"] == "Div":
                (_, classes, _), content = b["c"]
                if any(k in classes for k in ("question", "checkpoint")):
                    label = content[0]
                    if label["t"] != "Header" or not set(label["c"][1][1]) & set(LABELS):
                        raise AssertionError("{}: a question's label is not a heading".format(path.name))
                    found.append((label["c"][0], "label", None))
                    walk(content[1:], label["c"][0])
                else:
                    walk(content, box)
            elif b["t"] == "BlockQuote":
                walk(b["c"], box)
            elif b["t"] in ("BulletList", "OrderedList"):
                for item in (b["c"] if b["t"] == "BulletList" else b["c"][1]):
                    walk(item, box)

    walk(doc["blocks"], None)
    return found


def skips(levels):
    """Each (index, level, previous level) where a heading goes down by
    more than one level."""
    return [(i, b, a) for i, (a, b) in enumerate(zip(levels, levels[1:]), 1) if b > a + 1]


class HeadingLevels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.labs = {p.stem: headings(p) for p in sorted((ROOT / "curriculum").glob("*/*.md"))}

    def test_no_lab_skips_a_level(self):
        for lab, found in self.labs.items():
            with self.subTest(lab=lab):
                found = skips([level for level, _, _ in found])
                if lab in KNOWN_SKIPS:
                    self.assertNotEqual(found, [], "fixed: remove it from KNOWN_SKIPS")
                else:
                    self.assertEqual(found, [])

    def test_label_is_one_below_its_section(self):
        for lab, found in self.labs.items():
            with self.subTest(lab=lab):
                section = 1
                for level, kind, _ in found:
                    if kind == "section":
                        section = level
                    elif kind == "label":
                        self.assertEqual(level, section + 1)
```

- [ ] Run `python -m unittest tests.test_headings -v`; expected failure:
  `setUpClass` raises "ph211-capstone-handout.md: a question's label is not
  a heading" (the label is still a `Div`).
- [ ] Filter. In `tools/filters/questions.lua` add, after
  `local colours = {}`:

```lua
-- The level of the last heading before a label, outside any question box
-- (D-0176). The page's H1 is its title, so a label is never above H2.
local section = 1
```

  and replace the second filter table with:

```lua
  {
    -- Top-down, so headings and questions are met in document order. A
    -- question's own content is not walked: a heading in its box is not a
    -- section, and nothing in it is labelled.
    traverse = "topdown",
    Header = function(h) section = h.level end,
    Div = function(el)
      local kind
      if el.classes:includes("question") then
        kind = "question"
      elseif el.classes:includes("checkpoint") then
        kind = "checkpoint"
      else
        return nil
      end
      local name = el.identifier ~= "" and ("#" .. el.identifier) or "without an id"
      local first = el.content[1]
      if not first or first.t ~= "Para" then
        error(kind .. " " .. name .. " must open with a paragraph, not "
          .. (first and first.t or "nothing"))
      end
      local level = section + 1
      if level > 6 then
        error(kind .. " " .. name .. " sits under an h6; its label would be h7 (D-0176)")
      end

      local n
      if kind == "checkpoint" then
        checkpoints = checkpoints + 1
        n = checkpoints
      else
        if el.classes:includes("restart") then questions = 0 end
        questions = questions + 1
        n = questions
      end

      el = unbold(el)
      local text = (kind == "question" and "Question " or "Checkpoint ") .. n
      if FORMAT == "docx" then
        local label = pandoc.Div({ pandoc.Para({ pandoc.Str(text) }) },
          pandoc.Attr("", { kind .. "-label" }, { ["custom-style"] = "Question Label" }))
        table.insert(el.content, 1, label)
        local prefix = kind == "question" and "box" or "checkpoint"
        return word_box(el.content, colours[prefix .. "-rule"], colours[prefix .. "-fill"], kind), false
      end
      table.insert(el.content, 1,
        pandoc.Header(level, { pandoc.Str(text) }, pandoc.Attr("", { kind .. "-label" })))
      return el, false
    end,
  },
```

  and in the header comment replace "The block becomes a labeled block
  ("Question N")" with "The block becomes a labeled block, its label
  ("Question N") a heading one level below its section (D-0176)".
- [ ] Run the `Filter` tests; expected: pass, and the rest of
  `tests.test_check_numbers` still passes (`check_numbers` reads the
  `Header`'s plain text).
- [ ] CSS, `themes/modern.css`: replace the `.question-label p,
  .checkpoint-label p` rule with

```css
/* The label is a heading one level below its section (D-0176), drawn as
   the small capitals line it was: everything a heading brings is undone. */
.question-label, .checkpoint-label {
  font-size: .8rem;
  font-weight: 400;
  line-height: 1.6;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--quiet);
  margin: 0 0 .35rem;
}
```

  and in the print block, after `h1, h2, h3, h4 { break-after: avoid; }`,
  add `  .question-label, .checkpoint-label { break-after: avoid; }`.
- [ ] `tests/test_downloads.py:877`: the split check's pattern becomes
  `r'<h[2-6] class="question-label">Question (\d+)</h[2-6]>(.*?)</div>'`.
- [ ] `tests/test_downloads.py`, class `Html`, add:

```python
    def test_no_duplicate_ids(self):
        # D-0176: the label headings carry no id, so a week restart's
        # second "Question 1" adds none; every id on a page is unique.
        for doc_id, _ in converted():
            for text in (page(doc_id, "modern"), self.download(doc_id)):
                with self.subTest(doc=doc_id):
                    ids = re.findall(r'\sid="([^"]+)"', text)
                    self.assertEqual(len(ids), len(set(ids)))
```

- [ ] Probe before the full build: render one lab page with Quarto
  (`python tools/quarto_build.py`) and read the first label of PH 212
  Lab 1 in `build/quarto-site/labs/ph212-data-analysis-handout/modern/index.html`;
  expected `<h3 class="question-label">Question 1</h3>`, no `id=`, no
  `anchored` class. Anything else stops the task.
- [ ] Build, then `python -m unittest discover -s tests`; expected: all
  pass, including `test_main_is_the_line_then_the_modern_pages` (Quarto's
  label equals Pandoc's).
- [ ] Commit: "Question labels become headings on the page and HTML (D-0176)".

### T2: Word labels get an outline level

**Depends on:** T1
**Files:** modify `tools/filters/questions.lua` (Word branch),
`tools/make_reference_docx.py` (STYLES, docstring), regenerate
`tools/reference.docx`; test `tests/test_downloads.py` (class
`MarkdownAndWord`)
**Seams:** the built `.docx` (`word/document.xml`, `word/styles.xml`) via
`MarkdownAndWord.part`, `.style`, `.boxes`
**Interfaces:** consumes T1's `level` in the filter's Word branch
**Verify:** build, then `python -m unittest tests.test_downloads.MarkdownAndWord -v`

- [ ] Failing tests, class `MarkdownAndWord`, add near the top:

```python
LABEL_STYLE = re.compile(r"QuestionLabel[2-6]")


def is_label(style):
    return bool(style and LABEL_STYLE.fullmatch(style))
```

  (module level, after `OwnText`), and in the tests:
  `labelled = [b for b in self.boxes(doc_id) if is_label(b[1][0])]` in
  `test_word_questions_are_one_cell_tables`;
  `self.assertTrue(is_label(styles[0]))` in place of
  `self.assertEqual(styles[0], "QuestionLabel")`; the last assertion's
  pattern becomes `r'w:val="QuestionLabel\d?"'` via `assertNotRegex`;
  in `test_word_box_is_the_modern_block`,
  `if not is_label(styles[0]): continue`. New tests:

```python
    def test_word_label_styles_add_only_an_outline_level(self):
        # D-0176: "Question Label N" is "Question Label" with the outline
        # level of an hN, and nothing else, so the box looks as it did.
        for doc_id, _ in converted():
            for level in range(2, 7):
                with self.subTest(doc=doc_id, level=level):
                    style = self.style(doc_id, "QuestionLabel{}".format(level))
                    self.assertIn('<w:name w:val="Question Label {}" />'.format(level), style)
                    self.assertIn('<w:basedOn w:val="QuestionLabel" />', style)
                    self.assertEqual(re.findall(r"<w:(?:pPr|rPr)>.*?</w:(?:pPr|rPr)>", style, re.S),
                                     ['<w:pPr><w:outlineLvl w:val="{}" /></w:pPr>'.format(level - 1)])

    def test_word_label_levels_match_the_page(self):
        # D-0176: each Word label's level is its heading's level on the
        # page, label for label.
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                word = [int(b[1][0][-1]) for b in self.boxes(doc_id) if is_label(b[1][0])]
                html = [int(h) for h in re.findall(
                    r'<h([2-6]) class="(?:question|checkpoint)-label">', page(doc_id, "modern"))]
                self.assertEqual(word, html)
```

- [ ] Run (after a build); expected failure: `is_label` finds no label
  (styles are `QuestionLabel`), so `labelled` is empty and the counts
  differ; the style tests fail on a missing `QuestionLabel2`.
- [ ] `tools/make_reference_docx.py`: after the `QuestionLabel` style in
  `STYLES`, append

```python
    # D-0176: one style per label level, the label's look plus the outline
    # level of an hN, so Word lists the label as a heading.
    + ''.join(
        '<w:style w:type="paragraph" w:customStyle="1" w:styleId="QuestionLabel{0}">'
        '<w:name w:val="Question Label {0}" /><w:basedOn w:val="QuestionLabel" />'
        '<w:next w:val="BodyText" /><w:qFormat />'
        '<w:pPr><w:outlineLvl w:val="{1}" /></w:pPr></w:style>'.format(level, level - 1)
        for level in range(2, 7))
```

  (inside the `STYLES = (...)` expression, before its closing
  parenthesis), and in the docstring's Question Label item add "and
  Question Label 2 to 6, the same with the outline level of an h2 to h6
  (D-0176), which the filter picks by the label's level".
- [ ] Regenerate: `python tools/make_reference_docx.py`.
- [ ] Filter Word branch: `{ ["custom-style"] = "Question Label " .. level }`.
- [ ] Build; run the tests; expected: pass.
- [ ] Commit: "Word question labels get an outline level (D-0176)".

### T3: Box headings sit under their question

**Depends on:** T1
**Files:** modify `curriculum/ph212/ph212-data-analysis-handout.md:111`,
`curriculum/ph212/ph212-extending-a-model-handout.md:122`,
`docs/accessibility/2026-11-05-nvda-ph212.md:7-8`; test `tests/test_headings.py`
**Seams:** `headings(path)` from T1
**Interfaces:** consumes `headings` and `HeadingLevels.labs`
**Verify:** `python -m unittest tests.test_headings -v`; the two files
through `tools/check_unchanged.py` and `tools/check_numbers.py`

- [ ] Failing test, class `HeadingLevels`:

```python
    def test_box_heading_is_below_its_label(self):
        # D-0176: a heading inside a question's box sits under its label.
        for lab, found in self.labs.items():
            for level, kind, box in found:
                if kind == "box":
                    with self.subTest(lab=lab, level=level):
                        self.assertGreater(level, box)
```

- [ ] Run; expected failure: `ph212-data-analysis-handout` and
  `ph212-extending-a-model-handout`, `3 not greater than 3`.
- [ ] Sources: `### What is Uncertainty?` becomes `#### What is
  Uncertainty?`; `### Assumptions:` becomes `#### Assumptions:`. Nothing
  else.
- [ ] Run the test, then both files through the word and number checks;
  expected: pass, word counts unchanged.
- [ ] NVDA report line 7 to 8: "The math and the question labels are
  open." becomes "The question labels are headings (D-0176). The math is
  open." (a record's "Fixes since" clause; its findings stay as written).
- [ ] Commit: "PH 212 Labs 1 and 2: box headings sit under their question".

## After the tasks (main session, not a task)

1. Simplify pass against the spec (fresh context, cap three), then the full
   Verify, green.
2. Screen: serve `build/quarto-site` with a `python -m http.server`
   preview entry in `.claude/launch.json` and read, in the in-app browser,
   the first label's computed `font-size`, `font-weight`, `font-family`,
   `letter-spacing`, `text-transform`, `color`, `line-height`, margins and
   the box's height on PH 212 Lab 1 (h3), PH 211 Data Analysis (h4) and
   PH 212 Lab 3 (h5), at desktop and 375 px, before (the baseline build
   kept in the scratchpad) and after. Equal, or reported. The
   accessibility tree (`read_page`) lists the labels as headings at those
   levels.
3. Print: rasterize each lab's PDF before and after (`pdftoppm -r 50`) and
   compare page counts and pixels; report every difference with its cause.
   Count `/H2` to `/H5` in each new PDF: each lab's labels added.
4. Ledger: D-0176's `test:` names the tests as built.
5. Draft PR, body with the four rulings, the measurements, and the owner's
   Word checks (Navigation pane, a screen reader in Word, a Google Docs
   import) as his acceptance; green `verify`.

No NVDA run: its driver scripts are not in this folder. The accessibility
tree read in step 2 is not a screen-reader test and is reported as such.
