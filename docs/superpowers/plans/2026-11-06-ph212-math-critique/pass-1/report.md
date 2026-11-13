# Executing critique, pass 1 (2026-11-06)

Read: 561302e. Base: 561302e (origin/main 657fa4a plus D-0167 and the
plan). Windows 11 Enterprise 10.0.26200; Python 3.12.10; Pandoc 3.10
(Quarto's). Tasks executed: 6 of 6, verbatim at 561302e in a throwaway
tree; no F commits (the placement gaps below were bridged without one).
Opus, high effort; 212,215 tokens, 78 tool uses, 1,376 s. The patches
`0001` to `0006` in this folder are `T<n> as written`; the tripwire printed
nothing.

Confirmed: the six labs' word-check counts and the number check at base;
39 tests before and 48 after; the test helpers' signatures; the anchors in
`tools/check_unchanged.py`; every replacement's count; the undeclared
problem lists of T4, T5 and T6, word for word; the MathML reader's results
for T2 to T6; no `\mathbf` left; the `quarto-site` artifact and page path;
Lab 6's word declaration in the right sentence; front-matter strings with
`*`, `×`, `∑`, `)` and Greek read back verbatim. On base plus #70, #72 and
#73's lab files plus T1, T3, T5 and T6 give the plan's undeclared problems
and pass with the declarations.

## Findings and their fold

| # | Severity | Finding | Fold |
|---|---|---|---|
| 1 | medium | T2 and T3 "depend on none", but D-0167 reaches main only with T1's PR | every content task depends on T1 |
| 2 | medium-low | on #69, a PDF original's equations have `shape: None`, so a needless declaration passes silently | the needless test reads `o["shape"] in (None, c["shape"])`; a tenth test if #69 has merged |
| 3 | low | T6's word count: 4438 at base, not 4444 (the declared passage leaves the compare) | stated as 4444 less the passage's words, read from the run |
| 4 | low | T1's red step: 6 fail and 3 pass, not as stated; `-k ruled` matches nothing | the two guard tests tightened to go red; 8 fail, 1 passes; selection fixed |
| 5 | low | YAML placement: Lab 5 has neither list; Lab 3 unstated; Lab 6 has flow `[]` lists | named per task |
| 6 | low, scope | three `\ ` spaces removed outside D-0167 (1) to (3) | kept: a global constraint and three table rows (Lab 1, Lab 3, Lab 6); re-measured 2026-11-06, same problems, reader clean |
| 7 | low | the reader cannot see `*` or a word set as letters; it exits 1 on Lab 1 | flags `<mo>*</mo>`; blind spot and Lab 1's exit stated |
| 8 | low | conversion-spec "Content-unchanged check" and CLAUDE.md go stale | T1 amends both |
| 9 | low | `a11y-chrome` is #73; #72 carries #71; DECISIONS.md rebase | named in the order section |
| 10 | info | ". One" / "). One" is also unique and takes fewer words out of the compare | adopted |
