"""The post-render search strip, tools/quarto_build.py (D-0037, owner ruling).

Quarto 1.10.18 still writes its search markup and search.json when
`website.search` is false, so the driver removes them after render. These are
unit tests on strings and temporary folders: no build needed.
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import quarto_build                       # noqa: E402

OPTIONS = ('<script id="quarto-search-options" type="application/json">{\n'
           '  "language": {\n'
           '    "search-no-results-text": "No results"\n'
           '  }\n'
           '}</script>\n')
RESULTS = '<div id="quarto-search-results"></div>\n'

BEFORE_HEAD = ('<head>\n<meta name="generator" content="quarto-1.10.18">\n'
               '<link href="site_libs/bootstrap/bootstrap.min.css" rel="stylesheet">\n')
AFTER_HEAD = ('<meta name="robots" content="noindex, nofollow">\n</head>\n\n<body>\n\n')
AFTER_BODY = '<!-- content -->\n<main><h1>Title</h1></main>\n</body>\n'


def page(options=OPTIONS, results=RESULTS):
    return BEFORE_HEAD + options + AFTER_HEAD + results + AFTER_BODY


class StripPage(unittest.TestCase):

    def test_fragments_removed_rest_byte_identical(self):
        self.assertEqual(quarto_build.strip_search_page(page(), "index.html"),
                         page(options="", results=""))

    def test_no_blank_line_left_behind(self):
        out = quarto_build.strip_search_page(page(), "index.html")
        self.assertNotIn("\n\n\n", out)
        self.assertNotIn("quarto-search", out)

    def test_page_without_the_script_raises(self):
        with self.assertRaisesRegex(ValueError, "courses/index.html"):
            quarto_build.strip_search_page(page(options=""), "courses/index.html")

    def test_page_without_the_results_div_raises(self):
        with self.assertRaisesRegex(ValueError, "courses/index.html"):
            quarto_build.strip_search_page(page(results=""), "courses/index.html")

    def test_doubled_script_raises(self):
        with self.assertRaisesRegex(ValueError, "index.html"):
            quarto_build.strip_search_page(page(options=OPTIONS * 2), "index.html")

    def test_doubled_results_div_raises(self):
        with self.assertRaisesRegex(ValueError, "index.html"):
            quarto_build.strip_search_page(page(results=RESULTS * 2), "index.html")


class StripFolder(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.out = Path(self._tmp.name)

    def write(self, rel, text):
        p = self.out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="")
        return p

    def test_every_page_stripped_and_search_json_removed(self):
        a = self.write("index.html", page())
        b = self.write("labs/x/modern/index.html", page())
        j = self.write("search.json", "[]\n")
        quarto_build.strip_search(str(self.out))
        for p in (a, b):
            self.assertEqual(p.read_text(encoding="utf-8"), page(options="", results=""))
        self.assertFalse(j.exists())

    def test_site_libs_left_alone(self):
        lib = self.write("site_libs/x/y.html", "<p>no search markup here</p>\n")
        self.write("index.html", page())
        quarto_build.strip_search(str(self.out))
        self.assertEqual(lib.read_text(encoding="utf-8"), "<p>no search markup here</p>\n")

    def test_a_page_quarto_did_not_write_is_left_alone(self):
        # Quarto copies a sim's source page into the output as is; post()
        # replaces it. It carries no generator tag and no search markup.
        sim = self.write("sims/x/index.html", "<html><body>a sim</body></html>\n")
        self.write("index.html", page())
        quarto_build.strip_search(str(self.out))
        self.assertEqual(sim.read_text(encoding="utf-8"), "<html><body>a sim</body></html>\n")

    def test_missing_search_json_is_fine(self):
        self.write("index.html", page())
        quarto_build.strip_search(str(self.out))

    def test_a_bad_page_raises_and_names_it(self):
        self.write("index.html", page())
        self.write("sims/index.html", page(results=""))
        with self.assertRaisesRegex(ValueError, "sims"):
            quarto_build.strip_search(str(self.out))


if __name__ == "__main__":
    unittest.main()
