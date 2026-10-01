"""Check a deployed site against the folder that was tested (D-0049).

Usage: python tools/check_deployed.py FOLDER BASE_URL

For every file in FOLDER, fetches its public URL under BASE_URL and requires
the same bytes; an index.html is fetched at its directory URL, because Pages
redirects /x/index.html to /x/. A path that is not in the folder must answer
404 with the folder's own 404.html, because Pages answers unknown paths with
the landing page and a 200 when that file is absent. The folder must carry
robots.txt, and every HTML page the noindex meta (ledger 37).

The test suite reads folders, never URLs; this is the check that sees what
the host serves, so a host that rewrites HTML fails here. Standard library
only. Any failure, an unreachable host included, exits 1 (ledger 53).
"""

import os
import secrets
import sys
import urllib.error
import urllib.request

NOINDEX = b'<meta name="robots" content="noindex'
TIMEOUT = 30


def files(folder):
    """Every file under folder, as a forward-slash path relative to it."""
    for here, _, names in os.walk(folder):
        for name in names:
            rel = os.path.relpath(os.path.join(here, name), folder)
            yield rel.replace(os.sep, "/")


def public_path(rel):
    if rel == "index.html":
        return ""
    if rel.endswith("/index.html"):
        return rel[:-len("index.html")]
    return rel


def fetch(url):
    """(status, body). Redirects are followed; an HTTP error is a status."""
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as err:
        return err.code, err.read()


def check(folder, base_url):
    """A list of failures, empty when the deployment matches the folder."""
    if not os.path.isdir(folder):
        return ["FAIL {}: folder is missing".format(folder)]
    base = base_url if base_url.endswith("/") else base_url + "/"
    failures = []
    rels = sorted(files(folder))

    for required in ("404.html", "robots.txt"):
        if required not in rels:
            failures.append("FAIL {}: not in the folder".format(required))

    for rel in rels:
        with open(os.path.join(folder, rel), "rb") as fh:
            want = fh.read()
        if rel.endswith(".html") and NOINDEX not in want:
            failures.append("FAIL {}: no noindex meta".format(rel))
        url = base + public_path(rel)
        try:
            status, got = fetch(url)
        except (urllib.error.URLError, OSError) as err:
            # One unreachable fetch says the host is down; stop there.
            failures.append("FAIL {}: {} unreachable ({})".format(rel, url, err))
            return failures
        if status != 200:
            failures.append("FAIL {}: {} answered {}".format(rel, url, status))
        elif got != want:
            failures.append("FAIL {}: {} served {} bytes, not the tested {}".format(
                rel, url, len(got), len(want)))

    missing = base + "check-deployed-" + secrets.token_hex(8) + "/"
    try:
        status, got = fetch(missing)
    except (urllib.error.URLError, OSError) as err:
        failures.append("FAIL unknown path: {} unreachable ({})".format(missing, err))
    else:
        if status != 404:
            failures.append("FAIL unknown path: {} answered {}, not 404".format(missing, status))
        elif "404.html" in rels:
            with open(os.path.join(folder, "404.html"), "rb") as fh:
                if got != fh.read():
                    failures.append("FAIL unknown path: {} did not serve 404.html".format(missing))
    return failures


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    folder, base_url = argv
    failures = check(folder, base_url)
    for line in failures:
        print(line)
    if failures:
        print("{} failure(s) against {}".format(len(failures), base_url))
        return 1
    print("OK: {} files served byte for byte at {}".format(len(list(files(folder))), base_url))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
