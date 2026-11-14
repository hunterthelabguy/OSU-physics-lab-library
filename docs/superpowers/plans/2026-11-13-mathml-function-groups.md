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
<mo>U+2061</mo></mrow>` with no whitespace. Pandoc itself writes U+2061 as
`&#8289;`. The pages hold the literal character after Quarto's own
processing, and the HTML download after `--embed-resources`. The rewrite and
the tests accept the literal character, `&#8289;` and `&#x2061;`. What
follows it:
- a fenced argument, written as `<mrow><mo stretchy="true" form="prefix">(</mo>...
  <mo stretchy="true" form="postfix">)</mo></mrow>` (PH 212 Lab 6,
  `\cos\left( Ct + D \right)`);
- bare brackets in the same `<mrow>` as the name group, `<mo stretchy="false"
  form="prefix">(</mo>...<mo stretchy="false" form="postfix">)</mo>`
  (PH 213 Data Analysis, `\sin(\theta)`);
- a letter, script or fraction (`\sin\theta_{i}`, Lab 6's `\frac{m g\sin\theta}{b_1}`).
  This is left alone; it reads correctly.

Only round brackets count, matched by character, as D-0181 (1) says: `( )`,
fenced or bare. `[x]`, `\{x\}` and `|x|` after a function are left alone.
Brackets pair among the same row's children. A `)` that closes inside a
child element (`\sin(x)^{2}`, `\sin(x)_{i}`, `\sin(x)'`, where Pandoc puts the
`)` in the `<msup>` or `<msub>`), or a bracket that spans aligned rows, cannot
be paired, so the build stops (D-0181 (1)). Regrouping across an element
boundary would write broken MathML. Known limits, left alone
and not regrouped (pass 2 confirmed each on Pandoc's output): `\cos{\left( x
\right) + E}` (two nested rows; Lab 6 had it before D-0167, and Word's
converter writes it), `\sin\left( x \right)^{2}` and `\sin^{2}(x)` (the name
group is not followed by a bracket). No page holds any of them today; PH
211 has an unconverted `\mathbf{\tan}\left(`, so its conversion should look.
An empty element (`<mspace/>`) is never written by Pandoc; if one sits in an
argument the depth count is off: the build stops, or, inside an outer
bracket, the outer `)` is swept into the group; no page or Pandoc output
holds one.

A function written without U+2061 (`<mi>sin</mi>` alone, PH 212 Lab 6's
`g\sin\theta`) is not matched.

The grouping that read correctly (probe J, 2026-11-13) is `<mrow><mi>cos</mi>
<mo>U+2061</mo><mrow><mo>(</mo>...<mo>)</mo></mrow></mrow>`. Bare brackets are
therefore wrapped in an `<mrow>` of their own, so both cases give that shape.

## Files

| File | Change |
|---|---|
| `tools/downloads.py` | `FUNCTION_GROUP`, `MATH_TOKEN`, `argument_end`, `grouped_functions` after `without_empty_image_role`; `html()` runs it |
| `tools/quarto_build.py` | `dress_pages` runs it before `quarto_chrome.dress` |
| `tests/test_downloads.py` | class `FunctionGroups`, nine unit tests on made-up markup |
| `tests/test_quarto_site.py` | `Pages.test_functions_grouped_with_their_brackets` |
| `DECISIONS.md` | D-0181 (ruled, on this branch) |

### T1: the rewrite, test-first

**Depends on:** none
**Seams:** `downloads.grouped_functions(text) -> str`; raises `SystemExit` on
an unmatched bracket.
**Verify:** `python -m unittest tests.test_downloads.FunctionGroups` (9 OK).
`tests/test_downloads.py`'s `setUpModule` needs a `build/quarto-site`
folder: locally, an empty one does, for these unit tests.

- [ ] Branch `mathml-function-groups` (worktree
  `.superpowers/sdd/mathml-function-groups`), on `origin/main` plus D-0181.
- [ ] Failing tests: add after class `DecorativePictures` in
  `tests/test_downloads.py`:

```python
class FunctionGroups(unittest.TestCase):
    """D-0181: a function's name, U+2061 and its bracketed argument in one
    mrow, the grouping MathCAT reads as "cosine of (...)" (made-up markup)."""

    NAME = '<mrow><mi mathvariant="normal">{}</mi><mo>\u2061</mo></mrow>'
    OPEN = '<mo stretchy="{}" form="prefix">(</mo>'
    CLOSE = '<mo stretchy="{}" form="postfix">)</mo>'

    def grouped(self, name, arg, apply="\u2061"):
        return ('<mrow><mi mathvariant="normal">' + name + '</mi><mo>' + apply + '</mo>'
                + arg + '</mrow>')

    def bare(self, inner='<mi>x</mi>'):
        return self.OPEN.format("false") + inner + self.CLOSE.format("false")

    def test_fenced_argument_joins_its_function(self):
        arg = '<mrow>' + self.OPEN.format("true") + '<mi>x</mi>' + self.CLOSE.format("true") + '</mrow>'
        got = downloads.grouped_functions(
            '<math><mrow><mi>A</mi>' + self.NAME.format("cos") + arg + '<mo>+</mo></mrow></math>')
        self.assertEqual(got, '<math><mrow><mi>A</mi>' + self.grouped("cos", arg)
                         + '<mo>+</mo></mrow></math>')

    def test_bare_brackets_are_wrapped_and_joined(self):
        got = downloads.grouped_functions('<mrow><mi>m</mi>' + self.NAME.format("sin") + self.bare() + '</mrow>')
        self.assertEqual(got, '<mrow><mi>m</mi>'
                         + self.grouped("sin", '<mrow>' + self.bare() + '</mrow>') + '</mrow>')

    def test_the_entity_form_is_grouped_too(self):
        name = self.NAME.format("sin").replace("\u2061", "&#8289;")
        got = downloads.grouped_functions('<mrow>' + name + self.bare() + '</mrow>')
        self.assertEqual(got, '<mrow>' + self.grouped("sin", '<mrow>' + self.bare() + '</mrow>',
                                                       "&#8289;") + '</mrow>')

    def test_a_function_inside_an_argument_is_grouped_too(self):
        outer = self.bare(self.NAME.format("cos") + self.bare())
        got = downloads.grouped_functions('<mrow>' + self.NAME.format("sin") + outer + '</mrow>')
        want_inner = self.grouped("cos", '<mrow>' + self.bare() + '</mrow>')
        want = self.grouped("sin", '<mrow>' + self.bare(want_inner) + '</mrow>')
        self.assertEqual(got, '<mrow>' + want + '</mrow>')

    def test_what_is_not_a_round_bracket_after_a_function_is_left_alone(self):
        for after in ('<msub><mi>θ</mi><mi>i</mi></msub>',          # a letter or script
                      '<mo stretchy="false" form="prefix">[</mo><mi>x</mi>'
                      '<mo stretchy="false" form="postfix">]</mo>',  # square brackets
                      '<mo stretchy="false" form="prefix">|</mo><mi>x</mi>'
                      '<mo stretchy="false" form="prefix">|</mo>'):  # bars
            text = '<mrow>' + self.NAME.format("sin") + after + '</mrow>'
            with self.subTest(after=after):
                self.assertEqual(downloads.grouped_functions(text), text)
        other = '<mrow><mrow><mi>a</mi><mo>+</mo></mrow>' + self.bare() + '</mrow>'
        self.assertEqual(downloads.grouped_functions(other), other)

    def test_a_bracket_group_holding_more_stops_the_build(self):
        arg = ('<mrow>' + self.OPEN.format("true") + '<mi>x</mi>' + self.CLOSE.format("true")
               + '<mo>+</mo><mi>E</mi></mrow>')
        with self.assertRaises(SystemExit):
            downloads.grouped_functions('<mrow>' + self.NAME.format("cos") + arg + '</mrow>')

    def test_an_unmatched_bracket_stops_the_build(self):
        # The row ends first; a ")" after it does not pair with the "(".
        with self.assertRaises(SystemExit):
            downloads.grouped_functions(
                '<mrow><mrow>' + self.NAME.format("sin") + self.OPEN.format("false")
                + '<mi>x</mi></mrow>' + self.CLOSE.format("false") + '</mrow>')

    def test_a_bracket_closing_in_a_later_cell_stops_the_build(self):
        # Aligned rows, \sin( x \\ y ): the ")" is in the next cell.
        text = ('<mtable><mtr><mtd>' + self.NAME.format("sin") + self.OPEN.format("false")
                + '<mi>x</mi></mtd></mtr><mtr><mtd><mi>y</mi>' + self.CLOSE.format("false")
                + '</mtd></mtr></mtable>')
        with self.assertRaises(SystemExit):
            downloads.grouped_functions(text)

    def test_a_bracket_closing_inside_a_script_stops_the_build(self):
        # \sin(x)^{2}: Pandoc puts the ")" inside the msup.
        with self.assertRaises(SystemExit):
            downloads.grouped_functions(
                '<mrow>' + self.NAME.format("sin") + self.OPEN.format("false") + '<mi>x</mi>'
                '<msup>' + self.CLOSE.format("false") + '<mn>2</mn></msup></mrow>')
```

- [ ] Run; expected: 9 tests, all erroring (`AttributeError: ... grouped_functions`; unittest counts each subTest's error too).
- [ ] Implement, after `without_empty_image_role` in `tools/downloads.py`:

```python
# D-0181: Pandoc writes a function's name and U+2061 as an mrow of their own;
# before a bracket MathCAT then reads "cosine of times (...)".
APPLY = "(?:\u2061|&#8289;|&#x2061;)"
FUNCTION_GROUP = re.compile(r'<mrow>(<mi[^>]*>[^<]+</mi><mo>' + APPLY + r'</mo>)</mrow>'
                            r'(?=(?:<mrow>)?<mo[^>]*>\(</mo>)')
MATH_TOKEN = re.compile(r'<mo\b[^>]*>([()])</mo>|<(/?)\w+\b[^>]*>')


def argument_end(text, start):
    """End of the brackets that open at start: just past the ")" that closes
    the first "(" among the same row's children."""
    depth = parens = 0
    for m in MATH_TOKEN.finditer(text, start):
        if m.group(1):
            if depth == 0:
                parens += 1 if m.group(1) == "(" else -1
                if parens == 0:
                    return m.end()
        elif m.group(2):
            depth -= 1
            if depth < 0:
                break
        else:
            depth += 1
    raise SystemExit("D-0181: a function's bracket does not close in its own row: "
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

  Both cases scan from the opening `(` to the `)` that brings the count back
  to 0, counting only brackets that are direct children of the row, while
  tracking every element's open and close tags. A close tag below the
  starting depth (the row ends, or an `</msup>` or `</mtd>` closes first)
  means the bracket cannot be paired, and the build stops. A fenced argument
  must close its `<mrow>` right after its `)`. If that row holds more, the
  build stops rather than sweep the rest into the argument.
- [ ] Run; expected: 9 OK.
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
        # bracket, on a lab page or its HTML download; the two that had one
        # (PH 212 Lab 6's cosine, PH 213 Data Analysis's sine) are grouped.
        apply = "(?:\u2061|&#8289;|&#x2061;)"
        apart = re.compile(r'<mrow><mi[^>]*>[^<]+</mi><mo>' + apply + r'</mo></mrow>'
                           r'(?:<mrow>)?<mo[^>]*>\(</mo>')
        for doc_id, _ in converted():
            for rel in (f"labs/{doc_id}/modern/index.html", f"labs/{doc_id}/{doc_id}.html"):
                with self.subTest(page=rel):
                    self.assertIsNone(apart.search((QSITE / rel).read_text(encoding="utf-8")))
        for doc_id, name in (("ph212-capstone-handout", "cos"), ("ph213-data-analysis-handout", "sin")):
            for rel in (f"labs/{doc_id}/modern/index.html", f"labs/{doc_id}/{doc_id}.html"):
                with self.subTest(grouped=rel):
                    self.assertRegex((QSITE / rel).read_text(encoding="utf-8"),
                                     '<mi mathvariant="normal">' + name + '</mi><mo>' + apply
                                     + '</mo><mrow><mo')
```

- [ ] Locally: run `grouped_functions` on CI's artifact copies of every lab
  page and HTML download. Expected: exactly four files change (PH 212 Lab 6
  and PH 213 Data Analysis, page and download), one equation each; every
  other file comes back byte-identical; every `<math>` still parses as XML.
  Add this check to the MathML reader's `flags()` and run it: 1 flag before,
  0 after, on each of the four files.

```python
        if tag == "mrow" and [local(k) for k in kids] == ["mi", "mo"] \
                and (kids[1].text or "") == "\u2061":
            parent = parents.get(el)
            sibs = [k for k in parent if local(k) != "annotation"] if parent is not None else []
            nxt = sibs[sibs.index(el) + 1] if el in sibs and sibs.index(el) + 1 < len(sibs) else None
            first = nxt[0] if nxt is not None and local(nxt) == "mrow" and len(nxt) else nxt
            if first is not None and local(first) == "mo" and (first.text or "").strip() == "(":
                out.append("function apart from its bracket")
```

  (`parents` is `{c: p for p in math.iter() for c in p}`, built once at the
  top of `flags()`.)
- [ ] Commit `Build: function groups on pages and HTML downloads (D-0181)`;
  push; PR; green `verify`; read CI's artifact for the two pages.

## Not in this plan

- An NVDA rerun of the two pages (D-0181 (4), only on the owner's word).
- PH 213 Data Analysis's `sin(θ)` set as letters (PH 213's own entry).
- A report to MathCAT upstream (offered separately).
