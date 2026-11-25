# Perturb report: an accessibility gate over everything the build publishes

Branch `showcase/2026-11-24-a11y-gate`, cut from `origin/main` at `f5971ad`,
worked in a separate clone (`src/lib-a11y-gate`). Never merged; mine it in a
fresh session under the full charter. No handout source, CSS, template or
filter is changed: every student-visible fix below is an ask.

## 1. Goal

Turn the library's hand-picked contrast pairs and one source-level heading
test into a gate that audits every published page and download, in both
themes and at WCAG's widths, and fails CI on anything new.

## 2. Tour, in reading order

1. `tests/fixtures/a11y/broken.html` and `clean.html`. Made-up pages. The
   broken one breaks each of the 16 rules once, at an element named by a
   class; the clean one passes all of them in both themes and at both
   widths (a visually hidden skip link, a scrolling wide table, 24 px grey
   text at 3:1, an inline link). Read these first: they are the spec of
   what each rule means.
2. `tools/a11y_audit.mjs`. One file, no dependencies: serves a folder,
   drives headless Chrome over the DevTools protocol with Node's own
   WebSocket, and runs the checks in the page. 49 pages, 4 passes each
   (light, dark; 1280, 320 px), about 22 s locally. The rules:
   - contrast (1.4.3) of every element with its own text, against what
     `elementsFromPoint` says is painted behind it, composited over the
     propagated canvas, ancestor opacity applied, large-text threshold
     honoured; an image or unknown colour behind text is its own finding
     (`contrast-unmeasured`), never a guess;
   - document: `lang` (3.1.1), title (2.4.2), zoom not blocked (1.4.4),
     one `main` (2.4.1);
   - structure: exactly one visible h1, rendered heading levels with the
     chrome included, data tables with a header cell, id references that
     name one element (1.3.1);
   - names: links, buttons, controls, summaries and iframes (4.1.2), and
     `img` alt or `role=img` names (1.1.1);
   - reflow at 320 px (1.4.10), naming the outermost element past the edge
     and allowing a box that scrolls on its own (D-0130's rule);
   - target size (2.5.8, AA): 24 px, or the 24 px spacing circle, with the
     inline-link exception and a label counted into its control's target;
   - focus visible (2.4.7): each control focused as a keyboard would,
     its drawn style compared before and after;
   - text spacing (1.4.12): WCAG's four values applied, then any clipping
     box that did not clip before.
3. `tests/test_a11y.py`. Four classes:
   - `AuditRules`: every rule in `RULES` has a broken case, fires at its
     element, and the clean page raises nothing;
   - `SiteRatchet`: the whole built site against `tests/a11y-known.json`,
     in both directions (new fails; fixed fails until the file is lowered),
     the `KNOWN_SKIPS` pattern of `tests/test_headings.py`;
   - `PdfTags`: each lab's PDF is tagged, has one H1, `/Lang (en)`,
     `/DisplayDocTitle true`, a `/Alt` per `Figure` and a `Table` per table
     in the HTML download. All 20 pass today (Chrome 158 tags its print);
     this pins it against a Chrome or `@page` change;
   - `DocxA11y`: alt text on every Word picture (ratchet
     `KNOWN_EMPTY_ALT`), `dc:language`, real heading styles, and the
     `dc:title` ratchet `KNOWN_UNTITLED` (all 20 today).
4. `tests/a11y-known.json`. The baseline: 146 keys of
   `rule|page|theme|width|target` with counts. Its content is the findings
   list below; its diff is how a fix shows up in review.

No workflow change: CI's `Tests` step already runs `unittest discover`
with node, `google-chrome` and `poppler-utils` (which brings `pdfinfo`).

## 3. Verify at the head

Local, Windows, Quarto 1.10.18, Pandoc 3.10 bundled, Chrome 158, Node
24.19.0, against a fresh `tools/quarto_build.py` build (exit 0, 4 min 27 s):

```
tools/check_em_dash.py                  exit 0
tools/check_unchanged.py <20 files>     exit 0  (ruled-change handbook skipped, D-0195)
tools/check_numbers.py <20 files>       exit 0
python -m unittest discover -s tests    Ran 387 tests in 1054.694s  OK
python -m unittest tests.test_a11y      Ran 8 tests in 52.929s      OK  (after the last edit)
```

Not run: CI. A push to a `showcase/` branch triggers no workflow, and no
PR is opened under `/perturb`, so the gate is unproven on Linux.

Mutation check (local, then restored and compared byte for byte): one
built page given a logo `img` with no alt and `main p { color: #999 }`.
`test_no_new_finding` failed, listing 35 contrast keys at each width in
light only (#999 passes on the dark paper), and `img-alt` and the logo
link's `name` in all four passes. The first run of this check exposed a
test bug, fixed before commit: `assertEqual(list, [])` truncates a long
diff, so only the first new finding showed.

## 4. What it found on main today

Real, student-visible, each confirmed in a browser:

- **Links in dark mode are the browser's #0000ee on the dark paper:
  1.90:1 on `--paper`, 1.71:1 on `--tint`** (AA needs 4.5:1). 11 labs, on
  both the page and the HTML download (54 findings per width).
  `themes/modern.css` darkens `--paper` and `--ink` and never sets a link
  colour or `color-scheme`. Seen in the pane at 375 px: Lab 2's data link
  (PH 211 Fundamentals of Data Analysis, "Position vs time data") is navy
  on near-black and barely legible.
- **Equations push 8 labs past the screen at 320 px** (24 findings per
  theme), page and download alike; WCAG 1.4.10's width is 320, and the
  earlier manual measure used 375, which is why it was never seen.
- **Rendered heading skips** in the capstones (h1 to h3, h2 to h4): the
  three labs `tests/test_headings.py` already lists, now seen as a reader
  hears them, chrome included.
- **Word**: no `dc:title` in any of 20 files (Word and a screen reader
  announce the file name); two pictures with `descr=""` and no Word
  decorative mark (the owner-tasks list already has them).

Zero findings site-wide for: names, alt, lang, title, zoom, landmarks, one
h1, id references, table headers, target size, focus visible and text
spacing. The PDFs pass every check.

False findings found and fixed in the auditor on the way (each now
covered by the clean fixture): a cell wider than the screen centred off
its own text; the canvas taken as white where the body's dark background
propagates past the body's box; a visually hidden skip link judged as a
1 px tap target.

## 5. Rulings

- Ruling (Claude): a separate clone at `src/lib-a11y-gate`, not a worktree
  of the shared checkout; why: the argument said "scratch copy", and the
  shared checkout holds another branch and 20 worktrees; cost if wrong: a
  folder to delete.
- Ruling (Claude): branch name `showcase/2026-11-24-a11y-gate` as proposed;
  why: the rerun of `/perturb` gave a place, not a name; cost if wrong: a
  rename.
- Ruling (Claude): a home-grown auditor over the DevTools protocol, not
  axe-core; why: no dependency download (an ask), Node 24 has WebSocket,
  and the house pins its tools; cost if wrong: 16 rules where axe has about
  90, so false negatives (ARIA validity, link purpose, non-text contrast).
- Ruling (Claude): audit at 1280 and 320 px, not 375; why: 320 is 1.4.10's
  own figure (1280 at 400 %); cost if wrong: the 48 reflow findings are
  noise if the owner rules 375 the floor.
- Ruling (Claude): the ratchet fails in both directions, keyed by rule,
  page, theme, width and a class-only CSS path, counted; why: the house
  `KNOWN_SKIPS` pattern, and generated ids would churn; cost if wrong:
  a structural edit to a handout moves keys and needs `--write-known`.
- Ruling (Claude): `contrast-unmeasured` is ratcheted like a failure; why:
  an unmeasurable background is a hole in the gate; cost if wrong: noise
  (none today).
- Ruling (Claude): no workflow change, the test rides `unittest discover`;
  why: CI already has node, Chrome and poppler; cost if wrong: unverified
  on Linux (see the risk under mineable pieces).
- Ruling (Claude): no CSS, filter or template fix on this branch; why: each
  changes what a student sees, which is the owner's (the charge and
  D-0168); cost if wrong: the owner mines a gate with no demo fix.
- Ruling (Claude): Word's empty alt and empty title are ratchets, not
  failures; why: the alt is the originals' (D-0132 call 6, owner tasks),
  the title a file-format ask; cost if wrong: none, both lists shrink.

## 6. Mineable pieces

Each against its payoff; order of magnitude only.

| Piece | Cost and time | Complexity | Risk | Payoff |
|---|---|---|---|---|
| The audit and ratchet as they are (one PR) | one session | low: 3 files, no dependency | medium: Linux fonts may move the math reflow keys, so the first CI run may need `--write-known` from CI's own build (an artifact, not a local rewrite) | every page in both themes gated on every PR |
| The PDF and Word invariants alone | an hour | low | low | pins Chrome's tagging, which nothing asserts today |
| Ask A1, dark links: `color-scheme: light dark` on the dark `:root` (Chrome's #9e9eff, 7.47:1 on paper, 6.72:1 on tint), or a `--link` token (Seafoam #b8dde1 12.30:1, Moondust #c6dae7 12.40:1, both the colours of other meanings) | minutes, plus the owner's look | low | low; also darkens form controls and scrollbars | 54 failures a width gone; the worst bug found |
| Ask A2, math at 320 px: block math in its own scroll box, as wide tables are | an hour | low for display math; inline math cannot scroll and needs a ruling on breaking | low | 48 findings, 8 labs |
| Ask A3, Word title: pass the lab title as Pandoc metadata to the docx writer | minutes | low | low (it is the title bar and file properties) | 20 files announce a title, not a file name |
| Ask A4, Word decorative mark on `descr=""` pictures | an hour | medium: raw OpenXML `adec:decorative` in `extLst` | low | Word agrees with the page that they are decorative |
| `tools/measure_chrome.js`'s contrast part retired into the audit | an hour | low | low | one contrast measure, not two |

## 7. Conjugate bets

- **Change frame (the screen-reader user, not the sighted checker).** The
  owner's framing is "checks"; the NVDA test of 2026-11-05 (D-0166) shows
  what hearing a page finds that no rule does. Bet: drive NVDA's speech
  log (the silent config already exists) over each built page and ratchet
  the transcript, so a change in what a student hears is a diff. Breaks
  the assumption that rules approximate experience well enough.
- **Invert an assumption (the build checks itself, not the deployment).**
  The gate reads `build/quarto-site`; `check_deployed.py` already proves
  production serves those bytes, so the audit is valid for production
  only through that chain. Bet: none needed while D-0048's exact-bytes
  deploy holds; if the host ever transforms HTML (Cloudflare's
  auto-minify or email obfuscation), audit the deployment URL instead.

## 8. Count

Rulings asked of the owner: 1; made by Claude: 9.
