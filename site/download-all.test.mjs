// download-all.test.mjs: checks for the Download all zip writer (D-0067).
// No dependencies. Run from this folder: node download-all.test.mjs
// Loads the CORE block out of download-all.js (the same code the page runs),
// as the sims' tests do, and reads every zip it writes back by hand. Python's
// zipfile reads one too, in tests/test_download_all.py.

import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = readFileSync(join(here, "download-all.js"), "utf8");
const block = source.match(/\/\/ BEGIN CORE\n([\s\S]*?)\/\/ END CORE/);
if (!block) {
  console.error("FAIL: no CORE block found in download-all.js");
  process.exit(1);
}
const core = new Function(block[1] + "\nreturn { crc32, isRelative, entryName, dosTime, makeZip, buildZip };")();

let failures = 0, passes = 0;
function check(name, ok, detail = "") {
  if (ok) { passes++; return; }
  failures++;
  console.log("FAIL: " + name + (detail ? "  (" + detail + ")" : ""));
}
const bytes = (text) => new TextEncoder().encode(text);
const same = (a, b) => a.length === b.length && a.every((x, i) => x === b[i]);

// Read a zip back from its end record: [{name, method, crc, bytes, flags}].
function readZip(zip) {
  const view = new DataView(zip.buffer, zip.byteOffset, zip.byteLength);
  const end = zip.length - 22;
  if (view.getUint32(end, true) !== 0x06054b50) throw new Error("no end record");
  const count = view.getUint16(end + 10, true);
  let at = view.getUint32(end + 16, true);
  const out = [];
  for (let i = 0; i < count; i++) {
    if (view.getUint32(at, true) !== 0x02014b50) throw new Error("bad central header " + i);
    const size = view.getUint32(at + 20, true), nameLength = view.getUint16(at + 28, true);
    const local = view.getUint32(at + 42, true);
    const name = new TextDecoder().decode(zip.subarray(at + 46, at + 46 + nameLength));
    if (view.getUint32(local, true) !== 0x04034b50) throw new Error("bad local header " + name);
    const start = local + 30 + view.getUint16(local + 26, true) + view.getUint16(local + 28, true);
    out.push({ name, method: view.getUint16(at + 10, true), crc: view.getUint32(at + 16, true),
      localCrc: view.getUint32(local + 14, true), flags: view.getUint16(at + 8, true),
      bytes: zip.subarray(start, start + size) });
    at += 46 + nameLength;
  }
  return out;
}

console.log("-- CRC-32");
check("crc32 of the check string is cbf43926", core.crc32(bytes("123456789")) === 0xcbf43926,
  core.crc32(bytes("123456789")).toString(16));
check("crc32 of nothing is 0", core.crc32(new Uint8Array(0)) === 0);
check("crc32 of one zero byte is d202ef8d", core.crc32(new Uint8Array([0])) === 0xd202ef8d);

console.log("-- paths and names");
check("entry name is the lab's folder and the file", core.entryName("../labs/ph211-x/ph211-x.docx") === "ph211-x/ph211-x.docx");
check("the same from a course page two folders down", core.entryName("../../labs/ph211-x/ph211-x.pdf") === "ph211-x/ph211-x.pdf");
check("a lab's picture stays in its media folder", core.entryName("../../labs/ph211-x/ph211-x-media/a.png") === "ph211-x/ph211-x-media/a.png");
check("a relative path is in the site", core.isRelative("../labs/a/a.pdf"));
for (const outside of ["https://example.org/a.pdf", "http://x/a", "//cdn.example/a.js", "data:text/plain,a", "HTTPS://X/A"]) {
  check("refused: " + outside, !core.isRelative(outside));
}

console.log("-- MS-DOS time");
const when = new Date(2026, 9, 2, 14, 30, 59);
const t = core.dosTime(when);
check("dos date 2026-10-02", t.date === ((46 << 9) | (10 << 5) | 2), t.date);
check("dos time 14:30:58", t.time === ((14 << 11) | (30 << 5) | 29), t.time);

console.log("-- a zip holds exactly the given files, byte for byte");
const binary = new Uint8Array(70000).map((_, i) => (i * 7 + 3) & 0xff);
const given = [
  { name: "lab-a/lab-a.md", bytes: bytes("# Lab A\n") },
  { name: "lab-a/lab-a.pdf", bytes: binary },
  { name: "lab-b/lab-b.md", bytes: new Uint8Array(0) },
];
const back = readZip(core.makeZip(given, when));
check("entry count", back.length === given.length, back.length);
given.forEach((g, i) => {
  const b = back[i] || {};
  check(g.name + ": name", b.name === g.name, b.name);
  check(g.name + ": stored", b.method === 0, b.method);
  check(g.name + ": bytes", b.bytes && same(b.bytes, g.bytes));
  check(g.name + ": CRC-32 in both headers", b.crc === core.crc32(g.bytes) && b.localCrc === b.crc);
  check(g.name + ": UTF-8 name flag", b.flags === 0x0800, b.flags);
});
check("one folder per lab", new Set(back.map((b) => b.name.split("/")[0])).size === 2);
const empty = core.makeZip([], when);
check("an empty zip is its end record alone", empty.length === 22 && readZip(empty).length === 0);

console.log("-- building from paths");
const site = { "../labs/a/a.md": bytes("A"), "../labs/b/b.md": bytes("BB") };
const fetched = [];
const fakeFetch = async (path) => { fetched.push(path); return site[path]; };
const none = await core.buildZip([], fakeFetch, when);
check("no box ticked writes nothing", none === null);
check("no box ticked fetches nothing", fetched.length === 0, fetched.join(" "));
const built = readZip(await core.buildZip(Object.keys(site), fakeFetch, when));
check("each path fetched once, in order", fetched.join(" ") === Object.keys(site).join(" "), fetched.join(" "));
check("each path under its lab's folder", built.map((b) => b.name).join(" ") === "a/a.md b/b.md");
let refused = false;
try { await core.buildZip(["https://example.org/x.pdf"], fakeFetch, when); } catch (e) { refused = true; }
check("a path outside the site is refused before any fetch", refused && fetched.length === 2);

console.log("-- the file itself");
check("no URL with a scheme", !/[a-z][a-z0-9+.-]*:\/\//i.test(source));
check("no protocol-relative string", !/["'`]\/\//.test(source));
check("no import or require", !/\bimport\s*\(|\brequire\s*\(|^\s*import\s/m.test(source));

console.log(passes + " passed, " + failures + " failed");
process.exit(failures ? 1 : 0);
