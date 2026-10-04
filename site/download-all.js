// Download all (D-0067): one zip of a course's lab files, written in the page.
// The course index lists each format's published files on its checkbox, at
// build time (tools/render.py, course_index_markdown). This script fetches
// the ticked formats' files from this site, relative paths only, and writes
// them into one zip byte for byte: stored, no compression, each with its
// CRC-32, one folder per lab. No library and no request outside the site.
// Entry dates are the time of download. Tested by download-all.test.mjs
// beside it and by tests/test_download_all.py, which reads a zip it writes
// with Python's zipfile.

(() => {
"use strict";

// BEGIN CORE
const CRC_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table[n] = c >>> 0;
  }
  return table;
})();

function crc32(bytes) {
  let c = 0xffffffff;
  for (let i = 0; i < bytes.length; i++) c = CRC_TABLE[(c ^ bytes[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

// A path inside this site: no scheme, no //host. Anything else is refused.
function isRelative(path) {
  return !/^(?:[a-z][a-z0-9+.-]*:|\/\/)/i.test(path);
}

// labs/<id>/<id>.<ext> becomes <id>/<id>.<ext>: the lab's folder, the file's name.
function entryName(path) {
  return path.split("/").filter(Boolean).slice(-2).join("/");
}

// Zip stores MS-DOS local time: seconds in steps of two, years from 1980.
function dosTime(when) {
  return {
    time: (when.getHours() << 11) | (when.getMinutes() << 5) | (when.getSeconds() >> 1),
    date: ((when.getFullYear() - 1980) << 9) | ((when.getMonth() + 1) << 5) | when.getDate(),
  };
}

// A stored zip of [{name, bytes}]: a local header and the bytes for each
// entry, then the central directory, then its end record.
function makeZip(entries, when) {
  const enc = new TextEncoder(), t = dosTime(when), files = [], dir = [];
  let offset = 0;
  for (const { name, bytes } of entries) {
    const n = enc.encode(name), crc = crc32(bytes);
    if (bytes.length >= 0xffffffff || offset >= 0xffffffff) throw new Error("too large for a zip without zip64");
    const head = new DataView(new ArrayBuffer(30)), cd = new DataView(new ArrayBuffer(46));
    head.setUint32(0, 0x04034b50, true); head.setUint16(4, 20, true); head.setUint16(6, 0x0800, true);
    head.setUint16(10, t.time, true); head.setUint16(12, t.date, true); head.setUint32(14, crc, true);
    head.setUint32(18, bytes.length, true); head.setUint32(22, bytes.length, true); head.setUint16(26, n.length, true);
    cd.setUint32(0, 0x02014b50, true); cd.setUint16(4, 20, true); cd.setUint16(6, 20, true); cd.setUint16(8, 0x0800, true);
    cd.setUint16(12, t.time, true); cd.setUint16(14, t.date, true); cd.setUint32(16, crc, true);
    cd.setUint32(20, bytes.length, true); cd.setUint32(24, bytes.length, true); cd.setUint16(28, n.length, true);
    cd.setUint32(42, offset, true);
    files.push(new Uint8Array(head.buffer), n, bytes);
    dir.push(new Uint8Array(cd.buffer), n);
    offset += 30 + n.length + bytes.length;
  }
  if (entries.length > 0xffff) throw new Error("too many entries for a zip without zip64");
  const size = dir.reduce((sum, part) => sum + part.length, 0), end = new DataView(new ArrayBuffer(22));
  end.setUint32(0, 0x06054b50, true); end.setUint16(8, entries.length, true); end.setUint16(10, entries.length, true);
  end.setUint32(12, size, true); end.setUint32(16, offset, true);
  const parts = files.concat(dir, [new Uint8Array(end.buffer)]);
  const out = new Uint8Array(parts.reduce((sum, part) => sum + part.length, 0));
  let at = 0;
  for (const part of parts) { out.set(part, at); at += part.length; }
  return out;
}

// The zip of every path, fetched in order; null when there is no path, so
// no box ticked fetches nothing and writes nothing.
async function buildZip(paths, fetchBytes, when) {
  if (!paths.length) return null;
  const entries = [];
  for (const path of paths) {
    if (!isRelative(path)) throw new Error("not a path in this site: " + path);
    entries.push({ name: entryName(path), bytes: await fetchBytes(path) });
  }
  return makeZip(entries, when);
}
// END CORE

function save(bytes, name) {
  const url = URL.createObjectURL(new Blob([bytes], { type: "application/zip" }));
  const link = Object.assign(document.createElement("a"), { href: url, download: name });
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 60000);
}

async function fetchBytes(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(path + " answered " + response.status);
  return new Uint8Array(await response.arrayBuffer());
}

// The quiet button just before each dialog opens it as a modal; the button
// is hidden in the page as built and shown only here, so a browser without
// the script or without <dialog> shows no control that does nothing.
for (const dialog of document.querySelectorAll("dialog.download-all")) {
  const opener = dialog.previousElementSibling;
  if (!opener || !opener.matches("button.download-all-open") || typeof dialog.showModal !== "function") continue;
  const boxes = Array.from(dialog.querySelectorAll('input[type="checkbox"]'));
  const button = dialog.querySelector("button.download-selected");
  const sync = () => { button.disabled = !boxes.some((box) => box.checked); };
  // Every format is opt-in: none is ticked each time the dialog opens.
  opener.addEventListener("click", () => {
    boxes.forEach((box) => { box.checked = false; });
    sync();
    dialog.showModal();
  });
  // Escape closes a modal dialog natively; a tap outside its box closes it too.
  dialog.addEventListener("click", (event) => {
    const r = dialog.getBoundingClientRect();
    const inside = event.clientX >= r.left && event.clientX <= r.right
      && event.clientY >= r.top && event.clientY <= r.bottom;
    if (event.target === dialog && !inside) dialog.close();
  });
  boxes.forEach((box) => box.addEventListener("change", sync));
  button.addEventListener("click", async () => {
    const paths = boxes.filter((box) => box.checked)
      .flatMap((box) => box.dataset.files.split(" ").filter(Boolean));
    button.disabled = true;
    try {
      const zip = await buildZip(paths, fetchBytes, new Date());
      if (zip) { save(zip, dialog.dataset.zip); dialog.close(); }
    } catch (err) {
      console.error("Download all:", err);
    } finally {
      sync();
    }
  });
  opener.hidden = false;
}
})();
