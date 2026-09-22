# Open Sans font files

Subset of Open Sans from `github.com/googlefonts/opensans` at commit
`bd7e37632246368c60fdcbd374dbf9bad11969b6`, subset to WOFF2 with fontTools.

## License

Open Sans is licensed under the SIL Open Font License 1.1. The full text
is in `OFL.txt`, which must travel with these font files. The fonts are
excluded from any other license this repository adopts (DECISIONS D-0007).

## Subset

Latin (Basic Latin and Latin-1, OE ligatures, spacing modifiers, General
Punctuation, euro, trade marks, arrows, true minus) and Greek (the Greek
and Coptic block, for symbols in physics text). See `tools/subset_fonts.py`
for the exact Unicode ranges (DECISIONS D-0025, D-0027).

## Files

| File | Size | Style |
|---|---|---|
| `OpenSans-Regular.woff2` | 25396 bytes | Regular (400) |
| `OpenSans-Bold.woff2` | 25008 bytes | Bold (700) |
| `OpenSans-Italic.woff2` | 26420 bytes | Italic (400) |
| `OpenSans-BoldItalic.woff2` | 25532 bytes | Bold Italic (700) |

## Tools

- fontTools 4.65.0
- brotli 1.2.0

## Rulings

D-0006: self-host the font as static files.
D-0025: subset to Latin and Greek.
D-0027: two weights only, 400 and 700.
