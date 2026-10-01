"""tools/check_deployed.py against a local server (D-0049; phase 5).

Each test copies a small site to a temp folder, serves a copy of it over
http.server the way Pages does (a directory URL serves its index.html; an
unknown path answers 404 with the top-level 404.html), then breaks one thing
in what is served and requires the check to fail for that reason. No network
beyond 127.0.0.1.
"""

import http.server
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import check_deployed                      # noqa: E402

NOINDEX = '<meta name="robots" content="noindex, nofollow">'
SITE = {
    "index.html": "<html><head>" + NOINDEX + "</head><body><h1>Home</h1></body></html>\n",
    "courses/index.html": "<html><head>" + NOINDEX + "</head><body><h1>Courses</h1></body></html>\n",
    "404.html": "<html><head>" + NOINDEX + "</head><body><h1>Not found</h1></body></html>\n",
    "robots.txt": "User-agent: *\nDisallow: /\n",
    "site/site.css": "body { color: #000; }\n",
}


def write_site(folder, files):
    for rel, text in files.items():
        p = Path(folder, rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(text.encode("utf-8"))


class PagesLike(http.server.SimpleHTTPRequestHandler):
    """Serves `directory`; unknown paths answer 404 with its 404.html.

    spa=True answers unknown paths with the landing page and 200, which is
    what Pages does when a site has no 404.html. Like Cloudflare (error
    1010, seen on the first preview, 2026-10-01), it refuses Python's
    default user agent with 403.
    """
    spa = False
    requested = None
    agents = None

    def log_message(self, *args):
        pass

    def do_GET(self):
        self.requested.append(self.path)
        self.agents.append(self.headers.get("User-Agent", ""))
        if self.headers.get("User-Agent", "").startswith("Python-urllib"):
            body = b"error code: 1010\n"
            self.send_response(403)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        path = Path(self.translate_path(self.path))
        if path.is_dir():
            path = path / "index.html"
        if path.is_file():
            return super().do_GET()
        root = Path(self.directory)
        page, code = (root / "index.html", 200) if self.spa else (root / "404.html", 404)
        body = page.read_bytes() if page.is_file() else b"not found"
        self.send_response(code)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class Served(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name, "tested")
        self.served = Path(self.tmp.name, "served")
        write_site(self.folder, SITE)
        write_site(self.served, SITE)
        self.server = None
        self.requested = []
        self.agents = []

    def tearDown(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        self.tmp.cleanup()

    def serve(self, spa=False):
        served, requested, agents = str(self.served), self.requested, self.agents

        class Handler(PagesLike):
            def __init__(self, *a, **k):
                super().__init__(*a, directory=served, **k)
        Handler.spa = spa
        Handler.requested = requested
        Handler.agents = agents
        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        return "http://127.0.0.1:{}/".format(self.server.server_address[1])

    def failures(self, spa=False):
        return check_deployed.check(str(self.folder), self.serve(spa))

    def assertFailsMentioning(self, text, spa=False):
        found = self.failures(spa)
        self.assertTrue(any(text in f for f in found), found)

    def test_identical_copy_passes(self):
        self.assertEqual(self.failures(), [])

    def test_names_itself_in_the_user_agent(self):
        self.assertEqual(self.failures(), [])
        self.assertTrue(self.agents)
        for agent in set(self.agents):
            self.assertIn("check_deployed", agent)

    def test_index_fetched_at_directory_url(self):
        # Pages redirects /x/index.html to /x/ (plan, premise correction 3).
        self.assertEqual(self.failures(), [])
        self.assertIn("/courses/", self.requested)
        self.assertNotIn("/courses/index.html", self.requested)
        self.assertIn("/", self.requested)

    def test_one_changed_byte_fails(self):
        p = self.served / "site" / "site.css"
        p.write_bytes(p.read_bytes().replace(b"#000", b"#001"))
        self.assertFailsMentioning("site/site.css")

    def test_injected_script_fails(self):
        p = self.served / "courses" / "index.html"
        p.write_bytes(p.read_bytes().replace(b"</body>", b"<script>x()</script></body>"))
        self.assertFailsMentioning("courses/index.html")

    def test_file_missing_from_host_fails(self):
        (self.served / "site" / "site.css").unlink()
        self.assertFailsMentioning("site/site.css")

    def test_unknown_path_answering_200_fails(self):
        self.assertFailsMentioning("unknown path", spa=True)

    def test_unknown_path_must_serve_the_404_page(self):
        p = self.served / "404.html"
        p.write_bytes(p.read_bytes().replace(b"Not found", b"Gone"))
        self.assertFailsMentioning("unknown path")

    def test_missing_404_page_fails(self):
        (self.folder / "404.html").unlink()
        self.assertFailsMentioning("404.html")

    def test_missing_robots_fails(self):
        (self.folder / "robots.txt").unlink()
        self.assertFailsMentioning("robots.txt")

    def test_page_without_noindex_fails(self):
        for d in (self.folder, self.served):
            p = d / "courses" / "index.html"
            p.write_bytes(p.read_bytes().replace(NOINDEX.encode(), b""))
        self.assertFailsMentioning("noindex")


class CommandLine(unittest.TestCase):

    def run_tool(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "tools" / "check_deployed.py"), *args],
                              capture_output=True, text=True)

    def test_usage_error_without_arguments(self):
        self.assertNotEqual(self.run_tool().returncode, 0)

    def test_missing_folder_is_an_error(self):
        # LEDGER 53: a missing input fails, never skips.
        proc = self.run_tool(str(ROOT / "build" / "no-such-folder"), "http://127.0.0.1:9/")
        self.assertNotEqual(proc.returncode, 0)

    def test_unreachable_host_fails(self):
        with tempfile.TemporaryDirectory() as d:
            write_site(d, SITE)
            # Port 9 (discard) on loopback: nothing listens there.
            proc = self.run_tool(d, "http://127.0.0.1:9/")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("FAIL", proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
