# OSU-physics-lab-library: agent runbook

Loaded every session, so it holds only what every session needs. Read the
named section of `docs/agent-reference.md` before the task it covers:
previewing or measuring a page, editing CSS (Widths), deploy or the
Cloudflare and Vercel projects, sims, course pages, drawn figures, and
Quarto internals.

## Shipping contract (read by /handoff)

- **Verify:** `python tools/check_unchanged.py <converted .md files>`, then
  `python tools/check_numbers.py` on the same files, with
  `PANDOC` set to the Pandoc bundled with Quarto (locally
  `C:\Program Files\Quarto\bin\tools\pandoc.exe`; D-0044). CI job
  `verify` runs both on every push to main and every PR, plus
  `tools/check_em_dash.py` (published sources only; converted files keep
  their original's, D-0103), then the builds and the tests. The word check
  reads words, bold, equations and alt text, not structure; the number check
  reads labels; review the rest by parse-tree block counts. Manual
  before any commit: no student-identifiable data. Which Pandoc each step
  uses, and the variables to export locally, are under Build, "Which
  Pandoc".
- **Landing rule:** code and converted content land via PR with green
  `verify` (charter floor 4), squash merge. Ledger and spec-only commits may
  land direct on `main`, and every push to `main` deploys production: read
  that run once it reports (`gh run list --branch main`), since no PR tool
  watches it (a failed alias check went unread for a session, 2026-10-01).
  Merge one PR at a time and read main's run before the next: two merges
  four seconds apart raced their deploys, and the first run's alias check
  read the second's files (2026-10-08). Merging on GitHub stamps the account's primary email
  as merge author, which the owner accepts (ledger 36). Nothing on GitHub
  enforces this rule: a private repo on the free plan has no rulesets or
  branch protection (API 403, 2026-10-02), so the gate is this file.
- **Shared checkout:** two sessions may work in this folder at once (one
  appended D-0062 to D-0066 mid-session, 2026-10-02). Just before appending
  to `DECISIONS.md` or editing `STATE.md`, run `git fetch` and `git log -3
  origin/main`, and number a new entry from the file's last one.
- **Living plan:** `DECISIONS.md` from 2026-09-21, under the decision
  ledger spec (`../OSU-lab-ops/docs/decision-ledger-spec.md`); this repo is
  its pilot. Agents append `proposed` entries only; the owner promotes in
  chat. `DECLINED.md` holds full declines and is not loaded by default.
  `STATE.md` is the one-screen handoff. `LEDGER.md` is frozen history:
  never appended to, still binding where not amended. The spec's validator
  does not exist; `tests/test_brand.py` asserts the ruled quantities.
- **Commit trailer:** none. Identity `hunterthelabguy` with the noreply email.
- **Remote:** `git@github-hunterthelabguy:hunterthelabguy/OSU-physics-lab-library.git`

## Build

- Production is the Quarto build (D-0033), deployed to Cloudflare Pages
  (reference: Deploy). Phases 2 to 5 of `docs/quarto-migration-plan.md`
  are done; phase 4 retired the old build and kept its templates (D-0061).
- Which Pandoc (D-0044, D-0045, D-0061). Export before the verify sequence:
  `QUARTO="/c/Program Files/Quarto/bin/quarto.exe"`,
  `PANDOC="/c/Program Files/Quarto/bin/tools/pandoc.exe"`, and for
  the downloads `CHROME` and `PDFTOTEXT` (below). `PANDOC` is Quarto's
  bundled 3.10; the word check, the Quarto build, the chrome lift and the
  tests all read with it. Never set `PANDOC` to the `quarto pandoc`
  command: its stdout truncates large output on Windows (D-0045). A
  missing tool fails the tests, never skips.
- Quarto site: `python tools/quarto_build.py` writes `build/quarto-site/`
  (Quarto 1.10.18 at `C:\Program Files\Quarto\bin\quarto.exe`, not on
  PATH). Generated pages (`/index.qmd`, `/courses/`, `/how-this-site-works/`,
  `/labs/`, `/sims/index.qmd`) are gitignored and rebuilt every run; never
  edit them. Its warning gate fails on any Quarto or Pandoc warning.
- Downloads (D-0052 to D-0054): `tools/downloads.py`, run at the end of
  `tools/quarto_build.py`, writes `labs/<id>/<id>.md` (the source, byte for
  byte), `.docx`, `.html` and `.pdf`, all from modern, each with the draft
  banner and "Department of Physics, Oregon State University" in place of
  the logo. The HTML is a plain Pandoc render with no site chrome; the PDF
  is the built modern page printed by Chrome with the `@page` rules. Word's
  page header (the draft notice), footer, Letter page, body spacing and
  question label style come from the committed `tools/reference.docx`
  (D-0057); rerun `tools/make_reference_docx.py` when one of those,
  `BANNER_MAIN`, `themes/modern.css`'s spacing or the Pandoc version
  changes. Pandoc's `custom-style` reaches a Div's paragraphs, never its
  list items (probe, 2026-10-01), so the question box is a one-cell table
  that `questions.lua` writes as raw OpenXML around Pandoc's paragraphs
  (D-0082), its colours `--accent` and `--tint` read from
  `themes/modern.css` by `downloads.box_colours()`. To see what Word draws
  or to compare downloads with production, read the reference's "Checking a
  built page". The
  tests read the Word file's XML; only the owner, in Word and Google Docs,
  checks what it shows. The PDF
  needs `CHROME` (locally
  `/c/Program Files/Google/Chrome/Application/chrome.exe`; in CI the
  runner's `google-chrome`, the default; never run it here except headless
  with a print target, since `--help` hung a session, 2026-10-02); the
  tests need `PDFTOTEXT`
  (locally poppler's from winget, the path in
  `docs/superpowers/plans/2026-10-01-downloads-tasks.md`; in CI
  `poppler-utils`). Missing either is an error. When a lab is added,
  measure its HTML download and add its cap to `HTML_CAPS` in
  `tests/test_downloads.py`; a lab without one fails.
- Pictures and drawn figures (D-0117, D-0118; spec "Pictures and drawn
  figures"): `tools/media.py` fills the generated `labs/<id>/<id>-media/`
  with a lab's pictures and each figure's SVG (`tools/figures.py`, from the
  original) and PNG (headless Chrome, so the build needs `CHROME`); the page
  lists them under `resources`. `tools/filters/media.lua` places them and
  must run at Quarto's `pre-ast`: later, Quarto turns a lone picture into a
  figure captioned with its alt text. Every step reads sources as
  `render.FROM` (`markdown-smart-implicit_figures`). The figure's layout
  rules were measured on Word's own PDFs; its fonts' numbers are
  `tools/font-metrics.json` (`tools/make_font_metrics.py`). LibreOffice is
  not used: measured and set aside (D-0117), and uninstalled 2026-10-08 on
  the owner's word.
- Course pages and the course download (D-0067 to D-0071): read the
  reference's "Course pages" before changing either.
- Chrome (D-0036, D-0061): every Quarto page is dressed with the header and
  footer rendered from `tools/template.html` and `tools/template-site.html`
  by `tools/quarto_chrome.py`; `tools/downloads.py` renders the HTML
  download through `template.html`, so both templates stay. Never hand-edit the chrome
  in a Quarto page, and never copy the templates into a second file. Every
  Quarto-specific rule in `site/site.css` sits between its
  `quarto-only: start` and `quarto-only: end` comments, because that file
  is embedded in the HTML download too; `QuartoOnlyCss` requires each selector there
  to name `#quarto-content` or `.quarto-light`.
- Quarto traps: it reserves the `theme` metadata key, so the presentation
  travels as `theme-name`. Never use the Cosmo theme (it imports Google
  Fonts) and never enable `algolia:` search (a third-party CDN the scans
  cannot see). Quarto writes a `robots.txt` that allows indexing; override
  it (ledger 37). `title-block-style: none` only strips styling; the empty
  `title-block.html` partial is what leaves one `<h1>` per page, so never
  delete it. `{{< include >}}` merges the included file's front matter into
  page metadata, so a curriculum key that collides with a Quarto option
  (`lang`, `toc`, `css`, `date`, `author`) would change a page. Inline
  HTML in a generated page's Markdown (labels, inputs) gets wrapped in a
  `<p>`; pass a control as a ```` ```{=html} ```` raw block, as
  `render.download_all()` does. Quarto also publishes any local file a page
  references, listed or not: list every published file under `resources`
  (it published a stray `build/site/...` logo copy until phase 4, found by
  diffing two CI artifacts, 2026-10-02).
- Brand assets: the header and footer are two Pandoc partials,
  `tools/brandheader.html` and `tools/brandfooter.html`. Logo files in
  `site/brand/` are never edited (`tests/test_assets.py` pins each
  SHA-256). The header logo is one published PNG, kept out of
  `--embed-resources` by `data-external="1"` (D-0056); only the sim bar
  embeds a logo. Never pass a data: URI as a Pandoc `-M` value (past the
  Windows command-line limit). Open Sans in `site/fonts/` is rebuilt only by
  `tools/subset_fonts.py`.
- One Markdown source feeds one presentation, `themes/modern.css`, and the
  downloads; never copy content into a second file. D-0108 retired the
  faithful page (amending ledger 28): each `labs/<id>/faithful/` address is
  a redirect stub to `../modern/`, and `render.THEMES` is `("modern",)`.
  `render.pandoc_meta` returns plain text, so
  every caller escapes what it writes, once (D-0099).
  Question numbers come from `tools/filters/questions.lua` at render time;
  none is stored in the source. The "How this site works" page is
  `site/how-this-site-works.md` (D-0072; its old address redirects); the banner wording is `BANNER_MAIN` and `BANNER_DETAIL` in
  `tools/render.py`. Output stays host-agnostic static files (ledger 39).
- Tools not on PATH: Python 3.12 at
  `%LOCALAPPDATA%\Programs\Python\Python312\python.exe`; the GitHub CLI at
  `C:\Program Files\GitHub CLI\gh.exe`. Node 24 is on PATH; the sim tests
  need it.

## Conventions that bite

- This repo will become public. Anything that may never be public (instructor
  notes, rubrics, make-up data) goes in `OSU-physics-lab-library-instructor`,
  never here, because git history is permanent. Nothing that carries an
  answer key belongs here: the Electric Force instructor guide and build
  prompt stay out.
- Conversion phase: no content changes. Format only, proven by the
  content-unchanged check (docs/conversion-spec.md).
- Roles, not names. No invented record data.
- Original source files are in `../Old Reference Material/` and are
  unvetted: read one in full for student data before planning around it.
  The PH 21X set (handouts, instructor notes, rubrics, summaries) is under
  its `21X Lab Curriculum/`; layout and files not to open are in section 2
  of `docs/superpowers/specs/2026-10-06-handout-conversion-and-templates-design.md`.
  D-0084: the owner's word clears its handouts, summaries and course-wide
  files; nothing outside that in-scope list is opened; notes only in pass 7.
- `tools/check_unchanged.py` counts equations and pictures in place and
  compares each apart (D-0113, the spec's "Equation rule"): an equation's
  text and structure through Pandoc's own OMML writer, a picture's alt text
  against Word's `descr`. Pandoc misreads a typed "√" or "°" and a
  delimiter's bars; the source's TeX is corrected, never the comparison.
  It reads a SYMBOL field and a Symbol-font run as Word displays them
  (`SYMBOL_FONT`, D-0123) and stops on a slot it does not know. A drawn figure (S13) is read from the SVG
  `tools/figures.py` makes of its drawings; a drawing anchored to a
  paragraph is read after that paragraph's words; a picture is also its
  file, Word's size and Word's crop (D-0118).
  Strip an original with `tools/strip_identity.py` before committing it
  (D-0086); it stops on comments, revisions, people or EXIF it does not
  strip. Questions and checkpoints are pinned in order in
  `tests/question-ids.json` (D-0077).
- Never trust Pandoc's list numbers from an original: it drops a level set
  by a style that inherits its list (PH 212 Labs 1, 2, 3, 5) and misreads
  week restarts. Word's own labels for all 19 handouts are in
  `docs/word-labels.json`, found by the SHA-256 of three content parts the strip leaves alone (D-0102, D-0112; `tools/check_numbers.py`); the survey and its
  anchors are `docs/handout-survey.md`, the markup rules
  `docs/conversion-spec.md` (D-0101, D-0109, D-0110). To read Word again:
  PowerShell 5.1 COM on copies in the scratchpad, `Documents.Open` and
  `Close`/`Quit` take `[ref]` arguments, read-only, never save. The owner
  may have Word open: stop only your own instance, by its process id.
- In `site/site.css`, `body.site-page a` sets the link color and outranks the
  single-class chrome rules, so a chrome color must be scoped to its parent
  (`.osu-banner .osu-sitename`). D-0032 is one bug this caused in production.
  The same holds for `body.site-page ul`, which kept a 1.4rem indent on
  `.lab-list` until D-0068 scoped it `body.site-page .lab-list`. Two more
  from the course index (2026-10-03): a child of `main`'s grid stretches to
  the column, so an inline control needs `justify-self: start`; and the
  quarto-only block reverts `box-sizing` to the browser's `content-box`, so
  a padded, width-capped box (the Download all dialog) needs `border-box`.
  Measure, never assume: both were caught only by measuring at 375 px. So
  was a third (2026-10-06): a phone media query's reset of table cells
  (0,2,2) lost to the desktop width on `.lab-title` (0,3,1), so a reset
  names every selector it undoes.
- `ch` resolves against each element's own font, so a heading capped at
  `--chrome-measure` is wider than the shell. The prose column is a grid on
  `main` for that reason (D-0029), and grid items do not collapse margins:
  vertical spacing there is one-sided and adds up to the scale's steps.
- Design mockups from a review are kept as files under `docs/design/`, with a
  README saying which decisions each board became. They are mockups, never
  the source of truth for what the site does. Boards drawn on a Claude
  Design canvas are kept as its `.dc.html` source and `canvas.json`; they
  need the canvas runtime and do not open alone (2026-10-06 folder).
- Deploy: never run wrangler from this machine inside a Claude Code session,
  never touch the Cloudflare or Vercel projects or any secret without the
  owner's word, and compare a deployment only against CI's artifact, never a
  local build (reference: Deploy).
