"""The old build's chrome, lifted for the Quarto pages (D-0036, D-0038).

The chrome is not copied. Each piece is rendered from the old templates,
tools/template.html and tools/template-site.html (with the brand partials
beside them), by Pandoc with an empty body and the metadata tools/render.py
passes, then cut at <main>. Phase 4 moves the templates when it retires the
old build. The Quarto shapes below are Quarto 1.10.18's; the driver pins
that version, and dress() fails loudly if a shape is not found exactly once.
"""

import os
import re

import render

OLD = re.compile(r'<body class="([^"]*)">\n(.*?)<main>.*?</main>\n(.*?)</body>', re.S)
QMAIN = re.compile(
    r'<main class="content" id="quarto-document-content">'
    r'<header id="title-block-header" class="quarto-title-block"></header>'
    r'(.*?)</main> <!-- /main -->', re.S)
QBODY = re.compile(r'<body class="([^"]*)">')
QCONTENT_END = "</div> <!-- /content -->"


def css_path(*parts):
    """Absolute, so --embed-resources finds it, as render.py does."""
    return os.path.join(render.ROOT, *parts).replace(os.sep, "/")


def old_chrome(page):
    """(body_class, top, bottom) for one page, from the old template.

    The arguments mirror render.render() and render.render_page(), including
    --embed-resources: that is what turns the logo path in render.site_vars
    into the data: URI the logo test checks. Passing the data URI itself
    would not work: at about 234 KB it exceeds the Windows command-line
    limit of 32767 characters.
    """
    cmd = [render.PANDOC, "-f", "markdown-smart", "-t", "html5", "--standalone",
           "--embed-resources", "-M", "pagetitle=chrome",
           "-M", "chromecss=" + css_path("site", "site.css")]
    if page["kind"] == "doc":
        theme = page["theme"]
        cmd += ["--template", os.path.join(render.ROOT, "tools", "template.html"),
                "-M", "theme=" + theme,
                "-M", "css=" + css_path("themes", theme + ".css"),
                "-M", "presentationnote=" + render.THEME_NOTE[theme]]
        cmd += render.site_vars(page["depth"]) + render.document_extras(theme, page["depth"])
    else:
        cmd += ["--template", os.path.join(render.ROOT, "tools", "template-site.html"),
                "-M", "footnote=" + page["footnote"]]
        cmd += render.site_vars(page["depth"])
    out = render.run(cmd, input="", capture_output=True, text=True, encoding="utf-8").stdout
    m = OLD.search(out)
    if m is None:
        raise ValueError("old template gave no <body>...<main> shape for " + page["html"])
    return m.group(1), m.group(2), m.group(3)


def once(pattern, text, what):
    found = list(pattern.finditer(text))
    if len(found) != 1:
        raise ValueError("{}: expected exactly one, found {}".format(what, len(found)))
    return found[0]


def dress(quarto_html, body_class, top, bottom):
    """A Quarto page with the old chrome: bare <main>, top chrome right after
    <body>, bottom chrome right after Quarto's content div."""
    m = once(QMAIN, quarto_html, "Quarto <main>")
    text = (quarto_html[:m.start()] + "<main>\n" + m.group(1).strip() + "\n</main>"
            + quarto_html[m.end():])
    b = once(QBODY, text, "<body class=...>")
    text = (text[:b.start()] + '<body class="{} {}">\n'.format(body_class, b.group(1))
            + top.rstrip("\n") + text[b.end():])
    e = once(re.compile(re.escape(QCONTENT_END)), text, "Quarto content div end")
    return text[:e.end()] + "\n" + bottom + text[e.end():]
