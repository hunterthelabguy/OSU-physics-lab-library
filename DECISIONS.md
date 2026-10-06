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
- proposed-by: owner
- ruled-by: owner
- date: 2026-09-21
- decision: The site's branding aims to be compliant enough that University Marketing could sign off on it, and eventually to fit under physics.oregonstate.edu.
- rationale: The owner chose compliance first and a department home later. The target is higher than merely looking recognizably OSU, and it sets how strictly the brand guide is read.
- alternatives: recognizably OSU to a student only; that stops short of what the owner wants.
- binds: site/, tools/render.py, tools/template-site.html
- corrected: 2026-09-30, proposed-by from claude to owner, owner stated in chat that the idea was the owner's (spec section 3, lab-ops ledger 25)

### D-0002  Put the official OSU logo on the site
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-09-21
- decision: The site carries the official Oregon State University logo, used unaltered from official files and never retyped or redrawn.
- rationale: The brand guide says the logo is to appear whenever the university is represented. It also bars unit logos without exception, so the library gets no mark of its own. The wordmark is custom lettering and cannot be typed.
- alternatives: text-only naming, see D-0003 (declined).
- binds: site/, tools/render.py
- corrected: 2026-09-30, proposed-by from claude to owner, owner stated in chat that the idea was the owner's (spec section 3, lab-ops ledger 25)

### D-0004  Mirror the Physics department's header and footer
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-09-21
- decision: Landing, course and method pages take the Physics site's structure: a Paddletail Black [#000000] top strip, a Beaver Orange [#D73F09] banner holding the logo and the site name as live text, a Bucktooth White [#FFFFFF] navigation bar, and a dark footer. The draft banner (LEDGER 37) stays above all of it.
- rationale: The shortest path to D-0001: the site reads as a department page, so a later move under physics.oregonstate.edu is a small step. The site name stays machine-readable text, as the typography page requires of OSU web pages.
- alternatives: a bespoke header in palette colors; compliant, but it does not look like the department and makes the eventual move harder.
- binds: tools/template-site.html, tools/render.py, site/site.css
- test: tests/test_brand.py::BrandPalette::test_palette_tokens
- corrected: 2026-09-30, proposed-by from claude to owner, owner stated in chat that the idea was the owner's (spec section 3, lab-ops ledger 25)

### D-0005  Give sims a slim bar, not the full header
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-09-21
- decision: Sim pages get a slim black strip with a small logo in place of the full header, and the sim plus its bar keeps within the no-scroll budget of LEDGER 51.
- rationale: The Physics header measured about 148 px tall. LEDGER 51 left a sim roughly 90 px of spare height, so the full header would make the sims scroll.
- alternatives: the full header on sims; breaks the budget.
- binds: tools/render.py (sim chrome injection)
- corrected: 2026-09-30, proposed-by from claude to owner, owner stated in chat that the idea was the owner's (spec section 3, lab-ops ledger 25)

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
- proposed-by: owner
- ruled-by: owner
- date: 2026-09-21
- decision: The logo goes on the unlisted draft deploy as soon as it is built, without waiting for the license (LEDGER 8). Public listing still waits on the license.
- rationale: The owner ruled the logo on (D-0002) without saying when. The first brainstorm round leaned toward waiting, because a logo on a "draft, license pending" page makes the draft look endorsed. The owner's plan to build first and show Marketing (D-0012) needs the logo in place.
- alternatives: wait for the license; nothing to show Marketing until then.
- binds: deploy timing
- corrected: 2026-09-30, proposed-by from claude to owner, owner stated in chat that the idea was the owner's (spec section 3, lab-ops ledger 25)

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
- proposed-by: owner
- ruled-by: owner
- date: 2026-09-21
- decision: The sim's source file takes the font: its Content Security Policy gains `font-src data:`, and it carries Open Sans embedded as a `data:` URI, so it stays one self-contained, offline page. The published copy still differs from the source only by the injected bar (LEDGER 51). The change lands via PR with the sim's own tests green.
- rationale: The owner ruled that sims can adjust their font (D-0021 declined). Editing the source keeps the file a student downloads identical to the published one. Rewriting the policy only in the published copy would break that. The legacy original (`index.legacy.html`) is untouched, and its SHA-256 test stands.
- alternatives: rewrite the policy in the published copy only (published and shipped files diverge); a linked font file (a sim opened from disk would lose it, and `default-src 'none'` blocks it anyway).
- binds: sims/modified-electric-force/index.html, D-0006, D-0025
- corrected: 2026-09-30, proposed-by from claude to owner, owner stated in chat that the idea was the owner's (spec section 3, lab-ops ledger 25)

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
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-09-22
- decision: On site pages (landing, course index, how this was made), `main` becomes a three-track grid inside the 72rem shell: the middle track is the 68ch reading measure, centered, and every child sits in it; `.lab-list` spans all three tracks. The measure itself is unchanged (LEDGER 56, 57). Document pages and the site chrome are unchanged: the header and nav still frame the shell (LEDGER 58), so on a wide screen they start left of the prose column.
- rationale: The owner asked for it in chat (2026-09-22) after a design review. Measured at 1440 px before the change, the prose column started 136 px from the left and ended 643 px from the right. After, it is 362 px and 378 px (the difference is the scrollbar). A grid is used instead of auto margins on each child because `ch` resolves in each element's own font: a 44 px h1 capped at 68ch is wider than the shell, so its text stayed at the left edge. Grid items do not collapse margins, so heading and list margins became one-sided and sum to the old gaps (h2 after a paragraph 40 px, h3 24 px).
- alternatives: auto margins on each child (headings stay left, measured); a fixed rem width for headings (a second copy of the measure that drifts when body type changes); align the chrome to the prose column too (LEDGER 58's reason still holds for document pages; open question for site pages).
- binds: site/site.css, LEDGER 56, LEDGER 58
- corrected: 2026-09-30, proposed-by from claude to owner, the rationale records the owner asked for it (spec section 3, lab-ops ledger 25)
- corrected: 2026-09-30, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0029 to D-0032, D-0036 to D-0042"; D-0041 excluded, which the owner said in the same message is not yet ruled)

### D-0030  Draft banner: one line, detail on request
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-09-22
- decision: The draft banner on site and document pages becomes one line: `BANNER_MAIN` in bold and a "What this means" control that opens `BANNER_DETAIL` in place, using `<details>` with no script. The wording (in `tools/render.py`) and the D-0022 colors are unchanged. The banner stays on every page (LEDGER 37). In print the detail and the control are hidden. The sim bar (LEDGER 51, D-0005) is not changed.
- rationale: Owner asked for less chrome above the content (2026-09-22 design review). Measured at 1440 px, the banner goes from 110 px to 39 px closed; open, it is 107 px. The warning sentence itself is still on screen at all times.
- alternatives: shorten the detail text (a wording change, owner-reviewed text); drop the detail (loses the "please do not pass these pages on" request); a script toggle (unneeded, and breaks with scripting off).
- binds: tools/template-site.html, tools/template.html, site/site.css, D-0022, LEDGER 37
- corrected: 2026-09-30, proposed-by from claude to owner, the rationale records the owner asked for it (spec section 3, lab-ops ledger 25)
- corrected: 2026-09-30, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0029 to D-0032, D-0036 to D-0042"; D-0041 excluded, which the owner said in the same message is not yet ruled)

### D-0031  Landing hero band and link cards
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-09-22
- decision: On the landing page only, the title, the lead and two actions ("Browse courses" to the course index, "Open Lab 1" to the modern handout) sit in a full-width Star Canvas band on the centered prose column (D-0029). The four links below become cards, two across from 40rem up. Colors are fixed hexes, not tokens, so the band is the same in dark mode: white on Star Canvas 11.8:1, Moondust lead 8.19:1, white on the Beaver Orange button 4.56:1 (computed 2026-09-22 with the WCAG formula). Card descriptions lose their leading colon and start with a capital; no other wording changes.
- rationale: Owner asked for the canvas hero and cards to be built (2026-09-22). The band uses a clipped box-shadow for full bleed, because `100vw` includes the scrollbar and scrolled the page 8 px sideways (measured). Band padding is 96 px, 64 px below 40rem.
- alternatives: a new headline in the hero (the canvas mockup had one; not ruled, so the title stays); a band inside the shell only (not full bleed); cards across the full shell (four cards of one short line each look sparse at 1152 px).
- binds: site/landing.md, site/site.css, D-0029
- corrected: 2026-09-30, proposed-by from claude to owner, the rationale records the owner asked for it (spec section 3, lab-ops ledger 25)
- corrected: 2026-09-30, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0029 to D-0032, D-0036 to D-0042"; D-0041 excluded, which the owner said in the same message is not yet ruled)

### D-0032  Keep the site name white on the orange banner
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-22
- decision: `.osu-banner .osu-sitename { color: #fff; }`. On site pages the rule `.site-page a` (Star Canvas) was more specific than `.osu-sitename` and turned the site name dark blue on Beaver Orange in production since PR #10.
- rationale: A bug found while building D-0031, measured live 2026-09-22 (computed color rgb(0, 59, 92)). D-0004 mirrors the Physics site, whose site name is white.
- alternatives: none worth keeping.
- binds: site/site.css, D-0004
- corrected: 2026-09-30, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0029 to D-0032, D-0036 to D-0042"; D-0041 excluded, which the owner said in the same message is not yet ruled)

### D-0033  Migrate the site build to Quarto
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-09-30
- decision: The site build moves from Pandoc plus `tools/render.py` to Quarto, a Pandoc-based site generator (MIT license). Kept: the Markdown sources, `tools/filters/questions.lua`, `tools/check_unchanged.py`, the sim chrome injection (LEDGER 51, as a post-render step), fonts and logo files. Rebuilt: page assembly (`_quarto.yml` plus a pre-render step for the course index and the page lifted from VISION.md), templates, and `site/site.css` against Quarto's markup. Conditions the migration must meet: one Markdown file per document still feeds both presentations (LEDGER 28); every page stays unlisted (LEDGER 37), with our own `robots.txt` and a test that asserts it; output stays plain static files that any host serves (LEDGER 39); no theme or setting that loads a third-party resource; the Quarto version is pinned, and `check_unchanged.py` uses the same Pandoc that renders. A second spike on LEDGER 28 and self-contained downloads gates the migration plan, not this decision. Amends LEDGER 38.
- rationale: Owner ruled in chat 2026-09-30: the site will grow to many pages quickly, so search, navigation and listing pages are needed soon, and the branding is not load-bearing enough to justify a custom build. The first spike (`docs/quarto-spike-2026-09-30.md`) passed sim byte identity, the question filter and static output unchanged; the brand chrome needs a rewrite, which the owner accepts.
- alternatives: keep the custom build until the site is large (Claude's recommendation after the first spike, on the grounds that the brand chrome does not port; overruled by the owner); Astro (deferred in LEDGER 38, needs a JavaScript toolchain, shares no code with the current build).
- binds: LEDGER 28, LEDGER 37, LEDGER 38, LEDGER 39, LEDGER 51, tools/render.py, tools/check_unchanged.py, site/site.css
- corrected: 2026-09-30, proposed-by from claude to owner, the owner raised Quarto in chat (spec section 3, lab-ops ledger 25)
- corrected: 2026-09-30, ruled-by added, required for ruled entries and omitted when written

### D-0034  Build in GitHub Actions and host on Cloudflare
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-09-30
- decision: The site is built by a GitHub Actions workflow running the pinned Quarto version (D-0033), and the finished `build/site/` folder is uploaded to Cloudflare as a direct upload, so Cloudflare never runs the build. The deploy needs a Cloudflare API token scoped to deploy only, created by the owner and stored as a repository secret; no agent creates, reads or enters it. Which Cloudflare product (Pages or Workers static assets) is settled when the workflow is written. The Vercel project (LEDGER 40, 47) stays live until the Cloudflare site passes the test suite, then gets a redirect or a notice before it is switched off. Amends LEDGER 40.
- rationale: Owner direction in chat 2026-09-30: Vercel's hobby tier is not viable long term. Vercel's Hobby plan is for personal, non-commercial use (from memory, to be checked against Vercel's current terms before the cutover), and an OSU teaching site is arguably outside that. Building in Actions keeps the build visible and rerunnable by a successor and keeps LEDGER 39's "moving hosts is a settings change": the same folder can go to any static host.
- alternatives: stay on Vercel (plan terms); let Cloudflare run the build (ties the build to one host's environment and limits); GitHub Pages (not raised by the owner; also host-agnostic, and would avoid a second account).
- binds: LEDGER 39, LEDGER 40, LEDGER 47, .github/workflows/, CLAUDE.md Deploy section
- corrected: 2026-09-30, proposed-by from claude to owner, the owner raised GitHub Actions and Cloudflare in chat (spec section 3, lab-ops ledger 25)

### D-0035  Widen the stylesheet check in the Quarto suite
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-30
- decision: `test_stylesheets_resolve` in `tests/test_quarto_site.py` reads every `<link>` tag and checks each one with `rel="stylesheet"`, whatever order its attributes come in. The plan's verbatim regex required `rel` before `href`, so it checked 2 of the 6 stylesheet links on a lab page (8 site-wide) and skipped Quarto's own, which write `href` first. The widened check covers 6 and 32, and all resolve. The test's name, its subTest keys and its `data:` skip are unchanged. This edits a test written in the same PR (phase 1, PR 13) and widens what it checks; it loosens nothing and was not made to turn a failure green.
- rationale: A test named "stylesheets resolve" that ignores four of six links is vacuous, which the owner's "a repo must not lie about its verification" rule forbids. The final whole-branch review of PR 13 found it. The owner's rule is to fix the build and never a test; this was applied as a disclosed exception, and the owner confirmed it in chat on 2026-09-30 ("Keep the stylesheet test change").
- alternatives: keep the plan's verbatim regex (leaves four links per page unchecked); add a second test beside it (leaves a half-vacuous test in place); leave it to phase 2 (the gap would outlast the merge).
- binds: tests/test_quarto_site.py, D-0033
- corrected: 2026-09-30, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0035 to ruled")

### D-0036  Phase 2 page assembly: flat body, bare main, chrome lifted from the old templates
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-30
- decision: The Quarto build sets `section-divs: false`, `anchor-sections: false` and `wrap: auto`. After `quarto render`, `tools/quarto_build.py` dresses each page. Quarto's `<main class="content" id="quarto-document-content">` and the empty title-block header become a bare `<main>`. The chrome above `<main>` (draft banner, OSU header, the document nav) goes in right after `<body ...>`. The chrome below it (document footer or site footnote, OSU footer) goes in right after Quarto's `</div> <!-- /content -->`. The old page's body class is added to Quarto's. The chrome is not copied: it is lifted from `tools/template.html` and `tools/template-site.html`, rendered by Pandoc with an empty body and the same metadata the old build passes, so the old templates stay the one source of the chrome until phase 4. Each anchor must occur exactly once or the build fails.
- rationale: Owner ruled in chat 2026-09-30 ("Rule your way on all eleven and write the plan", covering critique questions 2 and 9). Probes on 2026-09-30 with Quarto 1.10.18: with the three settings, the content of `<main>` is byte-identical to the old build on both lab pages, and the SHA-256 values in `tests/fixtures/main-bodies.json` match once the tag is bare, so `test_bodies_unchanged` passes with no edit to the test or its fixture. The 12 phase 1 tests stay green under the settings. `include-before-body` lands inside `<main>` (probe), which would put the header inside the document body (D-0010) and in the wrong landmark. Without section wrappers, `main > *` is again the paragraphs and headings that D-0029's grid expects.
- alternatives: rule an edit to `test_bodies_unchanged` and a new fixture (weaker: it pins Quarto's output, not the old build's); `include-before-body` (inside `<main>`); copy the chrome markup into a new file (two copies that can drift until phase 4).
- binds: D-0010, D-0029, D-0033, _quarto.yml, tools/quarto_build.py, tools/template.html, tools/template-site.html
- test: tests/test_site_chrome.py::DocumentBodies::test_bodies_unchanged with SITE_DIR=build/quarto-site, tests/test_quarto_chrome.py::ChromeParity (written in phase 2)
- corrected: 2026-09-30, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0029 to D-0032, D-0036 to D-0042"; D-0041 excluded, which the owner said in the same message is not yet ruled)

### D-0037  One nav under Quarto; search off until ruled
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-30
- decision: `_quarto.yml` drops `website.navbar` and sets `search: false`. The OSU header's nav (D-0004) is the only navigation. Search comes back only by its own ruling, placed so it does not add a second nav.
- rationale: Owner ruled in chat 2026-09-30 (critique question 4). With both, every page would carry two navigation bars whose four labels are the same words kept in two files. Quarto's search needs a navbar or a sidebar to live in. Nothing uses `search.json` today.
- alternatives: keep Quarto's navbar and drop the OSU nav (its collapse needs script, and it leaves D-0004); keep both (two navs).
- binds: D-0004, D-0033, _quarto.yml
- test: tests/test_quarto_config.py, tests/test_quarto_chrome.py::Navigation (written in phase 2)
- corrected: 2026-09-30, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0029 to D-0032, D-0036 to D-0042"; D-0041 excluded, which the owner said in the same message is not yet ruled)

### D-0038  Carry the untested chrome word for word; drop the landing footnote under Quarto
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-30
- decision: The Quarto pages carry every piece of chrome the old build writes, including the pieces no test covered: the document nav (library home, "Course index", the "Read it ..." switch), the presentation note, the "Both presentations" paragraph, and the "How this was made" footnote. New tests pin them against the old build. The landing footnote, which says the site is built "with Pandoc and one build script", is not carried, because it is false under Quarto; phase 4 rewrites the method text.
- rationale: Owner ruled in chat 2026-09-30 (critique question 5). The phase 1 exit criterion treated the chrome suite as the whole contract, and it never covered these, so a build driven only by the failing tests would have dropped them, and `site/landing.md` ("Either page switches to the other at the top") would then be false. The wording comes from `tools/render.py` and the templates unchanged; no new copy.
- alternatives: supply new wording for the landing footnote now (owner copy, not needed to migrate); carry the false footnote (a page that misstates how it was built).
- binds: D-0033, tools/render.py, tools/template.html, tools/template-site.html, site/landing.md
- test: tests/test_quarto_chrome.py::ChromeParity (written in phase 2)
- corrected: 2026-09-30, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0029 to D-0032, D-0036 to D-0042"; D-0041 excluded, which the owner said in the same message is not yet ruled)

### D-0039  Logo stays embedded; Quarto publishes only the fonts and their license
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-30
- decision: The header logo stays a `data:` URI in every page, so `test_logo_unaltered_and_linked` passes unedited. `resources:` in `_quarto.yml` lists exactly the four Open Sans WOFF2 files and `site/fonts/OFL.txt`. The two README files and the logo PNGs are not published.
- rationale: Owner ruled in chat 2026-09-30 (critique questions 6 and 7). The embedded logo costs about 234 KB of base64 per page (175634 bytes times 4/3), so the migration plan's "page weight falls" does not hold for the logo. Once it is embedded, nothing references the PNG files, which were about 532 KB of the output. The OFL requires the license to travel with the fonts.
- alternatives: rule the logo test to accept a file reference (lighter pages, a test edit); publish the READMEs (maintainer notes on a public site).
- binds: D-0014, D-0020, D-0025, _quarto.yml
- test: tests/test_site_chrome.py::FullChrome::test_logo_unaltered_and_linked with SITE_DIR=build/quarto-site, tests/test_quarto_chrome.py::Published (written in phase 2)
- corrected: 2026-09-30, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0029 to D-0032, D-0036 to D-0042"; D-0041 excluded, which the owner said in the same message is not yet ruled)

### D-0040  Math renders as MathML
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-30
- decision: `_quarto.yml` sets `html-math-method: mathml`, pinned by a config test.
- rationale: Owner ruled in chat 2026-09-30 (critique question 8). Quarto's default loads MathJax from a CDN, which breaks D-0033's no-third-party condition. No page has math today, so the output scans cannot catch it; the pinned setting is the guard. A probe on 2026-09-30 rendered `$x^2$` as a `<math>` element with no script.
- alternatives: host a copy of MathJax in the repo (size and upkeep); `plain` (math unreadable).
- binds: D-0033, _quarto.yml
- test: tests/test_quarto_config.py (written in phase 2)
- corrected: 2026-09-30, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0029 to D-0032, D-0036 to D-0042"; D-0041 excluded, which the owner said in the same message is not yet ruled)

### D-0041  The footer test ignores script blocks when it looks for contact links
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-30
- decision: In `tests/test_site_chrome.py::FullChrome::test_footer_as_ruled`, the banned-string loop checks the page with every `<script ...>...</script>` block removed: `self.assertNotIn(banned, re.sub(r"<script\b.*?</script>", "", text, flags=re.S))`. Nothing else in the test changes. The old build has no script blocks, so the edit changes nothing there.
- rationale: Quarto 1.10.18 writes an inline script on every page containing `new RegExp(/^mailto:/)` (its external-link handler). Probes on 2026-09-30 with no options, with `link-external-filter`, and with `code-copy` and `code-link` off all still emitted it. A correct footer therefore fails the test on a string no reader sees. The test exists to keep contact links and a copyright line off the page (D-0023), and script text is neither. This narrows what the test reads; it is a disclosed test edit and needs its own ruling (owner ruling on critique question 3).
- alternatives: strip that script from every page in the post step (breaks Quarto's link handling); keep the chrome job non-blocking (the contract never gates).
- binds: D-0023, D-0033, tests/test_site_chrome.py
- corrected: 2026-09-30, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0041 to ruled")

### D-0042  Phase 2 exit: the chrome suite gates the Quarto build; no brand test dropped
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-30
- decision: Phase 2 merges when every test in `tests/test_site_chrome.py` passes against `build/quarto-site/`, and the same PR moves that run into the blocking `verify` job and deletes the non-blocking `chrome-on-quarto` job. No brand test is dropped. The only test edit in phase 2 is D-0041, and only if it is ruled.
- rationale: Owner ruled in chat 2026-09-30 (critique questions 10 and 11). Four of the five failing chrome tests pass with no edit under D-0036, D-0038 and D-0039; the fifth depends on D-0041.
- alternatives: keep the job non-blocking until phase 4 (the contract would not gate the build that becomes production).
- binds: D-0033, .github/workflows/verify.yml, tests/test_site_chrome.py
- corrected: 2026-09-30, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0029 to D-0032, D-0036 to D-0042"; D-0041 excluded, which the owner said in the same message is not yet ruled)

### D-0043  The driver strips Quarto's search leftovers after render
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-30
- decision: After `quarto render`, `tools/quarto_build.py` removes the `quarto-search-options` script and the `quarto-search-results` div from every page Quarto wrote, and deletes `search.json`. The strip is strict: a page that lacks either fragment, or has two of either, fails the build. D-0037's config stays (`search: false`, no navbar).
- rationale: Quarto 1.10.18 ignores `website.search: false`: the search markup is on every page, `search.json` is written, and no search library lands in `site_libs`. Found in phase 2 Task 1. The owner chose this route in chat on 2026-09-30 when given three options (strip after render; find another Quarto switch; re-rule D-0037). D-0037 and its tests forbid the leftovers.
- alternatives: a template-partial override or another config key (not probed: it needs Quarto's install folder, outside the repo); re-rule D-0037 to accept inert markup (needs an owner amendment of the tests).
- binds: D-0037, D-0033, tools/quarto_build.py
- test: tests/test_quarto_strip.py, tests/test_quarto_chrome.py::Navigation
- corrected: 2026-10-01, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0043 confirmed")

### D-0044  One Pandoc: the word check, the chrome lift and the tests use Quarto's bundled Pandoc
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-30
- decision: In CI and locally, `PANDOC` is the Pandoc binary bundled with the pinned Quarto (Pandoc 3.10 under Quarto 1.10.18). `tests/test_one_pandoc.py` asserts that the first line of `"$PANDOC" --version` equals that of `"$QUARTO" pandoc --version`; a missing `PANDOC` or `QUARTO` fails the test. Pandoc changes version only with a Quarto upgrade, in that upgrade's own PR. Amends LEDGER 20 ("Pandoc 3.11") for every use except the old build (D-0046).
- rationale: Phase 3 of `docs/quarto-migration-plan.md`. Probes on 2026-09-30: Quarto 1.10.18 bundles Pandoc 3.10, not 3.11, so the Quarto pages' bodies already render with 3.10 while the word check reads with 3.11. Under 3.10 the Team Building handout's syntax tree equals 3.11's (blocks and meta), the word check prints the same result (989 words identical, bold identical on 943), and both builds are byte-identical when the bundled binary writes to files.
- alternatives: keep the standalone 3.11 for everything (the word check reads with a different Pandoc than the Quarto pages render with); install a standalone 3.10 to match (a second copy that drifts at each Quarto upgrade); compare against a literal "3.10" (a second pin to move in lockstep).
- binds: LEDGER 20, D-0033, .github/workflows/verify.yml, CLAUDE.md
- test: tests/test_one_pandoc.py::test_pandoc_is_quartos, tests/test_quarto_config.py::Version::test_ci_uses_quartos_pandoc
- corrected: 2026-10-01, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0044 to D-0046"); the plan's seven calls were ruled the same day as leaned
- corrected: 2026-10-01, test line updated: both tests were written and merged in phase 3 (PR #15); they replace "to be written in phase 3"


### D-0045  The tools call Pandoc as one binary, never through `quarto pandoc`
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-30
- decision: `PANDOC` names an executable, and the tools keep calling `[PANDOC, ...]` unchanged. `quarto pandoc` appears only in the version test, for its one-line `--version` output.
- rationale: Probe on 2026-09-30, Windows: a standalone `--embed-resources` render of the logo through `quarto pandoc` returned 178,569 bytes on stdout in each of three runs, where the same command with `-o` wrote 243,174. Through that route the chrome lift cut the logo's data URI out of five Quarto pages and `tests/test_quarto_dress.py::OldChrome::test_document_page` failed. Each call also costs about half a second more (one word check 1.0 s against 1.5 s; the old site build 6.4 s against 10.4 s). The Linux behavior of the stdout route was not probed, and the cause was not traced (Quarto's install folder is outside the boundary).
- alternatives: accept a command in `PANDOC` and route every captured call through a temp file (seven call sites, slower, and one missed `-o` silently cuts output).
- binds: D-0044, tools/check_unchanged.py, tools/render.py, tools/quarto_chrome.py
- test: tests/test_quarto_dress.py::OldChrome::test_document_page (existing; it failed under the stdout route in the probe)
- corrected: 2026-10-01, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0044 to D-0046"); the plan's seven calls were ruled the same day as leaned


### D-0046  The old build keeps its production Pandoc until phase 4
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-09-30
- decision: Until phase 4 retires the old build, the CI step "Site builds" runs `tools/render.py --site` with the standalone Pandoc 3.11, the version the Vercel build command downloads for production. The 3.11 install step stays, scoped to that step and to `test_old_build_pandoc_reads_the_same_tree`, which asserts that `PANDOC` and `PANDOC_OLD_BUILD` read every converted file to the same syntax tree. Phase 4 deletes the install, the variable and the test with the old build. Amends phase 3's "The separate Pandoc 3.11 install step goes" in `docs/quarto-migration-plan.md`.
- rationale: Production is built by the Vercel project setting with Pandoc 3.11 (CLAUDE.md, Deploy). Removing 3.11 from CI would leave "Site builds" verifying production's pages with a Pandoc production does not use. Probe on 2026-09-30: the old build is byte-identical under 3.10 and 3.11 (9 files), but nothing would keep it so; the tree test does, for the word check's half.
- alternatives: remove 3.11 now as the plan says (CI and production toolchains split, unguarded); change the Vercel build command to Pandoc 3.10 (a production setting change on a host being retired; the 3.10 download URL not verified); defer all of phase 3 into phase 4 (the word check keeps reading with a different Pandoc than the Quarto pages for two more phases).
- binds: D-0044, LEDGER 20, LEDGER 49, .github/workflows/verify.yml, docs/quarto-migration-plan.md
- test: tests/test_one_pandoc.py::test_old_build_pandoc_reads_the_same_tree
- corrected: 2026-10-01, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0044 to D-0046"); the plan's seven calls were ruled the same day as leaned
- corrected: 2026-10-01, test line updated: the tree test was written and merged in phase 3 (PR #15); it replaces "to be written in phase 3". Phase 3 as built sets PANDOC to the standalone Pandoc in "Site builds" and PANDOC_OLD_BUILD in "Tests" only (the decision's "scoped to that step and to the tree test" holds)
- corrected: 2026-10-02, superseded by D-0061 as built in phase 4 (spec call 7): the 3.11 install, "Site builds", `PANDOC_OLD_BUILD` and the tree test were deleted with the old build, as this entry said they would be; the entry is kept as the record of why they existed

### D-0047  Host on Cloudflare Pages as a Direct Upload project, from the Quarto build's folder
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-01
- decision: The site is hosted as a Cloudflare Pages project of the Direct Upload type, named `osu-physics-lab-library` if the name is free. What is uploaded is the folder `_quarto.yml` names as `output-dir` (`build/quarto-site/` today), never `build/site/`, which is the old build until phase 4 deletes it. Resolves D-0034's open choice between Pages and Workers static assets in favor of Pages. The account that holds the project is the owner's, until ruled otherwise; the successor path is to copy the repo and make their own project, never to hand over the account. Corrects phase 5's and D-0034's `build/site/` to the Quarto build's folder.
- rationale: Pages is the documented path for uploading a prebuilt folder from CI (Cloudflare, "Use Direct Upload with continuous integration": token permission Account, Cloudflare Pages, Edit; `pages deploy <directory> --project-name`). It needs no committed config, so LEDGER 39 and 49 hold. Cloudflare's own migration page calls moving to Workers optional and states no Pages end date (checked 2026-10-01); the wording "successor for new projects" in an earlier draft of this entry came from third-party posts and is withdrawn. The owner confirmed on 2026-10-01 that the dashboard offers a Pages Direct Upload project.
- alternatives: Workers static assets (a config file or extra flags, a token permission not verified here); GitHub Pages (D-0034's alternative, no second account); staying on Vercel (its Hobby terms count "a paid employee or consultant writing the code" as commercial use, Vercel Fair Use Guidelines dated 2026-09-14).
- binds: D-0034, LEDGER 39, LEDGER 40, LEDGER 49, _quarto.yml, CLAUDE.md Deploy section
- test: tests/test_deploy_workflow.py (to be written in phase 5)
- corrected: 2026-10-01, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0047 to D-0053")

### D-0048  A separate deploy job ships the tested folder; secrets live in that job only
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-01
- decision: `.github/workflows/verify.yml` gains a `deploy` job with `needs: verify`. `verify` uploads the folder it tested as an artifact; `deploy` downloads that folder and runs `npx wrangler@<exact version> pages deploy` directly, with no third-party action. Only `deploy` names `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`. A push to `main` deploys production; a pull request from this repository deploys a preview; a fork's pull request deploys nothing. The wrangler version is exact and pinned by a test, chosen at build time from the registry. No `wrangler.*`, `_redirects`, `_headers` or `vercel.json` is committed.
- rationale: The deployed bytes are the tested bytes, and the job that runs the test code never sees the token. Previews keep the habit of reviewing on a phone before merging, which Vercel's previews give today. A fork's pull request gets no secrets in GitHub Actions.
- alternatives: deploy steps at the end of `verify` (secrets beside all the test code, folder rebuilt); Cloudflare's GitHub Action (a third-party action on the token's path, maintenance status not checked); `main` only (no preview before merge).
- binds: D-0047, D-0044, LEDGER 39, LEDGER 49, .github/workflows/verify.yml
- test: tests/test_deploy_workflow.py (to be written in phase 5)
- corrected: 2026-10-01, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0047 to D-0053")

### D-0049  The cutover gate is the live URL served byte for byte; Vercel gets a redirect before phase 4
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-01
- decision: D-0034's "until the Cloudflare site passes the test suite" means: the folder that passed `verify` is the folder deployed, and `tools/check_deployed.py` then finds against the live URL that every file is served with identical bytes (the directory URL for an `index.html`), that a path not in the folder returns 404, and that `robots.txt` and the `noindex` meta are present; then the owner's phone check and the Lab 1 print preview, which has never been done. The site gains a `404.html` through the same chrome, because Pages answers unknown paths with the landing page when it is absent (Cloudflare, "Serving Pages"); its wording is the owner's and is a placeholder until approved. After the check, the old Vercel URL gets a redirect set as a project setting, not a file in the repo, before phase 4 merges, because Vercel's production build runs the old build's page assembly that phase 4 deletes. Pausing or deleting the Vercel project is the owner's word alone.
- rationale: The suite reads folders, not URLs, so it cannot see a host that rewrites HTML; Cloudflare's Email Address Obfuscation injects a script on regular zones and whether it applies on `pages.dev` was not found, and the footer carries contact links. The byte check answers it directly.
- alternatives: the suite alone (a rewrite by the host is invisible); a notice page on the old build (code that phase 4 deletes, and a click for every visitor); no 404 page (every dead link returns the landing page with a 200).
- binds: D-0034, D-0047, D-0048, LEDGER 37, LEDGER 49, LEDGER 53, docs/quarto-migration-plan.md
- test: tests/test_check_deployed.py (to be written in phase 5)
- corrected: 2026-10-01, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0047 to D-0053")

### D-0050  The project name is a repository variable; a hand-run workflow creates the project; production is checked at its alias
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-01
- decision: Amends D-0048. The Cloudflare Pages project name is read from the repository variable `CLOUDFLARE_PAGES_PROJECT`, never a literal in a workflow; it is `osu-physics-labs` (interim `osu-physics-labs.pages.dev`), set on the owner's word, and a job with the variable unset fails. The project lives in the owner's own Cloudflare account (owner's fact, 2026-10-01; call 2). The project is created once by `.github/workflows/create-pages-project.yml`, started by hand only, which runs the pinned `wrangler pages project create` with `--production-branch=main`; it is the second and last place that names `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`. On a push to `main`, the deploy job runs `tools/check_deployed.py` against the deployment's own URL and against the production alias `https://<project>.pages.dev/`.
- rationale: The owner ruled the variable and the name in chat on 2026-10-01, and chose this creation route over a dashboard upload and a local wrangler run. Cloudflare's dashboard creates a Direct Upload project only with a first upload (Cloudflare, "Direct Upload", fetched 2026-10-01 through a summarizing tool), whose production branch the page does not state; a project whose production branch is not `main` would take every merge as a preview while the alias kept serving the first upload, and a check against the deployment URL alone would pass. The workflow sets the branch explicitly, keeps the token in GitHub, and is the successor's first step in their own account.
- alternatives: dashboard drag and drop of a local build (live before the gate, production branch unstated); `wrangler pages project create` on the owner's machine (needs `wrangler login`, an OAuth sign-in not ruled, or the token on disk; and inside an agent session wrangler 4.146.0 delegates a create to Workers); creating the project from the deploy job when it is missing (any pull request could create a stray project).
- binds: D-0047, D-0048, D-0049, LEDGER 39, LEDGER 49, LEDGER 53, .github/workflows/create-pages-project.yml, .github/workflows/verify.yml
- test: tests/test_create_project_workflow.py; tests/test_deploy_workflow.py (PR #17)
- corrected: 2026-10-01, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0047 to D-0053")

### D-0051  The three GitHub actions move to their current majors after the cutover, pinned by major tag and by test
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-01
- decision: After PR #17 merges and the cutover is checked (Task 3), one PR moves `actions/checkout` from v4 to v7, `actions/upload-artifact` from v4 to v7 and `actions/download-artifact` from v4 to v8, in every workflow. They stay pinned by major tag, and a test asserts each action's major so an accidental change fails. `download-artifact` v8's default of failing on a hash mismatch is kept.
- rationale: The owner approved all three leans in chat on 2026-10-01. GitHub annotates every run that the v4 actions target the deprecated Node.js 20 and are forced onto Node.js 24; each current major declares `runs.using: node24` (each action's `action.yml` at v7.0.1, v7.0.1 and v8.0.1, read 2026-10-01). Doing it after the cutover keeps the first production deploy on the toolchain already tested, and keeps two open PRs from editing `verify.yml` at once. Release notes read 2026-10-01: `download-artifact` v5 changes paths only for downloads by ID (this repo downloads by name); v8 errors on a hash mismatch by default, which strengthens D-0048's "the deployed bytes are the tested bytes"; `upload-artifact` v7 adds unzipped single-file uploads (unused here). `checkout` v6 and v7 notes were not read in full and are to be read before building.
- alternatives: now, inside or beside PR #17 (two changes in one cutover); full commit SHA pins (stronger on the token's path; unreadable lines and a manual bump per patch, while `test_only_actions_org` already restricts the workflows to `actions/*`); turning the v8 hash check off (weakens D-0048).
- binds: D-0048, D-0050, .github/workflows/verify.yml, .github/workflows/create-pages-project.yml
- test: tests/test_deploy_workflow.py (to be extended in that PR)
- corrected: 2026-10-01, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0047 to D-0053")

### D-0052  Lab downloads in Word, HTML and PDF, one set per lab, each carrying the draft banner, before the license question
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-01
- decision: Each converted lab page gets downloads in three formats, one set per document (not per presentation), generated from the one Markdown source (LEDGER 28): Word by Pandoc through Quarto's `format-links`, never the original `.docx`; HTML as a fully self-contained page (fonts and logo embedded, opens offline); PDF as the lab page printed by headless Chrome with the site's print rules, run directly with no third-party action. Every file carries the draft banner text. Tests require all three files per lab, non-empty, with the banner text, and links that resolve; `check_deployed.py` covers them on deploy as it covers every file. Built in the Quarto build only (production since the phase 5 cutover), so it does not wait on phase 4; D-0016 already rules OSU icons on download cards.
- rationale: The owner needs downloads for a demo and ruled that they come before the license question, in Word, HTML and PDF (chat, 2026-10-01), then approved all six leans. The PDF matches the print previews the owner approved the same day (Lab 1, both presentations). The original `.docx` may carry comments, tracked changes or authors' names in its metadata and would need vetting. A downloaded file leaves the unlisted site, where `noindex` and `robots.txt` do not follow it; only text inside the file does, so the banner is what keeps "not for distribution" true for a file handed out at a demo.
- alternatives: a set per presentation (six files a lab; Word cannot carry the CSS presentations); Typst, bundled with Quarto, for the PDF (a third look needing its own styling); the original `.docx` (unvetted metadata); downloads after the license question (misses the demo). Not verified: that GitHub's Ubuntu runner has Chrome preinstalled; to be checked before the plan relies on it.
- binds: D-0016, D-0033, D-0047, LEDGER 28, LEDGER 37, LEDGER 51, _quarto.yml, tools/quarto_build.py
- test: to be written with the downloads plan
- corrected: 2026-10-01, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0047 to D-0053")

### D-0053  Every download comes from the modern presentation, and Markdown is a fourth format
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-01
- decision: Amends D-0052. All downloads come from the modern presentation: the HTML, the PDF (headless Chrome printing the modern page with the print rules) and the Word file (modern question labels, Pandoc's default Word styles). No download is offered for the faithful presentation. The source Markdown is a fourth download, byte for byte. The approved wording is "Download: Word · HTML · PDF · Markdown" in the lab page's `site-nav` bar, and the lab footer's "Downloads (Markdown, Word, PDF) are not wired up in this draft." becomes "Downloads carry the same draft notice as these pages." The other calls of `docs/superpowers/plans/2026-10-01-downloads.md` are ruled as leaned.
- rationale: The owner ruled this in chat on 2026-10-01: the faithful styling is expected to be retired, so a download for it is not worth offering now; Markdown costs nothing, since the file exists, and the footer already promised it. The retirement of faithful is the owner's stated expectation, not a ruling, and this entry does not change the faithful pages.
- alternatives: PDF from faithful (the lean; a look slated for retirement); downloads for both presentations (eight files a lab); no Markdown (the footer's promise dropped).
- binds: D-0052, LEDGER 28, tools/template.html, docs/superpowers/plans/2026-10-01-downloads.md
- test: to be written with the downloads plan (tests/test_downloads.py)
- corrected: 2026-10-01, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0047 to D-0053")

### D-0054  Downloads carry no site chrome; the department is named in words in every file
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-01
- decision: Amends D-0053's call 5 (the HTML download's chrome) and adds a line to every download. The HTML download is the source rendered by Pandoc through `tools/template.html` with only the banner variables set: the draft banner, then the line "Department of Physics, Oregon State University", the modern theme and the site's modern footer note, everything embedded; no header, logo, nav or policy footer. Every download names the department in those words in place of the logo: the HTML as its first line, the Word file in its page footer beside "Page N of M" (from `tools/reference.docx`, made once by `tools/make_reference_docx.py` from Pandoc's own default reference, adding only the footer), and the PDF in the print footer, through `@bottom-left` in `site/site.css`'s `@page` rule, which site printouts share. The PDF is otherwise as D-0053 rules: the built modern page printed, whose print rules already hide the header and footer. The HTML download is capped at [180000] bytes, measured 161,024 for Lab 1 times 1.10. The department line names where the lab comes from; it is not a copyright line and asserts no ownership (D-0023).
- rationale: The owner ruled each part in chat on 2026-10-01: the policy links and absolute links are not needed in a download, a link inside a lab's own text works on its own, the logo is not needed if the department is named in words, and the line belongs in every download, including the PDF, because downloads get printed. A probe showed the plain render at 161,024 bytes with no network reference, against about 0.9 MB for the built page made self-contained by regex (`standalone()`, deleted with its 11 unit tests). Searches of the record and of OSU's sites found no OSU rule requiring the policy links; D-0009 chose them to mirror the Physics footer, so the site footer keeps them and the downloads need not.
- alternatives: the built page made self-contained (`standalone()`: about 0.9 MB and regex to keep); the full chrome with absolute links to production (puts the unlisted address in every handed-out file, ledger 37, and bakes in today's host); the logo embedded in the Word body (crosses D-0010, about 234 KB a file); a Word footer by tab-aligned pair (Pandoc's default reference has no page size, so the tab position would be a guess).
- binds: D-0009, D-0010, D-0023, D-0052, D-0053, site/site.css, tools/downloads.py, tools/reference.docx, tools/make_reference_docx.py
- test: tests/test_downloads.py (Html, MarkdownAndWord::test_word_footer_names_the_department_and_counts_pages, Pdf::test_banner_running_header_title_and_footer)
- corrected: 2026-10-01, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0054 to D-0056")

### D-0055  Retire the top-chrome parity test; publish exactly the Markdown downloads
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-01
- decision: `tests/test_quarto_chrome.py::ChromeParity::test_top_chrome_matches_old_build` is deleted. `Published::test_no_markdown_published` becomes `test_only_markdown_downloads_published`: the Quarto build publishes exactly `labs/<id>/<id>.md` for each converted lab and no other Markdown.
- rationale: The owner ruled the deletion in chat on 2026-10-01. The download row is Quarto-only (D-0052), so the old build's top chrome is no longer a prefix of a modern lab page's; with the row removed the assertion held, measured. The test was the cutover's gate; the cutover is done and phase 4 deletes the old build. Bottom-chrome parity, the body-class check and the chrome contract (D-0042, `tests/test_site_chrome.py`, whose tests were edited, none dropped) stay. The Markdown guard still has a job, catching a leaked source or instructor file, so it is narrowed to the ruled downloads, not deleted.
- alternatives: amend the parity test to strip the row (new parts for a test with weeks to live); give the old build the row (dead links in a build that writes no downloads); delete the Markdown guard (loses the leak check).
- binds: D-0036, D-0042, D-0053, tests/test_quarto_chrome.py
- test: tests/test_quarto_chrome.py::Published::test_only_markdown_downloads_published
- corrected: 2026-10-01, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0054 to D-0056"); the test: line, missing when proposed, added at promotion

### D-0056  Publish the header logo once and reference it from every page
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-01
- decision: Amends D-0039. The header logo is a relative reference to one published file, `site/brand/OSU_horizontal_2C_W_over_B.png`, instead of a `data:` URI in every page. `tools/brandheader.html` marks it `data-external="1"` so `--embed-resources` leaves it alone; `_quarto.yml` publishes the one PNG, and `tools/render.py --site` copies it. Sims keep their own embedded logo (D-0026). `test_logo_unaltered_and_linked` requires the reference to resolve to a file whose SHA-256 is the official PNG's.
- rationale: The owner ruled it in chat on 2026-10-01, because the library is about to grow by many lab pages. An embedded logo is about 234 KB of base64 in each page that no browser cache can share; a file is fetched once. Measured: the Quarto modern lab page fell from 261,916 to 28,149 bytes and the landing page from 256,206 to 22,015.
- alternatives: keep it embedded (D-0039 as ruled; about 234 KB a page view).
- binds: D-0014, D-0020, D-0026, D-0039, _quarto.yml, tools/brandheader.html, tools/render.py
- test: tests/test_site_chrome.py::FullChrome::test_logo_unaltered_and_linked (both builds), tests/test_quarto_config.py::Pins::test_resources_exact, tests/test_quarto_chrome.py::Published
- corrected: 2026-10-01, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0054 to D-0056")

### D-0057  The Word download's page and styles: header, footer size, Letter, spacing, question box
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-01
- decision: Amends D-0053 (Pandoc's default Word styles) and D-0054 (the Word footer). `tools/make_reference_docx.py` makes `tools/reference.docx` from Pandoc's default reference with five changes. A page header on every page holds `render.BANNER_MAIN`, the approved words only, in a Header style at [9] pt bold, centered (the size and weight of the PDF's banner box); it replaces the banner's two body paragraphs, so `BANNER_DETAIL` leaves the Word file as it leaves the PDF's print, and the header goes when the license settles (ledger 37). The footer paragraph names a Footer style at [8] pt and no run in the footer sets a size. The section is Letter, [12240] by [15840] twips, with [1080] twip (0.75 in) margins on every side, from `site/site.css`'s `@page`. Pandoc's Body Text and Compact styles take the modern page's spacing (`themes/modern.css`): lines at least [1.6] times Word's 12 pt body, nothing before, and after a paragraph or a list item the page's 1rem and .5rem taken over its 1.0625rem body (226 and 113 twips); headings keep Pandoc's spacing, because the course line under the title is a Heading 2 in Word and the page's space above an h2 would open a gap under the title. Two paragraph styles, Question Label and Question, carry the modern page's question block: its Beaver Orange rule down the left and its tint behind, with one border, shading and indent shared so Word draws one box across both, the page's padding as the borders' distance from the text; the label in capitals in Rogue Wave; the question text not bold (ledger 29); both keep with the next paragraph and keep their lines, so a question stays whole and stays with the first lines of what follows; Question's next style is Body Text, so Enter after a question starts plain text. `tools/filters/questions.lua` names the two styles for Word output only, since any other output would carry the name into the page as an attribute (D-0010; `test_bodies_unchanged`). Headings already keep with the next paragraph in Pandoc's default styles; a test pins it. Not built: a style for the legend box and an arrow for hints, so in the Word file the legend's "Items with an arrow" and "Boxed information" still describe nothing. The tests read the file's XML; what Word shows is checked by the owner in Word. Disclosed test edit: `test_word_is_banner_then_the_modern_words` became `test_word_body_is_the_modern_words`, because this decision moves the banner out of the body.
- rationale: The owner found the Word file wrong in three ways (chat, 2026-10-01): page numbers far larger than the footer text, no page header, and questions neither bold nor boxed. Students fill in the Word file today, about 2,000 a term (owner, same chat). The owner ruled the design pass's calls as leaned ("Rule your way on all of them and build it", chat 2026-10-01). The 8 pt sat only on the cached field results; the footer paragraph had no style and the document default is 12 pt, which matches what the owner saw (inference: Word's rebuild was not observed here). Without a page size, pagination depended on each copy of Word. Probe on 2026-10-01 with Pandoc 3.10: a reference file's section properties reach the output; nested `custom-style` gives the label and the question their own styles; a `custom-style` on the box's Div styles its three paragraphs but not its two list items, so a box style would draw two pieces with the lists outside them. The hint arrow would be a character written into the text by the filter, since Pandoc chooses bullet glyphs itself, and whether students' Word fonts have it was not checked. The owner opened the first build in Word (chat, 2026-10-01): the draft notice at the top of every page, the footer numbers at the footer text's size, the left rule and the capitals label, no heading alone at a page foot, and Enter after a question giving plain text, all as intended; he found the line spacing tighter than the HTML page's and asked for the questions as a highlighted box like the page's, which the spacing and the box above carry. The spacing is "at least" a fixed proportion of the body size because Word's "single" depends on the body font's own line metrics (Aptos, Pandoc's default theme font), which were not read here.
- alternatives: drop "Page N of M" from Word (the bug goes by deletion; printed Word pages unnumbered while the PDF's are numbered); the MERGEFORMAT switch (relies on Word keeping a cached result's formatting, which is what failed); the header at 8 pt on the right like the PDF's running header (quieter); the PDF's print look for questions, a black rule only (the first build; the owner found it distinct but not prominent enough); bold for questions (the faithful look D-0053 left out); Word's "multiple" line spacing (the result depends on the font's metrics, not read); the page's heading spacing (a gap under the title, above); a box style for the legend box (a broken box, per the probe); an exact keep with a third style for a question's last paragraph (no converted lab has a question of more than one paragraph).
- binds: D-0052, D-0053, D-0054, LEDGER 29, LEDGER 37, tools/make_reference_docx.py, tools/reference.docx, tools/filters/questions.lua, tools/downloads.py
- test: tests/test_downloads.py::MarkdownAndWord (test_word_body_is_the_modern_words, test_word_header_is_the_draft_notice, test_word_footer_size_is_on_the_style, test_word_page_is_letter_with_the_print_margins, test_word_questions_have_their_own_styles, test_word_question_styles_are_the_modern_box, test_word_spacing_follows_the_modern_page, test_word_headings_keep_with_next)
- corrected: 2026-10-02, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Yes, D-0057 to D-0059 are promoted.")

### D-0058  The PDF's keep rules stay in the theme, pinned by a print test
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-01
- decision: No CSS is added for the PDF. Question blocks and boxes stay whole and headings stay with what follows by the print rules already in place: `themes/modern.css` (`.question, .box { break-inside: avoid; }` and `h1, h2, h3 { break-after: avoid; }`) and `site/site.css`'s heading rule. `tests/test_downloads.py::PrintKeeps` prints the built modern page from a temporary copy (a `<base>` points it at the build, so nothing is written into the folder that deploys) with a spacer at the top of `<main>` at five offsets, and asserts that nothing splits with the rules on and that something splits with them switched off, which proves the offsets still cross a page break in the environment running the test.
- rationale: The owner ruled the lean ("Rule your way on all of them and build it", chat 2026-10-01). Lab 1's PDF as printed puts no heading or question near a page break, so it could not show whether the rules work. Probe on 2026-10-01: 40 prints with a spacer from 0 to 975 px in 25 px steps, no split with the rules on and 50 with them off. Copying the rules into `site/site.css` would repeat them in a file that, by its own comment and D-0010, does not restyle document content.
- alternatives: the same rules in `site/site.css` (a duplicate across the D-0010 line); no test (the rules unguarded); a check that the CSS text exists (proves only that the text exists).
- binds: D-0010, D-0053, themes/modern.css, site/site.css
- test: tests/test_downloads.py::PrintKeeps
- corrected: 2026-10-02, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Yes, D-0057 to D-0059 are promoted.")

### D-0059  The download row's four formats are buttons
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-01
- decision: Amends D-0053's rendering of its approved wording: the label "Download:" and the four names stay, and the middots go, since the gaps between buttons separate the names. Each link is the landing hero's primary button (D-0031) at nav scale: Beaver Orange, white bold text at 16 px, [44] px tall, all four of equal weight. The rules sit in `site/site.css`'s quarto-only block, scoped to `.quarto-light`; `tools/template.html` gains class names only inside `$if(downloadid)$`, which the old build and the HTML download never set, so neither changes, and print already hides the nav. Below 40rem the label takes its own line and the four buttons share one row. Measured on the built Lab 1 page on 2026-10-01: at 375 px the `site-nav` grows from 118 to 170 px and the title's top moves from 418 to 470 px, the buttons are 59 to 115 px wide and 44 px tall, and nothing scrolls sideways; at 1440 px the `site-nav` grows from 59 to 73 px. White on the orange is 4.56:1; the orange against the page is 4.56:1 in the light scheme and 3.91:1 in the dark one; hovering keeps white on orange under Bootstrap. No format is made primary: which file students use is the owner's open question on how handouts are completed.
- rationale: The owner found the control too small to find on a site whose purpose is the download (chat, 2026-10-01) and ruled the lean, option A of the mockups in `docs/design/2026-10-01-download-control/` ("Rule your way on all of them and build it", chat 2026-10-01). One tap per file, no hidden state, and no new element: class names and CSS on the links that were there.
- alternatives: option B, one Download button opening a `<details>` list (stays open until its button is tapped again; covers the title at 375 px when open; the `popover` attribute, which closes on an outside tap without script, leaves the downloads unreachable in a browser without it); a Star Canvas fill (the button computes about 1.5:1 against the dark page, so it would need a dark-mode border); Word as the one primary button (presumes the owner's open question).
- binds: D-0031, D-0052, D-0053, D-0055, tools/template.html, site/site.css
- test: tests/test_downloads.py::Links (test_modern_page_links_every_download, test_approved_wording; both edited with the ruled markup and wording), tests/test_quarto_chrome.py::QuartoOnlyCss::test_download_buttons
- corrected: 2026-10-02, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Yes, D-0057 to D-0059 are promoted.")

### D-0060  The production alias check waits for the switch; the deployment URL is checked once
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-02
- decision: Amends D-0050's alias check. `tools/check_deployed.py` gains `--wait SECONDS`. With it, the whole D-0049 check (every file byte for byte, the 404 path, `robots.txt`, `noindex`) is run again every [5] s until one complete run passes or [120] s have passed since the first began; a pass prints the attempt count and the seconds taken, so every run measures the lag; a failure prints the last run's failures. Only the step "Production serves the tested bytes at its alias" passes `--wait`; the deployment-URL step stays one run. Nothing in D-0049 is loosened: a pass is still one complete run in which every file matched. The Word and PDF files keep their build-time dates. Disclosed test edit: `tests/test_deploy_workflow.py::test_production_alias_checked_on_main` will require `--wait` on the alias step and `test_checks_the_deployed_url` its absence on the other.
- rationale: Measured 2026-10-02 from CI logs. Two of the seven `main` runs since the downloads landed failed the alias step (`f8173c8`, `aab70bd`); the deployment-URL step passed in all seven on its first run. The failed runs' alias checks ran 2.2 to 4.2 s and 3.5 to 7.0 s after wrangler's "Deployment complete"; the passing runs' ran about 2 to 3 s after. In `f8173c8` the alias served a Word file of 14,741 bytes, the size of the previous deployment's (`317b31a`, from CI's artifact), against the tested 14,742: the alias was still on the previous deployment. Between two builds of the same source the only differences are the Word file's dates (`docProps/core.xml` and every zip entry's stamp) and 8 bytes of the PDF's `/CreationDate` and `/ModDate` (CI artifacts of `317b31a` and `f8173c8`). Before the downloads every file rebuilt byte-identical, so a slow switch was invisible. Fixing the dates alone would not fix the check: a commit that changes any page meets the same lag, and two such commits (`bbfa9b6`, `6ee86ee`) passed with the switch ahead of the check. The [120] s bound is chosen, not measured; the longest lag seen is over 7 s and its upper end is unknown, which the logged attempts will show. A fault the wait could hide (a production branch other than `main`) still fails, after the bound.
- alternatives: drop the Word and PDF files from the alias half (fixes docs-only commits only; production's downloads unchecked at the address students use; a content commit still meets the lag); delete the alias step (D-0050's guard against a wrong production branch goes); fixed dates in the files (Pandoc 3.10 honors `SOURCE_DATE_EPOCH` for docx, probed: two builds 2 s apart byte-identical; headless Chrome does not, probed, and `Page.printToPDF` has no metadata parameter, so the PDF needs a same-length rewrite of its two dates after printing; the epoch would come from the source's last commit, which needs `fetch-depth: 0` in `verify` and a build that fails on a shallow clone; alone it leaves content commits flaky, and with the wait it buys byte-identical downloads across builds, worth having if the course archive wants "unchanged means identical"); a wait on the deployment URL too (that URL passed on its first run every time; a retry there would hide a real fault).
- binds: D-0049, D-0050, tools/check_deployed.py, .github/workflows/verify.yml
- test: tests/test_check_deployed.py (to be written: a local server that serves the old bytes for its first requests passes with `--wait` and fails without; one that never switches fails when the bound passes), tests/test_deploy_workflow.py (edited as disclosed)
- corrected: 2026-10-02, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Rule D-0060, D-0061 and the download-all calls as leaned; the words are fine pending the preview.")


### D-0061  Phase 4 retires the old build and keeps the templates
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-02
- decision: Amends the phase 4 text of `docs/quarto-migration-plan.md` and supersedes D-0046 when built. Phase 4 deletes `tools/render.py`'s site and file modes and the functions only they use, `build/site/`, CI's Pandoc 3.11 install and "Site builds" step, `PANDOC_OLD_BUILD`, `test_old_build_pandoc_reads_the_same_tree`, the three old-build comparisons in `ChromeParity`, and `test_pages_embed_the_font`; the chrome contract defaults to `build/quarto-site/` and runs inside "Tests". It keeps `tools/template.html`, `tools/template-site.html` and the brand partials (D-0036, D-0054), `render.py` under its name with the functions the Quarto build imports, the `quarto-only` CSS block (the HTML download is its second consumer), and `test_bodies_unchanged` with its fixture. Before the comparisons go, direct tests pin D-0038's pieces by their words and the body class on every page. The design and its seven calls are `docs/superpowers/specs/2026-10-02-quarto-phase-4-design.md`.
- rationale: The plan's text deletes the templates that the Quarto chrome and the HTML download are now built from. The old build feeds only CI's comparisons and the retired Vercel project. D-0038's untested chrome pieces are guarded today only by those comparisons, so deleting them bare would leave ruled chrome unchecked while the repo still claimed it.
- alternatives: the plan as written (breaks the Quarto build and the HTML download); keep the old build for comparison only (a second Pandoc for a reference production does not serve); port the chrome to Quarto partials so the templates can go (a rewrite of working chrome).
- binds: D-0036, D-0038, D-0042, D-0046, D-0054, docs/quarto-migration-plan.md, tools/render.py, .github/workflows/verify.yml, tests/test_one_pandoc.py, tests/test_quarto_chrome.py, tests/test_quarto_config.py, tests/test_fonts.py, tests/test_site_chrome.py
- test: to be written with phase 4 (the D-0038 pins in tests/test_quarto_chrome.py)
- corrected: 2026-10-02, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Rule D-0060, D-0061 and the download-all calls as leaned; the words are fine pending the preview.")


### D-0062  Scan the full history before the repo goes public; start fresh only as the fallback
- status: proposed
- proposed-by: owner
- date: 2026-10-02
- decision: Before the repo is made public, scan every commit in its history, not only the current tree, for student-identifiable data, instructor-only material, credentials, and any file that was never meant to be public. If the scan is clean, the repo goes public with its history. If it finds something, remove it from history with `git filter-repo` and rescan. A fresh single-commit repo is the fallback only if filter-repo cannot remove it. Whichever route is taken, the private original is kept as the archive. The public flip also waits on the license (LEDGER 8).
- rationale: The owner raised cloning or forking to a fresh repo so that early commits are not public, and said a scan is worth doing either way (chat, 2026-10-02). A public repo exposes every past commit, and the flip cannot be undone once the history has been read or copied. A fresh repo would also discard the ledger's dated sequence, which is its value to a successor (floor item 7: append-only, a wrong entry corrected by a new one).
- alternatives: a fresh repo with no history (loses the ledger's history and the provenance of each ruling; right only if the scan finds what filter-repo cannot remove); go public as is without a scan (a one-way exposure of anything in history).
- binds: LEDGER 8, the public flip, `OSU-physics-lab-library-instructor` (never copied into this repo)
- test: none yet; the scan's date and result are recorded in `STATE.md` when it is run.

### D-0063  Ask OSU Digital Experience about the domain and the logo in one conversation
- status: proposed
- proposed-by: owner
- date: 2026-10-02
- decision: The owner asks OSU Digital Experience, in one request, (a) whether the site may live at a physics.oregonstate.edu address, and (b) whether the logo files may be redistributed in a public repo and shown on the deployed site. Until they answer, the site stays on its Cloudflare Pages address and the logo stays under D-0007's exclusion. The owner raised the domain request; the logo question was added to the same request on the lean of D-0064.
- rationale: The owner said the domain is open and may be requested from OSU Digital Experience, and that the logo files were behind a login and may have to be dropped while the prose stays (chat, 2026-10-02). Both questions go to the same kind of office, and one answer may settle both. This is the follow-through of D-0001 and D-0012 (a compliant site, shown to University Marketing, eventually under physics.oregonstate.edu).
- alternatives: ask about the domain alone and decide the logo privately (leaves a trademark question unanswered in a public repo); drop the logo now (loses the branding D-0002 ruled on before anyone has said it is not allowed).
- binds: D-0001, D-0002, D-0007, D-0012
- test: none; the answers are recorded as new entries when they arrive.

### D-0064  The build works without the logo; the README says to supply your own
- status: proposed
- proposed-by: claude
- date: 2026-10-02
- decision: The logo is a replaceable asset. The build and the tests pass when the official logo files are absent, the site then shows its name as live text, and the README tells anyone redeploying to supply their own logo or none. This does not remove the logo from the deployed site; it removes the dependency, so that a ruling to drop the logo from the public repo costs a deletion and not a rebuild. Disclosed edit: `tests/test_assets.py` pins each logo file's SHA-256 and would need to treat a missing logo as allowed.
- rationale: If the answer to D-0063 is no, the repo needs to work without the files. The same property lets a successor on another host deploy without trademark files they may not hold, which supports the continuity goal.
- alternatives: keep the logo hard-wired (a no from OSU breaks the build and the pinned tests); remove the logo now (decides before the answer to D-0063).
- binds: D-0002, D-0007, D-0063, site/brand/, tests/test_assets.py, tools/brandheader.html
- test: to be written with the change (a build with the logo files removed passes).

### D-0065  The README is tested cold before any claim that it enables a redeploy
- status: proposed
- proposed-by: claude
- date: 2026-10-02
- decision: No document, slide, or README sentence says that someone else, or another tool, can deploy this site until a fresh agent that has only the README and a throwaway host account has done it. The run is recorded (date, host, what the README lacked) and each gap becomes a README fix. Until then the wording is that the README is written so the site can be rebuilt and moved, and no more. A cold test is rerun when the build or hosting changes.
- rationale: The owner agreed not to claim more than the evidence supports (chat, 2026-10-02). The hosting migration plan says the move is three settings plus DNS, which is unproven. A repo must not lie about its verification (floor item 2).
- alternatives: assert it from the migration plan alone (a claim without evidence); test with the owner as the reader (the owner already knows the unwritten steps, so the test would not find them).
- binds: README.md, docs/hosting-migration-plan.md (in OSU-lab-ops), the curriculum meeting deck's slide 7 note
- test: none; the dated run record is the evidence.

### D-0066  The README names who holds the registrar, DNS, and host accounts, by role
- status: proposed
- proposed-by: claude
- date: 2026-10-02
- decision: The README lists, by role and not by name, who holds the domain registrar account, the DNS records, and the Cloudflare account, and the handover step for each (how a successor takes the role). A line that says "unknown" or "undecided" is acceptable and is marked as such, never guessed. Who holds each is open as of this entry.
- rationale: The site can be rebuilt from the repo anywhere, but the link only keeps working while someone controls the address. The owner has said the domain is undecided and will not be a university domain unless OSU Digital Experience agrees (chat, 2026-10-02). That control is the actual continuity risk, and the repo cannot close it by itself.
- alternatives: leave it to the owner's memory (the thing the lab-ops repo exists to avoid); name people (violates the roles-not-names rule and goes stale).
- binds: README.md, D-0063
- test: none.

### D-0067  Each course on the course index gets a quiet Download all button: a dialog of four opt-in format checkboxes, one zip built in the page
- status: proposed
- proposed-by: owner
- date: 2026-10-02
- decision: After the lab list of each course on the course index that has at least one converted lab, one quiet "Download all" button: outlined in `--chrome-quiet` with no fill, 44 px tall, never the download buttons' orange. It opens a modal `<dialog>` (named "Download all" for assistive technology) holding four checkboxes, "Word", "HTML", "PDF" and "Markdown" (D-0053's names, in the lab page's row order), none ticked each time it opens, and a "Download selected" button in D-0059's button look, disabled while no box is ticked. Escape or a tap outside the dialog closes it; it also closes once a zip is saved. The button runs a script of the page's own, `site/download-all.js`, that fetches the selected formats' published files of that course's converted labs (`labs/<id>/<id>.<ext>`, same origin) and writes one zip, `<code>.zip`, where `<code>` is the course code lowercased with its spaces removed (`ph211`): one folder per lab named by its document id, each file under its published name, byte for byte, stored without compression (the Word and PDF files are already compressed). The zip writer is the page's own code, no library and no request outside the site, tested by node beside it as the sims are. No zip is built or published, so the deploy check and the alias wait (D-0060) are unchanged. The list of files is written into the page at build time from the converted documents, never typed. The button is hidden as built and shown by the script, so a browser without the script or without `<dialog>` shows no control that does nothing; from a copy of the site opened from disk the browser refuses the fetches, so the control works on the served site only, while each lab's four buttons (D-0059) still work from disk (LEDGER 39). Zip entry dates are the time of download; no byte-identical zip is promised. Words: "Download all" is the owner's phrase, the four names are D-0053's, and "Download selected" was proposed by Claude; all are approved pending the owner's look at the PR preview. No close word is shown. Built after phase 4 (D-0061) and on D-0068's rows.
- rationale: The owner asked for a per-course download to store the most recent copies of a course's documents in Box or SharePoint (chat, 2026-10-02), chose a control per course on the course index, then amended it to four format checkboxes ("Download all should offer the four formats as checkboxes, and only those selected will be downloaded") and ruled option 1 of three ("Rule option 1 as leaned"): one zip built in the page. On the first preview (2026-10-03) he found it worked but sat flush against the Lab 1 card, and asked for it to be less prominent, behind a button with a pop-up, "specifically because students most of the time will not be using this. It's mostly just for me or instructors", with each format opt-in rather than opt-out; he ruled the leans ("Rule your way on all of them and build it"). A static site cannot turn a choice into one file without code in the page, and the zip needs the script anyway, so a script-run dialog costs nothing a `<details>` would not. Measured on the built course index at 375 px, 2026-10-03 (Chrome): the button 130 by 44 px, 24 px below the last lab row and 40 px above the next course heading; the dialog 343 px wide, centered; checkbox rows 44 px tall; "Download selected" 175 by 44 px; nothing scrolls sideways. The button's ink against the page is 8.89:1 light (Rogue Wave on white) and 14.58:1 dark (Moondust on black), computed with the WCAG formula.
- alternatives: the `<details>` under the course heading with its summary as the orange download button and every box ticked at open (this entry as ruled on 2026-10-02 and first built; too prominent for a control students rarely use, and opt-out); a further "more" or "instructor tools" button in front of the dialog (one more tap and new words); every combination prebuilt, 15 zips a course (each format stored in 8 of the 15, all fetched by the deploy check on every run); one zip per ticked format (several downloads at once); five fixed zips per course with no checkboxes (this entry as first proposed); a zip library from a CDN (a third-party request the scans cannot see); fixed dates for a byte-identical zip (D-0060's alternative); a "select all" box (more words for a four-box list); a visible close button (a new word; Escape and a tap outside close it).
- binds: D-0053, D-0059, D-0060, D-0061, D-0068, LEDGER 39, tools/render.py (download_all, course_index_markdown), tools/quarto_build.py, _quarto.yml, site/site.css, site/download-all.js, site/download-all.test.mjs
- test: site/download-all.test.mjs (run by tests/test_download_all.py::NodeTest); tests/test_download_all.py (ZipReadBack: a zip the script's own code writes, read back by Python's zipfile; Control: one control per course with a converted lab and none otherwise, after the lab list, the exact file list, ph211.zip, the words, opt-in and hidden until the script runs, the quiet button and the orange "Download selected" in the quarto-only block; Script: no URL outside the site, linked once, no zip published)
- corrected: 2026-10-02, title, decision, rationale, alternatives, binds and test rewritten while proposed, on the owner's amendment in chat ("Download all should offer the four formats as checkboxes, and only those selected will be downloaded") and his ruling ("Rule option 1 as leaned"): one zip built in the page from the ticked formats replaces five build-time zips
- corrected: 2026-10-03, decision, rationale, alternatives, binds and test rewritten while proposed, on the owner's review of the first preview in chat ("I'm also now thinking that we should intentionally make the download all button less prominent"; "I think it's better to have each format be opt-in rather than opt-out") and his ruling ("Rule your way on all of them and build it"): a quiet button after the lab list opening a dialog with no box ticked replaces the orange summary under the heading with every box ticked

### D-0068  The course index lists one lab per row on the reading column
- status: proposed
- proposed-by: owner
- date: 2026-10-03
- decision: Amends D-0029's "`.lab-list` spans all three tracks". On the course index and the sims page, `.lab-list` sits on the reading column like the prose and is one column at every width: one row per lab, all rows one width. Each row keeps its title, description and state line; a converted lab keeps its Beaver Orange left rule; a lab not yet converted gets a dashed border and its title in `--chrome-quiet`. Descriptions are never clipped, so row heights follow their line count. The rule is `body.site-page .lab-list`, because `body.site-page ul` (0,1,2) outranked `.lab-list` (0,1,0) and had kept a 1.4rem indent and its own margin on the list since the tiles. No new words.
- rationale: The owner found the tiles of different sizes and asked for one row per lab, like the demo catalog's rows (its amendment 21), chat 2026-10-03; ruled as leaned ("Rule your way on all of them and build it"). The catalog clamps its summaries; these descriptions are quoted word for word from the PH 211 curriculum summary, and a clamp would hide quoted text. Measured on the built course index, 2026-10-03: every row 700 px wide at 1440 px and 328 px at 375 px, flush with the prose column (before: 22 px in, the `ul` indent); heights 158 to 216 px at 1440 px; nothing scrolls sideways at 375 px.
- alternatives: keep the tiles with equal heights (stretched cards, empty space in the short ones); clamp descriptions to equal row heights (hides quoted text); a fixed minimum height (empty space without removing the variation).
- binds: D-0029, site/site.css
- test: tests/test_quarto_chrome.py::LabRows

### D-0069  One page per course; the course index chooses the course, as tiles; course tabs under the site nav
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-06
- decision: Each course gets its own page (PH 211, PH 212, PH 213), with an address of its own that does not change when a course name is filled in: `/courses/<code>/`, the course code lowercased with its spaces removed (`/courses/ph211/`), the slug D-0067's zip name already uses (the builder's proposal; this entry left the path form open). The course index stops listing labs and becomes the chooser: one tile per course, all tiles the same size in one row at desktop widths and stacked below 48rem, each holding the course code, the course name, and a count of labs drawn from `site/courses.md`, never typed: "8 labs listed, 1 converted" while some are unconverted, "No labs converted yet" while none is, "8 labs" once all are (the first two are the board's words, the third is new; all three approved by the owner, 2026-10-06). A name not yet in hand (PH 212; PH 213, Q4) is left out of the tile and the page's h1, not shown as a placeholder. A tile with a converted lab carries the orange top rule, as on the board. Every course page carries a row of course tabs under the site nav, a `<nav>` named "Courses" for assistive technology, rendered by `tools/template-site.html` from links `render.course_tabs()` writes; the current course is marked with `aria-current="page"`, and each tab is 44 px tall. No popover or modal is shown on load. Board C's course links and board D's select (`docs/design/2026-10-05-left-contents/`) are not built.
- rationale: The owner, reviewing board C (chat, 2026-10-06): the course table of contents was not prominent enough, Download all sat near PH 212 and could be read as that course's, and a PH 212 or PH 213 reader scrolled past all of PH 211 (about 1,770 px at desktop widths, 2,290 px at 375 px, four-items plan premise 1). He proposed separate course pages and a popover that must be answered on load. Claude argued against the forced popover (a click on every visit, deep links gated, focus moved into a dialog at load) and proposed the index itself as the chooser. Owner, ruling: "1 yes, 2 tiles". Boards in `docs/design/2026-10-06-course-pages/` (`Main.dc.html`, the tabs on `Course.dc.html`). This replaces calls 2.1 and 2.2 of the four-items plan: neither a side column nor rows across the shell is needed once a page holds one course. Measured on the built pages, 2026-10-06 (Chrome, `tools/measure_chrome.js`): the tiles 453 by 173 px at 1440 px and 496 by 173 px at 1920 px, three in one row 24 px apart; 328 by 200 px stacked at 375 px, all three one size; the tabs 93 by 44 px at desktop widths and 104 by 44 px at 375 px, sharing the width; nothing scrolls sideways at 375 px on the index or on any course page.
- alternatives: one page with board C's sticky course links in the left track (the 2026-10-05 lean; leaves the download control's course ambiguous and the scroll in place); a select that scrolls (board D, declined 2026-10-05); a popover that must be answered on load (the owner's first idea; costs every visit and gates deep links); remembering the last course in the browser (not proposed; storage for a three-way choice).
- binds: D-0068, docs/superpowers/plans/2026-10-03-four-items.md (item 1, calls 2.1 and 2.2, Q5), tools/render.py (course_slug, course_heading, lab_count, course_tiles, course_tabs, course_index_markdown, course_page_markdown), tools/quarto_build.py, tools/quarto_chrome.py, tools/template-site.html, _quarto.yml, site/courses.md, site/site.css
- test: tests/test_quarto_chrome.py::CoursePages (one page per course in `site/courses.md`; the index's tiles, one per course in order, each linking to its page with the code, the name when in hand and the count computed from the data; no dialog or script on the index; the tabs on course pages only, under the site nav, naming every course in order and marking only the current one, 44 px tall by the CSS; the h1 the course's code and name, or the code alone; the footnote only where labs are listed); tests/test_quarto_site.py::Pages::test_expected_pages
- corrected: 2026-10-06, decision, rationale, binds and test filled in while proposed, with the build: the path form proposed, the tile count's words drafted for approval, a name not in hand left out rather than shown as a placeholder (the boards' bracketed placeholders mark mockup text), measurements added
- corrected: 2026-10-06, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0069, D-0070", chosen as ruled as written in PR #26, with its words approved: "Approve, merge PR 1"); the tile words marked approved

### D-0070  A course page lists its labs in one dense table across a 96rem shell: Lab, Title, Description
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-06
- decision: Amends LEDGER 56's shell, D-0068's rows and, on the course index and the course pages, D-0029's centering. On site pages, `--chrome-shell` grows from 72rem to 96rem (1,536 px), set on `body.site-page` so document pages keep 72rem; prose keeps the 68ch measure. On a course page the labs are one `<table>` across the shell with three columns, "Lab", "Title" and "Description", in curriculum order. The title is the link to the lab's page. The description is quoted word for word, never clipped, and takes the width left after the first two columns (5.5rem and 18rem of content), so it is wider than the measure; this is the owner's choice for a scanning surface, and the measure still governs every line of prose elsewhere on the page. No status column, no state line, and no "Converted" heading: a lab is listed because it is converted. "Also available as it was written" leaves the course page; each lab's page already carries the switch "Read it as it was written" (`tools/render.py`, `switchlabel`). Below 48rem the table becomes stacked rows: "Lab N: Title" as the link, the description under it; on wider screens that "Lab N: " stays in the link for screen readers only, beside the Lab column. On the course index and the course pages the prose track sits at the shell's left edge rather than centered (D-0029), so the h1, the prose and the table share one left edge, as the boards draw (body class `courses`). The intro keeps only "Every lab below is listed under the number and title its own course summary gives it."; its two sentences about unconverted labs go. The footnote naming the curriculum summary as the source stays, on the page of the course whose list it quotes (`source_note` moves into that course's entry in `site/courses.md`). Before launch, while a course still has unconverted labs, the owner's earlier "5 collapsed" stands (ruled 2026-10-06, "Collapse stands", the open question in `docs/design/2026-10-06-course-pages/README.md`): they are listed under the table in a `<details>`, closed as built, its summary "Not yet converted (N)", in the same three columns without links; once every listed lab is converted it renders nothing, with no change to the code.
- rationale: The owner asked several times for more of the screen to be used (chat, 2026-09-19, LEDGER 56; again 2026-10-06: "Only the center third, roughly, of a standard computer monitor screen is being used"). LEDGER 56 had ruled card lists across the shell; D-0068 put quoted descriptions of up to 175 characters into the rows, and the four-items plan then read 56's premise as no longer holding (its premise 4), so the width went unused. Claude's reading, 2026-10-06: the measure bounds a line, not a page; a catalog is scanned, not read, so the width goes to more items per screen. The owner chose a table over cards: "3 dense table, otherwise we need rules that enforce cards to be the same size", and "4 96rem". On the PH 211 board he then widened the description column, relabeled it "Description", deleted the Status column ("if they are converted and checked, they'll be available, otherwise they won't be. It's implicit") and the "Converted" heading ("the site will have all lab materials converted by the time it goes live"), and moved "as written" to each lab's page. His earlier "5 collapsed" for unconverted labs is moot at launch by the same reasoning. Computed first: at 1440 px the description column about 1,000 px, the longest description about two lines. Measured on the built pages, 2026-10-06 (Chrome, same-origin iframes, `tools/measure_chrome.js`; a page taller than its frame gives 15 px to the scrollbar): at 1440 px (1,425 px of client width) the shell holds 1,393 px from x = 16; the h1 is one line, 51 px tall; the intro and the footnote 700 px; the table 1,393 px, its columns Lab 107 px, Title 307 px and Description 979 px (cells, padding included); the longest description, 173 characters (recounted; 175 before), sets 2 lines, a full line holding 111 characters. At 1920 px the shell caps the table at 1,536 px, Description 1,122 px, the longest 2 lines, a full line 127 characters. At 375 px (360 px of client width) the rows stack 328 px wide, the longest description 6 lines, and nothing scrolls sideways (scrollWidth 360 of 360) on the course index, any course page, or the five other pages measured. There the 44 px h1 "PH 211: General Physics with Calculus" takes 4 lines, 202 px. The collapse's summary is 243 by 47 px, Download all 130 by 44 px. The header's content now starts at x = 16 at 1440 px and x = 185 at 1920 px on site pages, against x = 137 and x = 377 on a lab page (72rem): it shifts 121 px and 192 px between the two kinds of page.
- alternatives: rows across the shell with two columns inside (four-items call 2.1); cards in a grid (LEDGER 56 as written; equal sizes need extra rules); D-0068's rows on the reading column (the width unused); the description capped at 60ch (the first board; the owner found it too narrow); a status column (implicit once every listed lab is converted); unconverted labs collapsed under "Not yet converted (N)" (ruled, then moot for launch).; the prose kept centered above a table at the shell's edge (D-0029 as ruled; the h1 would start 346 px right of the table at 1440 px, computed); unconverted labs as table rows without links (the status the owner deleted, shown by the missing link); no course page until every lab is converted (the other side of the open question)
- binds: LEDGER 56, D-0029, D-0068, site/site.css (`--chrome-shell`, `body.site-page.courses main`, `.lab-table`, `.lab-pending`), tools/render.py (`lab_table`, `pending_labs`, `course_page_markdown`), site/courses.md (the intro, `source_note`), tools/measure_chrome.js, tests/test_quarto_chrome.py::LabRows, tests/test_brand.py::Widths
- test: tests/test_brand.py::Widths (the measure 68ch, the document shell 72rem, the site-page shell 96rem, from the CSS text); tests/test_quarto_chrome.py::LabRows (one table of the converted labs per course page with the three column names, rows in curriculum order, each title a link reading "Lab N: Title", each description quoted whole; no state line, no "as it was written", no "Converted" heading; before launch the collapse only where labs are unconverted, its count and its rows, no links; the table across the shell with fixed Lab and Title widths and none on Description; rows stacking below 48rem with the title cell reset by name; descriptions never clipped; the sims page's D-0068 rows); the 375 px no-sideways-scroll result is the measurement above
- corrected: 2026-10-06, decision, rationale, alternatives, binds and test filled in while proposed, with the build: measurements added, the courses pages' prose track moved to the shell's left edge (amending D-0029 there), the pre-launch collapse built as Claude's lean for the owner's ruling, `source_note` moved to its course, the longest description recounted
- corrected: 2026-10-06, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0069, D-0070", chosen as ruled as written in PR #26, with its words approved: "Approve, merge PR 1"); the pre-launch sentence restated as ruled ("Collapse stands")

### D-0071  The course download covers every file of a course, grouped by kind, beside the course page's h1; hidden under two files
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-06
- decision: Amends D-0067. The control moves from after the lab list to the course page's heading row (a fenced div, which Quarto writes as a `<section class="course-head">` holding the h1), right of the h1 at desktop widths and under it when the two do not fit, keeping D-0067's quiet look. Its words name the course and say files, not labs: "Download PH 211 files" (Claude's words, approved by the owner 2026-10-06). The dialog's title repeats them and names the dialog, followed by the board's note, "One zip, a folder per lab. Only converted labs are included." (approved). Its checkboxes are grouped by kind: "Handouts", with D-0053's four formats (Word, HTML, PDF, Markdown); and "Lab files", with "Data files (CSV)" and "Simulations (HTML)", each listed only when that course has at least one. The Lab files group is not built: no way to attach a data file or a simulation to a lab is designed, and none is invented; it is written when one is. Every box is opt-in, as in D-0067. The zip keeps one folder per lab; a lab's data files and simulations would go in that lab's folder. "Download selected" and "Close" (Q8's lean) as drawn; "Close" is a dialog-method form, so it closes the dialog with no script. The control is hidden when the course has fewer than two downloadable files, each format of a converted lab's handout counted as a file, so one handout in four formats is four (the owner, 2026-10-06: "Four files"): a course with a converted lab always shows the control, and PH 211 shows "Download PH 211 files" today. The rule bites only on lab files alone.
- rationale: The owner, reviewing board C (chat, 2026-10-06): Download all "needs to specify which course it's for" and sat close enough to PH 212 to be read as that course's; "I'm wondering if it's cleaner just to put the download all affordance in the header". Then: "the download all needs to be general enough because it's not just labs that could be downloaded", naming the handout, a CSV attached to a lab, and an HTML simulation like the modified electric force sim attached to a lab, and asking for checkboxes for those beside the four formats. Claude grouped them by kind, since formats apply to handouts only. With one converted PH 211 lab, "Download all" duplicates that lab's own download row; the owner ruled "6 hide". Board `Download.dc.html` shows the dialog with placeholder counts. Claude leaned to one file per handout, after the owner's reason for hiding (with one lab the control repeats that lab's own download row); the owner ruled four. Measured on a probe build with the threshold lowered to one file, never committed, and again on the built page once the count was ruled, with the same numbers (2026-10-06, Chrome, `tools/measure_chrome.js`): at 1440 px the h1 is one line, 791 by 51 px, and the button, 202 by 44 px, sits right of it at the shell's right edge (x = 1207 to 1409); at 1920 px the same, at x = 1518; at 375 px the h1 takes 4 lines and the button sits under it at x = 16. The dialog is 448 by 317 px at desktop widths and 343 by 333 px at 375 px; its four checkbox rows and both buttons are 44 px tall ("Download selected" 175 px, "Close" 68 px wide); nothing scrolls sideways with it open. Checked by hand on the probe: it opens as a modal with focus on Word, "Download selected" enables on a tick, "Close" and Escape close it with focus back on the button and the address unchanged, and reopening finds every box unticked.
- alternatives: D-0067 as built (after the lab list, handouts only); one flat list of every format and kind (formats would read as applying to CSVs and sims); a "select all" box (D-0067's alternative, still declined); showing the control with one file (the owner: hide).; a raw `<div>` around the heading (Quarto then lifts the h1 into its title block, past the empty partial: probed); a handout counted once whatever its formats (Claude's lean; it hid PH 211's control while the course has one converted lab)
- binds: D-0053, D-0067, D-0069, site/download-all.js, site/download-all.test.mjs, site/site.css (the heading row; in the quarto-only block the opener, the dialog's title, note, legend and actions), tools/render.py (download_all, downloadable_files, course_page_markdown), tools/measure_chrome.js, tests/test_download_all.py
- test: tests/test_download_all.py: Control, on render.download_all() for a course with two converted labs (hidden under [2] files, four to a converted handout; the words; the title naming the dialog; one Handouts group and no Lab files group; the exact file list; ph211.zip; opt-in and hidden until the script runs; Close in a dialog-method form; in the heading row before the intro; the quiet opener and Close, the orange Download selected and the unfloated legend in the quarto-only block); BuiltPages (the control only where a course has two files, PH 211's page among them; written as render.download_all() writes it; the heading row holding the h1 on every course page); ZipReadBack (the files PH 211's built control lists, zipped by the page's own code from its page's folder, read back by Python's zipfile); Script; site/download-all.test.mjs (an entry name from a page two folders down). A data file and a simulation landing in their lab's folder waits on how they attach.
- corrected: 2026-10-06, decision, rationale, alternatives, binds and test filled in while proposed, with the build: the heading row's markup, the note, the Close form, the file count built as Claude's lean, the Lab files group not built for want of an attachment format, probe measurements added
- corrected: 2026-10-06, decision, rationale, alternatives and test rewritten while proposed on the owner's ruling in chat ("Four files": each format of a handout counts as a file), so PH 211 shows the control; the measurements repeated on the built page
- corrected: 2026-10-06, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0071", chosen as ruled as written in PR #27 with the file count chosen in the same answer, "Four files", and its words approved: "Approve PR 2 words"); the words marked approved
