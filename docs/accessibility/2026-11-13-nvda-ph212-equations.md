# NVDA rerun: PH 212 equations after D-0167

Run 2026-11-13, 16:07 to 16:27, Windows 11 10.0.26200, by a Claude
session driving NVDA with scripted key presses, on the owner's word. It
re-reads the five labs whose equations changed under D-0167 (#78, #79, #81,
#82, #83; main at `c70151f`), on the live site. Lab 4 changed nothing and was
not read. Findings are quoted from NVDA's IO log, which records the speech
NVDA queued, not audio. Nothing was audible. Capital letters are written
here as the page sets them; NVDA marks a capital by pitch, which the log
keeps apart from the words. The 2026-11-05 column quotes that run's report
with its notation simplified. One notification from another window, logged
during Lab 2, is left out.

## 1. Setup

What matches the 2026-11-05 run (`2026-11-05-nvda-ph212.md`, section 1):
- NVDA 2026.3 AMD64, a portable copy. The launcher is 69,352,040 bytes,
  with a valid signature from NV Access Limited.
- Flags: `-m --disable-addons --no-sr-flag --log-level=12`, with its own
  `--log-file` and `--config-path`.
- MathCAT 0.7.2, built into NVDA, at its defaults: ClearSpeak, Medium
  verbosity.
- eSpeak NG 1.52.0 at volume 0, with sounds at 0. Welcome dialog, update
  check, usage statistics and automatic say-all are all off.
- Edge with a throwaway profile, `--inprivate --disable-sync --no-first-run
  --no-default-browser-check --force-renderer-accessibility`.

What differs:
- **Reading.** Each page was read top to bottom in browse mode: Ctrl+Home,
  then Down arrow about every 0.45 s, until NVDA repeated its last line.
  Before each key the driver checked that the test window was in front.
- **Fallback voices.** OneCore's and SAPI5's volumes were also set to 0, so
  a voice fallback would stay silent.

Keys per lab:

| Lab | Keys |
|---|---|
| Lab 1 | 701 |
| Lab 2 | 311 |
| Lab 3 | 531 |
| Lab 5 | 341 |
| Lab 6 | 531 |

## 2. What 2026-11-05 heard, and what NVDA says now

| Lab | 2026-11-05 | 2026-11-13 |
|---|---|---|
| 1 | `delta bold T sub bold t bold o bold t bold a bold l end sub is equal to the square root of open paren delta bold T sub bold 1 close paren to the bold 2 power ...` | `delta T sub total end sub is equal to the square root of open paren delta T sub 1 close paren squared plus open paren delta T sub 2 close paren squared plus ...` |
| 1 | `bold 5 degrees`; raw `𝟏𝟎 degrees` | `5 degrees`; `10 degrees` |
| 2 | `bold t bold o bold t bold a bold l` | `delta T sub total end sub is equal to the square root of open paren delta T sub m close paren squared plus open paren delta T sub s close paren squared` |
| 3 | `delta sub bold s bold l bold o bold p bold e end sub` | `the fraction with numerator delta sub slope end sub and denominator slope is approximately equal to the fraction with numerator delta sub I and denominator I` |
| 3 | `the sum from empty to empty of tau sub i` | `I alpha is equal to the sum of tau sub i is equal to the sum of F sub i d sub i sine of theta sub i` |
| 5 | `bold v is equal to times the square root of bold T sub bold S divided by bold mu` | `v is equal to the square root of T sub S divided by mu` |
| 5, 6 | `w star times` | `delta w is equal to w times the square root of ...`; `x squared is equal to x times x` |
| 6 | `bold g bold s bold i bold n bold theta`; `bold 1 minus times`; raw `𝒄𝒐𝒔` | `v of t is equal to open paren g sine theta minus the fraction with numerator b sub 0 and denominator m close paren times open paren t minus t sub 0 close paren`; `... times open paren 1 minus e raised to the fraction with numerator b sub 1 and denominator m times open paren t minus t sub 0 close paren power close paren` |

Across all five labs:
- "bold" is spoken 0 times.
- "star" 0 times.
- "empty" 0 times.
- No raw math-bold characters.
- No "Error in speaking math."

D-0167's targets read as intended.

## 3. Still read badly

1. **Lab 6, the damped oscillator.** It reads `x of t is equal to A e raised
   to the negative B t power cosine of times open paren C t plus D close
   paren plus E`.
   - The cause: Pandoc writes `\cos` as its own group (`<mi>cos</mi>` and
     U+2061). Before a parenthesized group, MathCAT reads that as "cosine of
     times".
   - Before a single letter it reads well (`g sine theta`, `sine of theta
     sub i`).
   - D-0167's check of the built MathML let U+2061 end a group, so it did
     not catch this. The equation was raw math-bold on 2026-11-05, so this
     is the first time its speech can be heard.
2. **Lab 3, `F^{T}`.** `I alpha is equal to F transpose r` and `m a is
   equal to m g minus F transpose`. D-0167 left this as it was: a rename,
   not a format change.
3. **Labs 5 and 6, the uncertainty rule.** It reads `alpha of open paren
   delta x over x close paren squared`: MathCAT takes `alpha( )` as a
   function applied to the bracket. The source sets
   `{\alpha\left( \frac{\Delta x}{x} \right)}^{2}`, as Word does, and
   D-0167 did not touch this equation.
4. **Lab 1.** `T is proportional to`, then the prose `(is proportional
   to)`, then `the square root of L`. The original splits this equation
   around a parenthesis in the text; D-0167 left it.

## 4. Not tested

- Labs 1 to 6's other findings from 2026-11-05 (headings, question labels,
  links, figure), except as they pass by in reading.
- Lab 4; the course page.
- Braille.
- Other screen readers and browsers.
- MathCAT navigation (NVDA+Alt+M).
- The Word, PDF and Markdown downloads.

## 5. Files

The IO log and the per-key extracts stayed in the run session's
scratchpad, outside the repo; this report quotes them.
