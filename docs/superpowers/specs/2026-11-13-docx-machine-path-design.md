# Word downloads carry the build machine's path: design

Status: draft for the owner's review, 2026-11-13. Written by Claude in a
side session started from the question-headings (D-0176) session, whose
third executing critique found the symptom. Ledger: D-0177 (proposed).
Ledger entries win over this file. Plan and build wait for the ruling; the
build ends in a draft PR with green `verify`.

## 1. Problem and cause

Reported: three Word downloads (PH 212 Designing Experiments, PH 213
Hypothesis Testing, PH 213 Model Building) write the build machine's
absolute path into a picture's `descr` in `word/document.xml`. Measured
here: that is one of two leaks, and the second reaches every Word download.

Evidence: a full build of `main` at 6599a5f (`tools/quarto_build.py`,
2026-11-13, worktree `.superpowers/sdd/docx-machine-path`), every part of
every `build/quarto-site/labs/*/*.docx` searched for the worktree's path.
Counts are in section 1.3.

### 1.1 Leak A: a drawn figure's file path, three downloads

`tools/filters/media.lua`, `figure_docx`, returns the figure's PNG as
`pandoc.Image(alt, figure_file(el, ".png"), ...)`. `figure_file` is
`media-dir .. "/" .. name`, and `media-dir` is the absolute path
`tools/downloads.py` passes (`-M media-dir=` + `media_dir(doc)`, which is
`os.path.join(render.ROOT, "labs", id, id + "-media")`). Pandoc's Word
writer puts an image's `src` into `pic:cNvPr descr` (the picture's
non-visual name) and its alt text into `wp:docPr descr` (what Word shows
as alt text). So the alt text is right; the inner `descr` is the path.

Only drawn figures (class `drawn`, S13) go through `figure_docx`, and only
those three labs have one: one figure each, so one path each. Every other
picture keeps its source `src`, relative (`<id>-media/<file>`), which
Pandoc finds through `--resource-path` = the lab folder. Example, PH 213
Model Building on `main`:

```
<wp:docPr descr="Rectangle with conductive strips at opposite ends. ..." .../>
<pic:cNvPr descr="C:/Users/<user>/src/OSU-physics-lab-library/.../labs/ph213-model-building-handout/ph213-model-building-handout-media/conductive-strip-rectangle.png" .../>
<wp:docPr descr="A spreadsheet with one cell showing the function ..." .../>
<pic:cNvPr descr="ph213-model-building-handout-media/excel-linest-function.png" .../>
```

### 1.2 Leak B: `media-dir` as a custom document property, every download

Pandoc's Word writer writes every metadata field it does not map to a core
property into `docProps/custom.xml` as a custom property. The Word build
passes `media-dir` (absolute), so every Word download carries the path in
its properties (File, Info, Properties, Custom, in Word). The same file
also holds `theme`, the four box colours and `library-url`: build plumbing,
but the same on every machine and not private.

### 1.3 Measured on `main`

Script in the session scratchpad: every part of every built `.docx`
searched case-insensitively for the worktree's path in both slash forms;
every `descr` tested for an absolute path; every other built file except
binaries searched for the path.

| What | Count |
|---|---|
| Word downloads built | 19 |
| holding the path in `docProps/custom.xml` (leak B) | 19 |
| holding it in `word/document.xml` (leak A) | 3: the three named above, one `pic:cNvPr descr` each |
| `wp:docPr descr` (alt text) that is an absolute path or starts with a slash | 0 |
| other built text files (pages, HTML downloads, `.md`, CSS, JS) holding it | 0 |
| PDF downloads holding it in plain bytes | 0 of 19 (compressed streams not opened) |

Custom properties in each Word download on `main`: `box-fill`, `box-rule`,
`checkpoint-fill`, `checkpoint-rule`, `library-url`, `media-dir`, `theme`.

### 1.4 What is not affected

- The word check. `tools/check_unchanged.py` reads `descr` only from the
  **original** Word file (`docx_content`: `pic:cNvPr` for a picture,
  `wp:docPr` for a drawing) and compares it with the source's alt text. It
  never opens a built download. The fix changes no source and no original.
- Alt text a reader meets: `wp:docPr descr` keeps the figure's alt text
  (label, caption, each picture's `data-alt`), unchanged.
- The lab page, the HTML download and the PDF: a drawn figure is inline SVG
  there, with no path (1.3).
- Sources: no wording changes, so no D-0168 ruled passage.

## 2. Fix

**A.** In `figure_docx`, the PNG's `src` is the source's own relative path
with `.svg` swapped for `.png` (`el.src:gsub("%.svg$", ".png")`), resolved
by `--resource-path` like every other picture. `media-dir` stays the way
the filter reads the SVG (size and alt text); a missing PNG is a Pandoc
warning, which fails the build. The inner `descr` then
reads `<id>-media/<figure>.png`, the same form as every other picture.

**B.** For Word only, the filter drops `media-dir` from the metadata once
it has read it, so Pandoc writes no such custom property. Nothing after
`media.lua` in the Word run reads `media-dir` (`questions.lua` and
`landscape.lua` do not). The lab page is untouched: Quarto never writes
custom properties, and the page's front matter is a gitignored source.

## 3. Test

One test in `tests/test_downloads.py`, `MarkdownAndWord` class, over every built
`.docx`:

1. no part contains `render.ROOT` in either slash form (catches leak A,
   leak B and any later one, on a laptop or the CI runner); and
2. no `descr` attribute, in any part, is an absolute path (a drive letter
   and slash, or a leading `/` or `\`), so a path from outside the repo
   (a temporary folder) also fails.

Red on `main` before the fix (19 downloads fail item 1, three fail item 2),
green after.

A second, faster assertion in `MediaDownloads`, whose made-up lab (one
drawn figure, one cropped picture) builds in a temporary folder outside the
repo: its Word file holds neither that folder's path nor an absolute
`descr`. Item 1 cannot see that case, and this one runs without the full
site build, so a filter change fails at the unit level first.

## 4. Calls for the owner

1. **Scope of the custom-property cleanup.** Lean: drop `media-dir` only.
   The other six properties are the same on every machine and public;
   dropping them too means one more filter step after `questions.lua` has
   read them, for no reader. Cost of the alternative: one more moving part
   and a second place that must know the build's metadata keys.
2. **Test reach.** Lean: Word parts only, as above. The HTML download and
   PDF carry no path today. Cost of adding the HTML download: a few lines,
   guarding against nothing yet seen; adding the PDF means decompressing its
   streams.
3. **Build timestamps (declined, noted).** `docProps/core.xml` carries
   `dcterms:created` and `modified` set to the build time, so two builds
   of the same commit still differ. Not a leak; making the downloads
   byte-reproducible (`SOURCE_DATE_EPOCH`) is its own change. Lean:
   decline here, raise separately if wanted.

## 5. Critique

5.1 **Severity, stated plainly.** Production is built in CI, so the
published downloads carry the runner's checkout path
(`/home/runner/work/...`), not anyone's user folder; the user-folder form
appears only in local builds, which are not published. Inferred from the
deploy path (CI builds, CI deploys), not fetched from production. The
build outputs are gitignored, so nothing is in git history to scrub. What
is real: build plumbing in a public file, and downloads that differ by
machine for no reason. Small, cheap fix; not an incident.

5.2 **Wrong layer?** Dropping a metadata key is not `media.lua`'s job
(placing pictures). But `media.lua` is the only reader of `media-dir`, so
the key's last reader drops it; any other home (a fourth filter, a
post-pass in `downloads.py`) adds a part whose only job is this. Kept.

5.3 **Fix at the source instead?** The Word and HTML download runs could
read the figure's SVG through Pandoc's resource path
(`pandoc.mediabag.fetch(el.src)`) and stop passing `media-dir` at all, so
the path never enters the run. The lab page still needs `media-dir` (its
resource path is the page's folder), so the filter would carry two ways to
find one file. More change, two read paths, same output. Declined (6.1).

5.4 **False positives in the test.** Item 1 matches the repo path, which
no download has a reason to hold; compared case-insensitively, since a
Windows drive letter's case can differ between two spellings of one path.
Item 2's "absolute" pattern would also match alt text that begins with a
slash; no `wp:docPr descr` on `main` does (1.3), and if one ever does,
the test names it.

5.5 **Does the relative path resolve everywhere?** `--resource-path` is
the lab folder (`lab_dir`), and the PNG is at
`lab_dir/<id>-media/<figure>.png` both in the site build and in the
`MediaDownloads` fixture (whose `lab_dir` is its temporary folder). A
missing PNG is a Pandoc warning, and the build's warning gate fails on it.

## 6. Declined

6.1 Reading the SVG through Pandoc's resource path so the Word run gets no
`media-dir` (5.3): two read paths for one file, same output.
6.2 Dropping all build-only custom properties (call 1's alternative):
values that are neither private nor machine-specific.
6.3 Reproducible build timestamps (call 3): not a leak; its own change.
6.4 Scanning the PDF download (call 2): no path seen there; decompressing
its streams is test machinery for nothing observed.
