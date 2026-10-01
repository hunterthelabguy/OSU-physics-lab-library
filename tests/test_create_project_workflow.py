"""The one-time project creation workflow (D-0050, proposed; phase 5).

The Cloudflare dashboard creates a Direct Upload project only with a first
upload; `wrangler pages project create` makes an empty one with its
production branch named. This workflow runs it by hand from the Actions tab,
with the secrets already in GitHub, so the token never reaches a machine.
A successor standing the site up in their own account runs it once too.

The wrangler pin lives here, the one place, and the deploy job's test reads
it from this module.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / ".github" / "workflows" / "create-pages-project.yml"
# Chosen from the npm registry at build time (2026-10-01, `latest`), never
# from memory. An upgrade is its own PR that changes this line.
WRANGLER_VERSION = "4.146.0"
SECRETS = {"CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID"}
PROJECT_VARIABLE = "CLOUDFLARE_PAGES_PROJECT"


def workflow():
    if not WORKFLOW.is_file():
        raise AssertionError("missing " + WORKFLOW.relative_to(ROOT).as_posix())
    return WORKFLOW.read_text(encoding="utf-8")


class CreateProject(unittest.TestCase):

    def test_runs_only_by_hand(self):
        on = re.search(r"(?m)^on:\n((?:  .*\n)+)", workflow())
        self.assertIsNotNone(on, "no on: block")
        self.assertEqual(on.group(1), "  workflow_dispatch:\n")

    def test_one_job_read_only(self):
        body = workflow().split("\njobs:\n", 1)[1]
        self.assertEqual(re.findall(r"(?m)^  ([A-Za-z0-9_-]+):$", body), ["create"])
        self.assertRegex(body, r"(?m)^    permissions:\n      contents: read\n")

    def test_names_exactly_the_two_secrets(self):
        self.assertEqual(set(re.findall(r"secrets\.([A-Za-z0-9_]+)", workflow())), SECRETS)

    def test_pinned_create_with_production_branch_main(self):
        runs = [l.strip() for l in workflow().splitlines()
                if re.search(r"\bnpx\b", l) and not l.lstrip().startswith("#")]
        self.assertEqual(runs, [
            'npx --yes wrangler@' + WRANGLER_VERSION
            + ' pages project create "$PROJECT" --production-branch=main'])

    def test_project_name_from_variable_and_required(self):
        text = workflow()
        self.assertIn("PROJECT: ${{ vars." + PROJECT_VARIABLE + " }}", text)
        self.assertIn('test -n "$PROJECT"', text)

    def test_no_third_party_actions_and_no_checkout(self):
        # Creating a project needs nothing from the repository.
        self.assertEqual(re.findall(r"uses:[ ]*(\S+)", workflow()), [])


if __name__ == "__main__":
    unittest.main()
