# Quarto spike, 2026-09-30 (D-0033)

Throwaway trial port, built outside the repo in the session scratchpad with
Quarto 1.10.18 (installed by winget, MIT license). Nothing merged. Inputs:
`site/landing.md`, the PH 211 Lab 1 handout in both presentations, and the
`modified-electric-force` sim. The course index was a placeholder.

## Against the D-0033 criteria

1. **Sim byte identity: pass.** The sim was copied as a project resource and
   a 15-line post-render script injected the bar into the published copy.
   The published file with the bar removed equals the source byte for byte
   (checked in Python). The existing `render_sim` logic ports as is.
2. **Brand chrome: partial.** The Quarto navbar took Beaver Orange, white
   links, the logo, and Open Sans with a four-line SCSS file. Two defects,
   both fixable, not yet fixed: every page showed its title twice (the Quarto
   title block plus the page's own `#` heading), and the landing hero band
   lost its Star Canvas background because `site.css` rules are written for
   our template's classes. The Physics strip, the draft banner at the top, and
   D-0032's white site name were not rebuilt. Estimate: the chrome is a
   rewrite of `site.css` against Quarto's markup, not a copy.
3. **Plain static output: pass, with two catches.** Output is a folder of
   static files (site_libs 1.2 MB). No request left localhost on any page
   tested (browser resource timing). But (a) the Cosmo theme `@import`s
   Google Fonts; the default theme does not, so Cosmo is out; (b) Quarto
   writes its own `robots.txt` with a Sitemap line and no `Disallow`, which
   would break ledger 37's unlisted draft unless overridden. Also, pages
   link shared `site_libs/` instead of embedding everything, so a single
   downloaded page is no longer self-contained, and search needs HTTP, not
   `file://`. Both matter for the planned offline downloads.
4. **Question numbering filter: pass unchanged.** `questions.lua` ran as a
   Quarto filter with no edits: "Question 1..." labels in modern, bold "1)"
   in faithful.

## Telemetry and third parties

No analytics or telemetry strings in the output. External URLs present are
license comments and Algolia code paths, which load only if Algolia search is
configured. Only the Cosmo Google Fonts import made a live third-party
reference, removed by switching themes.

## What it would cost

Kept: the Markdown sources, `questions.lua`, `check_unchanged.py` (it reads
the Markdown, not the build), the sim injection logic, fonts and logos.
Rewritten: `render.py`'s page assembly becomes `_quarto.yml` plus a small
pre-render step for the course index; `site.css` and the templates are
redone against Quarto markup. Gained: search, navigation, listing pages.
Lost unless worked around: per-page self-contained HTML.

## Second spike, same day: the two gating questions

Owner ruled the migration (D-0033); this spike tested the two things that
could still block it.

1. **One source, two presentations (LEDGER 28): pass.** Each presentation is
   a thin wrapper page (`faithful.qmd`, `modern.qmd`: title, presentation
   name, filter, stylesheet) whose body is one include of the single
   curriculum Markdown file. The source's own front matter did not leak into
   the page. The modern output is word for word identical to the first
   spike's direct render; faithful differs only by the expected labels.
   One change forced: Quarto reserves the `theme` metadata key for its page
   theme, so the presentation name moves to `theme-name` and
   `questions.lua` reads that (a one-line edit). Still open: each page shows
   its title twice (wrapper title plus the source's `#` heading).
2. **Self-contained downloads: pass, as a separate small render.** Inside the
   website project, pages share `site_libs/`. A second small Quarto project
   with `embed-resources: true` rendered the same wrapper to one 127 KB HTML
   file with no external references, question labels intact. The real build
   would run that as a post-render step and generate its wrappers rather than
   store them. Bonus: `format-links` put a Word (.docx) download link on each
   page with no extra code, which covers part of the planned downloads.
   Quarto printed one "variable used before declaration" warning in that
   render; not traced.

Neither gate blocks the migration.
