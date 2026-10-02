# Quarto Migration Phase 5 Plan: new host

Status: calls ruled 2026-10-01 (owner in chat: "I approve your leans on all
eight"); D-0047 to D-0049 not yet promoted. Nothing built. Owner's side is in
`docs/quarto-phase-5-owner-checklist.md`. Ledger entries D-0047 to D-0049 are
appended to `DECISIONS.md` as proposed.

**Spec:** `docs/quarto-migration-plan.md`, phase 5: "GitHub Actions builds,
then uploads `build/site/` to Cloudflare. Needs a deploy-scoped Cloudflare API
token, which the owner creates and stores as a repo secret; Claude never
handles it. Old Vercel URL gets a redirect or a notice before it is switched
off."

Ledger: D-0034 (ruled), D-0047 to D-0049 (proposed); binds LEDGER 37, 39, 40,
47, 48, 49, 53

## The premise, checked against the record

Four things in the phase 5 text or in D-0034 do not hold as written. Sources:
the repo, and Cloudflare's and Vercel's documentation as fetched 2026-10-01
(pages cited; a fetch tool summarized them, so verify against the page before
anything load-bearing).

1. **The folder is `build/quarto-site/`, not `build/site/`.** `_quarto.yml`
   writes there (`output-dir`), and `build/site/` is the old build, which
   phase 4 deletes after this phase. The plan text and D-0034 both say
   `build/site/`. Uploading that would deploy the old build to the new host.
2. **Cloudflare Pages treats a site with no top-level `404.html` as a
   single-page app and answers every unknown path with the landing page**
   (Cloudflare, "Serving Pages": "Pages assumes that you are deploying a
   single-page application", and matches all incoming paths to `/`). Neither
   build has a `404.html`. On Vercel an unknown URL is a 404; on Pages it
   would be a 200 showing the landing page, and no test in the repo would
   notice.
3. **Pages redirects `/x/index.html` to `/x/`** (same page). Any check that
   fetches files by their path in the folder must ask for the directory URL
   for each `index.html`.
4. **D-0034's Vercel premise holds, now with the source.** Vercel's
   Fair Use Guidelines, page dated 2026-09-14: Hobby is "non-commercial
   personal use only", and commercial use includes "a paid employee or
   consultant writing the code". The rationale in D-0034 said "from memory,
   to be checked"; it is now checked. Whether this site counts is Vercel's
   call, not mine, but the owner's concern has a basis in the text.

Also relevant, and not a premise error: Vercel builds production from
`main` with the old build's command (CLAUDE.md, Deploy), which runs
`tools/render.py --site`. Phase 4 deletes that. So **the Vercel redirect or
notice must be in place before phase 4 merges**, or Vercel's next production
build fails.

Not verified, and treated as probes in the plan below: whether Cloudflare
rewrites HTML on `*.pages.dev` (its Email Address Obfuscation feature
rewrites email addresses and injects a decode script on regular zones; I did
not find whether it applies to `pages.dev`, and the footer carries contact
links); whether Vercel projects take a redirect as a setting with no file in
the repo; whether the name `osu-physics-lab-library` is free on `pages.dev`.

## Plan, assuming the leans below are ruled

Failing tests first. One PR for the code (Tasks 1 and 2), then the cutover
(Task 3) and docs (Task 4). The first real deploy needs the owner's secrets,
so Tasks 1 and 2 can be built and unit-tested without them, and Task 3 cannot
start until the checklist's items A to E are done.

**Task 1: red.**
- `tests/test_deploy_workflow.py`, reading the workflow files:
  - a `deploy` job exists with `needs: verify`, so nothing deploys from a red
    commit;
  - the Cloudflare secrets are named only in the `deploy` job, and only
    `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`;
  - the upload directory equals `_quarto.yml`'s `output-dir` (read, never a
    literal, so the premise error above cannot recur);
  - the wrangler version is an exact version, never `latest`; no third-party
    action (only `actions/*`);
  - production only for a push to `main`; a pull request deploys only when
    its head repository is this one (call 3);
  - no host config committed: no `wrangler.*`, `_redirects`, `_headers` or
    `vercel.json` (LEDGER 39, 49).
- `tests/test_check_deployed.py`, unit tests for a new `tools/check_deployed.py`
  against a local `http.server` serving a temp folder: a byte-identical
  copy passes; one changed byte fails; an injected script tag fails; an
  unknown path that answers 200 fails; a missing `404.html` fails.
- 404 page (call 6): `tests/test_quarto_site.py::test_expected_pages` gains
  `404.html`, and the chrome contract covers it (banner, noindex, one `<h1>`).
- Each fails today. Written to fail for the named reason, with a missing
  tool failing, never skipping (LEDGER 53).

**Task 2: green.**
- `tools/check_deployed.py <folder> <base url>`: for every file in the folder
  fetch its public URL (the directory URL for an `index.html`) and require
  identical bytes; require 404 and the 404 page for a path that is not in the
  folder; require `robots.txt` and the `noindex` meta on every page. One
  executable, standard library only.
- The 404 page (call 6), built by the driver through the same chrome; wording
  is the owner's (call 6).
- `.github/workflows/verify.yml`: a `deploy` job after `verify`. `verify`
  uploads the folder it tested as an artifact; `deploy` downloads exactly that
  folder, runs the pinned `wrangler pages deploy` against the project, then
  runs `tools/check_deployed.py` against the deployment URL it printed. The
  deployed bytes are the tested bytes.
- No tool's page-making code changes.

**Task 3: cutover** (needs the checklist). First production deploy from
`main`; `check_deployed.py` green against the production URL; the owner opens
it on a phone (and does the Lab 1 print preview that has never been done);
then the Vercel notice or redirect (call 8), then phase 4 may merge.

**Task 4: docs.** CLAUDE.md, Deploy: the Cloudflare project, the two secret
names, the deploy command and the three-line recipe to set the same thing up
on another host (LEDGER 49's rule); the Vercel text marked retired. Migration
plan: phase 5 done. STATE.md. A successor page in the lab handbook
(`OSU-lab-ops`, by role): where the site is hosted, how the token is renewed,
how to stand the same site up in your own Cloudflare account (copy the repo;
never hand over the account).

## Numbered calls for the owner

1. **Which Cloudflare product, and the project name.** Lean: Pages, as a
   Direct Upload project (not connected to Git), named
   `osu-physics-lab-library` if free. Reason: it is the documented path for
   uploading a prebuilt folder from CI with one command and one token
   permission (Account, Cloudflare Pages, Edit), needs no committed config,
   and gives every non-production deployment a `noindex` header and its own
   URL. Cost of the alternative, Workers static assets: Cloudflare's own
   migration page calls moving optional and states no Pages end date (the
   wording "successor for new projects" came from third-party posts, and an
   earlier draft of this call overstated it; corrected 2026-10-01). Workers
   wants a config file (Cloudflare calls it mandatory) and a different token
   permission (Account, Workers Scripts, Edit). Moving later changes settings,
   not the folder (LEDGER 39).
2. **Whose Cloudflare account hosts it.** Lean: your own account, as the
   GitHub and Vercel setups are (LEDGER 47, and "org ownership deferred until
   it matters"), with the successor note in Task 4: copy the repo and make
   your own project, never hand over the account. Cost of the alternative, a
   department or institutional account: it is the durable answer, and I do
   not know whether one exists or what OSU requires. I did not check
   Cloudflare's own terms for this use or any OSU hosting policy; that is
   yours to read before the account holds the site (checklist B).
3. **What deploys and when.** Lean: a push to `main` is production; a pull
   request from this repository is a preview (its own URL, `noindex` by
   default); a fork's pull request deploys nothing, since it gets no
   secrets. Reason: it keeps the review-on-your-phone habit that Vercel's
   preview gives you today. Cost of the alternative, `main` only: no preview
   to open before merging, so a layout problem is found on production.
4. **How the deploy job is built.** Lean: a separate `deploy` job after
   `verify`, handed the tested folder as an artifact, secrets visible to that
   job only. Reason: the deployed bytes are the tested bytes, and a step that
   runs the test suite never sees a token. Cost of the alternative, deploy
   steps at the end of `verify`: shorter file, secrets in the same job as all
   the test code, and the deploy folder rebuilt rather than carried.
5. **How wrangler is invoked.** Lean: `npx wrangler@<exact version> pages
   deploy` directly, the version chosen at build time from the registry, never
   from memory, and pinned by a test the way Quarto is. Reason: no third-party
   action holds the token, and a Wrangler upgrade is its own PR. Cost of the
   alternative, Cloudflare's GitHub Action: one fewer line, a third-party
   action in the path of the token (whether Cloudflare still maintains it I
   did not check), and an unpinned moving part.
6. **The 404 page.** Lean: add `404.html`, built through the same chrome, so
   unknown URLs return 404 as they do today, with wording you approve; I will
   propose wording in the PR, ship nothing you have not approved, and mark it a
   placeholder until then. Cost of the alternative, no 404 page: every typo
   and every dead link returns the landing page with a 200, and no check can
   tell a broken link from a working one. Cost of the page: one new page of
   copy in a site where "no page copy invented" is a rule, hence your approval.
7. **What "the Cloudflare site passes" means (D-0034).** Lean: the folder that
   passed `verify` is the folder deployed, and `tools/check_deployed.py` then
   proves every file is served byte for byte, unknown paths 404, `robots.txt`
   and `noindex` are present, all against the live URL; plus your phone check
   and the Lab 1 print preview. Reason: the suite reads folders, not URLs, so
   "passes the suite" alone would not see a host that rewrites HTML (the
   obfuscation question above). Cost of the alternative, the suite only:
   a rewrite by the host is invisible until a reader finds it.
8. **Retiring Vercel.** Lean: after the cutover check, a redirect from the
   old URL to the new one, set as a Vercel project setting so no file in the
   repo names Vercel (LEDGER 49), kept until you say it can go; Vercel itself
   is paused or deleted only on your word. It must be in place before phase 4
   merges. Reason: the old URL is the one you have shown colleagues. Cost of
   the alternative, a notice page: it needs code in the old build that phase
   4 deletes, and it makes every visitor click. Not verified: that a Vercel
   project takes a redirect as a setting; the first step is a read-only look
   at the project, and every change to Vercel needs your word first.

## Declined

- Cloudflare building the site (D-0034 already rules it out).
- A custom domain now: the default `pages.dev` URL is the same posture as
  LEDGER 48 (unlisted means `noindex`, `robots.txt` and the banner, not access
  control); a domain is its own decision.
- Cloudflare Access on previews: optional, adds a login to the review path;
  the checklist lists it as yours to turn on.
- Committing `wrangler.toml`, `_redirects`, `_headers` or `vercel.json`:
  LEDGER 39 and 49, and a test.
- `X-Robots-Tag` through a `_headers` file: the meta tag and `robots.txt`
  already carry the ruling, and a headers file only one host understands is
  what LEDGER 39 forbids.
- Re-measuring chrome, print or weights: no page changes except the new 404.
- Tracing whether Pages rewrites HTML from its documentation: the byte check
  against the live URL answers it directly.

## After the rulings (2026-10-01)

Recorded from the chat that followed the owner's approval; none of it is built.

- **Workers evaluated against Pages, and Pages stands.** Sources are
  Cloudflare's documentation as fetched 2026-10-01 (a fetch tool summarized
  the pages; verify before relying). For a static library Workers wins on no
  axis: it needs a mandatory `wrangler.jsonc` (to be generated on the runner,
  never committed, if ever used), a token with Workers Scripts Edit, an
  explicit `not_found_handling`, version URLs for previews with no documented
  `noindex` and branch aliases listed as "coming soon", and a longer default
  URL (`<name>.<account>.workers.dev` against `<project>.pages.dev`).
  Limits are equal on the free plan (20,000 files, 25 MiB per file), and the
  site is 29 files and 3 MB. The owner confirmed the dashboard offers a Pages
  Direct Upload project. Premise correction 2 (unknown paths return the
  landing page) is Pages-only; on Workers the 404 would be explicit config.
  What would make Workers clearly better: a ruling that relaxes LEDGER 39 for
  server-side code; Cloudflare giving Pages an end date; the domain living on
  Cloudflare DNS anyway; a CI dry run proving a flags-only deploy plus a
  documented `noindex` on versions.
- **Terms.** Cloudflare's Self-Serve agreement, as fetched, has no
  Vercel-style commercial-use clause for the free plan; section 2.1 says
  agreeing on behalf of an entity represents authority to bind it, so sign up
  as an individual unless OSU has agreed to host the site. OSU's own hosting
  policy was not checked.
- **The name is open.** Cloudflare offers only the `pages.dev` default;
  anything better is a custom domain. Lean: a subdomain of the department's
  OSU domain, which the department already uses for another service, pointed
  by CNAME (Pages accepts a CNAME for a subdomain once the domain is added in
  the dashboard first; Workers custom domains need a zone on Cloudflare). It
  needs OSU IT, by role, and also answers D-0012's concern about the logo on a
  non-OSU address. Interim: a short `pages.dev` name. A project name probably
  cannot be renamed (unverified), and an old project can stay as a redirect.
- **Proposed amendment to D-0048, not yet approved:** read the Cloudflare
  project name from a GitHub repository variable, not a literal in the
  workflow, so the interim name can change without touching code.
- **Draft on request:** one note by role to OSU IT covering the library's
  address and the D-0012 heads-up. The owner will ask once the site is live.
- **Separate thread, not this plan.** Moving the owner's other production
  service to Cloudflare is its own spec with its own ledger (plan before
  patch). It does not change this phase: the library is static and stays on
  Pages. Keep that thread's details out of this repo.

## Cutover and Vercel (2026-10-01)

- **Cutover checked.** PR #17 merged; the production run deployed
  `https://27d18c33.osu-physics-labs.pages.dev` and `check_deployed.py`
  passed against it and against `https://osu-physics-labs.pages.dev/`: 30
  files byte for byte, unknown paths 404 with `404.html`. The owner checked
  production on a phone and printed Lab 1 in both presentations; both fine.
  The project was created by `create-pages-project.yml` (PR #18), because
  the dashboard creates a Direct Upload project only with a first upload.
- **Vercel, read-only look** (Vercel API through the connector, 2026-10-01).
  Hobby, personal account, no team. Project `osu-physics-lab-library` has one
  domain, `osu-physics-lab-library.vercel.app`, with no redirect. Bulk
  redirects answer "not available ... on the Hobby or Pro Trial plan".
  Project routing rules are available: 0 of 100 used. Per Vercel's docs, a
  rule is staged (with a staging alias to preview it), then promoted, and a
  promoted version can be restored or discarded; a rule may answer 308 with
  a `Location` header to an external URL. No file in the repo is involved
  (LEDGER 49). Every page path of the old build exists in the Quarto build
  (only `404.html` is new), so the path can be kept.
- **Proposed change, awaiting the owner's word:** one routing rule, source
  `/(.*)`, status 308, `Location: https://osu-physics-labs.pages.dev/$1`;
  stage it, open the staging alias to confirm, then promote. Not verified:
  the exact capture syntax the rules accept, and whether a rule applies to
  the `vercel.app` domain without a redeploy; staging answers both before
  anything goes live. Then, before phase 4 merges, production builds from
  `main` must stop failing silently: either Vercel's Git builds are turned
  off for the project or the redirect holds whatever the build does; to be
  checked once the rule is live.
- **Vercel redirect live (2026-10-01, on the owner's word).** One project
  routing rule, "Moved to Cloudflare Pages": regex `^/(.*)$`, status 308,
  `Location: https://osu-physics-labs.pages.dev/$1` (rule
  `2c62b1ef-2f4a-4193-8f7a-842a135b74c7`, version
  `ee4d901c-ef50-49bb-a4d4-0587a74e1513`). Staged first and checked on the
  staging alias: `/`, `/courses/`, a lab page, a query string and an unknown
  path all answered 308 to the same path, query kept; production still
  served 200 while staged. Promoted, then checked on
  `osu-physics-lab-library.vercel.app`: the same 308s, with no redeploy.
  To undo: restore the previous routing version or disable the rule in the
  project's settings. Kept until the owner says it can go; the owner notes
  the old URL was not widely shared. Still open for phase 4: Vercel builds
  the old site on every push to `main`, and phase 4 deletes what that build
  runs; decide then whether to turn off the project's Git builds (the
  redirect is a project setting and does not depend on a deployment, as the
  promote without a redeploy showed).
