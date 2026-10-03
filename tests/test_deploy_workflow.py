"""The deploy job in verify.yml (D-0047, D-0048; phase 5).

Reads the workflow as text with the standard library, as
test_quarto_config.py does. The folder deployed is read from _quarto.yml's
output-dir, never written here as a literal, so the phase 5 premise error
(deploying build/site/, the old build) cannot recur.
"""

import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
from test_quarto_config import values     # noqa: E402
# One pin for wrangler, one list of secret names, one variable name (D-0050).
from test_create_project_workflow import (  # noqa: E402
    PROJECT_VARIABLE, SECRETS, WRANGLER_VERSION)

WORKFLOW = ROOT / ".github" / "workflows" / "verify.yml"
WORKFLOWS = ROOT / ".github" / "workflows"
# Production for a push to main; a preview for a pull request from this
# repository; nothing for a fork's pull request (call 3).
DEPLOY_IF = ("(github.event_name == 'push' && github.ref == 'refs/heads/main') || "
             "(github.event_name == 'pull_request' && "
             "github.event.pull_request.head.repo.full_name == github.repository)")


def workflow():
    return WORKFLOW.read_text(encoding="utf-8")


def jobs():
    """{name: text} of each job under jobs:, in order."""
    body = workflow().split("\njobs:\n", 1)[1]
    parts = re.split(r"^  ([A-Za-z0-9_-]+):\n", body, flags=re.M)
    return dict(zip(parts[1::2], parts[2::2]))


def steps(job_text):
    """(name, text) of each step of one job, in order."""
    out = []
    for text in re.split(r"^      - (?=name:|uses:)", job_text, flags=re.M)[1:]:
        m = re.match(r"name:[ ]*(.*)", text)
        out.append((m.group(1).strip() if m else text.splitlines()[0], text))
    return out


def output_dir():
    found = values("output-dir")
    assert len(found) == 1, found
    return found[0]


def deploy():
    j = jobs()
    if "deploy" not in j:
        raise AssertionError("verify.yml has no deploy job")
    return j["deploy"]


class DeployJob(unittest.TestCase):

    def test_needs_verify(self):
        self.assertRegex(deploy(), r"(?m)^    needs: verify$")

    def test_runs_only_for_main_or_this_repositorys_pull_requests(self):
        m = re.search(r"(?m)^    if: (.*)$", deploy())
        self.assertIsNotNone(m, "deploy job has no if:")
        self.assertEqual(m.group(1).strip(), DEPLOY_IF)

    def test_read_only_token_for_github(self):
        self.assertRegex(deploy(), r"(?m)^    permissions:\n      contents: read\n")

    def test_secrets_named_only_in_deploy(self):
        deploy()
        for name, text in jobs().items():
            found = set(re.findall(r"secrets\.([A-Za-z0-9_]+)", text))
            with self.subTest(job=name):
                if name == "deploy":
                    self.assertEqual(found, SECRETS)
                else:
                    self.assertEqual(found, set())

    def test_project_name_from_repository_variable(self):
        text = deploy()
        self.assertIn("${{ vars." + PROJECT_VARIABLE + " }}", text)
        self.assertNotIn("--project-name=osu", text)
        self.assertNotIn("--project-name osu", text)

    def test_missing_project_variable_fails(self):
        # LEDGER 53: an unset variable is an error, never a deploy to a guess.
        self.assertIn('test -n "$PROJECT"', deploy())

    def test_wrangler_pinned_exactly(self):
        text = workflow()
        self.assertRegex(WRANGLER_VERSION, r"^\d+\.\d+\.\d+$")
        calls = re.findall(r"wrangler@(\S+)", text)
        self.assertEqual(calls, [WRANGLER_VERSION])
        self.assertNotIn("wrangler@latest", text)
        # Every command that runs wrangler names the pinned version.
        runs = [l for l in text.splitlines() if re.search(r"\b(npx|wrangler)\b", l)
                and not l.lstrip().startswith("#") and "wrangler-output" not in l
                and "wrangler reported" not in l]
        self.assertEqual(len(runs), 1, runs)
        self.assertIn("npx --yes wrangler@" + WRANGLER_VERSION + " pages deploy", runs[0])

    def test_deploys_the_output_dir(self):
        self.assertIn("pages deploy " + output_dir() + " ", deploy())

    def test_branch_and_commit_through_env_not_interpolated(self):
        # A branch name is attacker-chosen text; it reaches the shell only as
        # an environment variable, never pasted into the script.
        for name, text in steps(deploy()):
            run = text.split("run:", 1)[1] if "run:" in text else ""
            with self.subTest(step=name):
                self.assertNotIn("${{", run)

    def test_checks_the_deployed_url(self):
        names = [n for n, _ in steps(deploy())]
        texts = [t for _, t in steps(deploy())]
        i = next(k for k, t in enumerate(texts) if "pages deploy" in t)
        later = "".join(texts[i + 1:])
        self.assertIn("tools/check_deployed.py " + output_dir() + ' "$URL"', later, names)
        self.assertIn("WRANGLER_OUTPUT_FILE_PATH", texts[i])
        # D-0060: the deployment URL is checked once; a retry there would
        # hide a real fault, since it passed on its first run every time.
        step = [t for t in texts[i + 1:] if '"$URL"' in t]
        self.assertEqual(len(step), 1, names)
        self.assertNotIn("--wait", step[0])

    def test_production_alias_checked_on_main(self):
        # D-0050: a project whose production branch is not main would take a
        # merge as a preview while the alias kept serving older bytes, and the
        # check against the deployment's own URL would still pass.
        s = steps(deploy())
        name, text = s[-1]
        self.assertRegex(text, r"(?m)^        if: github.event_name == 'push' && "
                               r"github.ref == 'refs/heads/main'$", name)
        self.assertIn("PROJECT: ${{ vars." + PROJECT_VARIABLE + " }}", text)
        # D-0060: the alias may lag the deployment by seconds, so this step
        # alone reruns the whole check every 5 s for up to the ruled 120 s.
        self.assertIn('tools/check_deployed.py ' + output_dir()
                      + ' "https://$PROJECT.pages.dev/" --wait 120', text)


class TestedFolderIsDeployedFolder(unittest.TestCase):
    """call 4: verify hands deploy the folder it tested, as an artifact."""

    def test_verify_uploads_output_dir_last(self):
        s = steps(jobs()["verify"])
        name, text = s[-1]
        self.assertIn("uses: actions/upload-artifact@", text, name)
        self.assertRegex(text, r"(?m)^          path: " + re.escape(output_dir()) + "$")
        self.assertRegex(text, r"(?m)^          name: quarto-site$")

    def test_deploy_downloads_into_output_dir(self):
        text = "".join(t for _, t in steps(deploy()) if "actions/download-artifact@" in t)
        self.assertRegex(text, r"(?m)^          name: quarto-site$")
        self.assertRegex(text, r"(?m)^          path: " + re.escape(output_dir()) + "$")

    def test_deploy_never_builds(self):
        text = deploy()
        for word in ("quarto_build", "render.py", "unittest", "actions/checkout"):
            with self.subTest(word=word):
                if word == "actions/checkout":
                    # The checker script is the one file it needs from the repo.
                    self.assertIn("sparse-checkout: tools/check_deployed.py", text)
                else:
                    self.assertNotIn(word, text)


class NoThirdPartyOrHostConfig(unittest.TestCase):

    def test_secrets_only_in_the_two_cloudflare_workflows(self):
        # D-0050: verify.yml's deploy job and the hand-run creation workflow.
        allowed = {"verify.yml", "create-pages-project.yml"}
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            if re.search(r"secrets\.", path.read_text(encoding="utf-8")):
                with self.subTest(workflow=path.name):
                    self.assertIn(path.name, allowed)

    def test_only_actions_org(self):
        for use in re.findall(r"uses:[ ]*(\S+)", workflow()):
            with self.subTest(uses=use):
                self.assertTrue(use.startswith("actions/"), use)

    def test_no_host_config_committed(self):
        # LEDGER 39 and 49: build and host settings live in the project.
        tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                                 text=True, check=True).stdout.splitlines()
        for path in tracked:
            name = path.rsplit("/", 1)[-1]
            with self.subTest(path=path):
                self.assertFalse(name.startswith("wrangler."), path)
                self.assertNotIn(name, {"_redirects", "_headers", "vercel.json"})


if __name__ == "__main__":
    unittest.main()
