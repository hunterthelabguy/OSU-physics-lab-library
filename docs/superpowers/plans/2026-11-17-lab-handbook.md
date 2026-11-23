# Lab Handbook implementation plan

**Revision 2, 2026-11-18.** Rewritten after D-0195 (a handout is re-baselined at its first ruled change) and D-0197 (the handbook is created re-baselined; the span omission is deleted). Revision 1 (commit 72e36d6) had seven tasks, a span omission in both Word checks and a two-step handbook; its executing critique (pass 1) is kept below. This revision builds D-0195 first, since every remaining task depends on it.

**Revision 2.1, 2026-11-18.** Pass 2's mechanical fixes folded (section "Executing critique, pass 2").
**Revision 2.2, 2026-11-18.** Pass 2's six needs-ruling findings folded as D-0198: D-0169's lists dropped unconditionally, the `ruled-change` set pinned, image hashes checked by the build, the handbook held to Lab 7's appendix (D-0191 as amended), the landing card, Lab 3's PDF in the trial check.
**Revision 2.3, 2026-11-18 (the owner's note added 2026-11-19).** Pass 3's mechanical fixes folded (section "Executing critique, pass 3"). Pass 3 was the third under the cap and not clean, so this revision is handed to the owner, not to `/build`. The owner, 2026-11-19: "Promote, then do a fourth pass." A fourth pass runs past the cap on that word.
**Revision 2.4, 2026-11-19.** Pass 4's mechanical fixes folded (section "Executing critique, pass 4"). Not rebased: main moved past `bff3394` the same day (PRs #86, #88 and #90 merged), and #86 added a second `ruled-change` file; that is raised to the owner.
**Revision 2.5, 2026-11-19.** Rebased on main at `364ae73` (PRs #86, #88 and #90). On the owner's ruling (D-0200, promoted 2026-11-19), T1 treats D-0184's file as it treats D-0169's (drops its lists, pins it) and asserts that no `ruled-change` file keeps a list. The plan's line numbers in the files those PRs touched were rechecked against `364ae73` and hold.

**Revision 2.6, 2026-11-19.** The owner's D-0201 folded: the handbook is a starting point, not a copy of Lab 7. T3 drops `HeldToLab7` and keeps `handbook_body()` in its one-time creation script; T1's CLAUDE.md exception says the handbook changes only after the PH 211 appendix cuts. Nothing else in the build changes.

**Goal:** Build D-0195's re-baselining, link handouts to a converted document by stable addresses (D-0190), publish the Lab Handbook (D-0188 as amended by D-0197), and make PH 211 Lab 3's appendix cut as the trial (D-0192 as amended by D-0197).
**Architecture:** The two Word checks skip a file whose `status` is `ruled-change` and say so, and the em-dash scan reads such a file as a published source. `tools/filters/media.lua` rewrites a `<id>#<identifier>` link to the library's address, and a source-level test validates every such link. The handbook is a new `ruled-change` document whose body is copied by script, line for line, from PH 211 Lab 7's converted Markdown (proven against Word), with its name, opening line, contents links and fixed section addresses; it keeps Lab 7's `source_file` as provenance, so the existing page, listing and downloads carry it. Lab 3's cut is an ordinary ruled-change edit.
**Specs:** `docs/superpowers/specs/2026-11-16-lab-handbook-design.md` (revision 2, approved 2026-11-17; its spans, sections 4.1 and 4.7 and step A are superseded by D-0197) and `docs/superpowers/specs/2026-11-17-numbers-under-ruled-changes-design.md` (approved 2026-11-18; section 4 is T1). Executors read both and the entries D-0188, D-0190 to D-0192 and D-0195 to D-0201 in `DECISIONS.md`.
**Base:** `main` at the commit that lands this plan (a squash of branch `lab-handbook-spec`, 2026-11-19, on `037da53`; the capstone handout and Lab 3 are unchanged since `bff3394`). Each task branches from `main`. If `curriculum/ph211/ph211-capstone-handout.md` or `curriculum/ph211/ph211-uncertainty-handout.md` differs from `bff3394` when a task starts (`git diff bff3394 -- <file>` not empty), stop and report: T3 and T4 copy lines by number.
**Verify (full, Git Bash, from the repo root):**

```bash
export QUARTO="/c/Program Files/Quarto/bin/quarto.exe"
export PANDOC="/c/Program Files/Quarto/bin/tools/pandoc.exe"
export CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
export PDFTOTEXT="$LOCALAPPDATA/Microsoft/WinGet/Packages/oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe/poppler-25.07.0/Library/bin/pdftotext.exe"
files=$(for f in $(git ls-files '*.md'); do [ "$(head -1 "$f")" = "---" ] && sed -n '2,/^---$/p' "$f" | grep -q '^source_file:' && echo "$f"; done)
python tools/check_em_dash.py && python tools/check_unchanged.py $files && python tools/check_numbers.py $files && python tools/quarto_build.py && python -m unittest discover -s tests -v
```

`git ls-files` lists tracked files only: `git add` a new source file before running it. After T1, both checks print one `skip ... (ruled-change: its own Markdown is the baseline, D-0195)` line per `ruled-change` file.

## Global constraints

- Never loosen a check for a change to a `converted` file; a `converted` file is checked exactly as before, with its declarations (CLAUDE.md, D-0168, D-0195 (2)).
- A `ruled-change` file keeps `source_file` and `source_sha256` as provenance and carries no `ruled_omissions`, `ruled_additions` or `ruled_equations` (D-0195 (3), D-0197; asserted by T1's `test_no_ruled_change_file_keeps_a_list`, D-0200).
- The skip message, exactly: `skip <path> (ruled-change: its own Markdown is the baseline, D-0195)`.
- The seven addresses, exactly: `plot-elements`, `linearization`, `what-is-uncertainty`, `sources-of-uncertainty`, `predictions-hypotheses-models`, `graphical-analysis-tips`, `variables-and-parameters` (D-0190).
- A handout links to the handbook as `[text](ph21x-lab-handbook#<identifier>)`; every output but the Markdown download points at `render.LIBRARY_URL + "labs/ph21x-lab-handbook/modern/#<identifier>"` (D-0190).
- Handbook opening line, exactly: `Every lab after the first uses the ideas on this page. Read it before you start a lab, and come back whenever a lab asks for a plot, a fit or an uncertainty.` (D-0188, approved 2026-11-17).
- Lab 3 lead-in, exactly: `Read the Lab Handbook. It holds the key information from previous labs:` (D-0192, approved 2026-11-17).
- No bold on either new line (D-0192). No em dash in any `ruled-change` file (`tools/check_em_dash.py` after T1; measured 2026-11-18: Lab 3 and the copied appendix lines hold none).
- Commit subjects 72 characters or fewer, the why in the body, the ruling cited; identity `hunterthelabguy` with the noreply email; no trailer (CLAUDE.md).
- Nothing from the instructor repo enters this repo (CLAUDE.md, Conventions).

## PRs

Each a PR with green verify, squash-merged one at a time, main's run read after each (CLAUDE.md). No PR opens while D-0198 is `proposed`: the plan builds on it, and only the owner promotes it. Promoted 2026-11-19.

1. **Re-baselining (D-0195's build):** T1. D-0196's gate does not fire: PR #89 cut "How this site works" to a short page with no paragraph on the checks and merged on 2026-11-19 as `037da53` (main's run 44632177219, verify and deploy green), so this PR adds no public wording. Two ruled content fixes wait on this PR merging: PH 212 Lab 3's rename (D-0182) and Labs 5 and 6's bracket and hint (D-0183, whose new equation the Word checks cannot declare), so it goes first.
2. **Links by id:** T2. Independent of PR 1.
3. **The handbook:** T3, after PRs 1 and 2.
4. **Lab 3 cut:** T4, opened only after PR 3 is live on production (spec 4.4). Production deploys need main's run green; main's run 44414519194 for `bff3394` passed verify and deploy (2026-11-18; the failure on 2026-11-16, run 43979536449, was the artifact upload), and run 44597041464 for `364ae73` passed (2026-11-19). If main's deploy is failing when PR 3 merges, PR 4 waits.

Outside this plan: the Lab 3 instructor-notes line (D-0192 (5)), by its own PR and ruling in the instructor repo.

## Files

| File | Responsibility | Tasks |
|---|---|---|
| `tools/check_unchanged.py` | `rebaselined()`, `SKIP`; `main` skips `ruled-change`; docstring | T1 |
| `tools/check_numbers.py` | `main` skips `ruled-change`; docstring | T1 |
| `tools/check_em_dash.py` | Scan `ruled-change` files as published | T1 |
| `tests/test_check_unchanged.py`, `tests/test_check_numbers.py` | Skip tests | T1 |
| `tests/test_question_ids.py` | Em-dash scan of a `ruled-change` file; the pin on a reordered `ruled-change` file | T1 |
| `.github/workflows/verify.yml` | Two step comments | T1 |
| `tools/media.py`, `tests/test_downloads.py` (`MediaDownloads`) | A declared image's hash stops the build (D-0198 (4)) | T1 |
| `site/landing.md` | The "How this site works" card (D-0198 (5)) | T1 |
| `curriculum/ph211/ph211-describing-an-experiment-handout.md` | Drop D-0169's lists | T1 |
| `curriculum/ph212/ph212-data-analysis-handout.md` | Drop D-0184's lists (D-0200) | T1 |
| `CLAUDE.md`, `docs/conversion-spec.md` | The rule's words; D-0191's exception | T1 |
| `tools/filters/media.lua` | Rewrite `<id>#<identifier>` links | T2 |
| `tests/test_lab_handbook.py` (new) | Link rewrite, link validation, the seven addresses | T2, T3 |
| `curriculum/ph21x/ph21x-lab-handbook.md` (new) | The handbook | T3 |
| `curriculum/ph21x/ph21x-lab-handbook-media/` (new) | Its two icons, Lab 7's bytes | T3 |
| `tests/question-ids.json` | The handbook's empty pin | T3 |
| `tests/test_downloads.py` | The handbook's HTML cap; Lab 3's Word and HTML links | T3, T4 |
| `tests/test_quarto_site.py` | Built handbook addresses and heading; Lab 3's page links | T3, T4 |
| `curriculum/ph211/ph211-uncertainty-handout.md` | The Lab 3 cut | T4 |

---

### T1: Re-baselining: the Word checks skip a ruled-change file (D-0195)

**Depends on:** none
**Files:** modify `tools/check_unchanged.py` (docstring lines 63 to 75; after `FROM`, line 112; `main`), `tools/check_numbers.py` (docstring; imports; `main`), `tools/check_em_dash.py` (docstring lines 7 to 10; imports; `scan`), `.github/workflows/verify.yml` (comments at lines 35 to 36 and 50 to 52), `tools/media.py` (`build`, the images loop), `site/landing.md` (lines 25 to 26); test `tests/test_downloads.py` (class `MediaDownloads`), `tests/test_check_unchanged.py` (new class at the end, before any `if __name__` guard), `tests/test_check_numbers.py` (likewise), `tests/test_question_ids.py` (classes `Pin` and `EmDashScan`); modify `curriculum/ph211/ph211-describing-an-experiment-handout.md` (front matter lines 12 to 66), `curriculum/ph212/ph212-data-analysis-handout.md` (front matter lines 12 to 21), `CLAUDE.md` (Conventions, "Conversion first" bullet; Build, "One Markdown source" bullet), `docs/conversion-spec.md` (template line 21; "Content-unchanged check" section)
**Seams:** `check_unchanged.main(paths)` and `check_numbers.main(paths)` return an exit code and print a line per file; `check_unchanged.rebaselined(path) -> bool`; `check_em_dash.scan(root, paths)` returns offending relative paths.
**Interfaces:** produces `rebaselined(path)` and `SKIP` (a format string taking the path) in `tools/check_unchanged.py`, imported by the other two tools.
**Verify:** with the full Verify's exports, and after `python tools/quarto_build.py` has run once in this tree (`MediaDownloads`' `setUpModule` stops without `build/quarto-site`), `python -m unittest tests.test_check_unchanged tests.test_check_numbers tests.test_question_ids tests.test_downloads.MediaDownloads -v`, then the full Verify.

- [ ] Write the failing tests. At the end of `tests/test_check_unchanged.py`, before any `if __name__` guard (add `import contextlib` and `import io` to its imports):

```python
class Rebaselined(unittest.TestCase):
    """D-0195: from a handout's first ruled change, the Word checks skip it."""

    def lab(self, d, status):
        md = Path(d) / "lab.md"
        md.write_text('---\nsource_file: "missing.docx"\nstatus: ' + status
                      + '\n---\n\nWords.\n', encoding="utf-8", newline="\n")
        return md

    def run_main(self, md):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = check_unchanged.main([str(md)])
        return code, out.getvalue()

    def test_ruled_change_is_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            md = self.lab(d, "ruled-change")
            code, out = self.run_main(md)
        self.assertEqual(code, 0)
        self.assertEqual(out, check_unchanged.SKIP.format(md) + "\n")

    def test_converted_is_still_checked(self):
        # The original is missing, so a file that is checked fails to read it.
        with tempfile.TemporaryDirectory() as d, self.assertRaises((OSError, SystemExit)):
            self.run_main(self.lab(d, "converted"))

    def test_status_forms(self):
        with tempfile.TemporaryDirectory() as d:
            for status, want in (('"ruled-change"', True), ("ruled-change   # D-0195", True),
                                 ("converted", False), ("checked", False)):
                with self.subTest(status=status):
                    self.assertEqual(check_unchanged.rebaselined(self.lab(d, status)), want)
            plain = Path(d) / "plain.md"
            plain.write_text("No front matter.\nstatus: ruled-change\n", encoding="utf-8")
            self.assertFalse(check_unchanged.rebaselined(plain))

    # D-0198 (3): every re-baselined file, with the ruling that changed it
    # first. Setting `status: ruled-change` switches both Word checks off, so
    # it edits this list in the same diff.
    REBASELINED = {
        "curriculum/ph211/ph211-describing-an-experiment-handout.md": "D-0169",
        "curriculum/ph212/ph212-data-analysis-handout.md": "D-0184",
    }

    def test_rebaselined_files_are_pinned(self):
        found = {p.relative_to(ROOT).as_posix() for p in sorted((ROOT / "curriculum").rglob("*.md"))
                 if check_unchanged.rebaselined(p)}
        self.assertEqual(found, set(self.REBASELINED))

    LISTS = ("ruled_omissions:", "ruled_additions:", "ruled_equations:")

    def test_no_ruled_change_file_keeps_a_list(self):
        # D-0195 (3), D-0200: a ruled change keeps no front-matter list of
        # changed passages; nothing reads one once the Word checks skip it.
        kept = []
        for path in self.REBASELINED:
            lines = (ROOT / path).read_text(encoding="utf-8").split("\n")
            front = lines[1:lines.index("---", 1)]
            kept += [(path, line) for line in front if line.startswith(self.LISTS)]
        self.assertEqual(kept, [])
```

In class `MediaDownloads` of `tests/test_downloads.py`, after `test_a_changed_file_stops_the_build`:

```python
    def test_a_changed_image_stops_the_build(self):
        # D-0198 (4): a picture's bytes are pinned too, since the word check
        # that compared pictures skips a ruled-change file.
        images = [dict(self.doc["meta"]["images"][0], sha256="0" * 64)]
        doc = dict(self.doc, meta=dict(self.doc["meta"], images=images))
        with tempfile.TemporaryDirectory() as out, self.assertRaises(SystemExit):
            media.build(doc, out, downloads.CHROME)
```

At the end of `tests/test_check_numbers.py`, likewise (add `import contextlib` and `import io`):

```python
class Rebaselined(unittest.TestCase):
    """D-0195: the number check skips a ruled-change file too."""

    def test_ruled_change_is_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "lab.md"
            md.write_text('---\nsource_file: "missing.docx"\nstatus: ruled-change\n---\n\n'
                          '::: question\nWords.\n:::\n', encoding="utf-8", newline="\n")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = check_numbers.main([str(md)])
        self.assertEqual(code, 0)
        self.assertIn("ruled-change: its own Markdown is the baseline, D-0195", out.getvalue())
```

In `tests/test_question_ids.py` (it already holds D-0103's scan test, and `verify.yml` points readers there), add to its imports `import check_unchanged  # noqa: E402` after `import check_em_dash`, and add to class `EmDashScan`:

```python
    def test_ruled_change_is_scanned(self):
        # D-0195: a ruled-change file is the site's own wording.
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "curriculum").mkdir()
            (root / "curriculum" / "lab.md").write_text(
                '---\nsource_file: "originals/x.docx"\nstatus: ruled-change\n---\n\n'
                'new words—here\n', encoding="utf-8")
            found = check_em_dash.scan(str(root), ("curriculum",))
        self.assertEqual(found, ["curriculum/lab.md"])
```

and to class `Pin`, after `test_reordering_a_question_fails_the_pin`:

```python
    def test_reordering_a_ruled_change_file_fails_the_pin(self):
        # D-0195: re-baselining skips the Word checks, never the pin.
        text = PH211.read_text(encoding="utf-8")
        self.assertIn("\nstatus: converted\n", text)
        text = text.replace("\nstatus: converted\n", "\nstatus: ruled-change\n", 1)
        a = text.index("::: {.question #ph211-team-building:good-lab-partner}")
        b = text.index("::: {.question #ph211-team-building:sketches}")
        end = text.index(":::\n", b) + 4
        first_end = text.index(":::\n", a) + 4
        swapped = text[:a] + text[b:end] + text[first_end:b] + text[a:first_end] + text[end:]
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / "lab.md"
            md.write_text(swapped, encoding="utf-8", newline="\n")
            self.assertTrue(check_unchanged.rebaselined(md))
            lab, ids = read(md)
        self.assertEqual(sorted(ids), sorted(PIN[lab]))
        self.assertNotEqual(ids, PIN[lab])
```

- [ ] Build once if this tree has no `build/quarto-site`: `python tools/quarto_build.py` (pass 3: on a fresh tree `MediaDownloads` otherwise errors in `setUpModule`, and neither this red step nor the green one below shows its result).
- [ ] Run it; expected failure: `check_unchanged`'s `test_ruled_change_is_skipped` errors with `FileNotFoundError` on `missing.docx` (the file is checked, not skipped) and `test_status_forms` with `AttributeError` (no `rebaselined`); the number check's test raises reading `missing.docx`; `test_ruled_change_is_scanned` gets `[]`; the new pin test and `test_rebaselined_files_are_pinned` error with `AttributeError` (no `rebaselined`); `test_a_changed_image_stops_the_build` fails with `SystemExit not raised`. `test_converted_is_still_checked` passes before and after: it is a guard, not a red test.
- [ ] Implement. In `tools/check_unchanged.py`, after the `FROM = ...` line (112):

```python
SKIP = "skip {} (ruled-change: its own Markdown is the baseline, D-0195)"


def rebaselined(path):
    """True when a file's front matter sets `status: ruled-change`. From a
    handout's first ruled change its own Markdown is the baseline, and the
    Word checks skip it (D-0195)."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().split("\n")
    if lines[0].rstrip("\r") != "---":
        return False
    for line in lines[1:]:
        line = line.rstrip("\r")
        if line == "---":
            return False
        if line.startswith("status:"):
            value = line.split(":", 1)[1].split("#", 1)[0].strip().strip("\"'")
            return value == "ruled-change"
    return False
```

In `check_unchanged.main`, make the loop's first lines:

```python
    for p in paths:
        if rebaselined(p):
            print(SKIP.format(p))
            continue
```

In `tools/check_numbers.py`, after `import zipfile` add `from check_unchanged import SKIP, rebaselined  # noqa: E402  (D-0195)`, and make `main`'s loop open the same way. In `tools/check_em_dash.py`, after `import sys` add `from check_unchanged import rebaselined  # D-0195`; in `scan` replace

```python
        if path.endswith(".md") and converted(path):
            continue
```

with

```python
        if path.endswith(".md") and converted(path) and not rebaselined(path):
            continue
```

and in its docstring replace "is skipped: it keeps every em dash its original holds, and the word check proves its words are the original's (D-0103)." with "is skipped unless its status is `ruled-change`: it keeps every em dash its original holds, and the word check proves its words are the original's (D-0103). A `ruled-change` file is the site's own wording and is scanned (D-0195)." (The old text spans three docstring lines: replace it with whitespace normalised and rewrap the paragraph to its own widest line before the edit.)

In `tools/media.py`'s `build`, make the images loop check each picture's bytes as the files loop does (D-0198 (4)):

```python
    for e in media["images"]:
        src = os.path.join(source_dir, e["file"])
        with open(src, "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
        if digest != e.get("sha256"):
            raise SystemExit("{}: {} has sha256 {}, front matter says {}".format(
                doc["path"], e["file"], digest, e.get("sha256")))
        name = os.path.basename(e["file"])
        shutil.copyfile(src, os.path.join(dest, name))
        published.append(name)
```

and above the images loop add the comment `# A picture's bytes are pinned the same way (D-0198 (4)): the word check that compares pictures skips a ruled-change file.` (Measured 2026-11-18: all 41 declared images match their front matter.)

Amend the usage text the tools and CI print. In `tools/check_unchanged.py`'s docstring, before "Differences are allowed only when declared in front matter and ruled in a ledger:" add the paragraph "A file whose `status` is `ruled-change` is skipped with a printed reason: from a handout's first ruled change its own Markdown is the baseline (D-0195). The declarations below are for conversions only." In `tools/check_numbers.py`'s docstring, before "Exit code 0 when every file passes." add "A file whose `status` is `ruled-change` is skipped with a printed reason (D-0195)." In `.github/workflows/verify.yml`, change the em-dash step's comment "a converted file keeps its original's (D-0103)." to "a converted file keeps its original's (D-0103); a ruled-change file is scanned (D-0195).", and the "Content unchanged" step's "The word check, then Word's labels (D-0102, D-0112)." to "The word check, then Word's labels (D-0102, D-0112); both skip a ruled-change file (D-0195)." Rewrap each comment to its block's width.
- [ ] Run it; expected: pass, except `test_no_ruled_change_file_keeps_a_list`, which fails listing the five list keys of the two files until the next step.
- [ ] Drop D-0169's lists, unconditionally (D-0198 (1)), and D-0184's (D-0200). Run, from the repo root:

```python
from pathlib import Path

p = Path("curriculum/ph211/ph211-describing-an-experiment-handout.md")
lines = p.read_text(encoding="utf-8").split("\n")
assert lines[10] == "status: ruled-change", lines[10]
first = lines.index("ruled_omissions:")
stop = lines.index("images:")
assert first == 11 and lines[40] == "ruled_additions:" and stop == 66, (first, stop)
p.write_text("\n".join(lines[:first] + lines[stop:]), encoding="utf-8", newline="\n")

p = Path("curriculum/ph212/ph212-data-analysis-handout.md")
lines = p.read_text(encoding="utf-8").split("\n")
assert lines[10] == "status: ruled-change", lines[10]
assert (lines[11], lines[14], lines[17], lines[21]) == (
    "ruled_omissions:", "ruled_additions:", "ruled_equations:", "---"), lines[11:22]
p.write_text("\n".join(lines[:11] + lines[21:]), encoding="utf-8", newline="\n")
```

Then run `python -m unittest tests.test_check_unchanged.Rebaselined -v`; expected: pass.

- [ ] Amend the words. In `site/landing.md`, replace the two lines

```markdown
  How a page is built, how it is checked against the original, and who
  did the work.
```

with `  How a page is built and who did the work.` (D-0198 (5), approved 2026-11-18). In `CLAUDE.md`, replace the bullet that begins "Conversion first, then ruled changes (D-0168)." and ends "Never loosen the check for a change." with:

```markdown
- Conversion first, then ruled changes (D-0168, D-0195). A handout's
  conversion is format only, proven by the content-unchanged check
  (docs/conversion-spec.md), and lands on its own. A wording change comes
  after, never folded into a conversion. The first ruled change sets
  `status: ruled-change`; from then on the handout's own Markdown is the
  baseline, and both Word checks skip it and print why. Each change is
  reviewed in its PR's diff, its commit cites the ruling, and the ruling,
  in the instructor repo's ledger, records who drafted the words and who
  approved them. A ruled change keeps no front-matter list of changed
  passages. Never loosen a check for a change to a `converted` file.
```

In the Build bullet that begins "One Markdown source feeds one presentation", after "never copy content into a second file" insert " (one exception, until PH 211 Labs 3 to 7's appendix copies are cut: the Lab Handbook's sections, D-0191, which change only after those cuts, D-0201)". Match both by a script that normalises whitespace; assert each matches once; rewrap both changed bullets to 76 characters, the file's prose width (the "One Markdown source" bullet already holds a 111-character line, which is not the width to copy), never breaking "PH 211" or "D-0201" across lines. The paragraph added to `docs/conversion-spec.md` below is already wrapped at 75: add it as given.

In `docs/conversion-spec.md`, change the template's line 21 comment to `# converted | checked | ruled-change (the Word checks skip ruled-change, D-0195)`, and after the "Content-unchanged check" section's first paragraph (ending "(ledger 20).") add the paragraph:

```markdown
A file whose `status` is `ruled-change` is skipped, with a printed reason:
from a handout's first ruled change its own Markdown is the baseline
(D-0195). Its changes are reviewed in the PR diff and cite their ruling in
the instructor repo; the declarations above are for conversions only.
```

- [ ] Run the full Verify; expected: pass, with one `skip` line from each check for `ph211-describing-an-experiment-handout.md` and one for `ph212-data-analysis-handout.md`.
- [ ] Commit: `Re-baseline a handout at its first ruled change (D-0195)` (body: the skip and why it prints; the pinned set; the em-dash scan; image hashes; D-0169's and D-0184's lists dropped and none allowed back (D-0200); the CLAUDE.md, conversion-spec and landing words; D-0191's exception; D-0198).

### T2: Links to a converted document by id, rewritten and validated

**Depends on:** none
**Files:** modify `tools/filters/media.lua` (comment lines 28 to 30; `Link` 129 to 135); test `tests/test_lab_handbook.py` (new)
**Seams:** the filter's output through Pandoc (`html` and `docx`); `bad_links(sources)` in the test module.
**Interfaces:** produces the link form `[text](<id>#<identifier>)` and, in `tests/test_lab_handbook.py`, `sources(docs=None) -> dict[str, Path]` (from `render.converted_documents()`, no third copy of that walk), `bad_links(sources) -> list[tuple[str, str]]`, `ADDRESSES` and `HANDBOOK`, which T3 and T4 reuse.
**Verify:** with the full Verify's exports (the build in the green step needs `CHROME`, `test_downloads` needs `PDFTOTEXT`), `python -m unittest tests.test_lab_handbook -v`

- [ ] Write the failing tests, `tests/test_lab_handbook.py`:

```python
"""The Lab Handbook (D-0188, D-0190): links to a converted document by id,
and the handbook's fixed section addresses."""

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import render  # noqa: E402

PANDOC = os.environ.get("PANDOC", "pandoc")
MEDIA = ROOT / "tools" / "filters" / "media.lua"
HANDBOOK = "ph21x-lab-handbook"
ADDRESSES = ["plot-elements", "linearization", "what-is-uncertainty", "sources-of-uncertainty",
             "predictions-hypotheses-models", "graphical-analysis-tips", "variables-and-parameters"]
# media.lua's own pattern, `^([%w%-]+)#([%w%-_]+)$`, so every link it
# rewrites is one this test validates, whatever its case, title or brackets.
DOC_LINK = re.compile(r"^([A-Za-z0-9-]+)#([A-Za-z0-9_-]+)$")
DOC_TARGET = re.compile(r"^[A-Za-z0-9-]+#")   # an `<id>#...` target; a path form
# (`a.md#x`, `a/#x`) is neither rewritten nor checked, and no source has one (pass 4).


def sources(docs=None):
    """{id: path} of every converted document (render.converted_documents())."""
    docs = render.converted_documents() if docs is None else docs
    return {i: Path(d["path"]) for i, d in docs.items()}


def parsed(path):
    """(link targets, explicit identifiers) in a source. Generated heading
    identifiers are off: spec 4.4 links only to explicit ones."""
    doc = json.loads(subprocess.run([PANDOC, str(path), "-f", render.FROM + "-auto_identifiers", "-t", "json"],
                                    capture_output=True, check=True, encoding="utf-8").stdout)
    targets, idents = [], set()

    def walk(node):
        if isinstance(node, list):
            for n in node:
                walk(n)
        elif isinstance(node, dict):
            if node.get("t") == "Link":
                targets.append(node["c"][2][0])
            elif node.get("t") in ("Header", "Div", "Span"):
                attr = node["c"][1] if node["t"] == "Header" else node["c"][0]
                if attr[0]:
                    idents.add(attr[0])
            walk(node.get("c"))

    walk(doc["blocks"])
    return targets, idents


def bad_links(sources):
    """(id, target) of each `<id>#<identifier>` link whose id is no such
    document or whose identifier is not one on that document."""
    read = {i: parsed(p) for i, p in sources.items()}
    bad = []
    for doc_id, (targets, _) in read.items():
        for target in targets:
            if not DOC_TARGET.match(target):
                continue
            # A fragment media.lua cannot rewrite (a colon, a dot) would ship
            # as a relative link that 404s (pass 3): bad, as D-0190 (3) says.
            m = DOC_LINK.match(target)
            if not m or m.group(1) not in read or m.group(2) not in read[m.group(1)][1]:
                bad.append((doc_id, target))
    return bad


class Links(unittest.TestCase):
    TEXT = "[Linearization](ph21x-lab-handbook#linearization) and [here](#local).\n"
    URL = render.LIBRARY_URL + "labs/ph21x-lab-handbook/modern/#linearization"

    def run_filter(self, to, out=None):
        args = [PANDOC, "-f", render.FROM, "--lua-filter", str(MEDIA),
                "-M", "library-url=" + render.LIBRARY_URL]
        args += ["-o", str(out)] if out else ["-t", to]
        return subprocess.run(args, input=self.TEXT, capture_output=True, encoding="utf-8")

    def test_page_link_points_at_the_library(self):
        page = self.run_filter("html").stdout
        self.assertIn('href="' + self.URL + '"', page)
        self.assertIn('href="#local"', page)

    def test_word_link_points_at_the_library(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "links.docx"
            self.assertEqual(self.run_filter("docx", out).returncode, 0)
            with zipfile.ZipFile(out) as z:
                rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
        self.assertIn('Target="' + self.URL + '"', rels)

    def test_every_document_link_resolves(self):
        self.assertEqual(bad_links(sources()), [])

    def test_bad_links_are_found(self):
        # Every form media.lua rewrites (pass 2, probes/link_forms.py): plain,
        # titled, angle-bracketed, upper case.
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "a.md", Path(d) / "b.md"
            a.write_text("## Heading {#x}\n\n## Plain Heading\n", encoding="utf-8")
            b.write_text('[ok](a#x) [no](a#y) [none](c#x) [titled](a#z "T")'
                         " [angle](<a#w>) [upper](A#x) [local](#x)"
                         " [colon](a#a:q1) [dot](a#x.y) [web](https://e.org/a#x) [auto](a#plain-heading)\n", encoding="utf-8")
            found = bad_links(sources({"a": {"path": a}, "b": {"path": b}}))
        self.assertEqual(sorted(found),
                         [("b", "A#x"), ("b", "a#a:q1"), ("b", "a#plain-heading"), ("b", "a#w"), ("b", "a#x.y"),
                          ("b", "a#y"), ("b", "a#z"), ("b", "c#x")])
```

- [ ] Run it; expected failure: the two filter tests find `href="ph21x-lab-handbook#linearization"` unchanged; the other two pass.
- [ ] Implement. In `tools/filters/media.lua` replace the `Link` function with:

```lua
    Link = function(el)
      local id = el.target:match("^([%w%-]+)%-media/[^/]+$")
      if id then
        if not url then error("media.lua: a link to a lab's file needs library-url: " .. el.target) end
        el.target = url .. "labs/" .. id .. "/" .. el.target
        return el
      end
      local doc, ident = el.target:match("^([%w%-]+)#([%w%-_]+)$")
      if doc then
        if not url then error("media.lua: a link to a document needs library-url: " .. el.target) end
        el.target = url .. "labs/" .. doc .. "/modern/#" .. ident
        return el
      end
    end,
```

and after the comment paragraph on a lab's own file (line 30) add, with a bare `--` line between the two paragraphs:

```lua
--
-- A link to another converted document's section, `<id>#<identifier>`
-- (D-0190), points at that page under `library-url` the same way. Its
-- identifier is written on the target's heading; tests/test_lab_handbook.py
-- fails on a link to an unknown document or identifier.
```

- [ ] Run it; expected: pass. Then, with the full Verify's exports (with `PANDOC` alone the build deletes `build/quarto-site` and then stops for want of `CHROME`), run `python tools/quarto_build.py` and `python -m unittest tests.test_downloads tests.test_quarto_site`; expected: pass (no current source has such a link).
- [ ] Commit: `Links to a document by id point at the library's page` (body: D-0190; `media.lua` runs at `pre-ast`, so Quarto never sees the source form; the Markdown download keeps the source form by design).

### T3: The Lab Handbook

**Depends on:** T1, T2
**Files:** create `curriculum/ph21x/ph21x-lab-handbook.md`, `curriculum/ph21x/ph21x-lab-handbook-media/graphical-analysis-view-icon.png`, `curriculum/ph21x/ph21x-lab-handbook-media/graphical-analysis-graph-tools-icon.png`; modify `tests/question-ids.json` (last entry), `tests/test_check_unchanged.py` (`REBASELINED`), `tests/test_downloads.py` (`HTML_CAPS`), `tests/test_quarto_site.py` (import after line 22; new class), `tests/test_lab_handbook.py` (new class)
**Seams:** the source file; the built page `build/quarto-site/labs/ph21x-lab-handbook/modern/index.html`.
**Interfaces:** consumes `rebaselined` behaviour (T1), `sources()`, `ADDRESSES`, `HANDBOOK` (T2).
**Verify:** the full Verify above.

- [ ] Write the failing test. At the end of `tests/test_lab_handbook.py`, before any `if __name__` guard:

```python
class Addresses(unittest.TestCase):

    def test_seven_fixed_addresses(self):
        source = sources()[HANDBOOK].read_text(encoding="utf-8")
        found = re.findall(r"^## .*\{#([A-Za-z0-9_-]+)\}$", source, re.M)
        self.assertEqual(found, ADDRESSES)
```

No test holds the handbook to Lab 7 (D-0201 (1)): it is `ruled-change`, so each later edit is reviewed in its PR diff (D-0195), and until PH 211's appendix cuts land it changes only as below (D-0201 (3)).

- [ ] Run it; expected failure: `KeyError: 'ph21x-lab-handbook'`.
- [ ] Create the files. Copy the two icons byte for byte:

```bash
mkdir -p curriculum/ph21x/ph21x-lab-handbook-media
cp curriculum/ph211/ph211-capstone-handout-media/graphical-analysis-view-icon.png curriculum/ph211/ph211-capstone-handout-media/graphical-analysis-graph-tools-icon.png curriculum/ph21x/ph21x-lab-handbook-media/
```

Then write the handbook with this script, kept outside the repo in a scratch folder and run from the repo root (`python -X utf8 "$TMP/make_handbook.py"`). Every line of the body is the capstone handout's, which the word check proves against Word while that file is `converted`; `handbook_body()` asserts each line it changes. The script is used once and not committed (D-0201 (1)).

```python
from pathlib import Path

LAB7 = Path("curriculum/ph211/ph211-capstone-handout.md")
OPENING = ("Every lab after the first uses the ideas on this page. Read it before you start a lab,"
           " and come back whenever a lab asks for a plot, a fit or an uncertainty.")
ITEMS = [("Required Plot Elements", "plot-elements"), ("Linearization", "linearization"),
         ("What is Uncertainty?", "what-is-uncertainty"),
         ("Sources of Uncertainty", "sources-of-uncertainty"),
         ("Predictions, Hypotheses, and Models", "predictions-hypotheses-models"),
         ("Tips for Using Graphical Analysis", "graphical-analysis-tips"),
         ("Variables and Parameters", "variables-and-parameters")]
SWAPS = {
    "#### Required Plot Elements": "## Required Plot Elements {#plot-elements}",
    "#### Linearization": "## Linearization {#linearization}",
    "#### What is Uncertainty?": "## What is Uncertainty? {#what-is-uncertainty}",
    "#### Sources of Uncertainty:": "## Sources of Uncertainty: {#sources-of-uncertainty}",
    "**[Predictions, Hypotheses, and Models]{.underline}**":
        "## Predictions, Hypotheses, and Models {#predictions-hypotheses-models}",
    "#### Tips for Using Graphical Analysis:":
        "## Tips for Using Graphical Analysis: {#graphical-analysis-tips}",
    "#### Variables and Parameters": "## Variables and Parameters {#variables-and-parameters}",
}


def handbook_body():
    """The handbook's body: Lab 7's Appendix B (its lines from the heading
    to the end) with D-0188's and D-0197's changes, nothing else."""
    lines = LAB7.read_text(encoding="utf-8").split("\n")
    assert lines[-1] == "", "Lab 7 must end with a newline"
    body = lines[lines.index("## Appendix B – Reference Information"):-1]
    assert body[2] == "This section contains key information from previous labs:", body[2]
    assert body[4:11] == ["{}.  {}".format(n, t) for n, (t, _) in enumerate(ITEMS, 1)], body[4:11]
    body[0] = "# Lab Handbook"
    body[2] = OPENING
    body[4:11] = ["{}.  [{}](#{})".format(n, t, a) for n, (t, a) in enumerate(ITEMS, 1)]
    for old, new in SWAPS.items():
        assert body.count(old) == 1, old
        body[body.index(old)] = new
    text = "\n".join(body).replace("ph211-capstone-handout-media/", "ph21x-lab-handbook-media/")
    assert text.count("ph21x-lab-handbook-media/") == 2
    return text


FRONT = """---
id: ph21x-lab-handbook
title: "Lab Handbook"
course: PH21X
audience: student
visibility: public
layer: curriculum
source_file: "originals/PH211/Lab 7 - Capstone - Handout.docx"
source_sha256: "b8f38b5a04e1a01304f7ec7b71e7e54c2e13e46af80f5fe91f58cf76c8722ea6"
status: ruled-change
images:
  - file: "ph21x-lab-handbook-media/graphical-analysis-view-icon.png"
    source_part: "word/media/image1.png"
    sha256: "7a85a2239d2a80de52693e4df786a1a22c14eff78027951153a8b42bdf2c941a"
  - file: "ph21x-lab-handbook-media/graphical-analysis-graph-tools-icon.png"
    source_part: "word/media/image2.png"
    sha256: "36df8e6bdf281576cc60c1e819bfc8b499fad38ed8027eaee5ca5e8dc9a32b4f"
---

"""
lines = Path("curriculum/ph211/ph211-capstone-handout.md").read_text(encoding="utf-8").split("\n")
assert len(lines) == 379 and lines[283] == "## Appendix B – Reference Information", \
    "capstone handout changed since bff3394"
Path("curriculum/ph21x/ph21x-lab-handbook.md").write_text(FRONT + handbook_body() + "\n",
                                                          encoding="utf-8", newline="\n")
```

What changes from Lab 7's lines, all ruled in D-0188 and D-0197: the title and heading "Lab Handbook"; the opening line in place of the lead-in; the seven list items as links; the sections as `##` headings with the seven addresses, "Predictions, Hypotheses, and Models" (a bold underlined paragraph in Lab 7) among them (WCAG 1.3.1: a real heading a screen reader can reach); and the two icons' paths, `ph211-capstone-handout-media/` to `ph21x-lab-handbook-media/` (the page's own media folder, not a wording change). Every other word is Lab 7's.
- [ ] `git add curriculum/ph21x`. Run `python tools/check_unchanged.py curriculum/ph21x/ph21x-lab-handbook.md` and `python tools/check_numbers.py curriculum/ph21x/ph21x-lab-handbook.md`; expected: the `skip` line from each. Write the two sides to files outside the repo and diff them (Git for Windows cannot read process substitution): `sed -n 284,378p curriculum/ph211/ph211-capstone-handout.md > "$TMP/lab7.md"`, `sed -n '/^# Lab Handbook$/,$p' curriculum/ph21x/ph21x-lab-handbook.md > "$TMP/handbook.md"`, `git diff --no-index --word-diff "$TMP/lab7.md" "$TMP/handbook.md"`, where `$TMP` is a scratch folder. Paste its output in the PR body: it must show only the changes listed above.
- [ ] Pin it as re-baselined (D-0198 (3)): add `"curriculum/ph21x/ph21x-lab-handbook.md": "D-0197",` to `REBASELINED` in `tests/test_check_unchanged.py`, keeping the dict sorted by path.
- [ ] Add the empty pin, keeping the file sorted by id: in `tests/question-ids.json` change the last entry to

```json
  "ph21x-lab-handbook": [],
  "ph21x-problem-solving-strategy": []
```

keeping the file's closing brace.
- [ ] Build: `python tools/quarto_build.py`. Measure `wc -c < build/quarto-site/labs/ph21x-lab-handbook/ph21x-lab-handbook.html`. Add to `HTML_CAPS` in `tests/test_downloads.py`, just before the `"ph21x-problem-solving-strategy"` entry (alphabetical within PH 21X), `"ph21x-lab-handbook": <cap>,  # <measured> bytes, D-0188`, where `<cap>` is the measured size times 1.10 rounded up to the next 10,000, written as the file's other caps are (`190_000`), as the comment above `HTML_CAPS` says (pass 2 measured 169,306 bytes for this revision: cap `190_000`).
- [ ] Add the built checks to `tests/test_quarto_site.py`: after its line `import render` (line 22) add `import test_lab_handbook                 # noqa: E402  (ADDRESSES)`, and after the class holding `test_course_index_links_course_wide_documents`:

```python
class LabHandbook(unittest.TestCase):
    """D-0188, D-0190: the handbook page and its fixed addresses."""

    ADDRESSES = test_lab_handbook.ADDRESSES   # one list (spec 4.3)

    def page(self):
        return (QSITE / "labs" / "ph21x-lab-handbook" / "modern" / "index.html").read_text(encoding="utf-8")

    def test_addresses_on_its_sections(self):
        found = re.findall(r'<h2[^>]*\bid="([^"]+)"', self.page())
        self.assertEqual(found, self.ADDRESSES)

    def test_titled_lab_handbook_with_contents_links(self):
        page = self.page()
        self.assertRegex(page, r"<h1[^>]*>Lab Handbook</h1>")
        for address in self.ADDRESSES:
            self.assertIn('href="#' + address + '"', page)
```

- [ ] Run the full Verify; expected: pass. The course index lists the handbook under "For every course" by the existing `test_course_index_links_course_wide_documents`.
- [ ] Commit: `The Lab Handbook, from PH 211 Lab 7's Appendix B` (body: D-0188 as amended by D-0197, in this repo's `DECISIONS.md`, ruled before D-0195 moved handout rulings to the instructor repo; the lines copied and what changed; who drafted and who approved the opening line).

### T4: The Lab 3 cut

**Depends on:** T1, T2, T3
**Files:** modify `curriculum/ph211/ph211-uncertainty-handout.md` (front matter line 11; body lines 242 to 284); `tests/test_check_unchanged.py` (`REBASELINED`); `tests/test_quarto_site.py` (class `LabHandbook`); `tests/test_downloads.py` (three new tests in class `MarkdownAndWord`, line 179)
**Seams:** Lab 3's built page, Word download, HTML download and PDF.
**Interfaces:** consumes the handbook's addresses (T3) and the link rewrite (T2).
**Verify:** the full Verify above.

- [ ] Write the failing tests. In `LabHandbook` (`tests/test_quarto_site.py`):

```python
    def test_lab3_links_to_the_handbook(self):
        page = (QSITE / "labs" / "ph211-uncertainty-handout" / "modern" / "index.html").read_text(encoding="utf-8")
        for address in ("plot-elements", "linearization"):
            self.assertIn('href="' + render.LIBRARY_URL + "labs/ph21x-lab-handbook/modern/#"
                          + address + '"', page)
```

In `tests/test_downloads.py`, three tests in class `MarkdownAndWord` (line 179, the class whose method at line 182 returns `QSITE / "labs" / doc_id / (doc_id + ".docx")`):

```python
    def test_lab3_word_links_to_the_handbook(self):
        # D-0190: a saved Word file still reaches the handbook.
        with zipfile.ZipFile(QSITE / "labs" / "ph211-uncertainty-handout"
                             / "ph211-uncertainty-handout.docx") as z:
            rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
        for address in ("plot-elements", "linearization"):
            self.assertIn('Target="' + render.LIBRARY_URL + "labs/ph21x-lab-handbook/modern/#"
                          + address + '"', rels)

    def test_lab3_html_download_links_to_the_handbook(self):
        # D-0190: the HTML download too.
        text = (QSITE / "labs" / "ph211-uncertainty-handout"
                / "ph211-uncertainty-handout.html").read_text(encoding="utf-8")
        for address in ("plot-elements", "linearization"):
            self.assertIn('href="' + render.LIBRARY_URL + "labs/ph21x-lab-handbook/modern/#"
                          + address + '"', text)

    def test_lab3_pdf_links_to_the_handbook(self):
        # D-0190 (2) names the PDF: Chrome writes each link as a /URI action.
        pdf = (QSITE / "labs" / "ph211-uncertainty-handout"
               / "ph211-uncertainty-handout.pdf").read_bytes()
        for address in ("plot-elements", "linearization"):
            self.assertIn((render.LIBRARY_URL + "labs/ph21x-lab-handbook/modern/#"
                           + address).encode("ascii"), pdf)
```

- [ ] Run them after a build; expected failure: no such `href` or `Target`.
- [ ] Implement with this script, from the repo root:

```python
from pathlib import Path

p = Path("curriculum/ph211/ph211-uncertainty-handout.md")
lines = p.read_text(encoding="utf-8").split("\n")
assert len(lines) == 285 and lines[284] == "", "Lab 3 changed since bff3394"
assert lines[10] == "status: converted"
assert lines[241] == "## Appendix – Reference Information"
assert lines[243] == "This section contains key information from previous labs:"
assert lines[245] == '::: {.numbered anchors="o14.0.1 o14.0.2"}'
assert lines[246:249] == ["1.  Required Plot Elements", "2.  Linearization", ":::"]
assert lines[250] == "#### **Required Plot Elements**"
lines[10] = "status: ruled-change"
lines[243] = "Read the Lab Handbook. It holds the key information from previous labs:"
lines[246] = "1.  [Required Plot Elements](ph21x-lab-handbook#plot-elements)"
lines[247] = "2.  [Linearization](ph21x-lab-handbook#linearization)"
lines = lines[:249] + [""]             # drop line 250 on: both sections, to the end
p.write_text("\n".join(lines), encoding="utf-8", newline="\n")
```

The `.numbered` div and its anchors stay: they are inert once the number check skips the file, and keeping them keeps the diff to the ruled lines. `tests/test_headings.py` keeps Lab 3 in `KNOWN_SKIPS`: its skips at lines 29 and 232 remain. The question-id pin is unchanged (no question moves).
- [ ] Pin it as re-baselined (D-0198 (3)): add `"curriculum/ph211/ph211-uncertainty-handout.md": "D-0192",` to `REBASELINED` in `tests/test_check_unchanged.py`, keeping the dict sorted by path.
- [ ] Run the full Verify; expected: pass, with the `skip` line for Lab 3 from each check.
- [ ] In the PR body, ask the owner to look at Lab 3's PDF as part of the trial check (D-0198 (6)): measured in pass 2, the appendix heading and lead-in end page 9 and the two links stand alone on page 10. The plan does not change it.
- [ ] Commit: `PH 211 Lab 3: the appendix's reference sections move to the handbook` (body: D-0192 rows C1 to C3 as amended by D-0197, in this repo's `DECISIONS.md` for the same reason; who drafted and who approved the lead-in; the trial's pass line; that the PR opens only after the handbook is live).

---

## Self-review (revision 2, 2026-11-18)

- **Spec coverage.** Numbering spec section 4 items 1, 3, 4, 5 (CLAUDE.md, conversion-spec, the tools' usage text, `verify.yml`) and 6 to T1, item 6's pin case to `test_reordering_a_ruled_change_file_fails_the_pin` (revision 2.1); item 5's public page to PR 1's D-0196 gate; item 2 is moot (D-0193 withdrawn by D-0197). Handbook spec 4.2 to T3 (one step, D-0197); 4.3 to T2 and T3's address tests; 4.4 to T2 and the PR order; 4.5 to T4 (the trial's pass line is PR 4's merge gate); 4.6 is a rule for later PRs; 4.7 to T1 (the em-dash scan reads `ruled-change` files); 4.8 met by headings and link text in T3 and T4. 4.1 (spans) is deleted by D-0197.
- **Names agree.** `rebaselined`, `SKIP`, `REBASELINED`, `sources`, `bad_links`, `ADDRESSES`, `HANDBOOK`; `handbook_body` lives only in T3's creation script.
- **D-0198 (revision 2.2).** (1) and (3) to (5) in T1; (2) in T3, withdrawn by D-0201 (1) in revision 2.6; (3) extended in T3 and T4; (6) in PR 4's body.
- **Edges.** T1 and T2 touch disjoint files and are independent; T3 needs T1 (its file is `ruled-change`, so the checks must skip it) and T2 (the test module); T4 needs T1, T2 and T3 (the handbook it links to).
- **Ponytail.** Deleted from revision 1: the span omission in both checks, the span-label rule, the ruled-additions scan, the two-step handbook. One helper serves three tools; no new module; link validation is a test, not build plumbing.
- **Other callers.** `tools/media.py` reads a document's `source_file` only for drawn figures; the handbook has none, and its pictures are copied from its own media folder. `tools/render.py` needs `source_file` present, which the handbook keeps.
- **Checked against the files, 2026-11-18.** The capstone handout has 378 lines (379 entries when split on newlines, as the script asserts; Lab 3 likewise 284 and 285); Appendix B is lines 284 to 378, with the lead-in at 286 and the list at 288 to 294. Lab 3 and those lines hold no U+2014. D-0169's file has `ruled_omissions` at line 12, `ruled_additions` at 41 and `images` at 67.

## Executing critique, pass 1 (2026-11-17), on revision 1

Report: `docs/superpowers/plans/2026-11-17-lab-handbook-critique/pass-1/report.md`, with the patches of revision 1's T1 to T7 as written. All seven tasks ran verbatim and every full Verify passed; twelve findings. Their fate in revision 2:

- Findings 1, 2, 5, 8, 10 (spans, span fixtures, the span docstring, the additions regex, the span section's text): gone with the span omission (D-0197).
- Finding 3 (D-0191 and CLAUDE.md): T1 adds the exception.
- Finding 4 (cap factor ×1.10), 7 (HTML download links), 9 (line slips), 11 (one address list): carried into T2 to T4.
- Finding 6 (Lab 3's PDF leaves the lead-in on page 9 and its links alone on page 10): held for the owner.
- Finding 12 ("How this site works"): D-0196, PR 1's gate.

## Executing critique, pass 2 (2026-11-18), on revision 2

Report: `docs/superpowers/plans/2026-11-17-lab-handbook-critique/pass-2/report.md`, with the patches of T1 to T4 as written and its probes. Opus, xhigh effort. All four tasks ran verbatim; the full Verify passed after T1, T3 and T4; no F commits. Six revision breaks (B1 to B6) and ten findings. Their fate in revision 2.1:

- Folded (mechanical): B3 (the pin test on a reordered `ruled-change` file, in T1); B4 (the word diff through two files; the media-path rewrite listed in T3's "What changes"); B5's PDF half (T4 asserts the PDF's links, since D-0190 (2) names the PDF); B6 (main's run status); finding 2 (no new em-dash test file: one test in `EmDashScan`); 3 (`bad_links` reads link targets from Pandoc's tree with `media.lua`'s pattern; checked on the current tree 2026-11-18, both link tests pass); 5 (the tools' usage text and `verify.yml` comments); 6's first half (a Files row for `site/how-this-site-works.md`; the gate fires today); 7 (red-step text); 8 (`sources()` wraps `render.converted_documents()`); 10 (nits); edit 11 (`HTML_CAPS` order and form).
- Ruled by the owner, 2026-11-18 ("Take all six"), as D-0198 and folded in revision 2.2: B1 (T1 drops D-0169's lists unconditionally); B2 (T3's `HeldToLab7` holds the handbook to Lab 7's appendix until the capstone pass; CLAUDE.md names the same-PR rule); finding 1 (T1's `REBASELINED` pin, extended in T3 and T4); finding 4 (T1: `media.build` checks image hashes for every file); finding 6's second half (T1 trims the landing card); finding 9 (the owner checks Lab 3's PDF in the trial, noted in PR 4's body).

## Executing critique, pass 3 (2026-11-18), on revision 2.2

Report: `docs/superpowers/plans/2026-11-17-lab-handbook-critique/pass-3/report.md`, with the patches of T1 to T4 as written and its probes. Opus, high effort. All four tasks ran verbatim; the full Verify passed after T1, T3 and T4 (354, 362, 366 tests); no F commits. Two revision breaks and five findings. Their fate in revision 2.3:

- Folded (mechanical): B1 (T1 builds once before its focused verify, since `MediaDownloads` needs `build/quarto-site`); B2 (D-0198 in the reading list; no PR opens while it is `proposed`); finding 2 (`bad_links` flags every link aimed at another document that `media.lua` cannot rewrite, a colon or a dot in the fragment; checked on the current tree 2026-11-18, both link tests pass); finding 5's nits (the question-id pin sorted; the em-dash docstring says "unless its status is `ruled-change`"; `HeldToLab7` names the constants it takes with it; each rewrap to its paragraph's own widest line, "PH 211" kept together).
- Not folded: finding 5's unasserted constraint (no `ruled_omissions` or `ruled_additions` in a `ruled-change` file), on the rationale that a test would guard a form nobody writes. Pass 4 found that false: PR #86 (D-0184) writes that form, and merged 2026-11-19. Raised to the owner with pass 4's finding 1, ruled as D-0200 and folded in revision 2.5.
- For the owner: finding 4 (PLAUSIBLE, low). A `ruled-change` file's drawn figures are drawn from `source_file` at build time, and after D-0195 nothing checks that original's `source_sha256`. No `ruled-change` file has a drawn figure today; three converted handouts do. Options: `media.build` checks `source_sha256` whenever a document has drawn figures, as D-0198 (4) did for pictures; or record that it is unpinned and decide at the first such ruled change. Ruled 2026-11-19, "Record, decide later": D-0199 (ruled 2026-11-19) records it; nothing in this plan changes. D-0198 promoted the same day.

## Executing critique, pass 4 (2026-11-19), on revision 2.3

Report: `docs/superpowers/plans/2026-11-17-lab-handbook-critique/pass-4/report.md`, with the patches of T1 to T4 as written and its probes. Ordered by the owner past the cap. Opus, xhigh effort (a first try on Fable stopped on the usage-credit limit). All four tasks ran verbatim; the full Verify passed after T1, T3 and T4 (354, 362, 366 tests) and, minus the rebuild, at T2 (358); every red step failed as predicted; no F commits. Not clean. Their fate in revision 2.4:

- Folded (mechanical): B1 and B3 (the rewrap width is 76, stated; the line-21 clause dropped); finding 3 (T2's Verify and build step name the full exports); finding 4 (`parsed()` reads with generated identifiers off, since spec 4.4 links only to explicit ones; the fixture gains a plain heading); finding 5 (`DOC_TARGET`'s comment narrowed to what it selects); nits (revision 2.3's date, D-0199 in the reading list, `make_handbook.py`'s run line, which ledger T3's and T4's commits cite).
- For the owner: B2 and finding 1. PR #86 (D-0184), open when pass 4 ran, merged on 2026-11-19 at 19:07 UTC (main's run green), with #88 and #90. Main now holds a second `ruled-change` file, `curriculum/ph212/ph212-data-analysis-handout.md`, that still carries `ruled_omissions`, `ruled_additions` and `ruled_equations`. Pass 4 measured, with #86's change on top of T1: both Word checks skip it, so its declarations become dead text, and `test_rebaselined_files_are_pinned` fails. The plan's base is therefore stale: it must move to current main, T1 must treat D-0184's file as it treats D-0169's (drop its lists, pin it as D-0184), and the plan's line numbers in the files #88 and #90 touched must be rechecked. Ruled 2026-11-19 ("Yes, rebase it") as D-0200 and folded in revision 2.5.

## Readiness: an exception to the clean-pass rule

The owner, 2026-11-19, shown that revision 2.5 had no critique pass and asked whether to run a fifth: "Skip pass 5, record the exception." Context (Claude): writing-plans calls a plan ready for `/build` only after a clean executing critique; none of the four passes was clean. The exception rests on the record: in every pass all four tasks ran verbatim with every full Verify green, the findings shrank to wording, test setup and edge cases, and pass 4's one medium finding came from main moving (PR #86), not from the plan. Untried end to end: the merge of `364ae73` (checked by hand against the files) and T1's D-0184 steps (dry-run on `364ae73`, nothing written). `/build`'s T1 runs exactly those, red then green, then the full Verify, before any PR opens.

So the plan is ready for `/build` attended, under this exception. Not for `/build overnight`: T4 waits on PR 3 being live on production and on the owner's Word and Google Docs check, and PR 4's body asks the owner to look at Lab 3's PDF page break. T1 to T3 name their seams and verify commands.

A second exception, the owner, 2026-11-19, leaving for the night: "Let's do T1 and T2 overnight, and then have that agent pause and write a handoff so I can review, merge, and spin up T3 and T4 tomorrow morning." Context (Claude): T1 and T2 run unattended in a separate session that opens their PRs and merges nothing; T3 and T4 stay attended. No clean critique pass precedes it, and the account's overnight /build setting is off: the run is a session started on this word, not /build overnight.
