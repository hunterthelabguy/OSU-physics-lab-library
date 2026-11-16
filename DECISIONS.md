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
- D-0093 Instructor notes and rubrics git-ignored here (declined: tracked in the private repo, D-0081) -> DECLINED.md
- D-0094 A no-print pre-scan before reading originals (declined: the owner's word clears them, D-0084) -> DECLINED.md
- D-0095 Hold the template until paper or typed is decided (declined: B ships regardless, D-0074) -> DECLINED.md
- D-0096 No target term until the gates settle (declined: Winter 2027, D-0080) -> DECLINED.md
- D-0097 Build the template after pass 3 (declined: rule 3.10 holds, D-0080) -> DECLINED.md
- D-0098 Cross-reference during the conversion passes (declined: pass 7, D-0083) -> DECLINED.md
- D-0146 A skim-only dry run by a TA before a stretch ships (declined: owner, "Skip the dry run gate.") -> DECLINED.md
- D-0147 PH211H, 212H and 213H as the sandbox course codes (declined: PH 211H is an OSU course number; Sandbox names, D-0144) -> DECLINED.md
- D-0148 Sandbox courses unlisted, reached by address only (declined: owner, listed within the site, D-0144) -> DECLINED.md

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
- corrected: 2026-10-06, the PR that carried this entry to main is #28, squashed as `f65b1d4`; the promotion line's #27 is the same branch, which GitHub closed when #26's merge deleted its base, with main merged in and the owner's "Four files" applied

### D-0072  "How this was made" becomes "How this site works": the build explained first, the AI use disclosed in the body
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-06
- decision: The page now at `/how-this-was-made/` is re-framed and retitled "How this site works", at `/how-this-site-works/`, the old address redirecting there. Its text gets its own source, `site/how-this-site-works.md`, included as the landing page's is, and stops being lifted from VISION.md; VISION.md's "How this was made" section keeps the four commitments (no content changes; the claim is checked, not asserted; the originals remain; the same standard as students) and the open later-phase standard, and points to the page. The page explains the build first (one Markdown file per handout and the versions built from it, the tools that build them, the word check, how a change is published), then who did the work, in the body and not a footnote: "Hunter Reaves directs Claude, an AI model from Anthropic, ...", the dictation tool no longer named. The concerns table and the open later-phase standard stay. The nav, the footer's "License and credits" line, the landing card and the page's footnote take the new title. Words: drafted by Claude in `docs/superpowers/plans/2026-10-06-how-this-site-works.md` for the owner's line edits; nothing is built until he approves them.
- rationale: The owner (chat, 2026-10-06): "edit the 'How this was made' page to de-emphasize the use of AI tools. Not to hide it, but rather to re-frame. I want it to explain the boring parts first. Markdown SSOT, Pandoc, Quarto, etc. New page title 'How this site works'." Claude's reading: the trust case is the word check and the kept originals, and leading with the build puts it first; the disclosure stays plain because the page cites the students' AI policy, which says to disclose use. Each tool is named with one sentence on what it does for the reader, since the names alone mean nothing to a TA. The owner chose each of Claude's leans: "Its own file", "New URL plus redirect", "Name, Claude; drop Wispr", "Draft first".
- alternatives: keep the lift from VISION.md under a new heading (the vision document would carry the build explainer); keep the old address (it would no longer match the title); a role instead of the owner's name (nobody accountable by name); keep Wispr Flow named (process detail that reads as tool emphasis); the disclosure in a footnote, or dropped (the owner: "Not to hide it"); build first and review on the preview (the owner chose the draft first).
- binds: D-0038, VISION.md (principle 6 and "How this was made"), site/how-this-site-works.md (new), site/landing.md, tools/render.py (how_this_was_made, METHOD_FOOTNOTE, site_vars, redirect_page), tools/quarto_build.py, _quarto.yml, tools/brandheader.html, tools/brandfooter.html
- test: tests/test_quarto_site.py (test_old_method_address_redirects: the old address a stub to the new one with its own link words; test_method_page_from_its_own_source: every heading of site/how-this-site-works.md on the page, the disclosure present, no Wispr; Pages::test_expected_pages); tests/test_quarto_chrome.py::ChromePieces (the footnote only on its page; the nav and footer words from the templates); tests/test_quarto_dress.py. Measured on the built page, 2026-10-06: at 375 px nothing scrolls sideways (scrollWidth 360 of 360); at 1440 px the prose and the concerns table are 700 px from x = 362
- corrected: 2026-10-06, decision widened while proposed on the owner's request in chat: the page also explains the site's basics in plain terms (a static site, a build, a repository), where it lives (Cloudflare Pages, with Cloudflare's privacy policy), how search engines and AI crawlers are treated (noindex, robots.txt), and continuity (the repository planned public, D-0062; its instructions' limits, D-0065; accounts by role, D-0066); drafted as revision 2, with placeholders for the two Cloudflare settings nobody has checked
- corrected: 2026-10-06, built while proposed on the owner's word in chat ("Say 'are being written' and build it"): the continuity section says the instructions are being written; the draft's two bracketed placeholders (what the Cloudflare account records; its AI-crawler block) were dropped rather than published, so the page claims only what the repo shows, and both settings stay open for the account holder
- corrected: 2026-10-06, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Merge it and promote D-0072", ruled as built in PR #29, squashed as `c3c8620`)

### D-0073  The opening ask for the course materials is CC BY-NC-SA 4.0, the authors' names kept
- status: proposed
- proposed-by: owner
- date: 2026-10-06
- decision: Narrows LEDGER 8 without settling it. When the license is raised with the copyright holders of the course materials (the original authors, the previous coordinator, other faculty: LEDGER 8's list), the site's first ask is Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) for the handouts in every presentation and every download, with every prior author credited by name (VISION principle 4). The ask is put as a concrete license with a yes or no, not an open question. What the site does if a holder declines is not decided; nothing is invented ahead of the answer. Outside this entry, unchanged: the code license stays LEDGER 8's lean, MIT, not ruled (Creative Commons advises against its licenses for software); the OSU logo stays excluded (D-0007); Open Sans stays under the SIL Open Font License (D-0039); the footer's copyright line stays held (D-0023); nothing publishes until LEDGER 8 settles.
- rationale: The owner (chat, 2026-10-06): "Even I prefer NC", then "record it as the opening ask". Claude had leaned CC BY 4.0 with BY-NC-SA as the fallback; with NC chosen, Claude leaned SA over plain BY-NC so adaptations stay open on the same terms, at the cost of not mixing with differently licensed material such as CC BY-SA. Who can grant the license, read 2026-10-06: OSU University Policy 06-200, Intellectual Property (policy.oregonstate.edu/policy/intellectual-property, effective 2023-04-12), defines Course Materials (4.7) and excludes them from OSU's intellectual property (5.1.2) unless made with university facilities and funds beyond the support typical for faculty; OSU receives a "fully paid-up, royalty-free, perpetual, non-transferrable, and non-exclusive worldwide license" with revision rights. Claude's reading, not legal advice: the faculty authors hold the copyright, and a non-transferable license to OSU does not plainly let OSU license the materials to the public, so the authors' grant is the one that counts. OSU Libraries' copyright guide (guides.library.oregonstate.edu/copyright/author, updated 2026-09-04) says the same in terms of the UAOSU collective bargaining agreement, Article XVII section 4; the agreement itself was not read. Help on campus: Ecampus's Open Educational Resources Unit (open.oregonstate.edu, in the Valley Library) funds and consults on faculty open resources; its pages name no default license. Precedent in the department: a search result reports that Learning Introductory Physics with Activities, by Paul J. Emigh and others at lipa.physics.oregonstate.edu, is under CC BY-NC-SA 4.0; the license statement was not found on its pages, so it is unconfirmed.
- alternatives: CC BY 4.0 as the first ask (Claude's first lean; widest reuse, but the owner prefers NC); CC BY-NC 4.0 (adaptations could be closed); CC BY-SA 4.0 (allows commercial reuse); CC BY-ND (forbids the adaptations sharing is for); CC0 (drops attribution, against VISION principle 4); an open question to the authors with no license named (tends to stall).
- binds: LEDGER 8, VISION.md (principle 4), D-0007, D-0023, D-0039, D-0062, sims/modified-electric-force/index.html (its license placeholder)
- test: none; the entry holds no quantity. When a license is ruled, its text and its reach by path need a test of their own

### D-0074  Lab reports are written in a Word template generated per converted lab and submitted to Gradescope as one PDF per group, whichever way paper or typed goes
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-06
- decision: Students complete the lab report in a Word report template generated per converted lab from that lab's Markdown source: the questions only, with an answer area after each (approach B; spec `docs/superpowers/specs/2026-10-06-handout-conversion-and-templates-design.md`, rule 3.1). Every section submits to Gradescope as a PDF, one report per group (rule 3.2). The template is separate from the open paper-or-typed decision (rule 3.3) and ships whichever way that decision goes. The in-page worksheet (A) is held; Gradescope's Online Assignment (C) is declined (spec section 10). Premises, the owner's (rule 3.4, a premise rather than a rule): the group's scribe writes the report on a lab PC or a laptop, never a phone; some groups open the Word file in Google Docs and co-edit there, so the template must survive Word and Google Docs; each student signs in to a lab PC with their own account, so files stay in their own profile, though some students forget to log out.
- rationale: The owner chose B, the PDF per group and the separation in chat on 2026-10-06 (rules 3.1 to 3.3 are the owner's, confirmed 2026-10-07). On whether the template waits for the paper decision (critique F7), the owner, 2026-10-07: "B ships regardless and record the reason: if paper wins, the templates already exist and serve as the starting point for the paper worksheets." On F8 (a Word file on a shared lab PC leaves answers behind), the owner, 2026-10-07: own sign-in per student, but "occasionally some students forget to log out before leaving the lab"; a forgotten logout exposes any file a student opens in lab, so it is a lab-ops matter, not the template's. The same fact weakens the spec's shared-PC reason for holding A; A stays held because one browser is one author and groups co-edit.
- alternatives: A, the in-page worksheet (held, earmarked if typed wins); C, Gradescope Online Assignment (a second copy of every question built by hand; group support unverified); pass 6 held until the paper decision (D-0095, declined).
- binds: spec sections 1, 3, 6 and 10; tools/downloads.py (pass 6); STATE.md (paper or typed, open)
- test: none yet; pass 6's, under D-0079
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0075  The template puts one question on each page, with a one-cell bordered answer box after each
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-06
- decision: In the report template every answered question starts a new page (rule 3.5), by an explicit page-break paragraph (call 4.5). A stem's text heads its first child's page with no box (spec section 5, S2); an item needing no answer is left out, its number a visible gap (S1). The answer area is a one-cell bordered box (rule 3.6): one per question, unless the Gradescope outlines grade lettered sub-parts as separate questions, in which case one per sub-part (spec 9.4); pass 6 asks the outline maintainers, by role, before it builds.
- rationale: Students tag pages to questions in Gradescope faster when each question has its own page. The owner's "Yes" of 2026-10-06 answered a question that bundled this with the PDF submission (critique finding 8); confirmed alone on 2026-10-07 ("Yes, one per page"). A plain empty paragraph as the answer area is invisible, so students guess where to type (spec section 10). Rules 3.5 and 3.6 were Claude's proposals, ruled by the owner (owner, 2026-10-07). 9.4's lean accepted 2026-10-07.
- alternatives: questions flowing, each boxed (fewer pages; one page may hold parts of two questions, so tagging is slower); a plain empty paragraph; a "page break before" style (its Google Docs import is unverified, call 4.5). Unprobed: a near-blank page when an answer ends at a page foot (F9).
- binds: spec sections 3, 4.5 and 5; tools/filters/report-template.lua (pass 6, new)
- test: D-0079's invariants (page breaks equal answered items less one; one table per answered item)
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0076  The template adds a group-members line and an AI-use slot read from its own file; the lab page gets its own template button
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-06
- decision: The template adds two things the handout does not hold (rule 3.7): a "Group members:" line on page 1, and an "AI use" slot at the end whose words live in their own file (call 4.6, for example `site/report-template-ai-use.md`), so colleagues can edit it or delete it entirely; with the file present the template ends with the slot, with it absent there is no slot and no code change. The slot applies to every PH 21X course, so one file serves every template and no per-course switch is built (spec 9.6). Its words name their source by title, "Statement on AI and labs" (a PH 21X course-wide file); the statement's authors are credited by name when D-0073's license conversation settles credit for every handout. The lab page gets a separate button, "Download template (.docx)" (rule 3.9).
- rationale: Rules 3.7 and 3.9 are the owner's (chat, 2026-10-06). On the slot's reach (spec 9.6) the owner, 2026-10-07: "Every course". On credit (critique finding 14: the template would quote co-owned work without credit, charter floor 9), the owner chose to cite by title now and name the authors by D-0073's rule, one rule for all course materials.
- alternatives: a per-course switch (no job: every course); the statement converted as a twentieth document the slot cites (another conversion and its own license question); the authors' names in the AI file now (names in a public repo ahead of D-0073).
- binds: D-0059, D-0073, spec 3.7, 3.9 and call 4.6; site/ (the AI file, pass 6); tools/render.py (the button, pass 6)
- test: pass 6: the template with the AI file present and absent (call 4.6)
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0077  The template's question numbers equal the handout's, which equal the original's; the ordered ids are pinned per lab
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-06
- decision: The template's question numbers equal the converted handout's, which equal the Word original's (rule 3.8). Gradescope outlines and the rubrics follow the original numbers. The rubrics are the owner's to edit in lockstep with handout changes; the outlines are not his task. The ordered question ids are pinned per lab by a test (call 4.8, built in pass 2a): adding, removing or reordering a question fails the build until the pin is updated in the same PR with an entry naming the numbers that moved, the owner's cue to edit the rubrics and the outline maintainers' notice. The pin is a deliberate lock that fails loudly, as `tests/test_assets.py` pins the logo hashes, not the second copy that call 4.1 declines (critique finding 11).
- rationale: Rule 3.8 is the owner's (chat, 2026-10-06; confirmed as his 2026-10-07). The pin freezes the order the conversion produced; that the order agrees with the original is D-0078's job, so the two guards have separate jobs: D-0078 during conversion, the pin once ruled content changes begin.
- alternatives: none raised.
- binds: spec 3.8 and call 4.8; tests (pass 2a)
- test: pass 2a: reordering a question in a fixture fails the pin
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0078  A check compares the original's question numbers, read through Pandoc, wherever a pass-1 count shows Word's numbering is simple
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: Pass 1's survey counts per handout, computing no labels, the numbering features that make Word's displayed numbers hard to read: a restart or override at the question level, more than one list among the questions, a label format other than "N)". Where a handout has none, pass 2a's check compares Pandoc's reading of the original's numbered items with the converted lab's question numbers, items needing no answer and stems included. Where a handout has any, its conversion task stops and comes to the owner, and a reader of Word's own numbering (`numPr` and `numbering.xml`, critique F1) is built only then. The faithful page's "N)" prefix (`tools/filters/questions.lua`) is right only where the count finds "N)".
- rationale: D-0077 is ruled but nothing proves it: the word check reads `w:t` only and cannot see Word's list numbers, and the pin freezes whatever the conversion produced (critique finding 2). The two critique passes disagreed on the method: finding 2 read the original through Pandoc (the sample extraction kept Word's numbering, including numbers that continue across parts), F1 read the XML, independent of the converter, as the word check is (`docs/conversion-spec.md`, "independent of Pandoc"). The owner, 2026-10-07: "The less manual work for me, the better, but also the best code is no code. I lean toward relying on Pandoc but only if there's low risk of mistake." The count measures that risk per handout before the check relies on it. The owner asked whether the rubric workbooks could supply the numbers. They cannot here: they are instructor material, never in this repo, which never reads the instructor repo (spec section 7); they score only some questions (PH 211 Lab 1's, four of five), so the S1 and S2 calls that shift numbers are invisible to them; and they are what the lockstep keeps in step. Their "Qn:" text is pass 7's job instead (D-0083).
- alternatives: XML from the start (F1; the largest code in pass 2, built whether or not any handout needs it); no number check, the task reviewer and the pin only (a missed S1 or S2 call shifts every later number silently, then is pinned); XML with Pandoc as a second opinion (both bodies of code; every disagreement a stop).
- binds: tools/check_unchanged.py or a sibling (pass 2a); tools/filters/questions.lua; docs/conversion-spec.md; the survey (pass 1)
- test: pass 2a: a fixture where an item needing no answer is marked a question, shifting later numbers, must fail
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0079  The template's merge waits on the owner's check in Word and Google Docs; named changes reopen it, and tests pin its shape
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: Gate 8.6 stands: the template merges only after the owner checks it in Word and Google Docs, and the check is recorded in an entry as D-0057's was. The check reopens on any change to `tools/filters/report-template.lua`, `tools/reference.docx`, the Pandoc pin, the AI file, or when a structure (spec section 5) first reaches the template. Tests pin per template: its question words equal the source's; page breaks equal answered items less one; one table per answered item; an answer row at least the probe's height. The probe's parameters, recorded here so they outlive the ignored `build/probe-report-template/` (critique F9): a one-cell table, row height 1440 twips, border colour 8C8C8C.
- rationale: A one-time owner check gates a file the build rewrites on every push, so later changes would ship unchecked (F9). Accepted by the owner 2026-10-07.
- alternatives: the first merge only (gate 8.6 as written).
- binds: spec 8.6 and section 6; tests (pass 6)
- test: pass 6, the four invariants above
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0080  Templates come after all 18 conversions; Winter 2027 is the target and slips if conversion does; the template carries no draft notice
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-07
- decision: Rule 3.10 holds: pass 6 builds the template after every remaining handout is converted. The target for students to have the templates is Winter term 2027; it is a target, not a commitment, and slips if conversion runs long. The template ships without the draft notice ("Draft: license pending, not for distribution."), amending D-0052 for the template file only; every other download keeps it. What the template's page header carries instead is pass 6's design. Amends call 4.3.
- rationale: Rule 3.10 is the owner's (chat, 2026-10-06). On the target term (critique finding 5) the owner, 2026-10-07: "Winter 2027, distribution ruled", the distribution ruling being that the template ships without the draft notice. Where the date and 3.10 collide, the owner, 2026-10-07: "3.10 holds; Winter slips".
- alternatives: no target until the paper decision and the license settle (D-0096, declined); the template built after pass 3 (D-0097, declined); 3.10 with a cut-off date after which pass 6 runs on what is converted; Spring 2027.
- binds: D-0052, spec 3.10 and call 4.3; tools/downloads.py (pass 6)
- test: pass 6: the template has no draft notice; every other download still has it
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0081  Instructor notes and rubrics are tracked in the private instructor repo, never in this one
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: Instructor notes, rubric workbooks and anything drawn from them live tracked in `OSU-physics-lab-library-instructor` (private), never in this repo, tracked or ignored (rule 3.11; LEDGER 2). The private repo reads this one; this one never reads it (spec section 7).
- rationale: The private repo already tracks PH 211 Lab 1's notes and rubric with its own check and CI; history is what lockstep needs ("what did the rubric say when the handout said X"); a tracked file is durable (charter floor 12); a check on it can run in CI (floor 2); and one `git add -f` of an ignored file would put answer keys into a public repo's permanent history. The owner, 2026-10-07: "Tracked, private instructor repo".
- alternatives: git-ignored in this repo (the owner's first proposal; D-0093, declined).
- binds: LEDGER 2, spec 3.11 and section 7, CLAUDE.md (Conventions: this repo will become public)
- test: none; the entry holds no quantity
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0082  Eight passes: survey, checks, downloads, the hardest two then PH 211, PH 212, PH 213, the template, the cross-reference; supersedes four-items 4a and 4b
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: The work runs as eight passes, each a session ending with /handoff, recounted after the survey. Pass 1: vet and survey (D-0084, D-0085) and the PH 212 and PH 213 course lists (D-0088). Pass 2a, checks, one PR: the word check counts equations and image alt text (four-items calls 4.2 and 4.3's check); the number check (D-0078); the ordered-ids pin (D-0077); every equation the survey finds probed through the Word and HTML writers, since Pandoc's "Could not convert TeX math" warnings, seen with the plain writer, would fail the build's warning gates, and an equation rule added to `docs/conversion-spec.md` (critique finding 1); `tools/filters/questions.lua` fails on a question that opens with anything but a paragraph, where today it counts the question and returns without a label (F14(a)); the Word question box redrawn as a one-cell shaded table, the answer box's mechanism, so a question holding a list or bullets between its parts draws whole (finding 3, F14(b); D-0057's `custom-style` misses list items), which reopens the owner's D-0057 Word check of that box, with Google Docs added; the metadata strip (D-0086). Pass 2b, downloads, one PR, merged before pass 3: `--resource-path` and `--mathml` for the downloads, image extraction and publishing, CSS reverts for img, figure and math, HTML caps per lab (four-items item 4a). Pass 3: the two hardest handouts by the survey (the likely pair is PH 213 Lab 2, the owner's 2026-10-03 pick, and PH 212 Lab 1), then PH 211 Labs 2 to 7, hardest first. Pass 4: the rest of PH 212. Pass 5: the rest of PH 213. Pass 6: the template (D-0074 to D-0080). Pass 7: the cross-reference (D-0083). Supersedes items 4a and 4b of `docs/superpowers/plans/2026-10-03-four-items.md` and its Order for them.
- rationale: Check before content (four-items call 4.1: a check written in the same diff as the content it passes cannot be told from one shaped to pass). The spec's pass 2 dropped most of 4a (F2). A rule wrong for a hard case is found before 16 labs embody it, and the hardest handouts are tested first (finding 9). Eight passes against the owner's budget of six; the survey sets 2b's size and each conversion pass's difficulty, so the recount waits for it (finding 12). The owner, 2026-10-07: "2a checks, 2b downloads", "Pass 2: one-cell shaded table", "Hardest two first, then courses", "Eight; recount after survey".
- alternatives: pass 2 as the spec wrote it (check, pin, metadata; download and CSS work would land inside a content PR); all of 4a as one PR; the question box fixed in pass 6 (broken boxes in production Word downloads for passes 3 to 5) or a build failure in its place; course order, hardest first within each pass; PH 213 Lab 2 alone first; seven passes (2a and 2b in one session) or six (also the rest of PH 212 and PH 213 in one pass).
- binds: spec section 6; docs/superpowers/plans/2026-10-03-four-items.md (items 4a and 4b, Order); D-0057; tools/check_unchanged.py; tools/filters/questions.lua; tools/reference.docx; tools/downloads.py; STATE.md
- test: per pass; pass 2a's include PH 211 Lab 1 unchanged at 989 words and bold on 943
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0083  The cross-reference becomes pass 7, after the template: rubric and notes numbers against each handout, run from an instructor checkout
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-07
- decision: No instructor notes or rubrics are read in passes 1 to 6. Pass 7, after the template, runs from a checkout of `OSU-physics-lab-library-instructor` and compares, per lab, the rubric's "Qn:" text and the notes' cited question numbers with the converted handout's question n; misalignments are recorded by lab in a named file in the instructor repo, and nothing in either repo's content changes. Pass 7 also copies the instructor originals into the instructor repo's `originals/` (spec 9.5), brings the owner the two PH 211 Lab 6 notes files to pick the canonical one (9.3), fixes the instructor `CLAUDE.md`'s stale path (9.8), applies D-0086's strip there, and brings the instructor repo's copy of the check and its Pandoc up to the library's (critique F10); until then that copy and that repo's CI's Pandoc 3.11 lag the library's, which pass 7 records in that repo's own LEDGER. Pass 1's "notes and rubric facts" landing is dropped.
- rationale: The two critique passes disagreed: finding 10 kept the cross-reference in passes 3 to 5 and dropped pass 1's instructor landing; F12 would delete it until content changes begin, since in a format-only phase its findings change nothing. The owner, 2026-10-07: "F12 but instead of deleting it and waiting until content changes, we do it in a separate pass once the rest of the work is done." Claude's conditions, confirmed by the owner the same day: a named job (the owner's own question that day, whether the rubric workbooks hold the numbers, supplies it) and an instructor checkout, which keeps gate 8.7 and needs no secret (D-0089).
- alternatives: once per course in passes 3 to 5 (finding 10; D-0098, declined); deleted until content changes (F12); its job left to its plan.
- binds: spec sections 6 and 7 and 9.3, 9.5, 9.8; OSU-physics-lab-library-instructor (its LEDGER 5, its CI's Pandoc, its CLAUDE.md)
- test: pass 7's own
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0084  Vetting: the owner's word clears the handouts, summaries and course-wide files; no pre-scan; nothing outside the in-scope list is opened
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: The owner's word is the ruling that the 19 PH 21X handouts, the PH 212 and PH 213 curriculum summaries and the four course-wide files at the folder's root (spec section 2) hold no student data; PH 211's summary was read and quoted on 2026-09-19 (LEDGER 45). Sonnet subagents may read them in full in pass 1; each reader's prompt says that on meeting anything resembling a student record it stops and reports the file and the location only, never the text. No pre-scan script is built. The excluded files (spec section 2) stay unopened, and PH 211's `List of terms.docx` joins them; gate 8.1 becomes: nothing outside the in-scope list is opened. Instructor notes and rubrics are read only in pass 7 (D-0083).
- rationale: The owner, 2026-10-07: "These are lab handouts; no student PII is in them. Is there still any need for a pre-scan?" A pre-scan (critique F3) would print counts and locations only; with the owner's word, its one remaining job, finding names in file metadata, belongs to the strip (D-0086), which reports what it removes. `CLAUDE.md`'s rule, read an original in full for student data before planning around it, is met by the survey's full read. LEDGER 22(e) groups `List of terms.docx` with the sample-contract candidates, and F3 found it unexcluded; F3 also found that gate 8.1 did not forbid out-of-scope files. The owner, 2026-10-07: "None; add List of terms", then "No pre-scan; subagents may read".
- alternatives: a pre-scan first (F3; D-0094, declined); the handouts alone cleared, the summaries and course-wide files read by the main session; three Sonnet readers with no clearance (spec section 6 as written); the excluded files moved out of the folder by the owner.
- binds: spec sections 2, 6, 8.1 and 9.1; CLAUDE.md (Conventions: originals unvetted); LEDGER 22(e); charter floor 11
- test: none; the entry holds no quantity
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0085  Pass 1's survey: one markup rule per structure for every output, em dashes counted, every original hashed, each lab's deliverable recorded
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: Pass 1 reads each in-scope handout and records, in a table in this repo that holds nothing drawn from notes or rubrics (spec 9.7): its structures (spec section 5, S1 to S8 and any new one), D-0078's numbering counts, its count of U+2014, its SHA-256, and per lab the deliverable, the weeks, the submissions and any report item that is not an answer to a question (data, plots, drawings; F7). It amends `docs/conversion-spec.md` with one markup rule per structure, each stating what the faithful page (the original's "4)" exactly), the modern page, the Word download and the template show, so an item needing no answer or a stem is never labelled "Question N" or boxed (finding 4). If any original holds an em dash, a rule comes before pass 3, since CI fails on U+2014 in `curriculum/` and `site/` and the word check fails on a changed word (F4); implementers never write `ruled_omissions` or `ruled_additions` without a promoted entry. Each conversion task re-hashes its original and stops on a change (F5). Pass 6 makes a template only for labs whose deliverable is a question report; capstones and the rest get none until the owner rules on the survey's evidence. Agent worktrees: pass prompts carry the absolute path to the originals, never committed, and the root `.gitignore` gains `.superpowers/` before pass 1 (F13).
- rationale: The owner, 2026-10-07, accepted finding 4, F4 and F5, and "Survey records it; pass 6 rules" for F7. Spec 9.7 and F13 were taken as Claude's calls, the owner told he could veto either; he did not.
- alternatives: none raised for finding 4, F4 or F5; for F7, every lab gets a template, or capstones ruled before the survey.
- binds: docs/conversion-spec.md; spec sections 5 and 9.7; .gitignore; the em-dash scan in .github/workflows/verify.yml
- test: none in pass 1; the hash re-check is per task
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0086  Originals are committed with every identity-bearing part stripped, in both repos; amends LEDGER 18
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: Before an original is committed, in either repo, every identity-bearing part is stripped: `creator` and `lastModifiedBy` in `docProps/core.xml`, `docProps/app.xml`'s Company and template path, comment and revision authors, `word/people.xml`, and EXIF in embedded photos. The stripped file is committed and front matter's `source_sha256` names it; an entry records both hashes, the original's and the stripped file's, so anyone holding the original can tie the two. No text run (`w:t`) changes, so the word check is unaffected; image checks read the stripped file. The strip is built in pass 2a and runs on every original committed here from then on; the instructor repo gets it in pass 7 (D-0083), its committed PH 211 rubric workbook replaced by a stripped copy. Neither repo's history is rewritten: PH 211 Lab 1's committed original and its history stay D-0062's question; the instructor repo is private and never published. Settles four-items Q16 for PH 213 Lab 2. Amends LEDGER 18 (originals byte for byte).
- rationale: This repo will become public, git history is permanent, and the house rule is roles, not names (`CLAUDE.md`). F6 found spec 9.2 too narrow: identity also sits in comment and revision authors, `people.xml`, `app.xml`, template paths and photo EXIF, and in both repos (the instructor repo's committed rubric workbook carries `creator` and `lastModifiedBy`). The owner, 2026-10-07: "Strip all parts, both repos", then "Pass 7, with 9.5 and 9.8" for the instructor repo.
- alternatives: `core.xml` only (spec 9.2's lean); this repo only; commit as is (LEDGER 18); the instructor strip in pass 2a.
- binds: LEDGER 18; docs/conversion-spec.md (Originals); four-items Q16; D-0062; both repos' `originals/`
- test: pass 2a: a fixture original with each identity part; after the strip none remains and its word sequence is unchanged
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0087  A Word original stays the live document until sections switch to the library's version
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: Until sections hand out the library's version of a handout, its Word original is the live document. When a colleague edits it after conversion, the new file is stripped (D-0086) and hashed, its word difference from the old original is applied to the Markdown, the check runs against the new file, and an entry records the old and new hashes. Once sections switch, the Markdown is the source (`docs/conversion-spec.md`, Flow) and edits are made there. Before a conversion merges, a changed original stops its task (D-0085).
- rationale: 11 of 19 handouts were saved between 2026-07-20 and 2026-08-20 and sections use the Word files now; rule 3.8 did not say which version is "the original" (critique F5). The owner chose this 2026-10-07.
- alternatives: frozen at conversion, later edits recorded for the content-change phase (the library drifts from what students hold this year); asking colleagues to stop editing the Word files (a mid-term ask they may not follow).
- binds: docs/conversion-spec.md (Flow); D-0077; D-0085
- test: none; when sections switch is the owner's call
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0088  PH 212 and PH 213 course lists are quoted from their summaries in pass 1; amends LEDGER 45
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: After pass 1 reads the PH 212 and PH 213 curriculum summaries, one PR quotes each summary's lab numbers, titles and one-line descriptions into `site/courses.md` word for word, as PH 211's were quoted from its Activities table, every lab under "Not yet converted" until converted; the two notes saying none is in hand to list are removed; the file's comment's "ledger 43" becomes "ledger 45". If a summary has no such list, the PR stops and the owner rules. Each later conversion adds its lab's `document` key the same way (F14(c)). Amends LEDGER 45's last sentence ("PH 212 and PH 213 have no material in hand").
- rationale: The live course pages for PH 212 and PH 213 say none is in hand to list (`site/courses.md` lines 47 and 51), false since both summaries reached the owner's folder (critique finding 7). A converted lab appears on its course page, tile and course download only through a row with a `document` key, and LEDGER 45 permits a row only for a lab its summary lists, so each conversion needs the quoting anyway. The owner, 2026-10-07: "Quote both lists in pass 1".
- alternatives: correct the sentence only and quote row by row as labs convert (the pages unlike PH 211's until the end; the same quoting ten times); leave until conversion (a false statement on the live site for several passes).
- binds: LEDGER 45; site/courses.md; D-0069; D-0070; D-0071
- test: the PR's: each course page lists its quoted labs
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0089  A check that crosses the two repos waits for the public flip; pass 7 runs locally
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: Pass 7 (D-0083) runs on the owner's machine from the two checkouts and needs no token or deploy key. Any CI check in the instructor repo that reads this repo's source (spec section 7, later) waits until this repo is public (D-0062); none is built before.
- rationale: While this repo is private, the instructor repo's CI could read it only with a secret, and `CLAUDE.md` forbids touching a secret without the owner's word (critique finding 13). Accepted by the owner 2026-10-07.
- alternatives: a deploy key or token for the instructor repo's CI.
- binds: spec section 7; D-0062
- test: none; the entry holds no quantity
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0090  Claude checks every page and PDF; the owner checks Word for the hardest two handouts and one lab per later pass
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: For each converted lab, Claude screenshots the modern page, the faithful page and the PDF in the browser pane and checks them against the original (equations, arrows, images, boxes). The owner checks the Word download, in Word, for the two hardest handouts (pass 3's first two), which set the conversion rules, and for one lab per later conversion pass. The template's check is D-0079's.
- rationale: The owner's time, not dispatches, is the binding cost: 18 labs, each two pages and four downloads, about 108 views (critique F16); only the owner, in Word, checks what Word shows (D-0057). The owner chose this 2026-10-07.
- alternatives: every view of every lab by the owner (full strength); the template check alone (Word display faults seen by no one before students).
- binds: spec section 6; D-0057
- test: none; a review practice
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0091  The outcome measure: a TA estimate of minutes per report before Winter 2027, and the same question a term after first use
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: Before Winter 2027, a few TAs are asked for a one-line estimate of the minutes they spend grading one group report; a term after the templates' first use, the same question. Both answers are recorded in an entry. No timed study.
- rationale: The spec says how B is built, not how anyone will know it worked; the 2026-10-06 session named TA minutes per report as the measure, and without a baseline taken before first use there is nothing to compare (critique finding 6). The owner chose this lean-plus-earmark 2026-10-07.
- alternatives: a timed week before and after (full strength: TA time and the owner's follow-up); no measure.
- binds: STATE.md (awaiting owner)
- test: none; two recorded answers
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0092  PH 213 Lab 2's carried calls: labels at Word's positions, a stop on equation differences, its id, the photograph as is, the 3 MB original
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: The leans of `docs/superpowers/plans/2026-10-03-four-items.md` Q12 to Q15 and Q17, carried into pass 3 by D-0082 (critique F2): Q12, the labelled photograph keeps its labels at the positions Word stores, generated by the build from the original (call 4.4, A); Q13, if the equation round trip shows differences normalization cannot remove, Claude stops and brings the list to the owner; Q14, the id `ph213-hypothesis-testing-handout`; Q15, the photograph published as is (944 KB, 2637 px wide), the page measured on a phone, then a smaller derived copy decided; Q17, the 3 MB original committed, stripped per D-0086 (Q16).
- rationale: "Do not use" must stay on its knob (Q12); a check loosened until it passes is no check (Q13); the course code separates it from PH 211 Lab 4, also titled "Hypothesis Testing" (Q14); the size is a one-time cost (Q17). The owner accepted all five leans 2026-10-07.
- alternatives: as the plan lists them (Q12 B and C; Q15's derived copy now; Q17 not committing the original).
- binds: docs/superpowers/plans/2026-10-03-four-items.md (calls 4.3 to 4.5, Q12 to Q17); D-0082; D-0086
- test: pass 2b's and pass 3's
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0074 to D-0092")

### D-0099  PH 212 and PH 213 course lists quoted whole from their summaries' Activities tables, with two quoting calls; amends LEDGER 45
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: Under D-0088, PR #30 (squashed as `35310ce`) quotes into `site/courses.md` the Activities table of "PH 212 Curriculum Summary" and of "PH 213 Curriculum Summary": every row, the unnumbered Lab Skills practical row included as PH 211's is, seven per course, each lab under "Not yet converted". Cells are read from the summaries' Word XML, so quote marks are Word's. A cell's paragraphs are joined by one space, so PH 212's Lab 3 and Lab 6 titles read "Designing Experiments (Two weeks)" and "Capstone (Two weeks)" as their Title cells do; runs of spaces become one; no word or character is changed. Each course gets a `source_note` naming its summary, both "none is in hand to list" notes are removed, and the comment cites ledger 45. Course names stay empty while four-items Q4 is open; Q4 now covers PH 212 as well as PH 213. Amends LEDGER 45's last sentence ("PH 212 and PH 213 have no material in hand").
- rationale: D-0088 (ruled) directs the quoting and this entry. "(Two weeks)" sits in the Title cell, so word for word keeps it there. Whitespace is not a word, and HTML collapses it anyway. Found on the way: `render.pandoc_meta` returned strings already escaped by Pandoc's HTML writer, and every caller escaped them again, so "Sharing & Comparing" showed as "&amp;" in the PR's first build; fixed in the same PR. The data-driven page tests compared against the same escaped data, so the new test reads the raw HTML.
- alternatives: titles without "(Two weeks)" (not word for word); the parenthetical moved to the description (rearranges the summary's columns); course names from each handout's course line now (Q4, open).
- binds: LEDGER 45; D-0088; site/courses.md; tools/render.py (`pandoc_meta`); tests/test_quarto_chrome.py
- test: `test_every_course_lists_its_summary`: every course lists labs and a source note, no "none is in hand", each title and description on its page, each title escaped once
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("I agree with all your leans")


### D-0100  Pass 1's survey is recorded in docs/handout-survey.md; nine handouts are not simple under D-0078, and a style-set part level counts as a fourth feature
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: The survey D-0085 orders lives in `docs/handout-survey.md`. Its one table has a row per handout (19): SHA-256, U+2014 count, D-0078's counts and verdict, objects, structures by anchor, deliverable, weeks, submissions, report items that are not answers. Around it: the new structures S9 to S17, draft markup rules for ruling (its section 5, not binding until ruled into `docs/conversion-spec.md`), the hardest two, and the recount. Counts come from the originals' Word XML; classifications from four Sonnet readers (D-0084), none of which met a student record. Findings that bind until the owner rules otherwise: (1) a part's level set by a style whose list is inherited from its base style is a fourth D-0078 feature, since Pandoc reads such parts as top-level questions (PH 212 Labs 1, 2, 3 and 5); (2) nine handouts are not simple (PH 211 Labs 6, 7; PH 212 Labs 1, 2, 3, 5, 6; PH 213 Labs 5, 6) and each comes to the owner before its conversion, with the look in Word the survey's section 3 lists; (3) for those nine, Pandoc's reading of the numbers is not a check.
- rationale: D-0085 names no file. The table is public-safe (spec 9.7: nothing from notes, rubrics or the instructor guidance file; no names, link targets or absolute paths), so it lives beside the conversion spec it feeds. The fourth feature, PH 212 Lab 3: the "Subquestion" style sets `ilvl` 1 and is based on "Question", which carries the `numId`; `numbering.xml` links level 1 to "Subquestion"; Pandoc prints 42 top-level numbers where Word has 24. PH 212 Lab 1's own citations ("question 6", "question 11") resolve to the right items only under Word's levels.
- alternatives: the table inside the spec (the spec does not need a dated appendix); a dated file name (the hashes are the record until an original changes, D-0087, so the file is updated, not superseded).
- binds: D-0078, D-0082, D-0085, D-0092; docs/handout-survey.md; docs/conversion-spec.md (once its rules are ruled); spec section 5 (its PH 212 sample numbers are Pandoc's)
- test: none in pass 1; pass 2a's number check
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("I agree with all your leans")

### D-0101  One markup rule per structure, S1 to S17, is in docs/conversion-spec.md; drawn figures become SVG built in pass 2b
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: The survey's draft rules (D-0085, finding 4) enter `docs/conversion-spec.md` as "Markup rules per structure", the one copy; the survey keeps a pointer. Among them: an item needing no answer is `.question .no-answer`, labelled by its number alone, never "Question N", and left out of the template; a stem is question N, its parts inside one block; the modern page unbolds the whole question block; a restart is `.question .restart`; an unnumbered report item is marked `::: report-item` at conversion; page headers and page numbers are not converted; the contents field becomes links. Amended on ruling, S13: a figure drawn from Word's shapes, groups and text boxes becomes an SVG the build makes from the original, its text kept as SVG text at Word's positions, with a PNG made from it for the Word download and the template. Pass 2b builds it, opening with LibreOffice installed (winget locally, apt in CI, version pinned) and its SVG of the three figures (PH 212 Lab 3, PH 213 Labs 2 and 4) measured against Word; a small converter of the shapes these figures use only if LibreOffice is not faithful. Pictures (S12) stay the original files: all 53 media files are raster (45 PNG, 8 JPEG).
- rationale: The owner, 2026-10-07: "I agree with all your leans", then on SVG for images: "Yes, SVG for drawn figures in 2b", and on a converter of our own: "let's install LibreOffice". SVG keeps the labels as text (sharp, read aloud, readable by the word check) and is generated from the original, so it cannot drift; wrapping or tracing a raster would gain nothing or change the image. Google Docs' SVG import is not relied on, hence the PNG.
- alternatives: a raster rendering of each drawn figure (labels become pixels); figures redrawn by hand (a second copy the check cannot see); SVG for every picture (no vector source exists).
- binds: docs/conversion-spec.md; docs/handout-survey.md section 5; D-0092 (Q12, the labelled photograph); D-0082 (pass 2b); D-0079 (the template check covers the PNG); tools/filters/questions.lua (pass 2a: `.no-answer`, `.restart`, whole-block unbold)
- test: pass 2a's for `questions.lua`; pass 2b's for the SVG and its text

### D-0102  Word's own labels, read once per original by Word's automation, are what the number check compares; amends D-0078
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: Claude reads Word's displayed list labels for every handout through Word's automation on this machine, on copies in the session scratchpad, read-only, closed without saving; the owner's look in Word is not needed. The labels are recorded per original, keyed to its SHA-256, and pass 2a's number check compares the converted lab's numbers (questions, no-answer items, parts) against that record in CI. A changed original fails the hash and is re-read (D-0087). No reader of Word's numbering XML is built, and Pandoc's reading is not used as the check. Amends D-0078's method.
- rationale: Pandoc misreads four handouts (D-0100), and the five with overrides or a missing start value are exactly where an XML reader would have to guess Word's semantics. Word's own labels need no guess. The owner, 2026-10-07: "I agree with all your leans".
- alternatives: an XML reader of `numPr` and `numbering.xml` (critique F1; guesses where it matters); the owner reading the nine in Word (about 15 minutes, by hand); Pandoc for the simple ten (two methods for one check).
- binds: D-0078; D-0100; tools/check_unchanged.py or a sibling (pass 2a)
- test: pass 2a: a fixture whose numbers differ from its recorded labels fails

### D-0103  An original's em dash is kept; the em-dash scan skips converted files
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: A converted file keeps every U+2014 its original holds (PH 212 Lab 2 has one). CI's em-dash scan skips files whose front matter names a `source_file`, whose words the word check already proves are the original's. Built in pass 2a.
- rationale: Conversion is format only, and co-owned text keeps its authors' words (charter floor 9); a ruled change of dash would be a content change. The owner, 2026-10-07: "I agree with all your leans".
- alternatives: a ruled change to another dash, declared in `ruled_additions` and `ruled_omissions`.
- binds: D-0085; .github/workflows/verify.yml (pass 2a)
- test: pass 2a: a converted fixture with its original's em dash passes the scan

### D-0104  PH 212 Lab 2's activation code is a ruled omission; PH 212 Lab 6's personal OneDrive link loses its target
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: When PH 212 Lab 2 is converted, the software activation code's text is declared in `ruled_omissions` citing this entry, and the code never enters this repo. When PH 212 Lab 6 is converted, the word "your" linked to a personal OneDrive document stays as plain text, its link target dropped. Neither the code nor the target is written in any file here.
- rationale: The repo will become public and git history is permanent; an activation code is a secret, and a personal OneDrive path names a person. D-0086's strip does not reach link targets, and the word check does not read them. The owner, 2026-10-07: "I agree with all your leans".
- alternatives: keep either as written; replace the code with a placeholder sentence (a content addition).
- binds: D-0086; docs/handout-survey.md section 7; the PH 212 conversions
- test: those conversions' word check, with the omission declared

### D-0105  Pass 3 opens with PH 212 Lab 3 and PH 213 Lab 2; amends D-0082's likely pair
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: The survey's hardest two, PH 212 Lab 3 (most numbering risk) and PH 213 Lab 2 (most equation and figure risk), open pass 3, then PH 211 Labs 2 to 7; PH 212 Lab 1 joins the rest of PH 212 in pass 4. The owner checks the Word download of these two (D-0090).
- rationale: Between them they meet every structure but S1 at the top level, S6, S8 and S17; PH 212 Lab 1's numbering and equation hazards are smaller versions of Lab 3's (survey section 9). The owner, 2026-10-07: "I agree with all your leans".
- alternatives: PH 213 Lab 2 and PH 212 Lab 1 (D-0082's likely pair); PH 213 Lab 4 for its drawn figure.
- binds: D-0082; D-0090; D-0092
- test: none; pass 3's own

### D-0106  Eight passes in seven sessions: pass 7 runs in pass 6's session once 6 merges
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: The work stays eight passes (1, 2a, 2b, 3, 4, 5, 6, 7) in seven sessions against a budget of six: pass 7, local and landing in the instructor repo (D-0083, D-0089), runs in pass 6's session after pass 6 merges. 2a and 2b stay separate sessions, and so do 4 and 5.
- rationale: The survey grew 2a (Word's labels, the em-dash rule) and 2b (pictures in 15 handouts, equations in all 18, now the SVG figures); 4 and 5 are where S9 and S10 first meet volume (survey section 10). The owner, 2026-10-07: "I agree with all your leans".
- alternatives: eight sessions; six, by also pairing 2a with 2b or 4 with 5.
- binds: D-0082; STATE.md
- test: none

### D-0107  PH 212's and PH 213's course names come from their handouts' own course lines; settles four-items Q4
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: As PH 211's name comes from its Lab 1 handout's course line (`name_source` in `site/courses.md`), PH 212's and PH 213's come from their handouts' course lines, quoted, each with its `name_source`. The edit is site content, so it lands by PR; not yet made.
- rationale: The same rule for every course (four-items Q4's lean). The owner, 2026-10-07: "I agree with all your leans".
- alternatives: names left empty until a summary gives one.
- binds: site/courses.md; four-items Q4; D-0099
- test: the course-page tests already compare the heading with `name`

### D-0108  The faithful page is retired; the modern page is the one presentation; amends LEDGER 28
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-07
- decision: Colleagues have approved the modern format, so the faithful presentation (the original's look, "N)" numbering, bold questions) is retired. One Markdown source now feeds one presentation, modern, plus the downloads, which already come from modern (D-0053). To retire: `themes/faithful.css`; `questions.lua`'s faithful branch; the faithful pages and the switch link between the two presentations; and their tests and CSS. Each faithful address redirects to its modern page, as the old "How this was made" address does (D-0072). The public words that describe two presentations (VISION.md's method section, `site/landing.md`, "How this site works") are redrafted for the owner's line edits before the PR merges. Built as its own PR in pass 2a, which changes `questions.lua` anyway. Unchanged: conversion stays format only, and the template's and the handout's numbers still equal the original's (rule 3.8, D-0077), so Word's labels (D-0102) and the number check keep their job. The Faithful column of `docs/conversion-spec.md`'s markup rules (D-0101) lapses. Amends LEDGER 28; D-0090's faithful screenshot drops.
- rationale: The owner, 2026-10-07: "the modern format was greenlit by colleagues; 'read it as it was written' is no longer needed anyway", then "Retire the faithful page." LEDGER 28's pilot existed to let readers compare the two; the comparison is done.
- alternatives: keep the faithful page as an archive view (a second presentation to maintain, test and screenshot per lab, with no reader).
- binds: LEDGER 28; D-0053; D-0072; D-0090; D-0101; themes/faithful.css; tools/filters/questions.lua; tools/render.py; tools/quarto_build.py; site/site.css; tests; VISION.md; site/landing.md; site/how-this-site-works.md; CLAUDE.md (Build); docs/conversion-spec.md
- test: pass 2a's PR: no faithful page is built, each old faithful address redirects to its modern page, and the downloads are unchanged

### D-0109  A numbered item needing no answer is a required step, labelled "Required step N" on its own count, in a question-like block of another palette colour; amends D-0101's S1
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-07
- decision: A top-level numbered item that asks for no answer (S1; in the survey, PH 213 Lab 6's "0)", exchange contact information, and its Week 3 "1)", submit the slides) is marked `::: {.required-step #id}` in the source. The page shows it in the same kind of block as a question, in a different colour taken from the ruled palette and chosen by the owner on a design board. It is labelled "Required step 1", "Required step 2" and so on, counted per lab apart from the questions. Questions keep Word's numbers, so after PH 213 Lab 6's "0)" its questions read Question 1 and 2, and no "0" is shown. The Word download carries the same label and block. The template leaves required steps out, since they need no answer. S1 parts (options, case labels, actions inside a question) stay list items as written.
- rationale: The owner, 2026-10-07: "Question 0 is not really a question, but a WARNING/PAY ATTENTION/DO THIS", proposing the question's block in another colour, then "Callout 1, 2, 3, etc." so that a TA can point to it "when a student says 'I didn't know I was supposed to do that.'" Claude leaned "Required step N", plain terms (LEDGER 17) that say what to do; the owner, the same day: "Required step is better, I agree."
- alternatives: the number alone and no block (D-0101 as ruled); "Callout N" (a design word students may not know); keeping "0".
- binds: D-0101 (S1); docs/conversion-spec.md; tools/filters/questions.lua; tools/reference.docx (a required-step style); site/site.css and themes/modern.css (the colour, after the board); tests/test_brand.py (the palette)
- test: pass 2a: a fixture with a required step before two questions renders "Required step 1", then "Question 1" and "Question 2"; the template has none

### D-0110  The no-answer block is labelled "Checkpoint N", a general label for what students do or show; corrects D-0109
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-07
- decision: D-0109's label "Required step N" becomes "Checkpoint N" and its source mark `::: {.checkpoint #id}`. Everything else in D-0109 stands: a question-like block in another palette colour picked on a board, its own count per lab, questions keeping Word's numbers, the same in the Word download, left out of the template. "Checkpoint" is meant to generalize. When content changes begin, the same block can carry other things a group must do or show, for example a talk with a TA and a conceptual question at the end of every lab. Adding those is a content change, not part of the conversion.
- rationale: The owner, 2026-10-07: "required step" "implies that some steps are not required, which is not the message we want to send to students", then "I like checkpoint because it generalizes". Claude had leaned "Task N"; it had noted that "checkpoint" can suggest a TA signs off, which the owner's future use embraces.
- alternatives: "Required step N" (D-0109; implies optional steps); "Task N"; "Step N" (every round-bullet action is a step); "Action N" (collides with the legend's "action items").
- binds: D-0109; D-0101 (S1); docs/conversion-spec.md; tools/filters/questions.lua; tools/reference.docx
- test: as D-0109's, with "Checkpoint 1"

### D-0111  Pace markers ("by this time, be done with Part N") are earmarked as their own label, not built and not a gate
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-07
- decision: The owner wants consistent time markers through each lab, so that a group can see it is moving too slowly. These would be a separate label from "Checkpoint". Nothing is built and nothing waits on them, because the times are not known; they need measured times per part first. Adding them is a content change, for the content phase.
- rationale: The owner, 2026-10-07: "consistent timestamps to indicate the progression through the lab and give a signal if a group is moving too slowly. This does, however, require knowing what those times are, so I would earmark that rather than set it as a gate." Whether a time marker is a checkpoint he left open, "maybe that's a separate label"; it is recorded as separate until he rules otherwise.
- alternatives: pace markers as a kind of checkpoint; set now from estimates (times not known).
- binds: D-0110; the content phase
- test: none

### D-0112  Pass 2a ships as three PRs: checks, the Word box with the checkpoint colour, the faithful retirement; the number check keys on content parts; amends D-0082
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: Pass 2a lands as three PRs. PR 1, checks: the word check counts equations (four-items call 4.2), image alt text and a SYMBOL field's character; the number check against `docs/word-labels.json`; the ordered-ids pin (D-0077); the em-dash scan skips converted files (D-0103); the strip tool (D-0086); and `tools/filters/questions.lua`'s logic: whole-block unbold, `.checkpoint` labelled "Checkpoint N" on its own count, `.restart`, and a failure on a question that opens with anything but a paragraph. PR 2: the Word question box as a one-cell shaded table, the checkpoint's Word block and its palette colour, gated on the owner's pick from a board and his check in Word and Google Docs (D-0082, reopening D-0057's). PR 3: the faithful retirement (D-0108), gated on his line edits to the redrafted public wording. The equation probe, its rule in `docs/conversion-spec.md`, the board and the wording draft land direct on `main`. Three calls ruled with the split: (1) each record in `docs/word-labels.json` gains a SHA-256 over the parts its labels depend on (`word/document.xml`, `word/numbering.xml`, `word/styles.xml`), computed from the same 19 originals; the number check matches a converted lab's original by that hash, which the strip leaves unchanged, and fails when none matches. (2) PR 1 strips PH 211 Lab 1's committed original, with an entry recording both hashes; the instructor repo's originals are stripped by a PR there; the history question stays D-0062's. (3) At an anchor marked as a checkpoint the number check requires a checkpoint and compares no number; every question's number and every part's letter must equal Word's; so S9 needs `.restart` and no start value, since PH 213 Lab 6's questions count from 1 once its "0)" is a checkpoint. An anchor the check cannot place fails it.
- rationale: The number check reads the labels the filter writes, so it checks what students see rather than a second copy of the numbering rule, and it cannot be built before the filter knows `.checkpoint` and `.restart`; so the filter's logic rides with the checks. PR 2's two gates are both the owner's eye, and holding the checks behind them gains nothing. A whole-file hash cannot survive D-0086's strip, while the strip touches only `docProps` in all 19 handouts (survey section 8: no comments, revisions, `people.xml` or EXIF). The owner, 2026-10-07: "Three PRs, calls 1, 2, and 3 leans agreed."
- alternatives: two PRs, as D-0082 and D-0108 wrote it (the checks wait on the board and the Word and Google Docs check); for call 1, a typed `unstripped_sha256` in front matter (no file in the repo can verify it) or re-keying the record at each conversion; for call 2, waiting for pass 3; for call 3, a start value on S9.
- binds: D-0082; D-0086; D-0102; D-0108; D-0110; docs/word-labels.json; docs/handout-survey.md section 3; tools/check_unchanged.py; tools/filters/questions.lua; .github/workflows/verify.yml
- test: PR 1's fixtures: a question number differing from Word's fails; a checkpoint where Word has one passes with no number compared; an unplaceable anchor fails; a content-parts hash with no match fails

### D-0113  Equation rule: Pandoc's TeX, corrected where its round trip to Word's equation differs; the comparison reads OMML's attribute characters
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: The probe D-0082 orders ran on all 19 handouts (322 equations) and its rule is in `docs/conversion-spec.md`, "Equation rule". The Word writer and the HTML writer with `--mathml` warn on none; only the plain writer warns (66 warnings in 15 handouts), and no build step uses it. A converted source keeps Pandoc's TeX except where its round trip to OMML differs from Word's equation; there the TeX is corrected to Word's characters and structure: a typed "√" and a typed "°" stay characters (Pandoc reads them as an empty `\sqrt{}` and a superscript `\circ`), and a delimiter stays `\left...\right`. Six equations in four handouts need it. The comparison is four-items call 4.2's, amended: OMML's attribute characters (delimiters, n-ary operator, accent, group character) are read into the text; normalization adds U+002D to U+2212 and drops U+200B; the structure signature counts 18 kinds and leaves out `m:func`. PH 213 Lab 2's one equation inside the photograph's labels is the figure's (S13, pass 2b), not `Math`.
- rationale: Under call 4.2 as written, 13 equations differ; seven are normalization only (the minus sign, a zero-width space Pandoc's writer puts in empty limits), and six are Pandoc misreads that change what a student sees (an empty radical, a ring for a degree sign, lost bars). Correcting the TeX keeps the check strict and the page true to Word; loosening the compare to pass them would let the same misreads through silently. Each correction was round-tripped and equals Word's text and structure, with no warning from either writer.
- alternatives: keep Pandoc's TeX and declare each difference (the page would show the misreads); normalize the misreads away (the check would stop seeing them).
- binds: docs/conversion-spec.md (S5, Equation rule); tools/check_unchanged.py (pass 2a PR 1); tests/test_downloads.py (pass 2b: equations compared apart from the plain-writer words); D-0082; D-0092
- test: PR 1's equation fixtures: a dropped, swapped, changed or kind-changed equation fails; an empty `\sqrt{}` in place of a typed "√" fails
- corrected: 2026-10-07, the rationale's count: under call 4.2 as written, 17 equations differ, 10 of them normalization only (the minus sign, a zero-width space), 6 Pandoc misreads, and 1 inside the drawn figure; not 13 and seven. The spec's 315 of 322 stands.
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("C, promote D-0113 and D-0114, wording 1-7 as drafted. Word and Google Docs appear clean--nice work.")

### D-0114  PH 211 Lab 1's committed original is stripped of its identity parts; both hashes recorded
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: Under D-0086 and D-0112's call 2, pass 2a's PR 1 replaces `originals/PH211/Lab 1 - Team Building - Handout.docx` with its stripped copy, made by `tools/strip_identity.py`: `dc:creator` and `cp:lastModifiedBy` removed from `docProps/core.xml`, `Company` and `Template` from `docProps/app.xml`; every other part byte for byte. Original SHA-256 `49617ff874c0e2147a73bbfb39db38272e53be360ae10430a17e6a5358608091` (the survey's and `docs/word-labels.json`'s); stripped `aed082da8a25ecd8b5adc75dae1aa696c9d7d1503df4bb196cc8996c9e01fd00`, now the lab's `source_sha256`. The word check still reads 989 words identical and bold on 943; the number check finds Word's labels by the unchanged content parts. Its `customXml` parts hold Google Docs' round-trip data, which D-0086 does not list and which names no one. The file's history before this commit is D-0062's question. The instructor repo's originals are stripped by a PR there.
- rationale: D-0086 (ruled) and D-0112 (ruled): "Three PRs, calls 1, 2, and 3 leans agreed."
- alternatives: waiting for pass 3's first stripped original (D-0112, call 2).
- binds: D-0086; D-0112; curriculum/ph211/ph211-team-building-handout.md; originals/PH211
- test: CI's content check on PH 211 Lab 1 (hash, words, bold); tests/test_strip_identity.py
- corrected: 2026-10-07, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("C, promote D-0113 and D-0114, wording 1-7 as drafted. Word and Google Docs appear clean--nice work.")

### D-0115  The checkpoint block is Candela with a Luminance rule; the Word question box passes the owner's check in Word and Google Docs; the retirement wording is ruled as drafted
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-07
- decision: (1) Checkpoint colour, option C of `docs/design/2026-10-07-checkpoint/`: on the light page a Candela (#FDD26E) fill and a Luminance (#FFB500) rule; on the dark page the dark tint with a Luminance rule; in print a black rule and no fill, as a question; in the Word download a one-cell table with the light page's fill and rule. Built in pass 2a's PR 2 and pinned in `tests/test_brand.py`. (2) The one-cell shaded table that PR 2 draws for each question in the Word download passes the owner's check in Word and in Google Docs, as D-0082 required, reopening D-0057's; recorded as D-0057's check was. (3) The public wording of `docs/superpowers/plans/2026-10-07-faithful-retirement-wording.md`, passages 1 to 7, is ruled as drafted and ships in PR 3 with the retirement (D-0108).
- rationale: The owner, 2026-10-07: "C, promote D-0113 and D-0114, wording 1-7 as drafted. Word and Google Docs appear clean--nice work." Option C was the board's lean: yellow is the caution colour his "WARNING/PAY ATTENTION/DO THIS" (D-0109) asks for, and it is the one option that differs from the question box by fill, where A and B differed from its orange rule by hue alone (1.15:1, 1.05:1). Text on Candela: black 14.62:1, the Rogue Wave label 6.19:1; the Luminance rule on the dark tint 9.07:1.
- alternatives: A, Pine Stand rule on the question's tint; B, High Tide rule on the question's tint.
- binds: D-0057; D-0082; D-0108; D-0109; D-0110; themes/modern.css; tools/downloads.py; tools/filters/questions.lua; tests/test_brand.py; VISION.md; site/landing.md; site/how-this-site-works.md
- test: PR 2: the checkpoint tokens equal the two palette values and meet their contrasts; a checkpoint renders in a Candela box in Word. PR 3: the ruled passages are on the built pages.

### D-0116  The one-source sentence is not on student-facing pages; it stays only in "How this site works"
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-07
- decision: The lab page footer drops its sentence about the page and its downloads being built from one Markdown file (it read "Both presentations are built from one Markdown file, so they cannot drift apart." before D-0108); the footer keeps "Downloads carry the same draft notice as these pages." The point is made only on "How this site works" ("Nothing is copied by hand, so the versions cannot disagree."). Built in pass 2a's PR 3.
- rationale: The owner, 2026-10-07: "That sentence is not needed in student-facing materials. Leave it in \"How this site works\" and nowhere else." Claude had proposed "This page and its downloads are built from one Markdown file" in its place.
- alternatives: the proposed rewording on every lab page.
- binds: D-0108; D-0115; tools/template.html; site/how-this-site-works.md
- test: the lab page's footer holds the draft-notice sentence (tests/test_downloads.py, FOOTER_NEW) and no "drift apart"

### D-0117  Drawn figures come from a converter of our own, not LibreOffice; labels broken by font widths; inline SVG with a Chrome PNG for Word; amends D-0101
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-08
- decision: Pass 2b measured LibreOffice 26.2.5.2 against Word's own PDF of the three drawn figures (`docs/superpowers/plans/2026-10-08-pass-2b-figures.md`): not faithful. Four calls, ruled as leaned. (1) `tools/figures.py`, standard-library Python, reads a drawing's XML from the original and writes SVG, its labels and equation as SVG text; it knows only the shapes these figures use (rectangle, parallelogram, cube, straight connector with arrowheads, picture and picture-filled rectangle, text box) and stops the build on any other. LibreOffice is not installed in CI; D-0101's apt step lapses. (2) Word stores no line breaks for a wrapped label, so the converter breaks lines by a committed width table from Liberation Serif, metric-compatible with Times New Roman. (3) The SVG is inline in the page, so screen readers and find-in-page reach the labels; a photograph inside keeps the original's bytes (D-0092); the Word download gets a PNG rendered from the SVG by headless Chrome, already a build dependency. (4) PH 212 Lab 3's figure is one SVG of the paragraph's four anchored drawings (two screenshots, two arrows) at Word's offsets, the screenshots keeping their own alt text; PH 213 Lab 4's Text Box 2, one boxed sentence, converts as `::: box` (S14), not a figure.
- rationale: LibreOffice's shape export, the one route from the original that CI could run, keeps Word's positions exactly but none of the words: 0 of 5 labels in PH 213 Lab 2 ("Do not use" among them), 0 of 3 in Lab 4, and the ΔV_D equation; it also drops the label outlines and re-encodes the 944 KB JPEG as a PNG inside a 4.8 MB SVG. Writer's page SVG export fails on every document on this install; Draw's PDF import keeps text only from Word's own PDF, which CI cannot make, and sets the equation as loose glyphs. The owner, 2026-10-08, chose each lean: "Own converter, no LO in CI", "Font widths", "Inline SVG + Chrome PNG", "PH 212 Lab 3: one figure, PH 213 Lab 4: warning is a box".
- alternatives: LibreOffice's shapes with our text laid over them (the text code is needed anyway, a large install on every CI run, the photo re-encoded); HTML wrapping inside the SVG (`foreignObject`; labels not SVG text); the SVG as an `<img>` (screen readers get the alt text only); PH 212 Lab 3's arrows alone (they point at nothing); Text Box 2 as an SVG.
- binds: D-0101 (S13; its LibreOffice install and apt step); D-0092 (Q12, the photograph as is); docs/conversion-spec.md (S13); tools/figures.py; tools/check_unchanged.py; tools/downloads.py; .github/workflows/verify.yml
- test: pass 2b's fixtures: a figure's labels and equation are SVG text read by the word check; a shape the converter does not know fails; a wrapped label breaks where the width table says; the Word download holds the figure's PNG

### D-0118  Pass 2b's build calls: no implicit figures; anchored drawings read after their paragraph; Word's size and crop on every picture; font numbers beyond Liberation Serif; no new CSS revert
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-08
- decision: Seven calls made while building pass 2b, each from a measurement. (1) Every step reads a source as `markdown-smart-implicit_figures` (`render.FROM`, `_quarto.yml`'s `from`, both checks), and the lab page runs `tools/filters/media.lua` at Quarto's `pre-ast`: otherwise a lone picture becomes a figure whose caption repeats its alt text, words Word does not show, and Quarto ignores the reader setting and drops the `alt` attribute (probed 2026-10-08). (2) The word check reads a drawing Word anchors to a paragraph after that paragraph's words, and an inline one in place: all 23 anchored drawings in the 19 handouts sit at their paragraph's start, offset 0.29 to 1.55 in below its top, and where Word's PDF was read (PH 212 Lab 3, PH 213 Labs 2 and 4) they show below its words (PH 213 Lab 2's photograph, anchored in question 6); a placement this rule misses fails the check rather than passing. This amends pass 2a's "a text box's words are read where it is anchored". (3) A picture (S12) carries Word's extent as `width` and `height` in inches to four places and Word's `srcRect` as `crop`, and the check compares them with Word's: Word crops 14 of the 49 pictures and shows every screenshot smaller than its pixels (a 1596 px screenshot at 624 px). The bytes stay the original's; the page crops with a span, and the Word download writes the crop back. Front matter `images:` (`file`, `source_part`, `sha256`) is four-items call 4.3's. (4) D-0117 call 2 named Liberation Serif's widths; the converter also needs Calibri's, to place a word too wide for its box as Word does (PH 213 Lab 4's "T" starts at the left inset, not centred), and the line metrics of Cambria Math and Script MT Bold. Calibri's come from Carlito (OFL, metric-compatible: 736 of 737 widths equal); Cambria Math's and Script MT Bold's numbers (advance widths, ascent, descent, line gap; no glyphs) from Word's own font files, each with its file's SHA-256, in `tools/font-metrics.json`. (5) The CSS reverts four-items call 4.3 lists are not needed: measured against the HTML download at 375 and 1440 px, `img`, the crop span, the figure's `svg` and `math` take the same computed styles, since Bootstrap's one rule there was already reverted and no `<figure>` is made; a test fails if a lab page ever holds one. (6) The course download's Markdown carries each lab's media in the lab's folder in the zip, so a zipped `.md` opens with its pictures. (7) HTML caps are per lab; PH 211 Lab 1's remeasured at 168,938 bytes, cap 190,000.
- rationale: Each call keeps the outputs to what Word shows and the check strict. (1) and (5) are what the probe and the measurement found; (2) is the one placement that holds for all 23 anchored drawings; (3) because the file as is shows more, and larger, than Word does; (4) because the figure's labels would otherwise be placed by guess.
- alternatives: (1) `![alt](file)\` in every source to avoid the figure (a marker in content); (2) the drawing where its anchor sits (every picture before the words it follows on the page); (3) no size (screenshots at two to four times Word's), or a cropped copy made at build (a second file, the original's bytes not published); (4) stopping on those labels (PH 213 Lab 4's figure could not be made) or Liberation Sans for Calibri (not metric-compatible); (5) reverts written without a difference to undo.
- binds: D-0117; D-0101 (S12, S13); D-0092; four-items call 4.3; docs/conversion-spec.md (S12, S13, "Pictures and drawn figures"); tools/check_unchanged.py; tools/figures.py; tools/media.py; tools/filters/media.lua; tools/downloads.py; tools/render.py; _quarto.yml; site/download-all.js; tests/test_downloads.py (HTML_CAPS)
- test: tests/test_check_unchanged.py (FiguresAndFiles: figure read from its SVG, left out, before its paragraph, alt text; a picture's entry, bytes, size, crop and place); tests/test_figures.py; tests/test_downloads.py (MediaDownloads; HTML_CAPS); tests/test_quarto_config.py (one reader); tests/test_quarto_build.py (LabPages); site/download-all.test.mjs (media folder kept)
- corrected: 2026-10-08, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0118, leans agreed")

### D-0119  Pass 3 lands as seven PRs: the hardest two together, held for the owner's Word check, then one per PH 211 lab, hardest first; tool changes in their own PR
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-08
- decision: Seven calls for pass 3 (D-0082, D-0105), whose PR split no entry had ruled. (1) PH 212 Lab 3 and PH 213 Lab 2 share one PR, merged only after the owner checks both Word downloads in Word and Google Docs (D-0090). (2) PH 211 Labs 2 to 7 land one PR per lab, each merging on green `verify`; none waits on the owner's Word check, since D-0090 gives him the hardest two and one lab per later pass (4 and 5). (3) PH 211's order, hardest first: Lab 6 (a second list among report items, an override, S11), Lab 7 (the Week 2 restart), Lab 3 (pictures in table cells, a second list for parts, blank cells to fill), Lab 2 (29 equations), Lab 5 (11 pictures, D-0113's typed "√"), Lab 4. (4) A tool change a conversion needs lands as its own PR first, its fixtures made up, never in the content PR it unblocks (four-items call 4.1). (5) Each content PR's own entry records both hashes of each original it commits (D-0086). (6) PH 212's and PH 213's course names (D-0107) ride in the first PR, quoted from those two handouts' course lines. (7) Claude converts the hardest two in the main session; one Sonnet subagent converts each PH 211 lab in a worktree under `.superpowers/sdd/`, and the main session edits the shared files (`tests/question-ids.json`, `HTML_CAPS`, `site/courses.md`, this ledger), reviews each lab's parse-tree block counts against its original and screenshots its page and PDF (D-0090). Claude's calls, stated with a veto: ids `ph212-designing-experiments-handout` and `ph211-<title words>-handout` beside D-0092's `ph213-hypothesis-testing-handout`; question ids are descriptors from each question's own words.
- rationale: The hardest two wait on one check from one sitting; PH 211's do not need it, so holding them gains nothing. A lab merged when done is saved (charter floor 12), and `verify` runs in about 2 minutes (the last six runs, 2026-10-08). A check written in the diff it passes cannot be told from one shaped to pass. The owner, 2026-10-08: "Leans agreed".
- alternatives: PH 211 in one PR (all or nothing); all eight in one PR held for the owner's check; PH 211's PRs held until the owner checks the hardest two (a rule his check changes would then reach no merged lab); the hardest two as two PRs.
- binds: D-0082; D-0086; D-0090; D-0105; D-0107; site/courses.md; tests/question-ids.json; tests/test_downloads.py (HTML_CAPS); STATE.md
- test: none; each PR's own

### D-0120  Pass 3's first calls: Word's Heading 1 kept one level down under the title; math-font text left to the reader's math font; box alt text dropped; PH 213 Lab 2's photograph as is
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-08
- decision: Four calls met converting PH 212 Lab 3 and PH 213 Lab 2, which no rule covered. (1) A lab whose Word file uses Heading 1 (Week and Appendix headings: PH 212 Lab 3, PH 211 Labs 3 and 7) keeps Word's outline one level down under the title: Heading 1 is `##`, Heading 2 `###`, Heading 3 `####`, so a Part stays under its Week (WCAG 1.3.1); a lab without Heading 1 keeps Heading 2 as `##`, as PH 211 Lab 1 does. `themes/modern.css` gains `h4` (1rem, the heading colour; under h3's 1.1rem at every width), the course-line rule covers `h1 + h3`, and print keeps `h4` with what follows; measured against the HTML download at 375 and 1440 px, no computed style differs. (2) Characters an original types as text in its math font, not as an equation (PH 213 Lab 2's "∆𝑦" and "𝛥𝑉A": Mathematical Alphanumeric Symbols and U+2206), are left to the reader's math font, as Word sets them in Cambria Math; Open Sans has no such glyphs. `tests/test_fonts.py` reads converted text outside equations, whose characters are MathML, and exempts those. A screen reader announces such a character as written ("mathematical italic capital V"), in Word as on the page; changing it is a content change. A device with no math font at all would show boxes; not tested on a phone. (3) Alt text Word stores on a one-cell box (PH 213 Lab 2's three, PH 212 Lab 3's) repeats the box's own words; Pandoc shows it as a caption Word never shows, so it is dropped. The box's words are visible text (WCAG 1.1.1 covers non-text content), and the word check does not read table alt text. (4) D-0092 Q15, measured in the browser pane at 375 px on the pass 3 build: PH 213 Lab 2's page document is 1,320,834 bytes, its first visit 2,556,585 bytes (decoded: the page, every linked file and the four fonts); the photograph shows at 304 by 197 px from 2,637 px. It ships as is; a smaller derived copy is a later, separate decision. Claude's calls, stated with a veto: the built-lab tests read what the build makes (a `.restart` restarts the count, the plain-render comparison reads as the build reads with MathML, an inline drawn figure is compared by its words, the course download lists each lab's media by `media.published`), each on made-up markup first (D-0119, call 4).
- rationale: (1) Flattening Week and Part to one level would hide from heading navigation that each Part sits in a Week; the site tests one h1 per page, so the title keeps h1 and the outline moves down whole. h4 at 1em followed the body above 90rem (19 px, past h3), so it is 1rem. (2) and (3) change no word and drop no text alternative. (4) The owner, 2026-10-08: "Keep as is for now". The owner asked whether the first leans would silently drop WCAG requirements; (1) as first leaned (Heading 1 as `##`, flattened) would weaken 1.3.1, so it was revised. The owner, 2026-10-08: "Revised leans agreed".
- alternatives: (1) Heading 1 as `##` beside Parts (withdrawn: 1.3.1); every lab shifted, PH 211 Lab 1 included. (2) A marked span with a math font in CSS (markup added to content); self-hosting a math font. (3) The alt text kept as a visible caption. (4) A ~700 px derived copy now.
- binds: D-0092 (Q15); D-0101 (S14); D-0119; themes/modern.css; site/site.css (print); tests/test_fonts.py; tests/test_downloads.py; tests/test_quarto_site.py; tests/test_download_all.py; tools/media.py; curriculum/ph212/ph212-designing-experiments-handout.md
- test: test_fonts (math-font characters, text outside equations); PrintKeeps and the Word keep test read h4; Helpers (restart, figures)

### D-0121  PH 212 Lab 3's and PH 213 Lab 2's originals are committed stripped; both hashes of each recorded
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-08
- decision: Under D-0086 and D-0119 call 5, pass 3's first PR commits each original stripped by `tools/strip_identity.py`: `dc:creator` and `cp:lastModifiedBy` removed from `docProps/core.xml`, and from `docProps/app.xml` `Company` (empty in both), `Manager` (empty, PH 213 Lab 2 only) and `Template`; every other part byte for byte, so no `w:t` changes and Word's labels match by the content parts (D-0112). PH 212 Lab 3, `originals/PH212/Lab 3 - Designing Experiments - Handout.docx`: original SHA-256 `62d6708bf2b2cd6bea3f0170dab8ce92b09eb5a20ffd9f27fdb23486879fda6f` (the survey's), stripped `4713cbfe3ebb4e3cdb2fe2ef80534268122710295b65c9b56ae18a87418ac76f`, its `source_sha256`. PH 213 Lab 2, `originals/PH213/Lab 2 - Hypothesis Testing - Handout.docx`: original `36f41045875ea1bb0c1699a1ed50c7b18ae2d8e6397a0da37d05546aa069ab68` (the survey's), stripped `52bb40c81369f95310ee1de828b3f83d5f787e1c4c6b64dab4e05f43156130fc`. Each original was re-hashed from the owner's folder on 2026-10-08 and equals the survey's (D-0085). Neither has an external link; each `customXml` part is an empty bibliography and names no one.
- rationale: D-0086 (ruled): an entry records both hashes, so anyone holding the original can tie the two.
- alternatives: none; the entry records what D-0086 orders.
- binds: D-0086; D-0119; originals/PH212; originals/PH213; curriculum/ph212/ph212-designing-experiments-handout.md; curriculum/ph213/ph213-hypothesis-testing-handout.md
- test: CI's content check (hash, words, bold, equations, pictures, figures) and number check on both labs
- corrected: 2026-10-14, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0134 to D-0138, D-0121 and D-0124 to D-0129.")

### D-0122  The number check places anchors outside the question lists: x-anchors in order by label, report-item lists, and a `.numbered` list for an appendix entry; amends D-0112 call 3
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-08
- decision: `docs/word-labels.json` records three kinds of numbered paragraph no rule placed, so the number check failed on them (D-0112, call 3): PH 211 Lab 6's x1 to x4 ("1." to "4.", bold report items in a second list, S11), PH 211 Lab 3's x1 to x3 (question 13's parts "a." to "c.", from a second list), and PH 211 Lab 3's o14.0.1 and o14.0.2 (the appendix's contents, "1." and "2.", at the question list's third level with no part above them). One check-only PR with made-up fixtures, before PH 211 Lab 6 (D-0119, call 4): (1) an `xN` anchor is matched in document order with the rest; it records no level, so its label alone is compared, with a part's marker or a report-item list's; (2) the check reads the ordered list inside each `::: report-item` (S11) in place; (3) a list Word numbers from its question list outside any question is marked `::: {.numbered anchors="o14.0.1 o14.0.2"}`, which shows nothing on the page, and the check compares its markers with Word's labels at those anchors. An anchor still unplaced fails, as before.
- rationale: Word's labels are in document order, so order places the second lists without guessing; S11's mark already exists; the explicit marker states in the source what a bespoke rule would leave implied. The owner, 2026-10-08: "Leans agreed".
- alternatives: an `oN.0.K` anchor allowed anywhere after question N with no markup; the anchors re-read as `oN` (a second reading of Word's labels).
- binds: D-0102; D-0112 (call 3); D-0101 (S11); tools/check_numbers.py; tests/test_check_numbers.py; docs/conversion-spec.md (S11)
- test: the PR's fixtures: x-anchors as parts and as a report-item list pass, a wrong label fails; a `.numbered` list passes and fails on a wrong marker or a missing anchor

### D-0123  PH 211's calls: Symbol-font text read as Word draws it; dead internal links given their target's id; indentation alone is not a quote
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-08
- decision: Three calls met converting PH 211 Labs 2 to 7, which no rule covered. (1) A text run set in the Symbol font counts, in the word check, as the characters Word draws, as a SYMBOL field already does (survey section 6): PH 211 Lab 3 types "®" (0xAE) in the Symbol font three times in its appendix's steps, Word's own PDF prints "→" there (read 2026-10-08 on a scratchpad copy), Pandoc reads "→", and the converted text holds "→". `SYMBOL_FONT` gains 0xAE; a slot not listed still stops the check. A check-only PR with a made-up fixture lands first (D-0119, call 4). (2) An internal link whose Word bookmark does not exist (PH 211 Lab 4's `#_Linearization`; Lab 5's `#_Linearization` and `#_What_is_Uncertainty?`; dead in Word too) keeps its words and target, and the heading it names takes that id (`{#_Linearization}`), an attribute, not a word, so the link works as written (WCAG 2.4.4). (3) A paragraph Word only indents is a plain paragraph, not a block quote, though Pandoc reads one; a quoted example in quote marks (PH 211 Lab 3's "From my data ...") stays a block quote (WCAG 1.3.1).
- rationale: The page shows what students see in Word; the check reads it the same way and stays strict on any other slot. A dead link a reader can see is a defect the authors did not intend; giving the heading its id changes no word. Indentation is layout; a block quote says the text is quoted. The owner, 2026-10-08: "Leans agreed".
- alternatives: (1) "®" written as stored (passes as is; readers see ® where Word shows an arrow). (2) The links kept dead, or their words kept and the target dropped. (3) Every indented paragraph a block quote, as Pandoc reads it.
- binds: D-0102; D-0112; survey section 6; tools/check_unchanged.py (SYMBOL_FONT); tests/test_check_unchanged.py; docs/conversion-spec.md (Pass 3 additions); curriculum/ph211 (Labs 3, 4, 5)
- test: test_symbol_font_run_reads_as_words_display, test_unknown_symbol_font_character_stops

### D-0124  PH 211 Lab 6's original is committed stripped; both hashes recorded
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-08
- decision: Under D-0086 and D-0119 call 5, PH 211 Lab 6's PR commits `originals/PH211/Lab 6 - Describing an Experiment - Handout.docx` stripped by `tools/strip_identity.py`: `dc:creator` and `cp:lastModifiedBy` from `docProps/core.xml`, and `Template` with Company, Manager from `docProps/app.xml`; every other part byte for byte. Original SHA-256 `27d2c3ed2b33ce873960c5be409a756f7fd23882e60247a7b90afe35383b5229` (the survey's; re-hashed from the owner's folder 2026-10-08), stripped `cf18da95fc358c0c1006d8a9a42e2d027a27889363bc44a3fcdc8f5487754c19`, the `source_sha256` of `curriculum/ph211/ph211-describing-an-experiment-handout.md`.
- rationale: D-0086 (ruled): an entry records both hashes, so anyone holding the original can tie the two.
- alternatives: none; the entry records what D-0086 orders.
- binds: D-0086; D-0119; originals/PH211; curriculum/ph211/ph211-describing-an-experiment-handout.md
- test: CI's content check and number check on the lab
- corrected: 2026-10-14, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0134 to D-0138, D-0121 and D-0124 to D-0129.")

### D-0125  PH 211 Lab 7's original is committed stripped; both hashes recorded
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-08
- decision: Under D-0086 and D-0119 call 5, PH 211 Lab 7's PR commits `originals/PH211/Lab 7 - Capstone - Handout.docx` stripped by `tools/strip_identity.py`: `dc:creator` and `cp:lastModifiedBy` from `docProps/core.xml`, and `Template` with Company, Manager from `docProps/app.xml`; every other part byte for byte. Original SHA-256 `e9b900c8e35fccda8a9adb9495945f505fb8ecab3cd9a748e813095965bab466` (the survey's; re-hashed from the owner's folder 2026-10-08), stripped `b8f38b5a04e1a01304f7ec7b71e7e54c2e13e46af80f5fe91f58cf76c8722ea6`, the `source_sha256` of `curriculum/ph211/ph211-capstone-handout.md`.
- rationale: D-0086 (ruled): an entry records both hashes, so anyone holding the original can tie the two.
- alternatives: none; the entry records what D-0086 orders.
- binds: D-0086; D-0119; originals/PH211; curriculum/ph211/ph211-capstone-handout.md
- test: CI's content check and number check on the lab
- corrected: 2026-10-14, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0134 to D-0138, D-0121 and D-0124 to D-0129.")

### D-0126  PH 211 Lab 3's original is committed stripped; both hashes recorded
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-08
- decision: Under D-0086 and D-0119 call 5, PH 211 Lab 3's PR commits `originals/PH211/Lab 3 - Uncertainty - Handout.docx` stripped by `tools/strip_identity.py`: `dc:creator` and `cp:lastModifiedBy` from `docProps/core.xml`, and `Template` with Company, Manager from `docProps/app.xml`; every other part byte for byte. Original SHA-256 `421e2df388f532c4140f07c26815737393c4e6583ffb4e473a81c79d9ce1b960` (the survey's; re-hashed from the owner's folder 2026-10-08), stripped `bfc0d03a8df8b718c7fafa075ec9740a3bb0e3001465df7c27d2da983d0078c5`, the `source_sha256` of `curriculum/ph211/ph211-uncertainty-handout.md`.
- rationale: D-0086 (ruled): an entry records both hashes, so anyone holding the original can tie the two.
- alternatives: none; the entry records what D-0086 orders.
- binds: D-0086; D-0119; originals/PH211; curriculum/ph211/ph211-uncertainty-handout.md
- test: CI's content check and number check on the lab
- corrected: 2026-10-14, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0134 to D-0138, D-0121 and D-0124 to D-0129.")

### D-0127  PH 211 Lab 2's original is committed stripped; both hashes recorded
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-08
- decision: Under D-0086 and D-0119 call 5, PH 211 Lab 2's PR commits `originals/PH211/Lab 2 - Data Analysis - Handout.docx` stripped by `tools/strip_identity.py`: `dc:creator` and `cp:lastModifiedBy` from `docProps/core.xml`, and `Template` with Company, Manager from `docProps/app.xml`; every other part byte for byte. Original SHA-256 `112c2c0675829438c17b0a50c8a67615709b85f1c926cddca88ba96259a3a2ec` (the survey's; re-hashed from the owner's folder 2026-10-08), stripped `3891e5de553bd94a641881ef64671a73949e8e68445b6150614558fc0e99fd40`, the `source_sha256` of `curriculum/ph211/ph211-data-analysis-handout.md`. Its three external links (two OSU technology pages and one rb.gy short link) are kept as written; none names a person (survey section 7).
- rationale: D-0086 (ruled): an entry records both hashes, so anyone holding the original can tie the two.
- alternatives: none; the entry records what D-0086 orders.
- binds: D-0086; D-0119; originals/PH211; curriculum/ph211/ph211-data-analysis-handout.md
- test: CI's content check and number check on the lab
- corrected: 2026-10-14, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0134 to D-0138, D-0121 and D-0124 to D-0129.")

### D-0128  PH 211 Lab 5's original is committed stripped; both hashes recorded
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-08
- decision: Under D-0086 and D-0119 call 5, PH 211 Lab 5's PR commits `originals/PH211/Lab 5 - Designing an Experiment - Handout.docx` stripped by `tools/strip_identity.py`: `dc:creator` and `cp:lastModifiedBy` from `docProps/core.xml`, and `Template` with Company, Manager from `docProps/app.xml`; every other part byte for byte. Original SHA-256 `4330e4267d0cb2e4b80d28db091c3bbaae8792ae55ecc78b7a0960169ec273f0` (the survey's; re-hashed from the owner's folder 2026-10-08), stripped `35a53b8948816cfc710ae22690f260b76228423bf5984792d2ccab4789a98e76`, the `source_sha256` of `curriculum/ph211/ph211-designing-an-experiment-handout.md`.
- rationale: D-0086 (ruled): an entry records both hashes, so anyone holding the original can tie the two.
- alternatives: none; the entry records what D-0086 orders.
- binds: D-0086; D-0119; originals/PH211; curriculum/ph211/ph211-designing-an-experiment-handout.md
- test: CI's content check and number check on the lab
- corrected: 2026-10-14, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0134 to D-0138, D-0121 and D-0124 to D-0129.")

### D-0129  PH 211 Lab 4's original is committed stripped; both hashes recorded
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-08
- decision: Under D-0086 and D-0119 call 5, PH 211 Lab 4's PR commits `originals/PH211/Lab 4 - Hypothesis Testing - Handout.docx` stripped by `tools/strip_identity.py`: `dc:creator` and `cp:lastModifiedBy` from `docProps/core.xml`, and `Template` with Company, Manager from `docProps/app.xml`; every other part byte for byte. Original SHA-256 `54daee77e5e4e0ea8cbbadced928c4f312c3e09418af73eb56c3c54e47b505f1` (the survey's; re-hashed from the owner's folder 2026-10-08), stripped `ced38c004f3745e17a4850ab223519960a67b79659e95783b44d0f14d5b61d18`, the `source_sha256` of `curriculum/ph211/ph211-hypothesis-testing-handout.md`.
- rationale: D-0086 (ruled): an entry records both hashes, so anyone holding the original can tie the two.
- alternatives: none; the entry records what D-0086 orders.
- binds: D-0086; D-0119; originals/PH211; curriculum/ph211/ph211-hypothesis-testing-handout.md
- test: CI's content check and number check on the lab
- corrected: 2026-10-14, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0134 to D-0138, D-0121 and D-0124 to D-0129.")

### D-0130  A lab table draws a thin full grid in --quiet, on the page, the HTML and PDF downloads and in Word
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-08
- decision: A table an original draws as a grid (not a one-cell box, which stays `::: box`) had no rules on a lab page or in any download, since no stylesheet styled one; PH 211 Lab 7's lookup table was the first converted, and Labs 2 and 3 and passes 4 and 5 bring more. `themes/modern.css` gives `table` a collapsed border and a gap under it, and `th, td` a 1 px rule in `--quiet` (Rogue Wave, 8.9:1 on white; Moondust in the dark scheme), padding, left and top alignment, bold `th`; print draws the rules black. Two tokens, `--table-gap` and `--cell-pad`, hold the values once. On a lab page Quarto adds Bootstrap's `table` class, which out-specifies the theme; the quarto-only block in `site/site.css` points Bootstrap's margin, cell padding and rule width back at those tokens. Measured in the browser pane on PH 211 Lab 7's build at 375 and 1440 px against the HTML download: every computed style of the table, header cells, cells and rows equal; the page's table is 100% wide where the download's is 99%, Pandoc's width that Quarto drops from the markup. `tools/make_reference_docx.py` adds the same grid to Pandoc's default Table style (six single 0.5 pt rules in --quiet, 0D5257); the question and checkpoint boxes name their own borders, so they keep theirs. The test comparing a page's main with the HTML download now also sets aside Quarto's table and row attributes and its HTML5 void elements.
- rationale: Word's originals draw their tables as full grids, and a fill-in table's blanks need cell edges. `--rule` (#d6dbe0, 1.36:1 on white) is below WCAG 1.4.11's 3:1 for lines a reader needs; `--quiet` clears it. Quarto's `html-table-processing: none` does not stop the class on a Pandoc table (probed 2026-10-08), so the reverts are written against Bootstrap's own selectors, as the quarto-only block does for other elements. The owner, 2026-10-08: "Thin full grid".
- alternatives: rules under rows only (the site's course table); a board first; `--rule` as the grid colour (under 3:1).
- binds: themes/modern.css; site/site.css (quarto-only); tools/make_reference_docx.py; tools/reference.docx; tests/test_downloads.py; D-0057
- test: test_tables_draw_a_thin_grid (theme rule and Word's Table style); test_main_is_the_line_then_the_modern_pages on every lab with a table

### D-0131  The hardest two pass the owner's Word and Google Docs check; pass 3 is complete
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-09
- decision: The Word downloads of PH 212 Lab 3 and PH 213 Lab 2 (#37) pass the owner's check in Word and in Google Docs, as D-0090 and D-0119 call 1 require, and #37 is merged (squashed as `706dcdf`). With PH 211 Labs 2 to 7 merged earlier, pass 3 (D-0082, D-0105) is complete: eight handouts converted, nine labs on the site with PH 211 Lab 1.
- rationale: The owner, 2026-10-09: "Word and Google Docs look clean, merge #37".
- alternatives: none; the check was the gate.
- binds: D-0090; D-0119; STATE.md
- test: main's run for 706dcdf (verify and deploy green)

### D-0132  Pass 4 lands as six PRs: the redaction tool, then one per PH 212 lab, hardest first; Lab 6 held for the owner's Word check; an owner task list
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-09
- decision: Pass 4 (D-0082) converts PH 212 Labs 1, 2, 4, 5 and 6. (1) The redaction tool (D-0133) lands first as its own PR with made-up fixtures (D-0119 call 4); any further gap a conversion meets lands the same way. (2) One PR per lab, hardest first: Lab 6, Lab 1, Lab 2, Lab 5, Lab 4. Labs 1, 5 and 4 start while the tool is built; Labs 2 and 6 after it merges. Merges go one at a time with main's run read before the next. (3) The owner's one Word check this pass (D-0090) is Lab 6: a Week 2 restart through a level-0 override, third-level parts, six tables, four display equations, two links reduced to words. Its PR merges only after he checks its Word download in Word and Google Docs; the others merge on green `verify`. (4) The main session redacts Labs 2 and 6 before any subagent opens them; subagents receive only the redacted copies. (5) As D-0119 call 7: one Sonnet subagent per lab in a worktree under `.superpowers/sdd/`; the main session keeps `tests/question-ids.json`, `HTML_CAPS`, `site/courses.md` and this ledger, reviews block counts, and screenshots page and PDF. Ids `ph212-<title words>-handout`. Each lab's entry records both hashes (for Labs 2 and 6, the original's and the stripped and redacted file's). (6) Pictures Word leaves without alt text (PH 212 Labs 2 and 4, one icon each) ship with Word's empty alt text, noted as observed. (7) `docs/owner-tasks.md` lists what the owner must supply once conversion is done: each resource whose link was removed, and alt text for each picture shipped without it.
- rationale: The code and the OneDrive target must never enter the repo, so the tool gates both labs (D-0133); the three labs without them need not wait. Lab 6 carries the most structure only Word shows; Lab 1 has no restart and four tables. A subagent never sees the code if it only ever gets the redacted copy. Empty alt text marks an image decorative, which fails WCAG 1.1.1 if the icon carries meaning; inventing alt text is a content change, and the picture check compares alt text with Word's, so supplied alt text needs a tool change. The owner, 2026-10-09: "1. Yes. 2. Fine to lose the link, so long as I have a task list once everything is converted"; "3-6: yes. 7 fine for now but mark it in my task list (those images need alt text)."
- alternatives: Lab 1 as the Word-check lab; all five labs waiting on the tool; subagents redacting their own lab (the code in a subagent's transcript and report); alt text written now as a ruled addition.
- binds: D-0082; D-0090; D-0119; D-0133; docs/owner-tasks.md; tests/question-ids.json; tests/test_downloads.py (HTML_CAPS); site/courses.md; STATE.md
- test: none; each PR's own

### D-0133  PH 212 Labs 2 and 6 are committed redacted as well as stripped: the code and the two personal or code-bearing link targets never enter the repo; amends D-0086 and D-0104
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-09
- decision: A probe of scratchpad copies (hashes equal to the survey's), printing shapes only, found D-0104's premise short. Lab 2's activation code appears three times in `word/document.xml` (the box's text, and a link whose visible text is its own URL, whose query is the code) and once in `word/_rels/document.xml.rels`; Lab 6 carries the same link (the same target) behind four words of link text, besides the OneDrive target behind "your". D-0086's strip changes no text and does not reach link targets, and `ruled_omissions` quotes its passage in front matter, so either would put the code in the repo. The nine committed originals and the other ten PH 212 and PH 213 handouts hold neither (scanned 2026-10-09). Therefore: `tools/strip_identity.py` gains a redaction step, its targets named on the command line only and never committed, that replaces named text with the marker `[removed under D-0104]` and named external link targets with `https://removed.invalid/`; the committed original is stripped and redacted, and `source_sha256` names that file. Lab 2's code and its URL link text are omitted, declared in `ruled_omissions` by the marker; Lab 6's code link keeps its four words as plain text and loses its target, as "your" does. Lab 2's redacted `document.xml` has a new hash, so `docs/word-labels.json` gains an alias for the redacted parts, tested to carry the original's labels. Amends D-0086 (no `w:t` changes) and D-0104 (the code declared by its own text).
- rationale: D-0104's own rule is that neither the code nor the target is written in any file here; as built, the commit of the original would break it. Not committing the two originals would drop the word check for both labs; a hash in front matter still leaves the original carrying the code. The owner, 2026-10-09: "1. Yes. 2. Fine to lose the link", and the marker "[removed under D-0104]".
- alternatives: leave the two originals uncommitted; declare the omission by a hash of the passage; keep the vendor URL without its query (a content edit).
- binds: D-0086; D-0104; tools/strip_identity.py; tools/check_numbers.py; docs/word-labels.json; docs/owner-tasks.md; docs/handout-survey.md section 7
- test: the tool PR's fixtures; Labs 2 and 6's word and number checks; a scan of each committed original for the code and for personal-store targets

### D-0134  PH 212 Lab 5's original is committed stripped; both hashes recorded
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-09
- decision: Under D-0086 and D-0132 call 5, #54 commits `originals/PH212/Lab 5 - Sharing & Comparing - Handout.docx` stripped by `tools/strip_identity.py` (`dc:creator`, `cp:lastModifiedBy`; app.xml Company and Template). Original SHA-256 `1757716444fe6517ae53d8cfa0c9ab1fb86e506fb2b22ddbd4006b05c1fb33ea` (the survey's), stripped `2d9802178887e6ea3f89062cf750e105e725872ab35dfd790f2b025951862cd7`, the `source_sha256` of `curriculum/ph212/ph212-sharing-and-comparing-handout.md`.
- rationale: D-0086 (ruled): an entry records both hashes.
- alternatives: none; the entry records what D-0086 orders.
- binds: D-0086; D-0132; originals/PH212; curriculum/ph212/ph212-sharing-and-comparing-handout.md
- test: CI's content check and number check on the lab
- corrected: 2026-10-14, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0134 to D-0138, D-0121 and D-0124 to D-0129.")

### D-0135  PH 212 Lab 1's original is committed stripped; both hashes recorded; its question 4 is taller than a printed page
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-09
- decision: Under D-0086 and D-0132 call 5, #52 commits `originals/PH212/Lab 1 - Data Analysis - Handout.docx` stripped. Original SHA-256 `0329f26a1b76de0de520bf3bb3395fa938132dad5730d1a6d2829b792f173261` (the survey's), stripped `2d28c22db05827a39bcf703ac8643750423a800ec99d8af7bc59f93f14b5f032`, the `source_sha256` of `curriculum/ph212/ph212-data-analysis-handout.md`. Its question 4 holds the "What is Uncertainty?" box between stem and parts, inside the block as S14 rules, and prints longer than a page, so D-0058's keep cannot hold it whole; it is listed in `TALLER_THAN_A_PAGE` (#57), and `test_taller_than_a_page_is_true` fails if it ever fits.
- rationale: D-0086 (ruled). The box's place is Word's; moving it out of the question to keep the block whole would change the structure the spec rules.
- alternatives: the box outside question 4's block (against S14); no keep test for this question at all.
- binds: D-0058; D-0086; D-0132; tests/test_downloads.py (TALLER_THAN_A_PAGE); curriculum/ph212/ph212-data-analysis-handout.md
- test: PrintKeeps on the lab
- corrected: 2026-10-14, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0134 to D-0138, D-0121 and D-0124 to D-0129.")

### D-0136  PH 212 Lab 2's original is committed stripped and redacted; both hashes recorded; the removed link takes its sentence's period
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-09
- decision: Under D-0133, #56 commits `originals/PH212/Lab 2 - Extending a Model - Handout.docx` stripped and redacted (`document.xml` three passages, the link list one). Original SHA-256 `ae4d80de932b2bb5f0cc4fe3e306d4ac7301e8a49ebb37d54e37364de109e82d` (the survey's), stripped and redacted `11bfff3e11b12fc77bbe359c06d94e21e4f6a63aec9ea151cf67101dde738170`, the `source_sha256` of `curriculum/ph212/ph212-extending-a-model-handout.md`; `docs/word-labels.json` holds that file's record with `redacted_from`. Two markers are omitted in `ruled_omissions`. The removed link ended a sentence and the period is its own run after it, which the word check joins to the marker's last word, so the second declared passage is "[removed under D-0104]." and the sentence ("... go to") ends without its period, until the owner supplies the resource (`docs/owner-tasks.md`). A scan of the branch found the code in no file.
- rationale: D-0133 (ruled). Keeping the period alone would be a lone token the word check fails; teaching the check to split punctuation from a marker would be a tool change for one character in a sentence already broken by the ruled omission.
- alternatives: a check change splitting trailing punctuation from a declared passage.
- binds: D-0086; D-0104; D-0133; docs/word-labels.json; curriculum/ph212/ph212-extending-a-model-handout.md; docs/owner-tasks.md
- test: CI's content check and number check on the lab; test_a_redacted_record_carries_its_originals_labels
- corrected: 2026-10-14, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0134 to D-0138, D-0121 and D-0124 to D-0129.")

### D-0137  PH 212 Lab 4's original is committed stripped; both hashes recorded
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-09
- decision: Under D-0086 and D-0132 call 5, #53 commits `originals/PH212/Lab 4 - Hypothesis Testing - Handout.docx` stripped (`dc:creator`, `cp:lastModifiedBy`; app.xml Company and Template). Original SHA-256 `048b10bf3cab6a7f88e381658489df3ff5bf59b4230398cf27934b5df2d8da2c` (the survey's), stripped `8bdb32d3f8eb751bdd6f8d795bcce11247addb395a283e0c34447c1d7f9fc42a`, the `source_sha256` of `curriculum/ph212/ph212-hypothesis-testing-handout.md`.
- rationale: D-0086 (ruled): an entry records both hashes.
- alternatives: none; the entry records what D-0086 orders.
- binds: D-0086; D-0132; originals/PH212; curriculum/ph212/ph212-hypothesis-testing-handout.md
- test: CI's content check and number check on the lab
- corrected: 2026-10-14, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0134 to D-0138, D-0121 and D-0124 to D-0129.")

### D-0138  Pass 4's test and download fixes: a heading ends a page only as its own whole lines and in its own place; a question taller than a page is listed; an empty-alt picture stays decorative in the HTML download
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-09
- decision: Three faults pass 4's labs met in CI, each fixed in its own tool PR first with made-up fixtures (D-0119 call 4). (1) #57: the print-keep test read a contents item "4. Linearization" ending a page as that heading (PH 212 Lab 4); a heading must be the page's last whole lines. #58: a "Week 1" label paragraph read as the "Week 1" heading (PH 212 Lab 6); whole lines with a heading's words are matched in order to the page's blocks with them, and only a heading's counts. (2) #57: `TALLER_THAN_A_PAGE` lists question blocks longer than a printed page, each added by its lab's PR and proved by `test_taller_than_a_page_is_true` (D-0135). (3) #57: Pandoc's `--embed-resources` gives a picture with Word's empty alt text `role="img"` and an empty `aria-label`, an image with no name; the HTML download now keeps only `alt=""`, as the modern page writes it (WCAG 1.1.1; PH 212 Labs 2 and 4).
- rationale: Each failure was the test or the download, not the conversion, and was found by reading the printed pages (scratchpad, 2026-10-09). A test that reads a false heading would block every later lab with a contents list or a label matching a heading.
- alternatives: per-lab exemptions in the test; leaving `role="img"` in the download (an unnamed image to screen readers).
- binds: D-0058; D-0119; D-0132; tests/test_downloads.py; tools/downloads.py
- test: the fixtures in tests/test_downloads.py (PrintKeeps, DecorativePictures)
- corrected: 2026-10-14, status promoted from proposed to ruled and ruled-by added on the owner's explicit statement in chat ("Promote D-0134 to D-0138, D-0121 and D-0124 to D-0129.")

### D-0139  A table takes Word's column shares and the word check compares them; three PH 211 tables redrawn
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-09
- decision: The owner found PH 212 Lab 6's rubric drawn with its first column a letter per line in Word. Its Markdown dashes gave the columns 4/16/23/28/28 percent where Word's grid is 10/22/22/22/22: Pandoc's draft drew a table's dashes from its text, and no check read widths. #59 makes the word check compare each table of more than one column with Word's `w:gridCol` shares within 5 points, and fail a table at Pandoc's default widths. A pipe table serves where every cell is one paragraph (its separator's dashes set the shares once a line, the dashes included, passes 72 characters); a grid table where a cell holds paragraphs or pictures. The check failed three merged tables, redrawn in #59, format only: PH 211 Lab 7 (22/78 to 50/50), Lab 2 (16/8 to 11/9), Lab 3 (67/33 to 51/49, its grid edges widened in place).
- rationale: The owner, 2026-10-09: "1. Yes, check first." and, on the form, "Pipe table might be better" (checked: true for the rubric and PH 211 Lab 7; not for PH 211 Lab 3, whose cells hold paragraphs and pictures).
- alternatives: a build step reading Word's widths from the original (the Markdown would not say what the page draws); per-table fixes without a check.
- binds: tools/check_unchanged.py; docs/conversion-spec.md ("Pass 4 additions"); curriculum/ph211 (Labs 2, 3, 7)
- test: tests/test_check_unchanged.py::TableWidths; the word check on every lab

### D-0140  A table Word prints on a landscape page is a `::: landscape` block: a landscape section in Word, a landscape page in print
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-09
- decision: PH 212 Lab 6's rubric is 9.06 in wide because the original prints it in a landscape section; in a portrait page its first column still broke its words at Word's shares. #60: `tools/filters/landscape.lua` and `downloads.landscape_sections` give a `::: landscape` block its own landscape section in Word, copied from the document's own section (page, margins, draft header and footer); `@page landscape` and the theme's print rules give it a landscape page in the PDF; the web page is unchanged. The word check fails a table Word prints landscape outside the block, and a portrait one inside it. Only the two capstone rubrics are in landscape sections (all 19 handouts scanned). PH 212 Lab 6 (#55) wraps Word's whole landscape span, the "Remember, an experiment always:" box through the rubric.
- rationale: The owner, 2026-10-09: "Landscape page, tool PR first"; on the Word file, "keep the Word file as is. Earmark it" (D-0141), and of #60: "I'm merging PR 60 anyway because it does make it slightly more readable".
- alternatives: a wider first column in portrait, against Word's shares (an exception to D-0139); the rubric web-only, linked from Word (D-0141).
- binds: D-0139; tools/filters/landscape.lua; tools/downloads.py; site/site.css; themes/modern.css; tools/check_unchanged.py
- test: tests/test_downloads.py::LandscapePages; tests/test_check_unchanged.py::TableWidths

### D-0141  The capstone restructure, a web-only rubric and a page table of contents are one pass, after all other pending work
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-09
- decision: Earmarked, not built: (1) the capstone labs restructured toward the worksheet model, each downloadable template a stripped version of the lab's Markdown, with students pointed at the website for instructions; (2) a rubric shown on the web page only, the Word download carrying a sentence and a link to it in its place (a ruled addition when built); (3) a clickable table of contents on each lab page built from its headings, highlighting the section in view, with stable deep links a handout can point at. One design, specced and critiqued together, run as a pass after all other pending work. Until then the Word rubric stays as D-0140 leaves it.
- rationale: The owner, 2026-10-09: "Earmark the capstone restructure, web-only rubric, and table of contents as a pass after all other pending work"; "I suspect that I will be restructuring the Capstone Labs anyway".
- alternatives: each built now, piecemeal.
- binds: D-0074 to D-0080 (pass 6's template); D-0082 (passes); STATE.md
- test: none until specced

### D-0142  PH 212 Lab 6 passes the owner's Word and Google Docs check; its original is committed stripped and redacted; pass 4 is complete
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-10
- decision: The Word download of PH 212 Lab 6 (#55) passes the owner's check (D-0090, D-0132 call 3), with its rubric at Word's column shares (D-0139) on Word's landscape page (D-0140), and #55 is merged (squashed as `6a7fa5e`). It commits `originals/PH212/Lab 6 - Capstone - Handout.docx` stripped and redacted (D-0133; only the link list changed, two targets removed): original SHA-256 `68d4f8dfcda02ae7f10a005ce37ba2c5485259d0d17e30c7719256af9e0984ca` (the survey's), stripped and redacted `4820b23be0a293afd06790af560260f0290beb5c90b9d2ff67ba319de35597fb`, the `source_sha256` of `curriculum/ph212/ph212-capstone-handout.md`. With Labs 1, 2, 4 and 5 merged earlier, pass 4 (D-0082, D-0132) is complete: PH 212's six labs are on the site.
- rationale: The owner, 2026-10-09: "Word check passed, merge #55". D-0086: an entry records both hashes.
- alternatives: none; the check was the gate.
- binds: D-0086; D-0090; D-0132; D-0133; D-0139; D-0140; STATE.md
- test: main's run for 6a7fa5e (verify and deploy green); the word and number checks on the lab

### D-0143  Collapsible sections ("stretches") are built as a proof of the mechanism, in sandbox labs only
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-15
- decision: A `::: stretch` block keeps its first block (a heading or a paragraph) visible and puts the rest in a native `<details>` behind a "Show more" / "Show less" control that is obvious to click, at least 44 px tall, and needs no script. Existing sentences only. The build fails on the five rules of the design's section 6.4 (lead and tail; no heading after the lead; no question, checkpoint or hint inside; no link target after the lead; no stretch in a converted lab). Word, HTML and Markdown downloads are not changed by it; the PDF prints every section open. Its purpose is the mechanism (markup, filter, accessibility, the PDF), not whether shorter handouts get read. Readers are at the bench on lab computers and their own laptops; phones are not the intended medium. Design: `docs/superpowers/specs/2026-10-15-stretch-sandbox-design.md`.
- rationale: The owner, 2026-10-15, answering the critique of an outside recommendation to adopt stretchtext (after the `pro-vi/cc-stretch` plugin) for lab handouts: "At the bench on a screen."; "Existing sentences for now."; "`<details>` blocks for now."; "Testing the mechanism."; to the words "Show more" and "Show less": "Yes."; to the PDF printing from a copy with every section open: "yes"; "so long as it is obvious where to click to expand."; "Lab computers, student's personal devices. Phone is not the intended medium." Context (Claude): with existing sentences only, the survey (`docs/superpowers/specs/2026-10-15-stretch-survey.md`) finds 4 to 24% of a main path collapsible and 76 to 94% of an appendix, so the reading question waits for the wording-change phase (LEDGER 11).
- alternatives: stretches inside a sentence (script and focus handling; earmarked); newly written short versions (need LEDGER 11; earmarked); Quarto's collapsible callouts (script); the cc-stretch plugin itself (it runs only in Claude Code).
- binds: tools/filters/stretch.lua (new); tools/quarto_build.py; tools/downloads.py (pdf); the theme or site stylesheet; docs/conversion-spec.md; tests
- test: none until built (the design's section 10 names them)

### D-0144  Three sandbox courses on the production site; their labs are deliberate forks of converted labs
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-15
- decision: PH 211 Sandbox, PH 212 Sandbox and PH 213 Sandbox are courses on the existing site, listed on the course index in their own group, with pages at `/courses/ph211sandbox/` and so on. Each holds copies of converted labs under `sandbox/<slug>/`, made by `tools/sandbox.py`, whose front matter names the converted lab (`sandbox_of`) and the hash it was copied from, and carries no `source_file`. Their course data is `site/sandbox-courses.md`. Amends VISION principle 2 and CLAUDE.md's rule against copying content into a second file, for `sandbox/` only: nothing flows between a copy and its converted lab automatically, and a sandbox change reaches a course's handout only through the wording-change phase. The word check, the number check and the question-id pins skip sandbox labs; the em-dash check, the warning gate, the HTML caps, the stretch rules and the PDF test cover them.
- rationale: The owner, 2026-10-15: "It'll be added to the website under separate courses (more than one to prep for scaling): call them PH211H, 212H, 213H. [...] That'll give me a clean sandbox to make changes."; to the names PH 211 Sandbox, PH 212 Sandbox and PH 213 Sandbox: "That works." and "Sandbox."; "Listed within the site is fine, but to be clear I want it part of the existing osu-physics-labs.pages.dev site, not a separate site."; to the list of checks on and off: "Yes." Context (Claude): `site/courses.md` is quoted from the course summaries (ledger 45), so the sandbox gets its own data file; the names avoid PH 211H (D-0147).
- alternatives: an overlay of collapse maps on the converted sources (no content changes possible); a separate site (the owner: one site); unlisted courses (D-0148).
- binds: VISION.md principle 2; CLAUDE.md (Build); LEDGER 14 (ids); tools/render.py; tools/quarto_build.py; tools/media.py; tools/downloads.py; tools/check_em_dash.py; tools/sandbox.py (new); site/sandbox-courses.md (new); tests
- test: none until built

### D-0145  The sandbox labs: PH 211 Data Analysis, the PH 212 Capstone with its rubric collapsed, and PH 213 Hypothesis Testing
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-15
- decision: PH 211 Sandbox copies `ph211-data-analysis-handout` (5 stretches, about 482 words), PH 212 Sandbox copies `ph212-capstone-handout` (14 stretches, about 1,843 words, its grading rubric among them), and PH 213 Sandbox copies `ph213-hypothesis-testing-handout` (5 stretches, about 685 words), with the collapse maps of the design's section 7. Together they exercise every case the survey found except a drawn figure, which no lab can collapse. `ph211-capstone-handout` is earmarked as the later test of whether shorter pages get read.
- rationale: The owner asked for a survey of every handout with a recommendation (2026-10-15: "Spawn a subagent (Opus, medium) to review every lab handout and estimate how much can be collapsed in each one and provide a recommendation for the proof-of-concept.") and ruled on its picks and on collapsing the rubric: "Yes, and that's fine, so long as it is obvious where to click to expand." Context (Claude): the design adds a rule the survey did not have (no heading after a lead), so two of its ranges became stretches inside boxes.
- alternatives: PH 211 Lab 3, as first proposed (4% of its main path collapsible); `ph212-designing-experiments-handout` for PH 212 (no table, pictures or landscape); `ph211-capstone-handout` for PH 211 (its box case needs a less natural lead).
- binds: D-0143; D-0144; D-0141 (the earmarked capstone restructure and web-only rubric, which the sandbox copy can host)
- test: none until built
- corrected: 2026-10-15, D-0143, D-0144 and D-0145 promoted from proposed to ruled, ruled-by added, on the owner's explicit statement in chat ("Promote D-0143 to D-0145"); the sandbox line's words in the design's section 5.2 approved the same day ("wording approved").

### D-0149  Pass 5 lands as five lab PRs, hardest first, with no tool PR up front; Lab 6 held for the owner's Word check
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-17
- decision: Pass 5 (D-0082) converts PH 213 Labs 1, 3, 4, 5 and 6. (1) No tool PR up front. A read-only probe of the five originals (scratchpad copies, each equal to the survey's SHA-256) found every hazard the survey lists handled by existing tools: Lab 6's contents field is `TOC \o "1-2" \n \h` (11 entries, no page numbers), its "0)" and restarts take `.checkpoint` and `.restart` (D-0112), its landscape section `::: landscape` (D-0140); `tools/figures.py` draws Lab 4's figure (docPr 24) without stopping, and its text box 217 is a box; Lab 5's `symbol 87` and Lab 1's Symbol-font 0xAE are in `SYMBOL_FONT`; no picture lacks alt text. A gap a lab meets lands first as its own PR with made-up fixtures (D-0119 call 4). (2) One PR per lab, hardest first: Lab 6, Lab 4, Lab 5, Lab 3, Lab 1. All five subagents start at once; every PR goes through CI before any merges; merges go one at a time with main's run read before the next. (3) The owner's one Word check this pass (D-0090) is Lab 6; its PR merges only after he checks its Word download in Word and Google Docs, the others on green `verify`. Lab 4's "ℓ", an l in Script MT Bold, is only in the figure's four labels (and Word's VML fallback copies of them), so Word shows CI's PNG: Claude reads that PNG from the PR's CI artifact beside the page's SVG and brings any fallback-font finding back as its own call. (4) Lab 6's `::: landscape` block is Word's whole landscape section: the "Rubric" heading, its one-sentence introduction, the table and the empty paragraph after it. (5) Lab 6's Appendix C, five two-column sections in Word, is one column, as in PH 211 Lab 7 and PH 212 Labs 3 and 4; no tool reads Word's columns. (6) Lab 6's one external link, the words "google drive for presentations" to a Google Drive folder the handout says needs OSU sign-in, is kept as written: `strip_identity.py`'s personal-store pattern covers SharePoint and OneDrive only, and the target holds no code and names no person, so D-0104 does not reach it. (7) Lab 6's contents field becomes a list of 11 links to its own headings, words unchanged (S15, D-0101); it is not D-0141's earmarked page table of contents, and Appendix D's absence from it stays (survey section 11). As D-0132 call 5: one Sonnet subagent per lab in a worktree under `.superpowers/sdd/`; the main session keeps `tests/question-ids.json`, `HTML_CAPS`, `site/courses.md` and this ledger; ids `ph213-<title words>-handout`; each lab's entry records both hashes.
- rationale: The owner, 2026-10-17, to the seven calls with their leans: "All seven leans agreed. Record D-0149 and start the five subagents." Context (Claude): Lab 6 carries the most structure only Word shows (a "0)" checkpoint, two restarts, a landscape section, contents links, three weeks, five tables), while Lab 4's one Word-only risk sits in a PNG Claude can read; the lean on call 6 held "unless the folder sits on someone's personal Google account", and the owner did not say it does.
- alternatives: tool PRs built ahead of a need; subagents started in stages; Lab 4 as the Word-check lab; the rubric table alone in the landscape block; two columns in the Word download by a new filter; the Drive link's target dropped and the folder added to `docs/owner-tasks.md`.
- binds: D-0082; D-0090; D-0101; D-0104; D-0112; D-0119; D-0132; D-0140; D-0141; tests/question-ids.json; tests/test_downloads.py (HTML_CAPS); site/courses.md; STATE.md
- test: none; each PR's own

### D-0150  PH 213 Lab 4's figure ships as built: the Word download's PNG draws the script "l" in a fallback font
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-17
- decision: Under D-0149 call 3, Claude read the PNG that #65's CI run embeds in the Word download of `ph213-model-building-handout` (docPr 24, `tools/figures.py`). The length label, an "l" in Script MT Bold in the original, is drawn in a plain serif fallback, since CI's Linux runner has no Script MT Bold; the page's inline SVG shows the script glyph where the reader has the font and a generic cursive otherwise. The figure ships as built, recorded here as observed. The label's text stays "l", as Word stores it, in the SVG and the alt text.
- rationale: The owner, 2026-10-17: "Lab 4: ship the figure as is (A); record the plain l in the Word download as observed." Context (Claude): the arrows and Word's alt text ("Length marked as the distance between strips") carry the label's meaning; nothing changes for WCAG 1.1.1, since the text alternative and the label text are Word's.
- alternatives: a free script font installed in CI and added to the figure's font list after Script MT Bold (a CI dependency for one glyph, in a font not the original's, placed by Script MT Bold's metrics); the label drawn as U+2113 (a change to the stored character, a content change).
- binds: D-0117; D-0149; tools/figures.py; curriculum/ph213/ph213-model-building-handout.md
- test: none; an observation

### D-0151  PH 213 Lab 5's original is committed stripped; both hashes recorded
- status: proposed
- proposed-by: claude
- date: 2026-10-17
- decision: Under D-0086 and D-0149, #62 (squashed as `86b2444`) commits `originals/PH213/Lab 5 - Analysis and Testing - Handout.docx` stripped. Original SHA-256 `bdffcaa9b7b5716ae8fd87621465952ba9bf976ee80d126418b78ea8cc778138` (the survey's), stripped `bfb7ea415becb8a754a6d714a78b93c5ff1f63e52976a6c746dc519d043a511f`, the `source_sha256` of `curriculum/ph213/ph213-analysis-and-testing-handout.md`.
- rationale: D-0086 (ruled): an entry records both hashes.
- alternatives: none; the entry records what D-0086 orders.
- binds: D-0086; D-0149; originals/PH213; curriculum/ph213/ph213-analysis-and-testing-handout.md
- test: CI's content check and number check on the lab

### D-0152  PH 213 Lab 3's original is committed stripped; both hashes recorded
- status: proposed
- proposed-by: claude
- date: 2026-10-17
- decision: Under D-0086 and D-0149, #63 (squashed as `6c5ab5c`) commits `originals/PH213/Lab 3 - Data Taking - Handout.docx` stripped. Original SHA-256 `124a763be1fb64991954c769f6c99eba1c8b67d43fe63aa1e810799855934bf2` (the survey's), stripped `d1b09d299bcc9fc9fdbc48c06cb7949eb5b82dc9f230fd382adfd4f5588ac6d2`, the `source_sha256` of `curriculum/ph213/ph213-data-taking-handout.md`.
- rationale: D-0086 (ruled): an entry records both hashes.
- alternatives: none; the entry records what D-0086 orders.
- binds: D-0086; D-0149; originals/PH213; curriculum/ph213/ph213-data-taking-handout.md
- test: CI's content check and number check on the lab

### D-0153  PH 213 Lab 4's original is committed stripped; both hashes recorded
- status: proposed
- proposed-by: claude
- date: 2026-10-17
- decision: Under D-0086 and D-0149, #65 (squashed as `3b961b8`) commits `originals/PH213/Lab 4 - Model Building - Handout.docx` stripped. Original SHA-256 `09259a1b6297816d388b4743f64ac69b80e440afd83eaee9a2c726fb40d67f74` (the survey's), stripped `41751d161c90744186adef447ccf198b58cf2d4d5dfe52763126907ebc60a078`, the `source_sha256` of `curriculum/ph213/ph213-model-building-handout.md`.
- rationale: D-0086 (ruled): an entry records both hashes.
- alternatives: none; the entry records what D-0086 orders.
- binds: D-0086; D-0149; D-0150; originals/PH213; curriculum/ph213/ph213-model-building-handout.md
- test: CI's content check and number check on the lab

### D-0154  PH 213 Lab 1's original is committed stripped; both hashes recorded
- status: proposed
- proposed-by: claude
- date: 2026-10-17
- decision: Under D-0086 and D-0149, #64 (squashed as `294195f`) commits `originals/PH213/Lab 1 - Data Analysis- Handout.docx` stripped. Original SHA-256 `0ef396eb1ed513d3d60c0725b0df5e6044febd6097c5fc5fd9039293a4c8a3f5` (the survey's), stripped `d634444391c35b3afc8bfe7808e19a5b73f69261c1d139779a240dd6c4ec3356`, the `source_sha256` of `curriculum/ph213/ph213-data-analysis-handout.md`.
- rationale: D-0086 (ruled): an entry records both hashes.
- alternatives: none; the entry records what D-0086 orders.
- binds: D-0086; D-0149; originals/PH213; curriculum/ph213/ph213-data-analysis-handout.md
- test: CI's content check and number check on the lab

### D-0155  Pass 5's test fix: a checkpoint box is told apart from a question box, and a nested list item keeps its own words
- status: proposed
- proposed-by: claude
- date: 2026-10-17
- decision: PH 213 Lab 6 (#61), the first converted lab with a top-level checkpoint and a nested contents list, failed three tests in CI while its Word download and PDF were right. #66 (squashed as `c67c0ad`), a tests-only tool PR under D-0149 call 1: the two Word-box tests tell a checkpoint box from a question box by its label, count checkpoints against the source's `.checkpoint` blocks, and check a checkpoint's own palette (D-0115); `PrintKeeps.page_endings` reads each heading, paragraph and list item's own words (`OwnText`), so the contents item "Before Lab" ending page 1 is not taken for that heading. A made-up fixture fails on the old reader with CI's message and passes on the new.
- rationale: As D-0138: each failure was the test, not the conversion, found by reading the Word XML and the printed page (pdftotext of the lab's PDF, 2026-10-17).
- alternatives: per-lab exemptions in the tests.
- binds: D-0112; D-0115; D-0138; D-0149; tests/test_downloads.py
- test: tests/test_downloads.py::PrintKeeps::test_a_nested_contents_item_with_a_headings_words_is_not_a_heading; the Word-box tests on PH 213 Lab 6

### D-0156  The draft banner comes off every page and download: the department approves sharing; the license text stays open; the site stays unindexed
- status: ruled
- proposed-by: owner
- ruled-by: owner
- date: 2026-10-23
- decision: Amends LEDGER 8 and 37. The site may be shared: the "Draft: license pending, not for distribution." banner (`BANNER_MAIN`, `BANNER_DETAIL`) is removed from site pages, lab pages, the sim bar and every download (the Word page header from `tools/reference.docx`, the HTML download, the PDF, the course download), and the published sentences that say the license is unsettled are deleted, not reworded: the landing page's "What is deliberately missing" bullet beginning "The license is not settled.", the method page's sentence beginning "The license for this material is not settled", and the HTML download's footer line "Downloads carry the same draft notice as these pages." The license itself stays open: no LICENSE file, D-0007's logo exclusion and D-0023's copyright line still wait for it, and until then the pages carry default copyright. The site stays unindexed: every page keeps its `noindex` meta and `robots.txt` keeps `Disallow: /`, its comment's reason now this entry. D-0080's test ("every other download still has it") lapses with the notice. Built by a Sonnet subagent in a worktree, one PR, the owner reviewing every removed line in its body.
- rationale: The owner, 2026-10-23: "Ready to remove draft: license pending disclaimers from all pages and files. [...] URL is stable, the department approves, and I'm starting to share the site with others." To the three calls: "Sharing approved; license later", "Keep noindex for now", "Remove them; I review the diff". Context (Claude): LEDGER 8 held that nothing publishes until the license settles, and the banner's words claim it pending; the department's approval settles distribution, not the license text, so the entry keeps the two apart.
- alternatives: the license settled now (a LICENSE file with the logo excluded, D-0007, and the copyright line, D-0023); indexing allowed (the `noindex` meta, `robots.txt` and `tools/check_deployed.py` changed); replacement sentences drafted for approval.
- binds: LEDGER 8; LEDGER 37; LEDGER 44; D-0007; D-0022; D-0023; D-0030; D-0052; D-0057; D-0080; tools/render.py; tools/template.html; tools/template-site.html; tools/make_reference_docx.py; tools/reference.docx; tools/quarto_build.py; site/site.css; site/landing.md; site/how-this-site-works.md; tests
- test: the PR's tests: no page or download carries the banner; every page keeps `noindex`; `robots.txt` disallows all

### D-0157  A drawn figure sits on Word's white paper in both themes
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-10-23
- decision: #67 (squashed as `3d18d45`) adds `--figure-paper: #fff` to `themes/modern.css`, not overridden in dark mode, and gives `main svg.drawn-figure` that background. PH 213 Lab 4's figure (#65), Word's black lines and labels with no background of their own, read about 1.2:1 on the dark page (WCAG 1.4.3, 1.4.11); it now reads 21:1 in both themes. Measured in the branch's build, the lab page against its HTML download, at 375 and 1440 px: in dark mode white behind black labels on both, the box 326 by 252 on both, no sideways scroll; in light mode no visible change; PH 213 Lab 2's and PH 212 Lab 3's figures keep their sizes. Found in the post-merge review of pass 5 (D-0090), 2026-10-17.
- rationale: The owner, 2026-10-23: "Yes: tool PR giving svg.drawn-figure a white background, measured against the HTML download at 375 and 1440 px." Context (Claude): Word draws these figures on white paper, so white keeps Word's colours; a picture brings its own pixels and needs nothing.
- alternatives: recolouring the figure for dark mode (departs from Word's colours, and does nothing for a figure's pictures); leaving it (a live 1.4.3 and 1.4.11 failure for dark-mode readers).
- binds: D-0117; D-0150; themes/modern.css; tests/test_brand.py
- test: tests/test_brand.py::DrawnFigurePaper

### D-0158  Scope: the PH 21X problem-solving strategy PDF joins the in-scope originals
- status: proposed
- proposed-by: owner
- date: 2026-10-26
- decision: Amends D-0084's in-scope list (spec section 2) by one file: `A general phyiscs problem-solving strategy.pdf` at the root of the owner's `21X Lab Curriculum/` folder (the file name's spelling is the original's). It was not in the 2026-10-06 inventory. Claude read it in full on 2026-10-26: one page, the strategy and one example problem, no student data. Committed byte for byte as `originals/PH21X/A general phyiscs problem-solving strategy.pdf`, SHA-256 `ebb9842b2e0fa13b5af11b2b9f63781a7989eb0ad31e964eaebf63e8e90c59b5`. `pdfinfo` reads no metadata stream and no author field (Creator and Producer "PDFium"), so there is nothing for D-0086's strip, which reads Word files only. The page's own byline names its author (D-0159).
- rationale: The owner, 2026-10-26, asked for this file to be read, converted and placed in the library ("Read, convert to markdown, and tell me where it makes sense to add it"), then "Land it". D-0084 rules that nothing outside the in-scope list is opened, so the owner's request is the scope change, recorded here.
- alternatives: leaving the file outside the list and the library (the owner asked for it in).
- binds: D-0084; spec `docs/superpowers/specs/2026-10-06-handout-conversion-and-templates-design.md` section 2; D-0086
- test: none; the hash is checked by `tools/check_unchanged.py` on every run

### D-0159  The problem-solving strategy keeps its author's byline and names her in its front matter, ahead of D-0073's license conversation
- status: proposed
- proposed-by: owner
- date: 2026-10-26
- decision: `curriculum/ph21x/ph21x-problem-solving-strategy.md` keeps the original's byline under its title, "Dr. Rebecka Tumblin – General Physics with Calculus", and names her in its front matter as `credit: "Dr. Rebecka Tumblin"`. The key is `credit`, not `author`: Quarto reserves `author`, and an included file's front matter reaches the page's metadata (CLAUDE.md, Quarto traps). This narrows D-0076's hold on authors' names for one kind of document: an original that prints its author on its face, where the name is the original's own words and the conversion rule keeps it. Every other course material still waits for D-0073's conversation. The license for this document is not settled. LEDGER 8 and D-0073 still apply, and the author's own grant is the one that counts (D-0073's reading of OSU Policy 06-200).
- rationale: The owner, 2026-10-26: "Credit the author", then "byline kept". Claude's note: the byline is in the original, so the conversion keeps it whether or not credit is ruled; the `credit` key is the addition this entry rules. D-0076 declined names in the repo ahead of D-0073 for the AI-use file, whose words quote a statement without naming its authors; this file already names its author.
- alternatives: credit by title only, as D-0076 does (drops the name the original prints, and so changes the original's words under the conversion rule); waiting for D-0073 (holds a one-page document the owner wants published).
- binds: D-0073; D-0076; VISION.md principle 4; charter floor 9
- test: none; the byline is in the word check's sequence, so `tools/check_unchanged.py` fails if it is dropped

### D-0160  A PDF original is checked from its text layer; course-wide documents get their own heading on the course index
- status: proposed
- proposed-by: claude
- date: 2026-10-26
- decision: (1) Source and page. A converted document for all three PH 21X courses lives in `curriculum/ph21x/` with `course: PH21X`. It goes through the lab pipeline unchanged: page at `/labs/<id>/modern/`, the four downloads, an HTML cap (190,000 bytes; 164,146 measured) and an empty question-id pin in `tests/question-ids.json` (no questions, so no numbers moved). (2) Link. The course index lists each such document under "For every course", after the course tiles (`render.course_wide`, `render.COURSE_WIDE_HEADING`). No course page lists it: it is no course's lab and is not in `site/courses.md`. (3) The word check reads a PDF original with poppler's `pdftotext -enc UTF-8`. Only the word sequence and each equation's text are compared. A text layer keeps no bold, no equation structure and no pictures, and the check's ok line says so. A list's "1." markers and bullets are text in a PDF, so they are dropped; Word's numbering never reaches the sequence either. Word's math survives as Mathematical Alphanumeric Symbols, and each run of them is one inline equation (U+1D400 to U+1D7FF). The page number "1" at the page's top is a ruled omission under this entry. (4) The number check passes a PDF original only when its Markdown holds no question, checkpoint or numbered block, since there are no Word labels to compare. The 1 to 3 list is typed from the page. (5) CI installs poppler before the word check, not after it. (6) Three download tests assume a lab's question box: the Word body holds "Question", at least one box, and a print offset that splits a box. They skip course-wide documents (`COURSE_WIDE` in `tests/test_downloads.py`); every other download test runs on them. (7) The download tests read PDFs with `-enc UTF-8`, as the word check does. Without it, poppler's Windows build writes Latin-1, and 93 download tests errored on a local run, 2026-10-26.
- rationale: The owner, 2026-10-26: "Land it: curriculum/ph21x source, its own page linked from the course index". Claude's recommendation had been a `/guides/` address with no downloads. Building it showed that `render.converted_documents()` takes every converted file under `curriculum/`, so a separate guides pipeline would need an exclusion as well as a generator, a render rule and its own chrome. The lab pipeline gives the page and the four downloads with no new part; its one cost is that the address says `labs`. A real check against the page, not an exception: the word check now fails on a changed word ("breaks" to "brakes") and a changed equation ($v_o$ to $v_0$), tried on a copy 2026-10-26. Without `-enc UTF-8`, pdftotext writes Latin-1, which drops the math letters and turns the byline's en dash into a hyphen. That was found when the 2026-10-26 first read lost all five equations.
- alternatives: a `/guides/<id>/` page with its own generator and no downloads (more parts and no print copy); a recorded exception that skips the check for a PDF (a repo must not lie about its verification); the strategy under one course (it serves all three).
- binds: tools/check_unchanged.py; tools/check_numbers.py; tools/render.py; .github/workflows/verify.yml; tests/test_downloads.py (HTML_CAPS); tests/question-ids.json; D-0077; D-0102; D-0113
- test: tests/test_check_unchanged.py::PdfText; tests/test_quarto_site.py::Pages::test_course_index_links_course_wide_documents

### D-0161  PH 212 Lab 2's two short sentences are finished: the web app's address, and the code on the classroom wall
- status: proposed
- proposed-by: claude
- date: 2026-11-05
- decision: A content change. In PH 212 Lab 2, "If you want to use Graphical Analysis Pro on your own computer, go to" ends "<https://graphicalanalysis.app>.", and "The activation code for Pro is" ends "posted on the wall of the classroom." Both are declared in `ruled_additions`. The address is the host of the original's own activation link, without the path and query that carried the code (D-0133); the code itself stays out of the repo (D-0104). The wording of the second follows Lab 6's own "It may also be posted on the wall of the classroom." Closes the owner task for Lab 2's box.
- rationale: The owner, 2026-11-05: "Software activation code is not needed in the handout; it's posted on the wall in the room." then "Leans as agreed". Context (Claude): D-0136 left both sentences ending short; a student, or a screen reader, met a sentence that stops. Found while answering a Disability Access Services request for the PH 212 labs.
- alternatives: leave both sentences short (reads as broken); cut both sentences (drops the web app's address, which the student still needs off the lab computers).
- binds: D-0104; D-0133; D-0136; curriculum/ph212/ph212-extending-a-model-handout.md; docs/owner-tasks.md
- test: CI's content check on the lab (each declared passage must occur)

### D-0162  PH 212 Lab 6's "Open the Pro version of GA in a browser" links to the web app's address
- status: proposed
- proposed-by: claude
- date: 2026-11-05
- decision: A link change, no word changes. The four words lost their code-bearing target under D-0133; they now link to `https://graphicalanalysis.app`, the same address as D-0161. It opens the free version, which step 2 below it upgrades with the key from the instructor or the classroom wall. Closes that owner task.
- rationale: The owner, 2026-11-05: "Leans as agreed". Context (Claude): without a target, step 1 named an action with no way to take it.
- alternatives: leave the words unlinked.
- binds: D-0133; D-0161; curriculum/ph212/ph212-capstone-handout.md; docs/owner-tasks.md
- test: CI's content check on the lab (words unchanged)

### D-0163  The two Graphical Analysis button icons in PH 212 Labs 2 and 4 are decorative; their empty alt text stays
- status: proposed
- proposed-by: claude
- date: 2026-11-05
- decision: PH 212 Lab 2's Graph Tools icon (a small line graph) and Lab 4's Connection icon (a slanted probe in a rounded square) keep Word's empty alt text, now ruled decorative rather than missing. In each, the sentence around the icon already names the button ("the *Graph Tools* ... button", "the Connection icon"), so the picture adds only its look. WCAG 1.1.1 allows empty alt text on an image whose meaning the adjacent text carries. No tool change: the picture check keeps comparing alt text with Word's. Closes both owner tasks.
- rationale: The owner, 2026-11-05: "Leans as agreed", on Claude's lean. Context (Claude): drafts "line-graph icon" and "sensor-probe icon" were offered; either would be read next to the button's own name, and adding one needs the picture check taught to accept alt text that differs from Word's.
- alternatives: the drafted alt text (a check change for words that repeat the sentence's meaning).
- binds: D-0132; docs/owner-tasks.md
- test: none; a ruling on existing markup

### D-0164  PH 212 Lab 6's OneDrive link stays out; its Google Drive data file becomes a download from the library
- status: proposed
- proposed-by: claude
- date: 2026-11-05
- decision: Two parts. (1) The OneDrive target D-0104 removed from "your" (Model 1, task 3) is not lab material: read by host and path only on 2026-11-05, it is a document in a personal OneDrive under a hiring committee's folder. It stays out, and "your" stays plain text. The owner task, which assumed a lab document, closes. (2) "Download the GA data file from this google drive link" (an ONID login is required) gives way to the Graphical Analysis file itself, published with the lab: `GA Custom Fit Practice Data.gambl`, supplied by the owner in `New Reference Material/` on 2026-11-05. Read in full that day: a tar holding one `vstudm/data.udm`, Vernier's XML, the application header and two columns, X from 0 to 30.5 by 0.5 and Y a synthetic curve; no name, no student data. How a lab publishes a file that is not a picture, and how the Word, HTML and PDF downloads link to it, is a tool change with its own calls, not yet ruled.
- rationale: The owner, 2026-11-05: on the link, "I reviewed it and determined it's fine (or alternatively, and probably cleaner, the file--which is currently .gambl, can just become a .csv as another downloadable on the site)"; then "CSV does open but its wonky. If possible, I lean we just attach the .gambl file directly instead." Context (Claude): the owner's review covered the data file; the removed link was a different one, which Claude reported before the ruling.
- alternatives: a CSV (opens in Graphical Analysis, poorly, per the owner); keeping the Google Drive link (an ONID login, a link the library does not control).
- binds: D-0104; D-0133; curriculum/ph212/ph212-capstone-handout.md; docs/owner-tasks.md
- test: none yet; the tool change brings its own

### D-0165  A lab can publish its own file, named in `files:`; every output links it at the library's address
- status: proposed
- proposed-by: claude
- date: 2026-11-05
- decision: Three calls, for D-0164's Graphical Analysis file. (1) A lab names a file that is not a picture in front matter `files:` (`file` under `<id>-media/`, `sha256`), beside the source as its pictures are. `tools/media.py` copies it into the published media folder, `published()` lists it after the pictures and figures, so the page's `resources` and the course download carry it, and a file whose bytes differ from the recorded hash stops the build: the bytes are the ones read and ruled. (2) A link whose target is `<id>-media/<file>` points, in every output (the page, and the Word, HTML and PDF downloads), at `render.LIBRARY_URL` + `labs/<id>/<id>-media/<file>`, written by `tools/filters/media.lua`; the filter stops if the address is missing. The address lives in one constant, `https://osu-physics-labs.pages.dev/` today, so a move to another host changes one line; `_quarto.yml` was the lean's place, but nothing in Python reads that file, and Quarto's own `site-url` would also make a sitemap the noindex policy does not want. The Markdown download keeps the relative link, which works inside the course zip. (3) The wording change in PH 212 Lab 6 rides in its own content PR.
- rationale: The owner, 2026-11-05: "Leans agreed". Context (Claude): a relative link works on the site and in the course zip but breaks in a Word, HTML or PDF file saved on its own, and a student working from the Word file still needs the data; the PDF is Chrome's print of the page, so the page uses the same absolute address. The cost is one host-specific line against ledger 39's host-agnostic output, kept to that line.
- alternatives: a relative link everywhere (broken in saved downloads); a CSV (the owner: Graphical Analysis opens it poorly); embedding the file in the Word download (no such route in Pandoc).
- binds: D-0164; ledger 39; tools/media.py; tools/filters/media.lua; tools/downloads.py; tools/quarto_build.py; tools/render.py
- test: tests/test_downloads.py::MediaDownloads (published, changed file stops the build, Word, HTML and page links)

### D-0166  Screen-reader fixes from the NVDA test: skip link, named landmarks, PH 212 Labs 3 and 6 headings, a figure's name
- status: proposed
- proposed-by: claude
- date: 2026-11-05
- decision: From the NVDA 2026.3 test of the six PH 212 pages (`docs/accessibility/2026-11-05-nvda-ph212.md`, landed here). (1) Every site page opens with a "Skip to main content" link, shown only on keyboard focus, to `<main id="content">`; this amends D-0036's bare `<main>` by that one id (WCAG 2.4.1, 2.4.7). (2) The lab page's own navigation is named "This page", so no navigation landmark is unnamed. (3) The presentation note under a lab is a `div`, not a second `<footer>`, so a page has one footer landmark. (4) PH 212 Labs 3 and 6, whose Word files use Heading 1 for weeks (D-0120 call 1), skipped from h1 to h3: the headings before the first week and the appendix sections move up one level, so the appendices are siblings of the weeks and nothing skips (WCAG 1.3.1). Format only; the word and number checks pass. `tests/test_headings.py` holds every lab to no skips, with PH 211 Capstone, PH 211 Uncertainty and PH 213 Data Analysis listed as known, a list that only shrinks. (5) A drawn figure may carry a `label` attribute naming the whole; `tools/filters/media.lua` makes the inline SVG `role="group"` with that name, and in Word it leads the PNG's alt text. PH 212 Lab 3's figure gets one, drafted by Claude from the figure for the owner to edit: the two arrows point to the fit box's gear button and to the "Show Uncertainty of Fit Parameters" checkbox. The word check does not read the attribute. Not done here: the equations (bold read aloud, words spelled out, three malformed groupings) and the question labels as headings, each its own spec.
- rationale: The owner, 2026-11-05: "Leans as agreed except no input from a specific student. Use sensible best practices -- it shouldn't be based on one person's desires." Context (Claude): landmarks and headings already met 2.4.1, but 13 links precede the h1 and the skip link is the cheap fix for keyboard users; NVDA announced two content-info landmarks, an unnamed navigation, and an unnamed "graphic" for Lab 3's figure, whose arrows it never conveyed.
- alternatives: an empty anchor before `<main>` as the skip target (no change to D-0036's bare `<main>`, a target with no meaning); fixing the other three labs' skips here (each needs its own reading of the original's outline).
- binds: D-0036; D-0117; D-0120; tools/brandheader.html; tools/template.html; tools/template-site.html; tools/quarto_chrome.py; tools/filters/media.lua; site/site.css; curriculum/ph212/ph212-designing-experiments-handout.md; curriculum/ph212/ph212-capstone-handout.md
- test: tests/test_quarto_chrome.py::Landmarks; tests/test_headings.py; tests/test_downloads.py::MediaDownloads::test_figure_label_names_the_group; CI's content and number checks

### D-0167  PH 212 equations read correctly with a screen reader: Word's bold comes off, words in math are text, groupings are fixed; the word check takes declared equation changes
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-11-06
- decision: From the NVDA 2026.3 test (MathCAT 0.7.2, ClearSpeak) of the six PH 212 pages (`docs/accessibility/2026-11-05-nvda-ph212.md`, D-0166). The source's TeX may change only as follows, in `curriculum/ph212/*.md`. (1) Bold: every `\mathbf{...}` comes off. None marks a vector: each copies Word's bold run, either a whole equation (Labs 1, 2, 3 display; Labs 5, 6 inline and display) or an equation inside a bold question sentence (Labs 1, 2, 3). Pandoc writes it as Unicode math-bold letters, which MathCAT reads as "bold" before each one and, in a multi-letter run, as raw characters (Lab 6's `𝒄𝒐𝒔`, Lab 1's `𝟏𝟎`). An equation in a bold sentence then shows regular weight, as LaTeX sets `$x$` inside `\textbf`. (2) Words in math: a multi-letter word set as letters becomes `\text{...}` (Labs 1, 2 `total`; Lab 3 `slope`), which Pandoc writes as one `<mtext>`; `\mathrm{...}` is not used, since Pandoc writes it as one `<mi>` per letter and the letters are still spelled (measured 2026-11-06). A function name set as letters becomes its command (Lab 6 `\sin`, `\cos`), and `\cos` takes only its own argument, `\cos\left( Ct + D \right) + E`, as Word shows it. (3) Groupings: braces that only carried Word's bold runs go with the bold, so no `<mrow>` ends on an operator (Lab 5 `v = \sqrt{...}`, Lab 6 `1 - e^{...}` and `t - t_{0}`). Lab 3's two `\sum_{}^{}`, Word's n-ary with its limits hidden, become `\sum`: the empty limits are what MathCAT reads as "from empty to empty". Lab 6's inline `F_{D} = b_{1}v)` gives its `)` back to the sentence it closes. Labs 5 and 6's typed `*` as multiplication (`w*\sqrt{...}`, `x^{2} = x*x`) becomes `\times`, the sign Lab 6 already uses in its own drag equation; MathCAT reads `w*` as "w star". Nothing else changes: no symbol, letter, number or structure outside these, single-letter subscripts stay as Word set them, and plain-text superscripts ("R²") are not math. (4) The word check: (1) to (3) except the last three pass it as it stands (equation bold is exempt, D-0113; `\text`, `\sin`, `\cos` and the braces leave Word's text and counted structure as they were; measured on all six labs, 2026-11-06). The sums (n-ary 2 to 0, 1 to 0), the `)` (an equation's text and the words after it) and the `\times` (an equation's text) fail it. A new front-matter key, `ruled_equations`, declares each such equation as `original` (Word's text) and `converted` (the converted equation's text), both as the check prints them, with a `ledger` reference: at the first undeclared position where both match, the check skips that equation's text and structure compare; its kind and the equation count are still compared. A declaration that matches no position fails, and so does one whose equation would pass undeclared. The words go in `ruled_omissions` and `ruled_additions` as now. The declaration carries the check's text, never TeX, because front matter is read as Markdown (`_{D}` would start emphasis). (5) Delivery: the tool change is its own PR with made-up fixtures and the spec's Equation rule amended. Then one content PR per lab that changes (Lab 4's five equations need none), merged one at a time: Labs 1 and 2 need no declaration and do not wait for the tool PR; Labs 3, 5 and 6 do. Labs 2, 3 and 6 follow the open PRs that touch the same files (#70, #72, D-0166's). Each lab is re-checked by reading its built MathML for every changed equation: no `mathvariant="bold"`, no math-bold character (U+1D400 to U+1D7FF), no `<mrow>` ending in an `<mo>` other than a fence, no empty `<mrow>` as a script, and each word one `<mtext>`. NVDA is run again only on the owner's word. PH 211 and PH 213 follow under their own entries.
- rationale: The owner, 2026-11-05: "Use sensible best practices -- it shouldn't be based on one person's desires." The owner, 2026-11-06, to this entry and its three leans (an equation in a bold sentence shows regular weight; `\times` for `*`; Lab 3's `F^{T}` left out): "Rule as drafted". Context (Claude): bold in physics math means a vector, so Word's styling bold misleads a sighted reader too; multi-letter descriptive words are set upright as text (ISO 80000-2 practice); each grouping fix removes a construct that has no reading, and its rendering on the page is unchanged except the `*` and the n-ary.
- alternatives: keep bold visible on equations in bold sentences (`\boldsymbol` or CSS; the first is read "bold" again, the second does not reach Word); `\cdot` for `*` (also read "times" at MathCAT's defaults, but Lab 6 already writes `\times`); `\mathrm{total}` (still spelled); leave `*` and the stray `)` (the TeX would then still hold constructs a reader cannot parse); declare equations by position (shorter, but a reader cannot see what changed); loosen the comparison for `*` and n-ary (D-0113: the comparison is never loosened). Not done here: Lab 3's `F^{T}`, read "F transpose" (a rename, not a format change); the question labels as headings and the plain-text superscripts (their own specs).
- binds: D-0113; D-0133; D-0166; tools/check_unchanged.py; tests/test_check_unchanged.py; docs/conversion-spec.md; curriculum/ph212/ph212-data-analysis-handout.md; curriculum/ph212/ph212-extending-a-model-handout.md; curriculum/ph212/ph212-designing-experiments-handout.md; curriculum/ph212/ph212-sharing-and-comparing-handout.md; curriculum/ph212/ph212-capstone-handout.md
- test: tests/test_check_unchanged.py (a declared equation change passes; undeclared, stale and needless declarations fail); CI's content and number checks on each lab; each lab's built MathML read as in (5)

### D-0168  The library moves from conversion to ruled changes: a changed passage is declared in its handout and ruled here; the word check keeps running
- status: proposed
- proposed-by: owner
- date: 2026-11-06
- decision: Amends LEDGER 10 and settles LEDGER 11. Handout wording may now change. (1) A change is made only in the Markdown source, never in the original, and only after that handout's format-only conversion has landed: a change never folds into a conversion. (2) Each changed passage is declared in the source's front matter, the original's words under `ruled_omissions` and the words that replace them under `ruled_additions`, each citing the entry that rules it, and the file's `status` becomes `ruled-change`. This is the spec's existing mechanism ("Content-unchanged check"), used so far for D-0133's redaction markers; D-0167's `ruled_equations` is its counterpart for equations. (3) `tools/check_unchanged.py` and `tools/check_numbers.py` keep running on every converted file, unchanged; no comparison is loosened. An undeclared difference fails, and so does a declared passage that no longer occurs. (4) LEDGER 11's standard: each change's entry records who drafted the new wording (the owner or Claude) and who approved it. Drafted wording is not marked on the student's page. (5) Public wording. "How this site works": "How we know nothing changed" becomes "How we know what changed", with a paragraph on declared changes; "Who did the work" opens with the two open-source tools, Pandoc and Quarto, and names Claude in the middle of the paragraph as what the site's own software and the conversions were built with, and says nothing about drafting wording; the concerns table's Accuracy row names the listed changes; "Not settled yet" goes, since LEDGER 11 was its only item. The landing page's "What has not changed" becomes "What has changed", since its first sentence is false once a change lands. CLAUDE.md's "Conversion phase" line is amended to match.
- rationale: The owner, 2026-11-06: "it's been decided we are moving from conversion to changes for the website now. That's going to require updating the 'How This Site Works' page slightly." The owner, 2026-11-07, on a drafted sentence for the page, "Claude may draft the new words": "No, do not write this."; to (4) among the other leans: "leans as written"; and on "Who did the work": "instead of 'Hunter Reaves directs Claude' I want it rewritten such that an AI model name is not the fourth word; start by explaining the two open source tools. De-emphasize the use of AI by putting it in the middle, casually, totally normal and expected. No big deal, still disclosing." Context (Claude): declaring each passage keeps the comparison against the Word original, so the site can still say every difference from the original is listed and ruled. On (4), LEDGER 11's default read "drafted wording is marked as drafted". Marks on a student handout would be noise to the reader and need a render rule; the ledger is published with the repo and records the same fact.
- alternatives: re-baselining (the current Markdown becomes the new "original"; simpler declarations, but the check no longer compares against the Word file the site keeps for those who prefer it); retiring the check for changed handouts (a repo must not lie about its verification); marking drafted words on the page (LEDGER 11's literal default).
- binds: LEDGER 10; LEDGER 11; D-0072; D-0133; D-0167; docs/conversion-spec.md; site/how-this-site-works.md; site/landing.md; CLAUDE.md
- test: `tools/check_unchanged.py` on every converted file in CI's `verify`; tried 2026-11-06 on PH 211 Lab 6: an undeclared word change in a declared passage ("Position" to "Velocity") fails

### D-0169  PH 211 Lab 6: the whiteboard replaces the carpet; the Go Direct cart replaces the wired force sensor, connected in the browser
- status: proposed
- proposed-by: owner
- date: 2026-11-06
- decision: The first ruled change under D-0168, in `curriculum/ph211/ph211-describing-an-experiment-handout.md`: six declared omissions and seven additions. (1) "Carpet square" and "piece of carpet" become "whiteboard" in the goal, the introduction and its list, the equipment list and Part 2; "a" replaces "piece of" where the article is needed. (2) The introduction adds "Your instructor will tell your group which face of the block to put down." (3) Equipment. The block becomes "Wooden block (two wood faces, two felt faces)". Masses leave the all-stations list: ramp stations get none, since added mass slides off before the block slips. "Ramp" becomes "Adjustable ramp with the whiteboard clamped to it, and a protractor": the ramp has no angle scale. "Force sensor" becomes "Cart with a built-in force sensor, and masses". (4) Part 3's setup is seven steps. Step 1: open Graphical Analysis at graphicalanalysis.app in Chrome or Edge, choose Sensor Data Collection, click Wireless and select the cart, never through the computer's Bluetooth settings. Steps 2 to 6 are the owner's: open Sensor Setup, open Sensor Channels, select Force, deselect Position, click Done. Step 7: click Mode at the bottom left to open Data Collection Settings, change End Collection from a set duration to Manually, and click Done. Steps 1 and 7 take their labels from the web app, read on 2026-11-07 with no cart connected: the start screen's "Sensor Data Collection" (its banner says the web app does not detect sensors automatically); the Sensors dialog's "Wireless", with its warning "For wireless devices, do not use the system settings to pair"; and Data Collection Settings' "End Collection", set to "After 10 s duration" or "Manually", under "Mode: Time Based". Steps 2 to 6 need a connected cart and stand on the owner's word; he approved all seven as printed. The wired sensor's range step (10 N or 50 N) and its 50 N limit go. The zero step goes until the owner confirms where the web app zeros the cart. (5) Every other "force sensor" stays: the cart's sensor is a force sensor, so Experiment 2's name and the lines about preparing it remain true. (6) The appendix's Graphical Analysis tips stay. On 2026-11-07 the web app showed View Options top right and the graph tools bottom left, matching the two pictured icons, and Mode at the bottom left opened Data Collection Settings. Drafted by: the owner (the substitutions, steps 2 to 6, the address, and what (2) and (3) add); Claude (the joining words, the wording of (2) and (3) from the instructor repository's redline, and the wording of steps 1 and 7). Approved by: the owner, 2026-11-07, for (1) to (3) and the address ("leans as written"), and for the seven steps as printed in chat ("Approved.").
- rationale: The owner, 2026-11-06: "everywhere it says 'carpet' or 'carpet square,' it should say 'whiteboard'"; "Everywhere that refers to the force sensor and the LabQuest should instead refer to connecting the cart to graphical analysis using the browser (either Edge or Chrome) [...] not to connecting the cart to the computer's Bluetooth"; and the seven setup steps. The equipment change was ruled in the private instructor repository after the owner's bench run of 2026-11-06; its numbers stay there (they are expected values). The handout never named the LabQuest, so (4) covers that request. The owner, 2026-11-07, to twelve calls with leans (protractor, masses, faces, the ramp line, no mark on the page, the zero step once confirmed, among them): "leans as written. https://graphicalanalysis.app".
- alternatives: keeping the old range and zero steps (they name the wired sensor's 10 N and 50 N settings); step 7 as first worded, "change the stop condition from time-based to manual" (the dialog's Mode field also reads "Time Based" and must stay so, and the stop condition is labelled End Collection); a mark on the page saying the lab differs from its original (the list is in the source and here).
- binds: D-0168; curriculum/ph211/ph211-describing-an-experiment-handout.md
- test: `tools/check_unchanged.py` and `tools/check_numbers.py` on the file (2680 words identical outside the declared passages; Word's labels on 7 questions and 7 parts)

### D-0170  The site speaks to students: the landing page is its banner and three cards, and meta lines leave every page
- status: proposed
- proposed-by: owner
- date: 2026-11-07
- decision: The landing page still read as the first prototype. Since D-0168 its claims are also stale. Fifteen calls, each Claude's lean, ruled as written. (1) Landing: the banner keeps its title, lead and "Browse courses"; then one line, "Each handout downloads from its page as Word, PDF, HTML or Markdown."; then three cards, Course index ("Every lab for PH 211, 212 and 213."), Sims and How this site works, in one row from 48rem and stacked below it (the owner, 2026-11-07: "One row of three"; two across left the third alone). "Open Lab 1", the Lab 1 card, "One lab is converted so far", "How a lab page reads", "What has changed" and "What is deliberately missing" go. The layout sentence moves to "How this site works", reworded since a lab's words may now change. (2) The footer's "License and credits: see How this site works." goes: that page no longer speaks to the license, and the header links it. (3) "How this site works" loses its source footnote (`METHOD_FOOTNOTE`, a private repository's file name and ledger numbering), the "Common concerns" table and "If the people change". (4) Course pages: a tile counts the labs on the site ("7 labs"), not "8 labs listed, 7 converted". The intro line from `site/courses.md` and the closing note on where the list is quoted from go; `source_note` stays in the data as the record. The "Not yet converted" collapse goes, so PH 213 Lab 6 shows only once #61 lands. The download note is "One zip, a folder per lab." (5) Sims: "Which lab each sim belongs to is not recorded here yet." and the per-sim line that repeated the intro go. (6) A lab page's nav links its own course page, "PH 211 labs", not the chooser; a course-wide document still links the course index. (7) One name, "Physics Lab Library", on the landing page and lab pages, as the header already reads. (8) Found while building, not in the fifteen: the lab page's presentation note, "This page drops the Word page settings [...] The words are the original authors', unchanged [...]", sat on every lab page and in every HTML download. It became false for PH 211 Lab 6 under D-0169. It goes, with its template block and CSS, since the same sentence's substance is now on "How this site works". The `footnote` plumbing, the `.lab-pending` rules and `pending_labs` go with their last uses. No accessibility (WCAG) effect: text removed and one link's target changed.
- rationale: The owner, 2026-11-07: "It's current form is left over from the initial prototyping; it references Lab 1 but now it is much more. Just the 'Browse Courses' button and 'Course index', 'Sims' and 'How this site works' are needed there. [...] There are also a few lines (in footers and 'What is deliberately missing', for example) that don't need to be there on a student-facing website. Scan through and make recommendations for me to confirm or amend." To the fifteen: "Leans as written". Context (Claude): call (8) is outside the fifteen and is flagged in the PR body for the owner's veto. A false claim on a student page is a repo lying about its verification, and cutting it matches the other fourteen.
- alternatives: rewording the presentation note instead of cutting it ("any change is listed and ruled"; keeps a meta line on a student page); keeping the "Not yet converted" collapse as "Coming soon" (shows a lab marked "not implemented"); one name "OSU physics lab library" (the header's "Department of Physics" and logo already say OSU).
- binds: D-0038; D-0068; D-0069; D-0070; D-0071; D-0072; D-0088; D-0160; D-0166; D-0168; D-0169; site/landing.md; site/how-this-site-works.md; site/courses.md; tools/render.py; tools/quarto_build.py; tools/quarto_chrome.py; tools/downloads.py; tools/template.html; tools/template-site.html; tools/brandfooter.html; site/site.css; themes/modern.css; tests
- test: tests/test_quarto_chrome.py::ChromePieces::test_no_meta_notes_for_students and test_lab_nav_goes_to_its_course; LabRows::test_labs_not_on_the_site_not_shown; CoursePages::test_no_source_note_for_students and the tile counts; tests/test_quarto_dress.py::OldChrome::test_site_page_has_no_footnote

### D-0178  D-0167's equation changes leave a handout's `status` at `converted`, and "How this site works" does not list them
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-11-13
- decision: Applies D-0167 under D-0168. (1) A PH 212 lab whose equations change under D-0167 keeps `status: converted`, Labs 3, 5 and 6 included, though they declare `ruled_equations` (and Lab 6 its moved `)` under `ruled_omissions` and `ruled_additions`): the changes are equation format, not wording, and `ruled-change` stays for wording changes (D-0169's is the one so far). This matches the record: PH 212 Lab 2 (D-0133, D-0161), PH 212 Lab 6 (D-0164) and the PH 21X strategy (D-0160) declare differences and stay `converted`. Nothing in the repo reads `status`. (2) "How this site works" is not changed. Its "Each changed passage is listed in the handout's own file" speaks of words; bold inside an equation has never been compared (D-0113), and D-0167 itself records the bold coming off.
- rationale: The owner, 2026-11-13: "Leans; build", to these two leans from the plan's third executing critique (`docs/superpowers/plans/2026-11-06-ph212-math-critique/pass-3/report.md`). Context (Claude): the plan had said a file that declares a difference takes `ruled-change`; the critique found that false to the record.
- alternatives: Labs 3, 5 and 6 as `ruled-change` (calls a format fix a wording change, and Labs 2 and 6 already declare without it); a public sentence on the page about equation format fixes (new public wording to draft and approve).
- binds: D-0113; D-0167; D-0168; D-0169; curriculum/ph212/ph212-designing-experiments-handout.md; curriculum/ph212/ph212-sharing-and-comparing-handout.md; curriculum/ph212/ph212-capstone-handout.md; site/how-this-site-works.md
- test: none; a convention, and nothing reads `status`

### D-0184  PH 212 Lab 1's split proportionality becomes one sentence: "T is proportional to √L"
- status: ruled
- proposed-by: claude
- ruled-by: owner
- date: 2026-11-16
- decision: From the NVDA rerun (`docs/accessibility/2026-11-13-nvda-ph212-equations.md`, #85, section 3 item 4), which read `T is proportional to`, then the prose `(is proportional to)`, then `the square root of L`. Line 245 of `curriculum/ph212/ph212-data-analysis-handout.md` set `$T\  \propto$ (is proportional to) $\sqrt{L}$`, splitting the equation around a parenthesis as Word does. A wording change under D-0168: the sentence becomes "we are predicting that $T$ is proportional to $\sqrt{L}$." The symbol and the parentheses go, and the original's own words carry the meaning; ∝ is still introduced eleven lines later ("where ∝ means “is proportional to”"). Declared: `ruled_omissions` "(is proportional to)", `ruled_additions` "is proportional to", and `ruled_equations` original "T ∝", converted "T", each citing D-0184; the equation count is unchanged (17). `status` becomes `ruled-change` under D-0168 (2), since words are declared (D-0178 kept `converted` for equation-only changes). Drafted by: Claude. Approved by: the owner, 2026-11-16.
- rationale: The owner, 2026-11-13: "Can we go ahead and fix these too?" The owner, 2026-11-16, to this entry as drafted with its lean (a): "D-0184 lean approved."
- alternatives: one equation, `$T \propto \sqrt{L}$` with the gloss after it (17 equations become 16, which `ruled_equations` cannot declare since the count is always compared; a tool change under its own ruling, and D-0113 never loosens the comparison); "$T \propto \sqrt{L}$, where $\propto$ means “is proportional to”" (keeps the count but needs two equation declarations, and repeats line 256's definition); leaving it.
- binds: D-0113; D-0167; D-0168; D-0178; curriculum/ph212/ph212-data-analysis-handout.md
- test: `tools/check_unchanged.py` and `tools/check_numbers.py` on the file; the built MathML of the sentence; NVDA only on the owner's word
