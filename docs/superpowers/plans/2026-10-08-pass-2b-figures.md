# Pass 2b: LibreOffice measured against Word for the drawn figures (S13)

Status: measured 2026-10-08, brought to the owner before any converter is
written (D-0101). Calls below are proposed, not ruled.

## What was measured

LibreOffice 26.2.5.2 (winget, pinned; the same version exists as a Linux deb
in the Document Foundation's archive). Scratchpad copies of the three
originals, hashes equal to the survey's:

- PH 212 Lab 3 (`62d6708b...`): two straight arrow connectors, no text.
- PH 213 Lab 2 (`36f41045...`): group "Group 1", Word's `descr` "Photograph
  of the front panel of the power supply, labeling the relevant dials and
  displays": the photograph, 5 text boxes, 3 connectors, 1 equation (in the
  label "Deflecting voltage control ΔV_D").
- PH 213 Lab 4 (`09259a1b...`): "Text Box 2", a lone rectangle holding one
  sentence, and group "Group 23" (5 rectangles, 4 of them picture-filled,
  2 parallelograms, 1 cube, 2 double-headed connectors, text boxes "ℓ", "w",
  "T").

Word's own PDF of each (the reference's print recipe, Word automation on
copies, only the script's own WINWORD ids stopped), pages rendered with
poppler's `pdftoppm` at 110 dpi: PH 212 Lab 3 page 9, PH 213 Lab 2 page 5,
PH 213 Lab 4 pages 1 and 2.

## Result: not faithful

Three LibreOffice routes:

1. **Shape export** (`GraphicExportFilter`, one SVG per drawing, from the
   original; the only route that could run in CI). Positions are Word's
   exactly: Group 1 at 2.693 cm by 2.716 cm in both. But every text box's
   words are lost: 0 `<text>` elements in all three SVGs, so 0 of 5 labels
   in Lab 2 (the "Do not use" label among them), 0 of 3 in Lab 4, and Text
   Box 2's sentence. LibreOffice keeps a text box's words in a linked text
   frame outside the shape. The label boxes' outlines are lost too. The
   equation is lost with its label. The 944 KB JPEG comes back re-encoded as
   a PNG inside a 4.8 MB SVG.
2. **Writer's page SVG export** (`writer_svg_Export`): fails with an I/O
   error on every document on this install, a one-line Pandoc docx included.
3. **Draw's PDF import, then SVG**: keeps text, but only from Word's own
   PDF, so it needs Word, which CI does not have. It sets ΔV_D as loose
   mathematical italic glyphs, not an equation. It carries Word's
   downsampled photograph, and the figure must be cropped from a page.

## Also found

- PH 212 Lab 3's arrows are not a figure on their own. The paragraph anchors
  four drawings at offsets from the column and the paragraph: two
  screenshots ("Picture 1", "Picture 2", wrap top and bottom) and the two
  red arrows over them. Read alone, the arrows point at nothing.
- PH 213 Lab 4's Text Box 2 is a boxed warning sentence, the shape the
  conversion spec calls a box (S14), not a drawing.

## Ruled 2026-10-08 (D-0117)

All four leans: a converter of our own (`tools/figures.py`), no LibreOffice
in CI; label lines broken by a Liberation Serif width table; inline SVG on
the page and a PNG by headless Chrome for Word; PH 212 Lab 3 as one figure
of four drawings, PH 213 Lab 4's Text Box 2 as a box.

## Built (pass 2b PR)

`tools/figures.py` draws the three figures from the originals (scratchpad
copies; no handout converted). Against Word's PDFs, turned to vectors with
poppler's `pdftocairo -svg`: every label's baseline within 0.11 pt and every
start within 0.06 pt on PH 213 Labs 2 and 4; box widths equal (104.65 pt
in Word, 104.66 computed); arrowheads 6 by 6 pt as Word's. Its rules and the
calls made while building it (reading, anchored drawings, Word's size and
crop, font numbers) are D-0118.

Seen, not changed, for the owner's eye at conversion (D-0090): a label in a
face the reader's machine lacks falls back. PH 213 Lab 4's "ℓ" is the
letter l in Script MT Bold, which Linux, and so CI's PNG for Word, does not
have.
