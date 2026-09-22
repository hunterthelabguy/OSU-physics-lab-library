# Decisions

The decision ledger for this repo, under the decision ledger spec v1
(`OSU-lab-ops/docs/decision-ledger-spec.md`, ruled 2026-09-21). This repo is
the spec's pilot, and the pilot feature is the site branding refresh.
`LEDGER.md` is frozen history as of 2026-09-21 and still binds where it has
not been amended here.

Status moves from `proposed` only by the owner's explicit statement in chat.
An agent appends `proposed` entries only. Every bracketed quantity in a
`ruled` entry has a `test:` that asserts it. The validator the spec
describes in section 6 does not exist yet; nothing here is machine-checked
except the tests named in `test:` lines.

Sources for the brand entries: the OSU brand guide pages on logo guidelines,
graphic elements, typography and cobranding (communications.oregonstate.edu,
read 2026-09-21); the Physics department site (physics.oregonstate.edu,
measured 2026-09-21); and `OSU-branding/OSU-style-guide.md` in the sandbox for
palette values and contrast. Official logo files: `OSU-branding/` in the
sandbox, supplied by the owner 2026-09-21, PNG only.

## Declined (index)

- D-0003 Name the site in text, never the logo (declined: owner ruled logo on) -> DECLINED.md
- D-0017 Add a light grid pattern to the header area (declined: owner, no reason stated) -> DECLINED.md
- D-0021 Keep the system font inside sims (declined: sims may change font) -> DECLINED.md

## Entries

### D-0001  Aim for brand compliance now, a department home later
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: The site's branding aims to be compliant enough that University Marketing could sign off on it, and eventually to fit under physics.oregonstate.edu.
- rationale: The owner chose compliance first and a department home later. The target is higher than merely looking recognizably OSU, and it sets how strictly the brand guide is read.
- alternatives: recognizably OSU to a student only; that stops short of what the owner wants.
- binds: site/, tools/render.py, tools/template-site.html

### D-0002  Put the official OSU logo on the site
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: The site carries the official Oregon State University logo, used unaltered from official files and never retyped or redrawn.
- rationale: The brand guide says the logo is to appear whenever the university is represented. It also bars unit logos without exception, so the library gets no mark of its own. The wordmark is custom lettering and cannot be typed.
- alternatives: text-only naming, see D-0003 (declined).
- binds: site/, tools/render.py

### D-0004  Mirror the Physics department's header and footer
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: Landing, course and method pages take the Physics site's structure: a Paddletail Black [#000000] top strip, a Beaver Orange [#D73F09] banner holding the logo and the site name as live text, a Bucktooth White [#FFFFFF] navigation bar, and a dark footer. The draft banner (LEDGER 37) stays above all of it.
- rationale: The shortest path to D-0001: the site reads as a department page, so a later move under physics.oregonstate.edu is a small step. The site name stays machine-readable text, as the typography page requires of OSU web pages.
- alternatives: a bespoke header in palette colors; compliant, but it does not look like the department and makes the eventual move harder.
- binds: tools/template-site.html, tools/render.py, site/site.css
- test: tests/test_brand.py::BrandPalette::test_palette_tokens

### D-0005  Give sims a slim bar, not the full header
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: Sim pages get a slim black strip with a small logo in place of the full header, and the sim plus its bar keeps within the no-scroll budget of LEDGER 51.
- rationale: The Physics header measured about 148 px tall. LEDGER 51 left a sim roughly 90 px of spare height, so the full header would make the sims scroll.
- alternatives: the full header on sims; breaks the budget.
- binds: tools/render.py (sim chrome injection)

### D-0006  Self-host Open Sans; no Stratum 2 for now
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: Body and headings use Open Sans, with the font files committed to the repo and served from the site itself. Stratum 2 is requested from University Marketing when the site is shown to them, not used before.
- rationale: The typography page names Open Sans as the web substitute because of licensing. Self-hosting keeps pages working offline and keeps sims inside their no-network policy. Stratum 2 needs a license and a hosted font service.
- alternatives: Stratum 2 through a hosted kit (licensing, and breaks offline sims); Impact as the listed Stratum substitute (poor fit on screen); the current system stack (not the brand).
- binds: site/site.css, themes/modern.css, a new font directory

### D-0007  Commit the logo and exclude it from the open license
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: The official logo file is committed to this repo, and the eventual license (LEDGER 8) explicitly excludes it as a registered trademark.
- rationale: A static site has to serve the file itself. A Creative Commons license on the repo cannot cover a trademark the project does not own.
- alternatives: hotlinking an OSU-hosted file; breaks offline use and depends on a URL nobody here controls.
- binds: repo root license text (not yet written), logo asset path

### D-0008  Keep orange text large and the chrome palette-only
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: Beaver Orange [#D73F09] is used for text only at large size, [24] px regular or [18] px at weight 700 and up. Smaller text is Paddletail Black or Star Canvas [#003B5C]. The site chrome uses palette values only, with no tints or shades. Orange on white measures [4.56] against the AA threshold of [4.5].
- rationale: The style guide says not to set small orange text on white and allows no tints or shades. Orange passes AA by only 0.06, so it is kept for sizes where the margin does not matter. Correction to the second brainstorm round: it counted three off-palette values in `site/site.css`, but there are six (two light, four dark).
- alternatives: orange at any size (passes AA by 0.06, against the style guide's advice).
- binds: site/site.css
- test: tests/test_brand.py::BrandPalette::test_palette_tokens, tests/test_brand.py::BrandContrast::test_orange_on_white, tests/test_brand.py::BrandContrast::test_orange_on_white_meets_aa, tests/test_brand.py::BrandContrast::test_star_canvas_on_white, tests/test_brand.py::OrangeTextIsLarge::test_orange_text_is_large, tests/test_brand.py::OrangeTextIsLarge::test_checker_catches_small_orange

### D-0009  Footer: the department and policy links, no contact details
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: The footer names the Department of Physics, links the Accessibility Statement, Privacy and Non-Discrimination pages to OSU's own URLs, and carries a copyright line. It gives no address, email or phone for the library.
- rationale: Those three links appear on the Physics footer. The library has no contact details of its own, and borrowing the department's would be invented record data. The link URLs and the copyright wording are placeholders until taken from the source.
- alternatives: copying the Physics footer whole (asserts contact details the library does not have).
- binds: tools/template-site.html, tools/render.py

### D-0010  Keep the brand in the site chrome, never inside documents
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: Branding goes only in the header and footer the build adds. Neither document presentation is restyled by it, and the faithful one keeps its printed-page look.
- rationale: The faithful presentation exists to be compared with the original (LEDGER 28). Keeping the documents unbranded also keeps the curriculum portable to other institutions (VISION principle 3).
- alternatives: brand styling inside the modern presentation; mixes brand with the evidence review and harms portability.
- binds: themes/faithful.css, themes/modern.css (untouched by this refresh)

### D-0011  Put the logo on the unlisted draft now
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: The logo goes on the unlisted draft deploy as soon as it is built, without waiting for the license (LEDGER 8). Public listing still waits on the license.
- rationale: The owner ruled the logo on (D-0002) without saying when. The first brainstorm round leaned toward waiting, because a logo on a "draft, license pending" page makes the draft look endorsed. The owner's plan to build first and show Marketing (D-0012) needs the logo in place.
- alternatives: wait for the license; nothing to show Marketing until then.
- binds: deploy timing

### D-0012  Build first, then show University Marketing before wider sharing
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-09-21
- decision: Build the branded site unlisted, then send University Marketing a short heads-up with a screenshot before showing the branded version to anyone else, and ask for Stratum 2 web access (D-0006) in the same note.
- rationale: The owner judged building before asking acceptable while the site is unlisted. The added step addresses the real exposure: the official logo on a vercel.app address, which is not an oregonstate.edu address, is the kind of use a trademark office stops. A note sent early turns "we found this" into "they told us".
- alternatives: ask permission before building (slower, nothing concrete to show); build and never ask (risks a forced redo).
- binds: process; no files

### D-0013  Get reversed logo variants for the orange and black bars
- status: proposed
- proposed-by: claude
- date: 2026-09-21
- decision: Obtain the official logo variants for dark and orange backgrounds before building D-0004 and D-0005. The supplied file, `OSU_horizontal_2C_O_over_B.png`, is the two-color version for light backgrounds.
- rationale: A spec gap caught before code. The supplied file has an orange "Oregon State" and a black crest and "University". On the Beaver Orange banner the wordmark disappears, and on the black sim strip the crest and "University" disappear. The Physics site uses a reversed version on its banner, and the brand guide forbids altering the logo, so recoloring the file is not an option.
- alternatives: place the supplied logo on a white field inside the banner (changes the look D-0004 ruled); recolor the file (forbidden).
- binds: D-0004, D-0005

### D-0014  Use the supplied PNG in place of the SVG
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: Commit the supplied logo PNG byte for byte and scale it in the browser, until official SVG files are obtained. The ruled wording of D-0007 said SVG.
- rationale: The PNG is 3651 by 1168 pixels and 180034 bytes, sharp at any header size. Downscaling it at build time would be a derived copy with nothing to compare it against.
- alternatives: wait for the SVG; blocks D-0004.
- binds: D-0007, logo asset path

### D-0015  Use Paddletail Black paper in dark mode
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: In dark mode the chrome's paper is Paddletail Black and its text is Bucktooth White, replacing the four off-palette dark values, with Seafoam and Moondust for headings and quiet text as now.
- rationale: D-0008 rules the chrome palette-only, and the brand guide says nothing about dark mode. Pure black paper is the only palette-compliant choice.
- alternatives: drop dark mode for the chrome (worse for readers who set it); keep near-black grays (off-palette).
- binds: site/site.css

### D-0016  Use OSU icons on sim and download cards, never beside a course name
- status: proposed
- proposed-by: claude
- date: 2026-09-21
- decision: Use official OSU icons, one color each, on sim and download cards. Never place one beside a course or unit name.
- rationale: A cheap OSU look. The graphic elements page bars combining icons with unit or program names to make a logo.
- alternatives: no icons.
- binds: site/, sims page

### D-0018  Draw modern-presentation figures in the infographic style
- status: proposed
- proposed-by: claude
- date: 2026-09-21
- decision: When figures are redrawn for the modern presentation, follow the brand's infographic style (monoweight, rounded line work). This belongs to the content-change phase, not this refresh.
- rationale: The graphic elements page ties infographics to the icon style. Redrawing figures is a content change, so it cannot happen during the conversion phase.
- alternatives: keep original figures as is.
- binds: content-change phase

### D-0019  Build the decision ledger validator
- status: proposed
- proposed-by: claude
- date: 2026-09-21
- decision: Build the validator described in section 6 of the decision ledger spec as a CI test in this repo. It is not part of the branding refresh unless the owner rules it in.
- rationale: Until it exists, the ledger's rules are enforced only by PR review. This entry records the gap as a proposal and does not claim a check that does not run.
- alternatives: keep review-only enforcement through the pilot.
- binds: tests/, .github/workflows/verify.yml

### D-0020  Match each logo file to the background it sits on
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: Use `OSU_horizontal_2C_W_over_B.png` on the Beaver Orange banner (D-0004), `OSU_horizontal_2C_O_over_W.png` on the black sim strip (D-0005), and `OSU_horizontal_2C_O_over_B.png` anywhere on white. Commit those three byte for byte (D-0014), and nothing else from the library until it is needed.
- rationale: The owner supplied the full library, which covers what D-0013 asked for. It is PNG only, so D-0014 stays in force. Checked by laying every horizontal file over orange, black and white (2026-09-21): these three are the two-color versions that stay fully legible on each background, and the logo page asks for a two-color wordmark when possible. The one-color white file also reads on orange and black and is the fallback.
- alternatives: one-color white on both dark bars (legible but not the two-color preference); a white field in the banner holding the light-background file (unlike the Physics site, which D-0004 mirrors).
- binds: D-0004, D-0005, D-0007, D-0014, logo asset path

### D-0022  Set the draft banner in Luminance with black text
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: The draft banner (LEDGER 37) changes from Beaver Orange to Luminance [#FFB500] with Paddletail Black text, on site pages and in the sim bar, and keeps its wording.
- rationale: A spec gap caught before code. Under D-0004 an orange draft banner would sit directly on the orange brand banner, so the warning would read as part of the brand. Luminance is a palette secondary color used once, for a warning, which the "use sparingly" rule allows. Black on Luminance is 11.86:1 by the style guide's table.
- alternatives: keep it orange (merges with the brand banner); black (merges with the top strip); a secondary like Stratosphere (fails contrast with white text at small sizes).
- binds: site/site.css (.draft-banner), tools/render.py (SIM_CHROME)
- test: tests/test_brand.py::DraftBanner::test_black_on_luminance, tests/test_brand.py::DraftBanner::test_banner_colors (expected failure until built)

### D-0023  Hold the copyright line until the license settles
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- supersedes: D-0009 (the copyright line only)
- decision: The footer carries no copyright line until LEDGER 8 settles who holds what. Until then the footer points to the "How this was made" page.
- rationale: Any wording ("Oregon State University", the College of Science as on the Physics footer, or the original authors) asserts an ownership the record does not yet show, which is invented record data. The original authors' credit is also open (VISION principle 4).
- alternatives: copy the Physics line (claims the College holds copyright in the curriculum); a line saying "copyright pending" (placeholder text on a public page).
- binds: D-0009, tools/template-site.html, tools/template.html

### D-0024  Link the top strip to the Department of Physics
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: The black top strip holds one link, "Department of Physics", to https://physics.oregonstate.edu. On the Physics site the same strip names the parent unit ("College of Science"); for the library the parent is the department.
- rationale: It completes D-0004's structure without inventing a sitemap or a search, which the library does not have. The claim it makes, that this is the department's lab library, is one the owner can confirm or strike.
- alternatives: an empty strip (the structure without its purpose); link the College of Science (skips a level).
- binds: D-0004, tools/template-site.html, tools/template.html

### D-0025  Get Open Sans from the Google Fonts repository, Latin and Greek subset
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: Download Open Sans from the googlefonts/opensans repository on GitHub under the SIL Open Font License, and commit it with its license text under `site/fonts/`. The file names and sizes are placeholders until the owner approves the download (a download needs approval of source, file name and size).
- rationale: D-0006 rules self-hosting but not a source. That repository is the upstream for the family, and the SIL Open Font License allows redistribution with its license text. Every site page embeds its resources (`--embed-resources`), so each page carries the font. Size is the cost to watch, measured before committing.
- alternatives: a font-hosting service (network at view time, against D-0006).
- binds: D-0006, site/fonts/

### D-0026  Give sims the brand font by editing the sim itself
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: The sim's source file takes the font: its Content Security Policy gains `font-src data:`, and it carries Open Sans embedded as a `data:` URI, so it stays one self-contained, offline page. The published copy still differs from the source only by the injected bar (LEDGER 51). The change lands via PR with the sim's own tests green.
- rationale: The owner ruled that sims can adjust their font (D-0021 declined). Editing the source keeps the file a student downloads identical to the published one. Rewriting the policy only in the published copy would break that. The legacy original (`index.legacy.html`) is untouched, and its SHA-256 test stands.
- alternatives: rewrite the policy in the published copy only (published and shipped files diverge); a linked font file (a sim opened from disk would lose it, and `default-src 'none'` blocks it anyway).
- binds: sims/modified-electric-force/index.html, D-0006, D-0025

### D-0027  Subset four static styles and use two weights
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: Take `OpenSans-Regular.ttf`, `-Bold.ttf`, `-Italic.ttf` and `-BoldItalic.ttf` (147528, 147264, 153256 and 153308 bytes upstream, read from the GitHub API 2026-09-21) and `OFL.txt` (4216 bytes). Subset each to Latin and Greek as WOFF2 with fontTools (plus brotli), installed from PyPI into the user Python. CSS weights 600 and 650 become 700 and weight 500 becomes 400, in `site/site.css`, `themes/modern.css` and the sim, so only two weights exist.
- rationale: Three facts came up while preparing the download the owner approved in principle (D-0025). The upstream repository ships no subsets, so a tool has to make them. The converted handout uses italics ("Mystery equipment" and others), which would render as a slanted fake without italic files. The chrome uses weights 600 and 650, which a regular and bold pair would render as bold anyway. Static files are about a quarter the size of the variable ones (532636 and 583992 bytes) before subsetting.
- alternatives: the variable fonts (every weight, larger); regular and bold only (fake italics in the handout); keep 600 and 650 with static files (they silently render as 700).
- binds: D-0025, site/fonts/, site/site.css, themes/modern.css, sims/modified-electric-force/index.html

### D-0028  Let the sim's content checks skip embedded data
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-21
- decision: In `sims/modified-electric-force/test-law.mjs`, the static checks that search the page text ("does not describe the law's form", "no identity fields") run on the HTML with every `data:` URI removed first. The network, storage, policy and legacy-hash checks keep reading the whole file.
- rationale: A spec gap caught while planning D-0026. The law-form check rejects any occurrence of words such as "cube" or "square", case-insensitive, anywhere in the file. Base64 font data is tens of kilobytes of mixed-case letters, and the chance that "cube" appears by accident is (2/64) to the fourth, about 1 in 1.05 million, per position. Over roughly 50000 base64 characters per font file that is about 5 percent per file, and roughly 10 to 20 percent across the two to four files the sim would embed. The longer words add little. Sizes are estimates until the subsets exist. The check exists to keep the law's form out of what a student reads, and embedded binary data is not that.
- alternatives: pick font subsets until the data happens to pass (fragile, fails again on the next change); move the font to an external file (breaks the one-file offline sim).
- binds: sims/modified-electric-force/test-law.mjs, D-0026

### D-0029  Center the site pages' reading column in the shell
- status: proposed
- proposed-by: claude
- date: 2026-09-22
- decision: On site pages (landing, course index, how this was made), `main` becomes a three-track grid inside the 72rem shell: the middle track is the 68ch reading measure, centered, and every child sits in it; `.lab-list` spans all three tracks. The measure itself is unchanged (LEDGER 56, 57). Document pages and the site chrome are unchanged: the header and nav still frame the shell (LEDGER 58), so on a wide screen they start left of the prose column.
- rationale: The owner asked for it in chat (2026-09-22) after a design review. Measured at 1440 px before the change, the prose column started 136 px from the left and ended 643 px from the right. After, it is 362 px and 378 px (the difference is the scrollbar). A grid is used instead of auto margins on each child because `ch` resolves in each element's own font: a 44 px h1 capped at 68ch is wider than the shell, so its text stayed at the left edge. Grid items do not collapse margins, so heading and list margins became one-sided and sum to the old gaps (h2 after a paragraph 40 px, h3 24 px).
- alternatives: auto margins on each child (headings stay left, measured); a fixed rem width for headings (a second copy of the measure that drifts when body type changes); align the chrome to the prose column too (LEDGER 58's reason still holds for document pages; open question for site pages).
- binds: site/site.css, LEDGER 56, LEDGER 58
