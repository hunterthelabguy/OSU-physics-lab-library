// test-law.mjs: checks for the Electric Force tool. No dependencies.
// Run from this folder: node test-law.mjs
// Loads the CORE block out of index.html (the same code the page runs), then checks
// the law, the noise, law codes, input parsing, export format, the numeric claims in
// BUILD-PROMPT.md and INSTRUCTOR-GUIDE.md, and a few static properties of the files.

import { readFileSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const read = (name) => readFileSync(join(here, name), "utf8");
const html = read("index.html");

// DECISIONS D-0028: page-text checks skip embedded data (base64 fonts can
// contain any letters by chance); network, policy and hash checks still
// read the whole file.
const pageText = html.replace(/data:[^"')\s]+/g, "data:");

const block = html.match(/\/\/ BEGIN CORE[^\n]*\n([\s\S]*?)\/\/ END CORE/);
if (!block) {
  console.error("FAIL: no CORE block found in index.html");
  process.exit(1);
}
const core = new Function(block[1] + `
return { NOISE_MIN, NOISE_MAX, LAW_DEFAULT, LAW_CODE_MAX, LAW_CODE_TABLE, lawParams, signedPow,
  lawForce, drawNoise, randomLawCode, parseNumberText, parseDistance, parseLawCode, formatForce,
  EXPORT_HEADER, buildDelimited, GRID, nearestGridIndex, stepGrid };`)();

let failures = 0, passes = 0;
function check(name, ok, detail = "") {
  if (ok) { passes++; return; }
  failures++;
  console.log("FAIL: " + name + (detail ? "  (" + detail + ")" : ""));
}
function section(name) { console.log("-- " + name); }
// A file that is not beside this script is reported as skipped, never counted
// as a pass. The instructor guide lives apart from the shipped page in some
// checkouts, and a check that did not run must not read as one that did.
const skipped = [];
function skip(name, why) { skipped.push(name + " (" + why + ")"); }
const present = (name) => existsSync(join(here, name));

const P0 = core.lawParams(0);
const F = (q1, q2, r, p = P0, u = 1) => core.lawForce(q1, q2, r, p, u);

// ---------------------------------------------------------------------------
section("default law, hand-computed values with u = 1");
// 2^3 * 3 * 0.5^2 = 8 * 3 * 0.25 = 6, so F = 6 pi = 18.84955592153876
check("F(2, 3, 0.5) === 6 pi", F(2, 3, 0.5) === 6 * Math.PI, F(2, 3, 0.5));
check("F(2, 3, 0.5) matches 18.84955592153876", F(2, 3, 0.5) === 18.84955592153876);
// (-2)^3 * 5 * 4^2 = -8 * 5 * 16 = -640, so F = -640 pi = -2010.6192982974676
check("F(-2, 5, 4) === -640 pi", F(-2, 5, 4) === -640 * Math.PI, F(-2, 5, 4));
check("F(-2, 5, 4) matches -2010.6192982974676", F(-2, 5, 4) === -2010.6192982974676);
// 0.5^3 * (-4) * 3^2 = 0.125 * -4 * 9 = -4.5, so F = -4.5 pi = -14.137166941154069
check("F(0.5, -4, 3) === -4.5 pi", F(0.5, -4, 3) === -4.5 * Math.PI, F(0.5, -4, 3));
check("F(0.5, -4, 3) matches -14.137166941154069", F(0.5, -4, 3) === -14.137166941154069);
check("u scales the force linearly", F(2, 3, 0.5, P0, 1.1) === 6 * Math.PI * 1.1);
check("code 0 parameters are the default law", P0 && P0.k === Math.PI && P0.n1 === 3 && P0.n2 === 1 && P0.nr === 2);

const rel = (a, b) => Math.abs(a - b) / Math.abs(b);
// Claims in BUILD-PROMPT.md.
check("1 uC, 1 uC, 1 m gives about 3e-24 N", rel(F(1e-6, 1e-6, 1), 3.14159e-24) < 1e-5, F(1e-6, 1e-6, 1));
check("default ranges low corner about 3e-6 N", rel(F(0.1, 0.1, 0.1), 3.14159e-6) < 1e-5, F(0.1, 0.1, 0.1));
check("default ranges high corner about 3e6 N", rel(F(10, 10, 10), 3.14159e6) < 1e-5, F(10, 10, 10));

// ---------------------------------------------------------------------------
section("noise");
check("noise at rand() = 0 is 0.9", core.drawNoise(() => 0) === 0.9);
check("noise at largest rand() is below 1.1", core.drawNoise(() => 1 - 2 ** -53) <= 1.1);
let lo = Infinity, hi = -Infinity, sum = 0;
const N = 10000;
for (let i = 0; i < N; i++) {
  const u = core.drawNoise(Math.random);
  lo = Math.min(lo, u); hi = Math.max(hi, u); sum += u;
}
check("10000 draws stay within [0.9, 1.1]", lo >= 0.9 && hi <= 1.1, `min ${lo}, max ${hi}`);
check("10000 draws spread across the interval", lo < 0.905 && hi > 1.095, `min ${lo}, max ${hi}`);
check("10000 draws average near 1", Math.abs(sum / N - 1) < 0.005, sum / N);

// ---------------------------------------------------------------------------
section("sign behavior");
for (const code of [0, 1, 5, 10]) {
  const p = core.lawParams(code);
  const cases = [[2, 3, 1], [2, -3, -1], [-2, 3, -1], [-2, -3, 1]];
  for (const [q1, q2, want] of cases) {
    const f = F(q1, q2, 1.5, p);
    check(`code ${code}: sign of F(${q1}, ${q2}) is ${want}`, Number.isFinite(f) && Math.sign(f) === want, f);
  }
  check(`code ${code}: |F| is the same for all four sign pairs`,
    new Set(cases.map(([a, b]) => Math.abs(F(a, b, 1.5, p)))).size === 1);
}
check("signedPow equals ** for integer n on negatives", core.signedPow(-3, 3) === (-3) ** 3 && core.signedPow(-3, 1) === -3);
check("zero charge gives zero force", F(0, 3, 2) === 0 && F(3, 0, 2) === 0);
check("r = 0 gives zero force", F(2, 3, 0) === 0);

// ---------------------------------------------------------------------------
section("law codes");
const expected = { 1: ["nr", 2.1], 2: ["nr", 2.2], 5: ["nr", 2.5], 9: ["nr", 2.9], 10: ["nr", 3] };
for (const [code, [param, value]] of Object.entries(expected)) {
  const p = core.lawParams(Number(code));
  check(`code ${code} sets ${param} to ${value}`, p && p[param] === value, p && p[param]);
}
for (let code = 1; code <= core.LAW_CODE_MAX; code++) {
  const a = core.lawParams(code), b = core.lawParams(code);
  check(`code ${code} is deterministic`, JSON.stringify(a) === JSON.stringify(b));
  const changed = ["k", "n1", "n2", "nr"].filter((key) => a[key] !== P0[key]);
  check(`code ${code} changes only the r exponent`, changed.length === 1 && changed[0] === "nr", changed.join(","));
  check(`code ${code} raises it by a whole number of tenths`,
    Number.isInteger(Math.round((a[changed[0]] - P0[changed[0]]) * 10)) && a[changed[0]] > P0[changed[0]]);
}
const allParams = new Set();
for (let code = 0; code <= core.LAW_CODE_MAX; code++) allParams.add(JSON.stringify(core.lawParams(code)));
check("codes 0 to 10 are 11 distinct laws", allParams.size === 11, allParams.size);
for (const bad of [-1, 11, 30, 99, 1.5, NaN, "3"]) check(`lawParams(${JSON.stringify(bad)}) is rejected`, core.lawParams(bad) === null);
check("parseLawCode('11') says not assigned", /not assigned/i.test(core.parseLawCode("11").message || ""));
check("parseLawCode('7') is 7", core.parseLawCode(" 7 ").ok && core.parseLawCode(" 7 ").value === 7);
for (const bad of ["", "-1", "2.5", "abc"]) check(`parseLawCode(${JSON.stringify(bad)}) is rejected`, !core.parseLawCode(bad).ok);
check("random code at rand() = 0 is 1", core.randomLawCode(() => 0) === 1);
check("random code at largest rand() is 10", core.randomLawCode(() => 1 - 2 ** -53) === 10);
const seen = new Set();
for (let i = 0; i < 10000; i++) seen.add(core.randomLawCode(Math.random));
check("random codes cover exactly 1 to 10", seen.size === 10 && Math.min(...seen) === 1 && Math.max(...seen) === 10);

// ---------------------------------------------------------------------------
section("input parsing");
for (const [text, value] of [["2", 2], ["-3.5e-1", -0.35], [" 1E2 ", 100], ["+.5", 0.5], ["0", 0], ["5.", 5]]) {
  const p = core.parseNumberText(text);
  check(`parse ${JSON.stringify(text)} = ${value}`, p.ok && p.value === value, JSON.stringify(p));
}
for (const text of ["", "  ", "abc", "1e", "--1", "1,5", "Infinity", "0x10", "1e999", "NaN", "2 3"]) {
  const p = core.parseNumberText(text);
  check(`reject ${JSON.stringify(text)} with a message`, !p.ok && typeof p.message === "string" && p.message.length > 0);
}
check("negative distance is rejected", !core.parseDistance("-1").ok && /negative/i.test(core.parseDistance("-1").message));
check("zero distance is accepted", core.parseDistance("0").ok);

// ---------------------------------------------------------------------------
section("export format");
const rows = [
  { trial: 1, code: 0, q1: 1, q2: -2.5, r: 0.35, F: F(1, -2.5, 0.35) },
  { trial: 2, code: 7, q1: 1e-7, q2: 3, r: 12, F: F(1e-7, 3, 12, core.lawParams(7)) },
  { trial: 3, code: 0, q1: 0, q2: 3, r: 0, F: -0 },
];
const csv = core.buildDelimited(rows, ",");
const tsv = core.buildDelimited(rows, "\t");
check("CSV is plain ASCII", /^[\x09\x0a\x0d\x20-\x7e]*$/.test(csv));
const lines = csv.split("\r\n");
check("CSV header row", lines[0] === "Trial,Law code,q1 (C),q2 (C),r (m),F (N)", lines[0]);
check("CSV has one line per row plus header", lines.length === rows.length + 2 && lines.at(-1) === "");
check("every CSV line has 6 fields", lines.slice(0, -1).every((l) => l.split(",").length === 6));
check("TSV has 6 tab-separated fields per line", tsv.split("\r\n").slice(0, -1).every((l) => l.split("\t").length === 6));
check("F uses toExponential(3)", lines.slice(1, -1).every((l) => /^-?\d\.\d{3}e[+-]\d+$/.test(l.split(",")[5])), lines[1]);
check("row 1 exact text", lines[1] === "1,0,1,-2.5,0.35," + F(1, -2.5, 0.35).toExponential(3), lines[1]);
check("small charge written in scientific notation", lines[2].split(",")[2] === "1e-7", lines[2]);
check("negative zero force is written as 0.000e+0", lines[3].split(",")[5] === "0.000e+0", lines[3]);
check("no spreadsheet formula characters lead any field", lines.every((l) => l.split(",").every((f) => !/^[=@]/.test(f))));

// ---------------------------------------------------------------------------
section("slider and bench grid");
check("grid has 181 values from 0.1 to 10", core.GRID.length === 181 && core.GRID[0] === 0.1 && core.GRID.at(-1) === 10);
check("grid is strictly increasing", core.GRID.every((g, i) => i === 0 || g > core.GRID[i - 1]));
check("grid values have at most 2 significant figures", core.GRID.every((g) => Number(g.toPrecision(2)) === g));
check("grid index 90 is 1", core.GRID[90] === 1 && core.nearestGridIndex(1) === 90);
check("step up from an off-grid value lands on the next grid value", core.stepGrid(0.347, 1) === 0.35);
check("step down from an off-grid value lands on the previous grid value", core.stepGrid(0.347, -1) === 0.34);
check("step clamps at the ends", core.stepGrid(10, 1) === 10 && core.stepGrid(0.1, -1) === 0.1);
check("step from below the ruler enters at 0.1", core.stepGrid(0, 1) === 0.1);

// ---------------------------------------------------------------------------
section("sizing claims (simulated slope SD, 4000 runs each)");
// Claims: SD 0.032 for 5 points over one decade, 0.027 for 8 over one decade, 0.014 for 8 over two.
function slopeSD(points, decades, runs = 4000) {
  const xs = Array.from({ length: points }, (_, i) => (decades * i) / (points - 1));
  const mx = xs.reduce((a, b) => a + b) / points;
  const sxx = xs.reduce((a, x) => a + (x - mx) ** 2, 0);
  const slopes = [];
  for (let run = 0; run < runs; run++) {
    // Vary r with q1 = q2 = 1 C; the fitted slope estimates the r parameter.
    const ys = xs.map((x) => Math.log10(Math.abs(F(1, 1, 10 ** x, P0, core.drawNoise(Math.random)))));
    const my = ys.reduce((a, b) => a + b) / points;
    slopes.push(xs.reduce((a, x, i) => a + (x - mx) * (ys[i] - my), 0) / sxx);
  }
  const m = slopes.reduce((a, b) => a + b) / runs;
  return { mean: m, sd: Math.sqrt(slopes.reduce((a, s) => a + (s - m) ** 2, 0) / (runs - 1)) };
}
for (const [points, decades, claim] of [[5, 1, 0.032], [8, 1, 0.027], [8, 2, 0.014]]) {
  const s = slopeSD(points, decades);
  console.log(`   ${points} points over ${decades} decade(s): slope SD ${s.sd.toFixed(4)} (claim ${claim}), mean slope ${s.mean.toFixed(4)}`);
  check(`${points} points over ${decades} decade(s) slope SD near ${claim}`, Math.abs(s.sd - claim) / claim < 0.12, s.sd);
  check(`${points} points over ${decades} decade(s) fit is unbiased`, Math.abs(s.mean - 2) < 0.005, s.mean);
}

// ---------------------------------------------------------------------------
section("static checks on shipped files");
const EM = String.fromCharCode(0x2014);
for (const name of ["index.html", "INSTRUCTOR-GUIDE.md", "test-law.mjs"]) {
  if (!present(name)) { skip(`${name} has no em dash`, "not in this checkout"); continue; }
  const text = read(name);
  check(`${name} has no em dash`, !text.includes(EM) && (name === "test-law.mjs" || !/&mdash;|&#8212;|&#x2014;/i.test(text)));
}
check("index.html makes no network references", !/https?:\/\//i.test(html) && !/\bfetch\s*\(|XMLHttpRequest|WebSocket|EventSource|sendBeacon|<link[^>]+stylesheet|<script[^>]+src=/i.test(html));
check("index.html persists nothing", !/localStorage|sessionStorage|indexedDB|document\.cookie/i.test(html));
check("index.html has a CSP that blocks network access", /Content-Security-Policy" content="default-src 'none'/.test(html));
check("index.html has noindex", /<meta name="robots" content="noindex">/.test(html));
check("index.html title is Electric Force", /<title>Electric Force<\/title>/.test(html));
check("index.html has no identity fields", !/\b(name|email|student|onid|id number)\b\s*<\/label>/i.test(pageText) && !/type="email"/i.test(pageText));
check("index.html does not describe the law's form", !/(?<!to)exponent|power law|cube|cubic|square|inverse/i.test(pageText));
check("footer attribution present", html.includes("Oregon State University, Department of Physics"));
check("About panel is a native disclosure", /<details class="about[^"]*">\s*<summary>About<\/summary>/.test(html));
check("index.html embeds Open Sans", /@font-face\s*\{[^}]*font-family:\s*"Open Sans"/.test(html) && /font-src data:/.test(html));
const legacyHash = createHash("sha256").update(readFileSync(join(here, "index.legacy.html"))).digest("hex");
check("index.legacy.html is untouched", legacyHash === "e30dfbcfe90aac8b36a156639e7cc4755e616e51f15e57f263e6d9ceda7e8236", legacyHash);

// ---------------------------------------------------------------------------
for (const name of skipped) console.log("SKIP: " + name);
console.log(`\n${passes} passed, ${failures} failed` + (skipped.length ? `, ${skipped.length} skipped` : ""));
process.exit(failures ? 1 : 0);
