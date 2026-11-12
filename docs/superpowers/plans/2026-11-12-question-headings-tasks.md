# Question labels as headings implementation plan

**Goal:** every question's and checkpoint's label is a heading one level
below its section on the lab page, the HTML download and (by outline level)
the Word download, with the box drawn as it is today.
**Architecture:** `tools/filters/questions.lua` already writes every label;
it switches to top-down traversal so it meets headings and questions in
document order, tracks the last section level, and writes the label as a
`Header` in an attribute-less `Div` (Word: a "Question Label N" paragraph
style with an outline level).
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
- Word: styles "Question Label 3", "4" and "5" (D-0176's decision; the
  levels `main` uses: 112, 66 and 16 labels), each `basedOn` "Question
  Label" plus `<w:outlineLvl w:val="level-1"/>` and nothing else. A label
  at any other level fails the Word render, naming D-0176.
- The box stays a `<div>`: no question becomes a `<section>` (spec 8.1).
- Commit as hunterthelabguy with the noreply email, no trailer; subjects
  <=72 characters.

## Files

| File | Responsibility | Task |
|---|---|---|
| `tools/filters/questions.lua` | label as heading, level by section; Word style by level | T1, T2 |
| `themes/modern.css` | label look on a heading | T1 |
| `tests/test_check_numbers.py` (class `Filter`) | filter unit tests on small bodies | T1 |
| `tests/test_headings.py` | rendered heading reading: no skip, label level, box headings | T1, T3 |
| `tests/test_downloads.py` | label form in the print-split check; no duplicate ids; Word styles | T1, T2 |
| `tests/fixtures/main-bodies.json` | PH 211 Lab 1's pinned `<main>` digest, recomputed | T1 |
| `tools/make_reference_docx.py`, `tools/reference.docx` | the three level styles | T2 |
| `curriculum/ph212/ph212-data-analysis-handout.md:111`, `curriculum/ph212/ph212-extending-a-model-handout.md:122` | box heading `###` to `####` | T3 |
| `docs/accessibility/2026-11-05-nvda-ph212.md:8` | "Fixes since" names D-0176 | T3 |

`tools/check_numbers.py` is not changed: it reads the label as the plain
text of the box's first block, which the label's wrapper (T1) gives as
"Question N".

No print rule is added. An H3 or H4 label already takes the print block's
`h1, h2, h3, h4 { break-after: avoid; }`, and `.question` keeps
`break-inside: avoid`; an H5 label (16 of 194) prints as the old `<p>`
label did. A label-only print rule would have no test that could fail:
`PrintKeeps` reads headings `<h[1-4]` and the print's "QUESTION N" never
matches the label's "Question N" (executing critique 1, finding 5).

A question nested in a question is not labelled: top-down traversal with
`false` does not walk a box's content. None exists on `main` (194 labels,
194 questions), and `check_numbers` would fail on a missing label.

Revision 1 (2026-11-12) folds executing critique 1 (read 0e233cb; report
and patches in the scratchpad's `critique-1/`): F1 (label wrapper), F2
(digest), the print rule dropped, the Word styles brought back to D-0176's
three, the probe moved after the build, and the plan's text fixes.

### T1: Labels become headings on the page and the HTML download

**Depends on:** none
**Files:** modify `tools/filters/questions.lua`, `themes/modern.css:111-117`,
`tests/fixtures/main-bodies.json`; test `tests/test_check_numbers.py`
(class `Filter`), `tests/test_headings.py`, `tests/test_downloads.py:877`
and class `Html`
**Seams:** the filter's HTML output for a Markdown body; the rendered AST
of each source (`check_numbers.FROM`, `check_numbers.FILTER`,
`-M theme-name=modern`); the built page `build/quarto-site/labs/<id>/modern/index.html`
**Interfaces:** produces the module-level `section` in `questions.lua`
and, for non-Word output, the label element
`pandoc.Div({ pandoc.Header(level, {Str text}, Attr("", {kind.."-label"})) })`
(an attribute-less wrapper); T2 reads `level` in the Word branch.
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
        # A Div opening with a heading is written as a <section> carrying
        # the heading's class (Pandoc 3.10); the box stays a div (spec 8.1).
        self.assertIn('<div id="a" class="question">', out)
        self.assertNotIn("<section", out)

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
  (`skips` now takes a list of levels). The source-text reading goes,
  which departs from spec section 3 ("gains a second reading"): the
  rendered walk finds exactly every ATX heading in all 19 sources
  (critique 1, measured), so nothing is lost on `main`. It does not walk
  Table, DefinitionList or Figure content, where no source has a heading.

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
                    if label["t"] == "Div" and label["c"][0] == ["", [], []]:
                        label = label["c"][1][0]
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
      -- An attribute-less Div around the heading, which Pandoc writes as no
      -- element: a Div opening with a heading becomes a <section> carrying
      -- the heading's class (Pandoc 3.10, probed 2026-11-12).
      table.insert(el.content, 1, pandoc.Div({
        pandoc.Header(level, { pandoc.Str(text) }, pandoc.Attr("", { kind .. "-label" })) }))
      return el, false
    end,
  },
```

  and in the header comment replace the two lines

```lua
-- The block becomes a labeled block ("Question N"), and all its bold is
-- removed so that bold means emphasis again (ledger 29; D-0101, S4). The
```

  with

```lua
-- The block becomes a labeled block, its label ("Question N") a heading
-- one level below its section (D-0176), and all its bold is removed so
-- that bold means emphasis again (ledger 29; D-0101, S4). The
```
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

  The print block is not changed (see Files).
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

- [ ] Build (`python tools/quarto_build.py`; there is no single-page
  path). Probe after the build, in
  `build/quarto-site/labs/ph212-data-analysis-handout/modern/index.html`:
  the first question reads `<div id="ph212-data-analysis:group-member-qualities" class="question">`
  then `<h3 class="question-label">Question 1</h3>`, with no `id=` and no
  `anchored` class on the heading, and the page's count of `<section` is
  the baseline's (the build of 0e233cb, kept in the scratchpad as
  `before-site/`). Anything else stops the task.
- [ ] `tests/fixtures/main-bodies.json`: recompute PH 211 Lab 1's digest
  exactly as `DocumentBodies.test_bodies_unchanged` does (its five labels
  changed markup; D-0108 updated it the same way):

```python
import hashlib, re, pathlib
text = pathlib.Path("build/quarto-site/labs/ph211-team-building-handout/modern/index.html").read_text(encoding="utf-8")
main = re.search(r"<main id=\"content\">.*?</main>", text, re.S).group(0).replace('<main id="content">', "<main>", 1)
print(hashlib.sha256(main.encode()).hexdigest())
```

  Before replacing it, diff that `<main>` against the baseline's: the only
  change is the five labels' markup.
- [ ] `python -m unittest discover -s tests`; expected: all pass,
  including `test_main_is_the_line_then_the_modern_pages` (Quarto's label
  equals Pandoc's) and `PrintKeeps`.
- [ ] Commit: "Question labels become headings on the page and HTML (D-0176)".

### T2: Word labels get an outline level

**Depends on:** T1
**Files:** modify `tools/filters/questions.lua` (Word branch),
`tools/make_reference_docx.py` (STYLES, docstring), regenerate
`tools/reference.docx`; test `tests/test_downloads.py` (class
`MarkdownAndWord`), `tests/test_check_numbers.py` (class `Filter`)
**Seams:** the built `.docx` (`word/document.xml`, `word/styles.xml`) via
`MarkdownAndWord.part`, `.style`, `.boxes`
**Interfaces:** consumes T1's `level` in the filter's Word branch
**Verify:** `python -m unittest tests.test_check_numbers.Filter -v`, then
build and `python -m unittest tests.test_downloads.MarkdownAndWord -v`

- [ ] Failing tests. At module level in `tests/test_downloads.py`,
  directly after class `OwnText`, add:

```python
LABEL_STYLE = re.compile(r"QuestionLabel[3-5]")


def is_label(style):
    return bool(style and LABEL_STYLE.fullmatch(style))
```

  and in class `MarkdownAndWord`:
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
            for level in range(3, 6):
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
  differ; the style tests fail on a missing `QuestionLabel3`.
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
        for level in range(3, 6))
```

  (inside the `STYLES = (...)` expression, before its closing
  parenthesis), and in the docstring's Question Label item add "and
  Question Label 3 to 5, the same with the outline level of an h3 to h5
  (D-0176), which the filter picks by the label's level".
- [ ] Regenerate: `python tools/make_reference_docx.py`.
- [ ] Filter Word branch: `{ ["custom-style"] = "Question Label " .. level }`,
  and at the top of that branch:

```lua
        if level < 3 or level > 5 then
          error(kind .. " " .. name .. "'s label would be h" .. level
            .. "; tools/reference.docx has Question Label 3 to 5 only (D-0176)")
        end
```

  and its test in `tests/test_check_numbers.py`, class `Filter` (the
  check comes before `word_box`, so no colours are needed):

```python
    def test_word_label_outside_h3_to_h5_fails(self):
        # D-0176: Word has Question Label 3 to 5; an h2 label (no section
        # above it) has no style, so the render stops.
        out = self.render(q("a"), "-t", "docx", "-o", os.devnull)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("Question Label 3 to 5", out.stderr)
```
- [ ] Build; run the tests; expected: pass.
- [ ] Commit: "Word question labels get an outline level (D-0176)".

### T3: Box headings sit under their question

**Depends on:** T1
**Files:** modify `curriculum/ph212/ph212-data-analysis-handout.md:111`,
`curriculum/ph212/ph212-extending-a-model-handout.md:122`,
`docs/accessibility/2026-11-05-nvda-ph212.md:8`; test `tests/test_headings.py`
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
- [ ] NVDA report line 8: "The math and the question labels are
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
   Count `/H2` to `/H5` in each new PDF with `pdfinfo -struct` (poppler's,
   beside `PDFTOTEXT`): each lab's labels added, at their levels.
4. Ledger: D-0176's `test:` names the tests as built.
5. Draft PR, body with the four rulings, the measurements, and the owner's
   Word checks (Navigation pane, a screen reader in Word, a Google Docs
   import) as his acceptance; green `verify`.

No NVDA run: its driver scripts are not in this folder. The accessibility
tree read in step 2 is not a screen-reader test and is reported as such.
