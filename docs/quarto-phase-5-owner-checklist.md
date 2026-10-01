# Phase 5 owner checklist

For the owner. Written 2026-10-01 beside `docs/superpowers/plans/2026-10-01-quarto-phase-5.md`;
the plan says why each item exists. Claude never creates, reads or enters the
Cloudflare token: do the secret items yourself and tell Claude only "secrets
set". Never paste a token or an account ID into chat, a file or an issue.

Nothing here blocks Tasks 1 and 2 of the plan (tests and the deploy tooling).
Items A to E block the first real deploy.

## A. Rule the eight calls

- [ ] Answer the plan's calls 1 to 8 in chat ("leans" is a fine answer).
      Call 6 includes approving or rewriting the 404 page's wording; call 2
      needs your fact about whose account hosts the site.

## B. The Cloudflare account

- [ ] Decide which account holds the site (call 2). If it is a new account,
      create it with two-factor sign-in on.
- [ ] Read Cloudflare's current terms for hosting this kind of site on your
      account, and OSU's policy on hosting a departmental site on a personal
      account, before the account holds it. Claude has not checked either.
- [ ] If the answer is "I need to ask someone", ask before the cutover, not
      after. Route by role (department front office or IT), not by name.

## C. The project

- [ ] In the Cloudflare dashboard, create a Pages project of the **Direct
      Upload** type (not "Connect to Git"), named as ruled in call 1. Note
      whether the name you wanted was free; if Cloudflare changed it, tell
      Claude the name it gave.
- [ ] Do not upload anything by hand. The workflow does the first upload.

## D. The API token

- [ ] My Profile, API Tokens, Create Token, Custom token. One permission:
      **Account, Cloudflare Pages, Edit**. Limit it to the one account.
- [ ] Set an expiry date, and put the renewal date on your calendar.
- [ ] Copy the token once, straight into step E. Do not keep a copy in a
      note, a file or chat.

## E. The repository secrets

- [ ] GitHub, this repository, Settings, Secrets and variables, Actions, two
      repository secrets: `CLOUDFLARE_API_TOKEN` (the token) and
      `CLOUDFLARE_ACCOUNT_ID` (your account's ID, shown in the dashboard).
- [ ] Tell Claude: "secrets set". That is all Claude needs from this step.

## F. Optional

- [ ] Cloudflare Access on preview deployments (project Settings, General,
      "Enable access policy"): puts a login in front of previews. Without it,
      previews are public, at a hash URL per deployment plus a branch-name
      alias, with a `noindex` header; the same unlisted posture as the live
      site (LEDGER 48).

## G. At the cutover (Task 3)

- [ ] Open the production URL on your phone: banner, top strip, nav, a lab
      page in both presentations, a sim.
- [ ] Print preview of Lab 1 and of a Quarto lab page, on paper or the PDF
      preview. Never done; the print rules have shipped since PR #11 unchecked.
- [ ] Say "cutover checked" in chat. Claude will not claim the print preview.

## H. Retiring Vercel

- [ ] Say when the redirect from the old URL may be set (call 8). Claude
      looks at the Vercel project read-only first and asks before any change.
- [ ] Decide when the redirect may go, and when the Vercel project is paused
      or deleted. Only on your word; the order is redirect first, Vercel
      project last.
- [ ] Tell anyone you gave the old URL to which URL to use, if you want to.

## I. Carried, not blocked by this phase

- [ ] The D-0012 heads-up to University Marketing. If the new URL is the one
      you start showing people, decide whether the heads-up goes with it.
- [ ] The two unruled design items (nav in the orange bar; a new hero
      headline).
- [ ] The successor note (plan Task 4) will say where the site is hosted and
      who holds the Cloudflare account by role. Say if the role is not yours.
