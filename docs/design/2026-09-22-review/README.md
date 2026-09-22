# Site design review, 2026-09-22

Five mockup boards from a design review of the live site, kept so the
reasoning behind D-0029 to D-0031 is not lost with the session that made it.
These are mockups, not the site: nothing here is built, tested, or served,
and where a board and the built site disagree, the site is right.

Each `.dc.html` file is one board, and `canvas.json` records their titles and
positions on the canvas they came from. A board opens in a browser on its
own; the format is a Claude design canvas export, so the `<x-dc>` wrapper and
the trailing script matter only to that editor.

| File | Board | Became |
|---|---|---|
| `Main.dc.html` | The home page as it was, with the problems marked | the review |
| `Proposed.dc.html` | One centered reading column | D-0029 |
| `Tokens.dc.html` | The spacing scale and the type scale | the tokens in `site/site.css` |
| `Hero.dc.html` | Home page with a hero band and link cards | D-0031 |
| `Print.dc.html` | Lab 1 on letter paper | the print rules in `site/site.css` |

Placeholders on the boards are marked in brackets. The print board's question
text and page count are placeholders, and the logo is a label rather than the
real file on every board. The hero board carries a headline that was never
ruled; the built page keeps the site title instead.
