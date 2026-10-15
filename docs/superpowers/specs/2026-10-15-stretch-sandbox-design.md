# Collapsible sections in sandbox courses: design

Status: draft for the owner's review, 2026-10-15. Written by Claude from
the owner's rulings in chat the same day: step 1 (spec) of the
Symplecticator pipeline, classified architectural by spec-first. Inputs: the
chat critique of an outside recommendation to adopt stretchtext (after the
`pro-vi/cc-stretch` plugin) for lab handouts, three question rounds, and the
survey of all 14 handouts beside this file
(`2026-10-15-stretch-survey.md`). Ledger: D-0143 to D-0145 (proposed),
D-0146 to D-0148 (declined, full entries in `DECLINED.md`). Ledger entries
win over this file.

## 1. Purpose

Two things, built together:

1. **Collapsible sections ("stretches",** after Nelson's stretchtext): a
   block whose first paragraph or heading stays visible and whose rest opens
   in place on request. This build proves the mechanism: the markup, the
   filter, accessibility, and the PDF download. It does not test whether
   shorter handouts get read. Using existing sentences only, the survey
   finds 4 to 24% of a lab's main path collapsible and 76 to 94% of an
   appendix, because questions, procedure and text a question points to
   must stay visible. That question waits for the wording-change phase
   (LEDGER 11).
2. **Sandbox courses**: working copies of selected labs on the production
   site, where the owner can change content without touching the converted
   labs, and the only place stretches may appear.

## 2. Rulings carried from chat (the owner's words, 2026-10-15)

| Question | The owner | Entry |
|---|---|---|
| Where the handout is read | "At the bench on a screen." | D-0143 |
| Devices | "Lab computers, student's personal devices. Phone is not the intended medium." | D-0143 |
| Where the visible text comes from | "Existing sentences for now." | D-0143 |
| Mechanism | "`<details>` blocks for now." | D-0143 |
| Purpose | "Testing the mechanism." | D-0143 |
| Control words "Show more" and "Show less" | "Yes." | D-0143 |
| The PDF prints from a copy with every section open | "yes" | D-0143 |
| The control | "so long as it is obvious where to click to expand." | D-0143, D-0145 |
| Sandbox courses | "It'll be added to the website under separate courses (more than one to prep for scaling): call them PH211H, 212H, 213H. [...] That'll give me a clean sandbox to make changes." | D-0144 |
| Their names: PH 211 Sandbox, PH 212 Sandbox, PH 213 Sandbox | "That works."; "Sandbox." | D-0144, D-0147 |
| Listed or unlisted | "Listed within the site is fine, but to be clear I want it part of the existing osu-physics-labs.pages.dev site, not a separate site." | D-0144, D-0148 |
| Which checks cover sandbox copies (section 5.7) | "Yes." | D-0144 |
| The survey's three labs, the rubric collapsed | "Yes, and that's fine, so long as it is obvious where to click to expand." | D-0145 |
| A skim-only dry run before a stretch ships | "Skip the dry run gate." | D-0146 |

## 3. Goals, non-goals, done

Goals:

- **G1.** Three sandbox courses, PH 211 Sandbox, PH 212 Sandbox and PH 213
  Sandbox, on the production site and listed on the course index, each
  holding one lab copied from its converted source.
- **G2.** A `::: stretch` block that renders as its visible lead and a
  native `<details>` holding the rest, behind a "Show more" or "Show less"
  control that is obvious to click and works by keyboard, by screen reader
  and with scripting off.
- **G3.** The collapse maps of section 7 applied in the three copies.
- **G4.** Downloads: the PDF prints every section open; the Word, HTML and
  Markdown downloads are not changed by the feature.
- **G5.** The build fails on any broken rule of section 6.4.
- **G6.** The converted labs are untouched: no stretch under `curriculum/`
  (rule R5), and their word and number checks stay green.

Non-goals: whether shorter handouts get read; content changes in the copies
(the owner makes those later, by hand); stretches inside a sentence; newly
written short versions; defaults that differ by course; layered print;
expansion logging; a dry-run gate (D-0146); phones as a design target.

Done means: the three sandbox labs are on production; every test is green on
`main`; and the owner has looked at screenshots of the control (light and
dark, 1440 px) and called it obvious.

## 4. Approaches

Rendering a stretch:

1. **A Lua filter, `tools/filters/stretch.lua`, in the Quarto build**
   (recommended). It writes raw HTML around Pandoc's own blocks, as
   `questions.lua` writes raw OpenXML around them for Word. No script; its
   rules run on Pandoc's syntax tree, so a broken rule fails the build.
2. Quarto's collapsible callouts (`collapse="true"`). Declined: they need
   Bootstrap's script, break with scripting off (D-0030's reason for the
   banner), and add a callout box and title the handouts do not have.
3. Post-processing the built HTML in `tools/quarto_chrome.py`. Declined:
   regular expressions over generated HTML, and the rules would lose the
   syntax tree.

Making a sandbox lab:

1. **Copies under `sandbox/`, made by a small `tools/sandbox.py`**
   (recommended). The tool copies a converted source, rewrites its front
   matter and media folder prefix, and changes nothing else. It is the
   repeatable step for the next lab (the owner: "more than one to prep for
   scaling"). Cost: a small tool and its test; the alternative is three hand
   copies and a written procedure.
2. An overlay: the converted source plus a separate map of collapses applied
   at build time. Declined: the owner could not change content, which is
   the sandbox's job.
3. A separate site. Declined by the owner ("not a separate site").

## 5. Part A: sandbox courses

### 5.1 Names and addresses

Course codes `PH 211 Sandbox`, `PH 212 Sandbox`, `PH 213 Sandbox`.
`render.course_slug` makes their slugs `ph211sandbox`, `ph212sandbox` and
`ph213sandbox`, so their pages are `/courses/ph211sandbox/` and so on. Each
carries its course's name, so a heading reads "PH 211 Sandbox: General
Physics with Calculus". No file names the person the sandbox is for (roles,
not names).

### 5.2 Listing

The course index gets a second group after the three course tiles: a
heading, "Sandbox", one line of text, and the three sandbox tiles in the
existing tile style. On a sandbox course page, the course tabs list the three
sandbox courses; on a course page they are unchanged. Each sandbox course page
opens with the same line. Proposed words, for the owner to approve (O1):

> Working copies of selected labs, for trying changes before they reach a
> course's handouts. Each course's own page has its handouts as converted.

### 5.3 Files

- A copy lives at `sandbox/<slug>/<id>.md`, its id `<slug>-<descriptor>`,
  for example `ph211sandbox-data-analysis-handout` (ledger 14: a course code
  plus a descriptor, never reused).
- Front matter: the source's `title`, `sequence`, `audience`,
  `visibility`, `layer` and `images`; `id`; `course` (the sandbox code);
  `status: sandbox`; `sandbox_of: <converted id>`;
  `copied_from_sha256: <SHA-256 of the converted .md when copied>`. No
  `source_file` and no `source_sha256`.
- Body: the source byte for byte, except picture paths, which point at the
  copy's own media folder.
- Course data: `site/sandbox-courses.md`, front matter only, listing each
  sandbox course's code, name and lab documents. A lab's number, title and
  description are read from its converted lab's entry in `site/courses.md`
  through `sandbox_of`: quoted data reused, not quoted again. `courses.md`
  stays quote-only (ledger 45).

### 5.4 Media

`tools/media.py` finds a copy's Word original through `sandbox_of` (the
converted lab's `source_file`), so pictures and drawn figures come from the
same original, by the same rules (D-0117, D-0118).

### 5.5 Downloads

The same four per sandbox lab as for any lab, each with an HTML cap in
`tests/test_downloads.py`, and a "Download all" on each sandbox course page.

### 5.6 The one-source rule, amended for `sandbox/` (D-0144)

A copy is a deliberate fork. Nothing flows between a copy and its converted
source automatically. A change made in a sandbox reaches a course's handout
only through the wording-change phase (LEDGER 11). `copied_from_sha256`
records the fork point; drift after it is by design.

### 5.7 Checks

| Check | Converted labs | Sandbox labs |
|---|---|---|
| Word check (`check_unchanged.py`) | on | off: no `source_file` |
| Number check (`check_numbers.py`) | on | off: no `source_file` |
| Question-id pins (`tests/question-ids.json`) | on | off |
| Em-dash check | skips them (they keep their original's, D-0103) | on: `sandbox` joins `PUBLISHED` |
| Quarto and Pandoc warning gate | on | on |
| HTML download caps | on | on |
| Stretch rules (6.4) | R5: no stretch allowed | on |
| The PDF holds every collapsed word | not applicable | on |

None of the three picked labs contains an em dash (counted 2026-10-15). Of the
14 converted labs, only `ph212-extending-a-model-handout` has one; a copy of
it would remove it in the copy.

## 6. Part B: collapsible sections

### 6.1 Markup

```
::: stretch
<the lead: one heading or one paragraph>

<one or more blocks>
:::
```

A stretch can sit inside a `box` or a `landscape` block, using the repo's
usual fence nesting (`docs/conversion-spec.md` gains the class). Its extent is
its fences; heading levels never decide where it ends (the survey's issue 2:
PH 212 Designing Experiments puts Appendix B under Appendix A).

### 6.2 Rendering, on the web page only

```html
<div class="stretch">
  (the lead, as Pandoc writes it)
  <details class="stretch-more">
    <summary><span class="when-closed">Show more</span><span class="when-open">Show less</span></summary>
    (the rest, as Pandoc writes it)
  </details>
</div>
```

The label not in use is `display: none`, which also takes it out of the
accessibility tree: D-0030's script-free pattern. The browser announces the
expanded or collapsed state itself (WCAG 4.1.2). The lead stays outside the
control, so a heading lead keeps its heading role (1.3.1).

### 6.3 The control

The owner's condition: it must be obvious where to click. Requirements:

- a bordered button shape, not bare text, at least 44 px tall (WCAG 2.5.8
  asks 24; 44 matches the course page's collapse);
- the browser's disclosure triangle kept, and a pointer cursor;
- text at least 4.5:1 (1.4.3) and border at least 3:1 (1.4.11) against the
  page background, in the light and dark themes, computed by a test from the
  theme's tokens;
- a visible focus outline (2.4.7), as the banner's summary has.

Lean: the shape of the course page's `.lab-pending > summary`, with a stronger
colour than its `--chrome-quiet` so it reads as a control. The owner judges
the final look from screenshots before merge (O2).

### 6.4 Rules the build enforces

The filter fails the build, naming the lab and the stretch, when:

- **R1.** A stretch does not open with a heading or a paragraph, or holds
  nothing after it.
- **R2.** A heading appears after the lead. Every heading stays in the page
  outline while sections are closed (WCAG 1.3.1, 2.4.1).
- **R3.** A question, checkpoint or hint block is inside a stretch (opted out
  in round 1; hints by Claude's default, O3).
- **R4.** A link in the same document targets anything after a lead. Anchors
  must land on visible text: Chrome opens a closed section on fragment
  navigation, and other browsers are unconfirmed.
- **R5.** A stretch appears in a converted lab. Only files under `sandbox/`
  may carry one; D-0146 skipped the dry-run gate for sandbox labs only.

Authoring guidance, not checked: a tail under about 30 words is not worth a
control; nothing needed for valid data or graded work goes in a tail; text a
question or hint points to stays visible.

### 6.5 Downloads

- **Word and HTML:** the filter is not in `tools/downloads.py`'s Pandoc
  call, so a stretch passes through as a plain division: every word shows.
- **Markdown:** the source byte for byte, fences included.
- **PDF:** `downloads.pdf` prints a copy of the built page with `open` set
  on every `details.stretch-more`. A test reads each sandbox lab's PDF with
  `pdftotext` and finds every tail's words in it.

### 6.6 Browser print

A student who prints the page (Ctrl+P) gets every section open. A print
style rule if one can open a closed `<details>`; otherwise a `beforeprint`
script. The executing critique probes which.

### 6.7 Find in page

Chrome (97 and later) and Firefox (139 and later) open a closed `<details>`
when find-in-page matches inside it. Safari is unconfirmed: a student on a
Mac may not find collapsed text by searching. Accepted for the sandbox.

## 7. Collapse maps

Line numbers are those of the converted files at `ac833da`. Words are
approximate, counted by the survey's rule. The fences are added to the copies
by hand in the build, each lead found by its text, not its line number;
`tools/sandbox.py` adds none.

### 7.1 PH 211 Sandbox: `ph211-data-analysis-handout` (5 stretches, about 482 words)

| # | Lead (line) | Kind of lead | Tail lines | Words | Exercises |
|---|---|---|---|---|---|
| 1 | "**Experimental goal:** ..." (18) | paragraph | 20 | 60 | paragraph lead |
| 2 | "This lab activity is designed to help you practice ..." (26) | paragraph | 28-32 | 39 | list in tail |
| 3 | "## Installing Excel Software (optional)" (43) | heading 2 | 45-49 | 127 | heading lead, links in tail |
| 4 | "### Linearization" (119), inside a box | heading 3 | 121-133 | 201 | stretch in a box, action and inline math in tail |
| 5 | "### Why Linearize?" (162), inside a box | heading 3 | 164-168 | 55 | stretch in a box, action |

### 7.2 PH 212 Sandbox: `ph212-capstone-handout` (14 stretches, about 1,843 words)

| # | Lead (line) | Kind of lead | Tail lines | Words | Exercises |
|---|---|---|---|---|---|
| 1 | "This lab activity spans two weeks ..." (45) | paragraph | 47-56 | 44 | two lists in tail |
| 2 | "#### If you miss Week 1 of this activity:" (59), inside a box | heading 4 | 61 | 46 | stretch in a box |
| 3 | "This lab activity is designed to help you practice ..." (68) | paragraph | 70-76 | 36 | |
| 4 | "Your lab should investigate quantitative ..." (128) | paragraph | 130 | 67 | |
| 5 | "**Model 1 – Drag**" (134) | paragraph | 136 | 57 | |
| 6 | "#### Remember, an experiment always:" (182), in a box in the landscape block | heading 4 | 184-190 | 94 | landscape, nested list |
| 7 | "**The following criteria will be used to grade ...**" (197), in the landscape block | paragraph | 199-205 | 462 | table (the rubric), landscape |
| 8 | "#### Required Plot Elements" (364) | heading 4 | 366-373 | 78 | action |
| 9 | "#### What is Uncertainty?" (375) | heading 4 | 377-379 | 136 | |
| 10 | "#### Sources of Uncertainty" (381) | heading 4 | 383-394 | 166 | list |
| 11 | "**Linearization comes in handy ...**" (406) | paragraph | 408-418 | 146 | action; the heading and hint before it stay visible |
| 12 | "#### Assumptions" (420) | heading 4 | 422-450 | 313 | three actions |
| 13 | "#### Finding uncertainty in a slope:" (452) | heading 4 | 454-464 | 69 | pictures |
| 14 | "#### Propagation of Uncertainty:" (466) | heading 4 | 468-474 | 129 | display math; ends before the hint at 476 |

### 7.3 PH 213 Sandbox: `ph213-hypothesis-testing-handout` (5 stretches, about 685 words)

| # | Lead (line) | Kind of lead | Tail lines | Words | Exercises |
|---|---|---|---|---|---|
| 1 | "A CRT accelerates and deflects a beam ..." (24) | paragraph | 26 | 54 | |
| 2 | "This lab activity is designed to help you practice ..." (32) | paragraph | 34-37 | 48 | list |
| 3 | "## Understanding the CRT" (49) | heading 2 | 51-59 | 270 | list with inline math; the schematic (61) stays visible |
| 4 | "**[Required Plot Elements]**" (241) | paragraph | 243-250 | 78 | action |
| 5 | "**[Linearization]**" (252) | paragraph | 254-273 | 235 | actions |

Every tail above was scanned on 2026-10-15: none holds a heading, a
question, checkpoint or hint fence, or an `{#id}` anchor. Rule R4 also checks
targets made by other means when the build runs. Together the three labs
exercise every case the survey found except a drawn figure, which no lab can
collapse: both drawn figures sit where a question uses them.

## 8. Open items (none blocks planning)

- **O1.** Closed 2026-10-15: the sandbox line's words (5.2) approved
  ("wording approved"); D-0143 to D-0145 ruled.
- **O2.** The control's final look (6.3): the owner checks screenshots
  before merge.
- **O3.** Hints shown only on request: the owner's later call. Until then
  R3 keeps hints visible.
- **O4.** When to copy PH 211 Capstone, the later test of whether shorter
  pages get read (D-0145).

## 9. Considered and declined or deferred

Declined by the owner (ledger): D-0146, the skim-only dry run; D-0147, the
PH 211H course codes; D-0148, unlisted sandbox courses.

Declined in the critique (Claude's, not ledgered):

- **The `{{short|long}}` markup.** It looks like Quarto's `{{< >}}`
  shortcodes and is invisible to the Lua filters, the word check and the
  downloads. Pandoc fenced divs instead.
- **The cc-stretch plugin itself.** It is a Claude Code terminal plugin;
  nothing in it runs on a web page.
- **Quarto collapsible callouts:** section 4.
- **Stretches scoped by heading level:** explicit fences instead (6.1).
- **A separate `/sandbox/` index page.** It has no job once the courses are
  listed on the course index.

Deferred (earmarked):

- **Stretches inside a sentence:** script and focus handling.
- **Newly written short versions:** LEDGER 11.
- **Defaults by course:** a section open in PH 211 and closed by PH 212,
  with the skills matrix as the fading map.
- **Layered print typography.**
- **Expansion logging.** No landing zone: a static site with no
  third-party scripts, and a FERPA question.
- **Hints on demand:** O3.
- **One shared source for the reference text repeated across labs.** The
  survey's section 4 counts about 200 words in 13 labs. It is a content
  restructure.

## 10. Checks that pin it (names provisional; the plan decides)

- **The stretch filter:** each of R1 to R5 fails a made-up fixture; the
  rendered structure and the control's words.
- **Sandbox:**
  - the course index group, pages and tabs;
  - the copy tool's front matter;
  - the word and number checks and the pins skip sandbox labs;
  - the em-dash check covers them.
- **Downloads:** HTML caps for the three sandbox labs; each PDF holds every
  tail's words.
- **Widths and contrast** (`tests/test_brand.py` style): the control's
  minimum height, and the contrast of its text and border in both themes.
- **A built page:** in each sandbox lab, every heading sits outside every
  `<details>`.

The pipeline from here:

1. The owner reviews this file and promotes D-0143 to D-0145.
2. `writing-plans` turns it into tasks.
3. An executing critique runs them in a scratch copy.
4. `/build`, simplify passes and a clearing review.
5. A draft PR.
