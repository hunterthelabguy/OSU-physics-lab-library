# Function groups in MathML: implementation plan

**Goal:** a function of a bracketed argument (`\cos\left( \right)`,
`\sin( )`) reads correctly with MathCAT: the build puts the function's name,
U+2061 and the argument in one `<mrow>` (D-0181).
**Architecture:** one text post-processor, `downloads.grouped_functions`,
beside `without_empty_image_role`. `tools/downloads.py`'s `html()` runs it on
the HTML download; `tools/quarto_build.py`'s `dress_pages` runs it on every
built page. No source changes.
**Spec:** `DECISIONS.md` D-0181 (ruled 2026-11-13);
`docs/accessibility/2026-11-13-nvda-ph212-equations.md` (#85).
**Verify:** with `PANDOC="/c/Program Files/Quarto/bin/tools/pandoc.exe"`:
`python -m unittest tests.test_downloads.FunctionGroups`. The built-page test
(`tests.test_quarto_site`) needs the Quarto build and runs in CI's `verify`.

## Global constraints

- No handout source changes, and the word check is untouched (D-0181 (3)).
- An unmatched bracket after a function fails the build (D-0181 (1)).
- The Word download and the PDF are not post-processed (D-0181 (2)).
- One tool PR with green CI `verify`, squash merge on the owner's go-ahead,
  then read main's run.
- Identity `hunterthelabguy`, noreply email, no trailer, subject <=72.

## The markup (measured on CI's build at `c70151f`, 2026-11-13)

Pandoc writes a function's name as `<mrow><mi mathvariant="normal">cos</mi>
<mo>U+2061</mo></mrow>` with no whitespace and U+2061 as the literal
character, in pages and in the HTML download alike. What follows it:
- a fenced argument, written as `<mrow><mo stretchy="true" form="prefix">(</mo>...
  <mo stretchy="true" form="postfix">)</mo></mrow>` (PH 212 Lab 6,
  `\cos\left( Ct + D \right)`);
- bare brackets in the same `<mrow>` as the name group, `<mo stretchy="false"
  form="prefix">(</mo>...<mo stretchy="false" form="postfix">)</mo>`
  (PH 213 Data Analysis, `\sin(\theta)`);
- a letter or script (`\sin\theta_{i}`). This is left alone; it reads
  correctly.

A function written without U+2061 (`<mi>sin</mi>` alone, PH 212 Lab 6's
`g\sin\theta`) is not matched.

The grouping that read correctly (probe J, 2026-11-13) is `<mrow><mi>cos</mi>
<mo>U+2061</mo><mrow><mo>(</mo>...<mo>)</mo></mrow></mrow>`. Bare brackets are
therefore wrapped in an `<mrow>` of their own, so both cases give that shape.

## Files

| File | Change |
|---|---|
| `tools/downloads.py` | `FUNCTION_GROUP`, `MATH_TAG`, `grouped_functions` after `without_empty_image_role`; `html()` runs it |
| `tools/quarto_build.py` | `dress_pages` runs it before `quarto_chrome.dress` |
| `tests/test_downloads.py` | class `FunctionGroups`, six unit tests on made-up markup |
| `tests/test_quarto_site.py` | `Pages.test_functions_grouped_with_their_brackets` |
| `DECISIONS.md` | D-0181 (ruled, on this branch) |

### T1: the rewrite, test-first

**Depends on:** none
**Seams:** `downloads.grouped_functions(text) -> str`; raises `SystemExit` on
an unmatched bracket.
**Verify:** `python -m unittest tests.test_downloads.FunctionGroups` (6 OK).

- [ ] Branch `mathml-function-groups` (worktree
  `.superpowers/sdd/mathml-function-groups`), on `origin/main` plus D-0181.
- [ ] Failing tests: add after class `DecorativePictures` in
  `tests/test_downloads.py`:

```python
class FunctionGroups(unittest.TestCase):
    """D-0181: a function's name, U+2061 and its bracketed argument in one
    mrow, the grouping MathCAT reads as "cosine of (...)" (made-up markup)."""

    NAME = '<mrow><mi mathvariant="normal">{}</mi><mo>⁡</mo></mrow>'
    OPEN = '<mo stretchy="{}" form="prefix">(</mo>'
    CLOSE = '<mo stretchy="{}" form="postfix">)</mo>'

    def grouped(self, name, arg):
        return ('<mrow><mi mathvariant="normal">' + name + '</mi><mo>⁡</mo>'
                + arg + '</mrow>')

    def test_fenced_argument_joins_its_function(self):
        arg = ('<mrow>' + self.OPEN.format("true") + '<mi>x</mi>'
               + self.CLOSE.format("true") + '</mrow>')
        got = downloads.grouped_functions(
            '<math><mrow><mi>A</mi>' + self.NAME.format("cos") + arg + '<mo>+</mo></mrow></math>')
        self.assertEqual(got, '<math><mrow><mi>A</mi>' + self.grouped("cos", arg)
                         + '<mo>+</mo></mrow></math>')

    def test_bare_brackets_are_wrapped_and_joined(self):
        run = self.OPEN.format("false") + '<mi>θ</mi>' + self.CLOSE.format("false")
        got = downloads.grouped_functions(
            '<mrow><mi>m</mi>' + self.NAME.format("sin") + run + '</mrow>')
        self.assertEqual(got, '<mrow><mi>m</mi>'
                         + self.grouped("sin", '<mrow>' + run + '</mrow>') + '</mrow>')

    def test_a_function_inside_an_argument_is_grouped_too(self):
        inner = self.OPEN.format("false") + '<mi>x</mi>' + self.CLOSE.format("false")
        outer = (self.OPEN.format("false") + self.NAME.format("cos") + inner
                 + self.CLOSE.format("false"))
        got = downloads.grouped_functions('<mrow>' + self.NAME.format("sin") + outer + '</mrow>')
        want_inner = self.grouped("cos", '<mrow>' + inner + '</mrow>')
        want = self.grouped("sin", '<mrow>' + self.OPEN.format("false") + want_inner
                            + self.CLOSE.format("false") + '</mrow>')
        self.assertEqual(got, '<mrow>' + want + '</mrow>')

    def test_a_function_before_a_letter_is_left_alone(self):
        text = ('<mrow>' + self.NAME.format("sin") + '<msub><mi>θ</mi><mi>i</mi></msub>'
                '<mi mathvariant="normal">sin</mi><mi>θ</mi></mrow>')
        self.assertEqual(downloads.grouped_functions(text), text)

    def test_a_bracket_group_holding_more_stops_the_build(self):
        arg = ('<mrow>' + self.OPEN.format("true") + '<mi>x</mi>' + self.CLOSE.format("true")
               + '<mo>+</mo><mi>E</mi></mrow>')
        with self.assertRaises(SystemExit):
            downloads.grouped_functions('<mrow>' + self.NAME.format("cos") + arg + '</mrow>')

    def test_an_unmatched_bracket_stops_the_build(self):
        with self.assertRaises(SystemExit):
            downloads.grouped_functions(
                '<mrow>' + self.NAME.format("sin") + self.OPEN.format("false")
                + '<mi>x</mi></mrow>')
```

- [ ] Run; expected: 6 errors (`AttributeError: ... grouped_functions`).
- [ ] Implement, after `without_empty_image_role` in `tools/downloads.py`:

```python
# D-0181: Pandoc writes a function's name and U+2061 as an mrow of their own;
# before a bracket MathCAT then reads "cosine of times (...)".
FUNCTION_GROUP = re.compile(r'<mrow>(<mi[^>]*>[^<]+</mi><mo>⁡</mo>)</mrow>'
                            r'(?=(?:<mrow>)?<mo[^>]*form="prefix")')
MATH_TAG = re.compile(r'<mrow\b[^>]*>|</mrow>|<mo\b[^>]*form="(prefix|postfix)"[^>]*>[^<]*</mo>')


def argument_end(text, start):
    """End of the bare brackets that open at start: just past the bracket
    that closes the first."""
    rows = fences = 0
    for m in MATH_TAG.finditer(text, start):
        tag = m.group(0)
        if tag.startswith("<mrow"):
            rows += 1
        elif tag == "</mrow>":
            rows -= 1
            if rows < 0:
                break
        else:
            fences += 1 if m.group(1) == "prefix" else -1
        if rows == 0 and fences == 0:
            return m.end()
    raise SystemExit("D-0181: a function's bracket is not closed: "
                     + text[start:start + 120])


def grouped_functions(text):
    """D-0181: a function's name, U+2061 and its bracketed argument in one
    mrow, the grouping MathCAT reads as "cosine of (...)"."""
    out, pos = [], 0
    for m in FUNCTION_GROUP.finditer(text):
        if m.start() < pos:
            continue  # inside an argument already rewritten
        start = m.end()
        fenced = text.startswith("<mrow>", start)
        first = start + len("<mrow>") if fenced else start
        end = argument_end(text, first)
        if fenced:
            if not text.startswith("</mrow>", end):
                raise SystemExit("D-0181: a function's bracketed group holds more"
                                 " than its brackets: " + text[start:end + 40])
            arg, end = text[first:end], end + len("</mrow>")
        else:
            arg = text[start:end]
        out += [text[pos:m.start()], "<mrow>", m.group(1),
                "<mrow>", grouped_functions(arg), "</mrow>", "</mrow>"]
        pos = end
    return "".join(out) + text[pos:]
```

  Both cases scan the brackets from the opening `<mo>` to the one that
  brings the count back to 0. A fenced argument must close its `<mrow>` right
  there; if that row holds more (`{(x) + E}`, the shape Lab 6's TeX had before
  D-0167), the build stops rather than sweep the rest into the argument. An
  `</mrow>` that closes the enclosing row first means an unmatched bracket,
  and the build stops too.
- [ ] Run; expected: 6 OK.
- [ ] Commit `Downloads: group a function with its bracketed argument (D-0181)`.

### T2: run it on the pages and the HTML download

**Depends on:** T1
**Seams:** the built pages and HTML downloads under `build/quarto-site`.
**Verify:** CI `verify` (the build plus `tests.test_quarto_site`); locally,
`grouped_functions` run on CI's artifact pages from `c70151f` and read with
the MathML reader.

- [ ] In `tools/downloads.py`'s `html()`, change `decorative =
  without_empty_image_role(text)` to `decorative =
  grouped_functions(without_empty_image_role(text))`. The variable's name
  then undersells it: rename it `cleaned` in its three lines.
- [ ] In `tools/quarto_build.py`'s `dress_pages`, write
  `quarto_chrome.dress(downloads.grouped_functions(text), body_class, top, bottom)`.
- [ ] In `tests/test_quarto_site.py`, class `Pages`, after
  `test_expected_pages`:

```python
    def test_functions_grouped_with_their_brackets(self):
        # D-0181: no function's name sits in an mrow of its own before a
        # bracket, on a lab page or its HTML download; Lab 6's cosine is grouped.
        apart = re.compile(r'<mrow><mi[^>]*>[^<]+</mi><mo>⁡</mo></mrow>'
                           r'(?:<mrow>)?<mo[^>]*form="prefix"')
        for doc_id, _ in converted():
            for rel in (f"labs/{doc_id}/modern/index.html", f"labs/{doc_id}/{doc_id}.html"):
                with self.subTest(page=rel):
                    self.assertIsNone(apart.search((QSITE / rel).read_text(encoding="utf-8")))
        lab6 = (QSITE / "labs/ph212-capstone-handout/modern/index.html").read_text(encoding="utf-8")
        self.assertIn('<mi mathvariant="normal">cos</mi><mo>⁡</mo><mrow><mo', lab6)
```

- [ ] Locally: run `grouped_functions` on CI's artifact copies of PH 212
  Lab 6's and PH 213 Data Analysis's page and HTML download. Expected: each
  changes exactly one equation, and the MathML reader, with its function
  check added, flags none of them. (The reader's existing U+2061 exemption
  is why D-0167's check missed this; the added check flags an `<mrow>`
  holding only an `<mi>` and U+2061 that is followed by a prefix `<mo>`.)
- [ ] Commit `Build: function groups on pages and HTML downloads (D-0181)`;
  push; PR; green `verify`; read CI's artifact for the two pages.

## Not in this plan

- An NVDA rerun of the two pages (D-0181 (4), only on the owner's word).
- PH 213 Data Analysis's `sin(θ)` set as letters (PH 213's own entry).
- A report to MathCAT upstream (offered separately).
