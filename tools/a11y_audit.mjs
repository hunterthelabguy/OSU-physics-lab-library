// Accessibility audit of a built site, in headless Chrome, no dependencies.
//
//   node tools/a11y_audit.mjs <site folder> [--page <relative path>]...
//
// Serves the folder on a local port, opens every HTML page (redirect stubs
// skipped) in light and dark, at 1280 px and at 320 px (WCAG 1.4.10's
// reflow width: 1280 px at 400 %), runs the checks below in the page, and
// prints one JSON object: {pages: [...], findings: [...]}. Each finding is
// {rule, wcag, page, theme, width, target, detail}; `target` is a CSS path
// of tag and class names only (no generated ids), so a key built from it is
// stable across builds. The audit never fails on a finding: the ratchet in
// tests/test_a11y.py decides. It fails only when it cannot run.
//
// Chrome is CHROME (default google-chrome, as tools/downloads.py), driven
// over the DevTools protocol with Node's own WebSocket (Node 22 or later).
//
// What it measures, and what it does not, is in the AUDIT function's
// comments; the rule list is RULES.

import {spawn} from "node:child_process";
import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import {fileURLToPath, pathToFileURL} from "node:url";

export const RULES = {
  "contrast": "1.4.3",            // text against what is painted behind it
  "contrast-unmeasured": "1.4.3", // behind it is an image or an unknown colour
  "html-lang": "3.1.1",
  "page-title": "2.4.2",
  "one-h1": "1.3.1",              // exactly one visible h1 (the runbook's rule)
  "heading-skip": "1.3.1",        // rendered headings, chrome included
  "main-landmark": "2.4.1",       // exactly one main
  "img-alt": "1.1.1",             // img with no alt attribute; role=img with no name
  "name": "4.1.2",                // link, button, control, summary, iframe with no name
  "aria-ref": "1.3.1",            // an id reference that names nothing, or two things
  "table-headers": "1.3.1",       // a data table with no header cell
  "zoom-blocked": "1.4.4",
  "reflow": "1.4.10",             // sideways scroll at 320 px
  "target-size": "2.5.8",         // under 24 px with no 24 px spacing
  "focus-visible": "2.4.7",       // focus changes nothing drawn
  "text-spacing": "1.4.12",       // WCAG's spacing clips text
};

const MIME = {".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript",
  ".mjs": "text/javascript", ".json": "application/json", ".svg": "image/svg+xml",
  ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
  ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf", ".ico": "image/x-icon",
  ".pdf": "application/pdf", ".txt": "text/plain"};

export function serve(root) {
  const server = http.createServer((req, res) => {
    let rel = decodeURIComponent(new URL(req.url, "http://x").pathname);
    let file = path.join(root, rel);
    if (!path.resolve(file).startsWith(path.resolve(root))) { res.writeHead(403); return res.end(); }
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, "index.html");
    if (!fs.existsSync(file)) { res.writeHead(404); return res.end("not found"); }
    res.writeHead(200, {"content-type": MIME[path.extname(file).toLowerCase()] || "application/octet-stream"});
    fs.createReadStream(file).pipe(res);
  });
  return new Promise(done => server.listen(0, "127.0.0.1", () => done(server)));
}

export function pages(root) {
  const out = [];
  const walk = dir => {
    for (const e of fs.readdirSync(dir, {withFileTypes: true})) {
      const p = path.join(dir, e.name);
      if (e.isDirectory()) walk(p);
      else if (e.name.endsWith(".html")) {
        const head = fs.readFileSync(p, "utf8").slice(0, 2000);
        if (/http-equiv=["']?refresh/i.test(head)) continue;   // redirect stub
        out.push(path.relative(root, p).split(path.sep).join("/"));
      }
    }
  };
  walk(root);
  return out.sort();
}

class Cdp {
  constructor(url) {
    this.ws = new WebSocket(url);
    this.seq = 0; this.pending = new Map(); this.listeners = new Set();
    this.ws.onmessage = e => {
      const m = JSON.parse(e.data);
      if (m.id && this.pending.has(m.id)) {
        const {ok, fail} = this.pending.get(m.id); this.pending.delete(m.id);
        m.error ? fail(new Error(m.error.message)) : ok(m.result);
      } else for (const l of this.listeners) l(m);
    };
  }
  open() { return new Promise((ok, fail) => { this.ws.onopen = ok; this.ws.onerror = fail; }); }
  send(method, params = {}, sessionId) {
    const id = ++this.seq;
    this.ws.send(JSON.stringify({id, method, params, sessionId}));
    return new Promise((ok, fail) => this.pending.set(id, {ok, fail}));
  }
  event(method, sessionId, ms = 60000) {
    return new Promise((ok, fail) => {
      const t = setTimeout(() => { this.listeners.delete(l); fail(new Error("timeout waiting for " + method)); }, ms);
      const l = m => { if (m.method === method && m.sessionId === sessionId) { clearTimeout(t); this.listeners.delete(l); ok(m.params); } };
      this.listeners.add(l);
    });
  }
}

export async function launch(profile) {
  const chrome = process.env.CHROME || "google-chrome";
  fs.mkdirSync(profile, {recursive: true});
  const proc = spawn(chrome, ["--headless", "--disable-gpu", "--no-first-run",
    "--no-default-browser-check", "--remote-debugging-port=0",
    "--user-data-dir=" + profile, "about:blank"], {stdio: ["ignore", "ignore", "pipe"]});
  const url = await new Promise((ok, fail) => {
    let err = "";
    const t = setTimeout(() => fail(new Error("Chrome did not start: " + err)), 30000);
    proc.on("error", e => { clearTimeout(t); fail(new Error(`cannot run CHROME (${chrome}): ${e.message}`)); });
    proc.stderr.on("data", d => {
      err += d;
      const m = err.match(/DevTools listening on (ws:\/\/\S+)/);
      if (m) { clearTimeout(t); ok(m[1]); }
    });
  });
  const cdp = new Cdp(url);
  await cdp.open();
  return {cdp, close: () => { try { cdp.ws.close(); } catch {} proc.kill(); }};
}

// ---------------------------------------------------------------------------
// The checks, run inside the page. Kept to what a script can see; each
// comment says what a rule leaves out.
async function AUDIT(width) {
  await document.fonts.ready;
  const found = [];
  const vis = el => el.checkVisibility({checkOpacity: true, checkVisibilityCSS: true});
  const sel = el => {
    const parts = [];
    for (let e = el; e && e.nodeType === 1 && e !== document.documentElement; e = e.parentElement) {
      let s = e.localName;
      const cls = [...e.classList].filter(c => !/^(cell|quarto-|sourceCode$|js-)/.test(c)).slice(0, 2);
      if (cls.length) s += "." + cls.join(".");
      parts.unshift(s);
      if (/^(main|header|footer|nav|dialog|aside)$/.test(e.localName)) break;
    }
    return parts.slice(-6).join(" > ");
  };
  const add = (rule, el, detail) => found.push({rule, target: el ? sel(el) : "document", detail});

  // Colour. Chrome reports rgb(), rgba() or color(srgb ...); anything else
  // (oklch, a system colour) is reported unmeasured rather than guessed.
  const parse = c => {
    let m = c.match(/^rgba?\(([^)]+)\)$/);
    if (m) { const v = m[1].split(/[\s,/]+/).filter(Boolean).map(Number); return [v[0], v[1], v[2], v.length > 3 ? v[3] : 1]; }
    m = c.match(/^color\(srgb ([^)]+)\)$/);
    if (m) { const v = m[1].split(/[\s/]+/).filter(Boolean).map(Number); return [v[0] * 255, v[1] * 255, v[2] * 255, v.length > 3 ? v[3] : 1]; }
    return null;
  };
  const over = (t, b) => {
    const a = t[3] + b[3] * (1 - t[3]);
    if (a === 0) return [0, 0, 0, 0];
    return [0, 1, 2].map(i => (t[i] * t[3] + b[i] * b[3] * (1 - t[3])) / a).concat(a);
  };
  const lum = c => {
    const [r, g, b] = c.slice(0, 3).map(v => { v /= 255; return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
  const hex = c => "#" + c.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, "0")).join("");
  const dark = matchMedia("(prefers-color-scheme: dark)").matches
    && /dark/.test(getComputedStyle(document.documentElement).colorScheme);
  // The canvas: html's background, else body's (CSS propagates it to the
  // whole canvas, past the body's box), else Chrome's own.
  const opaque = el => { const c = el && parse(getComputedStyle(el).backgroundColor); return c && c[3] >= 1 ? c : null; };
  const canvas = opaque(document.documentElement) || opaque(document.body) || (dark ? [18, 18, 18, 1] : [255, 255, 255, 1]);

  // What is painted behind a point: every element there in paint order,
  // from the text's own element down, composited over the canvas. Misses
  // pseudo-element backgrounds and anything with pointer-events: none.
  const behind = (el, x, y) => {
    const stack = document.elementsFromPoint(x, y);
    let i = -1;
    for (let a = el; a && i < 0; a = a.parentElement) i = stack.indexOf(a);
    if (i < 0) return {why: `not hit at its own point (${Math.round(x)},${Math.round(y)} in ${innerWidth}x${innerHeight}; top ${stack[0] ? sel(stack[0]) : "none"})`};
    const layers = [];
    for (let k = i; k < stack.length; k++) {
      const cs = getComputedStyle(stack[k]);
      const c = parse(cs.backgroundColor);
      if (!c) return {why: "background " + cs.backgroundColor};
      if (c[3] > 0) layers.push(c);
      if (c[3] >= 1) break;
      if (cs.backgroundImage !== "none") return {why: "background image on " + sel(stack[k])};
    }
    let base = canvas;
    for (const l of layers.reverse()) base = over(l, base);
    return {color: base};
  };
  const hiddenBox = el => {   // visually-hidden text: a 1 px clipped box
    for (let a = el, n = 0; a && n < 5; a = a.parentElement, n++) {
      const r = a.getBoundingClientRect(), cs = getComputedStyle(a);
      if ((r.width <= 2 || r.height <= 2) && (cs.overflow !== "visible" || cs.clip !== "auto" || cs.clipPath !== "none")) return true;
    }
    return false;
  };

  // 1.4.3 Contrast, every element with its own visible text. Large text is
  // 24 px, or 18.66 px at weight 700. SVG text is the figures' (tested on
  // their white paper in tests/test_brand.py) and is left out.
  const seen = new Set();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let t = walker.nextNode(); t; t = walker.nextNode()) {
    const el = t.parentElement;
    if (!el || seen.has(el) || !t.textContent.trim()) continue;
    if (el.closest("svg, script, style, noscript, template, option")) continue;
    seen.add(el);
    if (!vis(el) || hiddenBox(el)) continue;
    const range = document.createRange(); range.selectNodeContents(t);
    let rect = [...range.getClientRects()].find(r => r.width > 1 && r.height > 1);
    if (!rect) continue;
    if (rect.top < 0 || rect.bottom > innerHeight || rect.left < 0 || rect.right > innerWidth) {
      el.scrollIntoView({block: "center", inline: "start"});
      rect = [...range.getClientRects()].find(r => r.width > 1 && r.height > 1);
      if (!rect) continue;
    }
    const cs = getComputedStyle(el);
    let fg = parse(cs.color);
    const bg = behind(el, Math.min(Math.max(rect.left, 0) + Math.min(rect.width, 8) / 2, innerWidth - 1), rect.top + rect.height / 2);
    if (!fg || !bg.color) { add("contrast-unmeasured", el, fg ? bg.why : "colour " + cs.color); continue; }
    let op = 1;
    for (let a = el; a; a = a.parentElement) op *= Number(getComputedStyle(a).opacity);
    fg = over([fg[0], fg[1], fg[2], fg[3] * op], bg.color);
    const size = parseFloat(cs.fontSize), weight = parseInt(cs.fontWeight, 10);
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const r = ratio(fg, bg.color), need = large ? 3 : 4.5;
    if (r < need) add("contrast", el, `${r.toFixed(2)}:1 < ${need}:1, ${hex(fg)} on ${hex(bg.color)}, ${size}px/${weight}`);
  }
  scrollTo(0, 0);

  // Document.
  if (!(document.documentElement.getAttribute("lang") || "").trim()) add("html-lang", null, "no lang on html");
  if (!document.title.trim()) add("page-title", null, "empty title");
  const vp = document.querySelector('meta[name="viewport"]')?.content || "";
  if (/user-scalable\s*=\s*(no|0)/i.test(vp) || (+(vp.match(/maximum-scale\s*=\s*([\d.]+)/i) || [])[1] < 2))
    add("zoom-blocked", null, vp);
  const mains = [...document.querySelectorAll("main, [role=main]")].filter(vis);
  if (mains.length !== 1) add("main-landmark", null, `${mains.length} main landmarks`);

  // Headings as rendered, the site's chrome included.
  const heads = [...document.querySelectorAll("h1, h2, h3, h4, h5, h6, [role=heading]")].filter(vis);
  const level = h => h.getAttribute("role") === "heading" ? +(h.getAttribute("aria-level") || 2) : +h.localName[1];
  const h1s = heads.filter(h => level(h) === 1);
  if (h1s.length !== 1) add("one-h1", h1s[1] || null, `${h1s.length} visible h1`);
  heads.forEach((h, i) => {
    if (i && level(h) > level(heads[i - 1]) + 1) add("heading-skip", h, `h${level(heads[i - 1])} then h${level(h)}`);
  });

  // Accessible names, by the parts of the naming algorithm a page here can
  // use: aria-labelledby, aria-label, label, contents (img alt, svg title),
  // value for input buttons, then title.
  const byId = id => document.getElementById(id);
  const textName = el => {
    let s = "";
    for (const n of el.childNodes) {
      if (n.nodeType === 3) s += n.textContent;
      else if (n.nodeType === 1 && n.getAttribute("aria-hidden") !== "true" && getComputedStyle(n).display !== "none") {
        if (n.localName === "img") s += n.getAttribute("alt") || "";
        else if (n.localName === "svg") s += n.getAttribute("aria-label") || n.querySelector("title")?.textContent || "";
        else s += " " + (n.getAttribute("aria-label") || textName(n)) + " ";
      }
    }
    return s.replace(/\s+/g, " ").trim();
  };
  const accName = el => {
    const lb = el.getAttribute("aria-labelledby");
    if (lb) { const t = lb.split(/\s+/).map(id => byId(id)?.textContent || "").join(" ").trim(); if (t) return t; }
    const al = (el.getAttribute("aria-label") || "").trim();
    if (al) return al;
    if (/^(input|select|textarea)$/.test(el.localName)) {
      if (el.id) { const l = document.querySelector(`label[for="${CSS.escape(el.id)}"]`); if (l && textName(l)) return textName(l); }
      const wrap = el.closest("label");
      if (wrap && textName(wrap)) return textName(wrap);
      if (/^(submit|button|reset)$/.test(el.type) && el.value) return el.value;
      if (el.placeholder) return el.placeholder;
    } else if (el.localName !== "iframe") {
      const t = textName(el); if (t) return t;
    }
    return (el.getAttribute("title") || "").trim();
  };
  const CONTROLS = 'a[href], button, input:not([type=hidden]), select, textarea, summary, iframe, [role=button], [role=link], [role=tab], [role=checkbox], [role=switch], [role=menuitem]';
  const controls = [...document.querySelectorAll(CONTROLS)].filter(vis);
  for (const el of controls) if (!accName(el)) add("name", el, `${el.localName} has no accessible name`);

  for (const img of document.querySelectorAll("img")) if (!img.hasAttribute("alt") && vis(img)) add("img-alt", img, img.getAttribute("src") || "");
  for (const el of document.querySelectorAll("[role=img]")) if (vis(el) && !accName(el)) add("img-alt", el, "role=img with no name");

  // Id references.
  const counts = {};
  for (const e of document.querySelectorAll("[id]")) counts[e.id] = (counts[e.id] || 0) + 1;
  for (const attr of ["aria-labelledby", "aria-describedby", "aria-controls", "aria-owns", "for"]) {
    for (const el of document.querySelectorAll(`[${attr}]`)) {
      for (const id of el.getAttribute(attr).split(/\s+/).filter(Boolean)) {
        if (!counts[id]) add("aria-ref", el, `${attr}="${id}" names nothing`);
        else if (counts[id] > 1) add("aria-ref", el, `${attr}="${id}" names ${counts[id]} elements`);
      }
    }
  }

  // Data tables need a header cell; role=presentation or none marks layout.
  for (const t of document.querySelectorAll("table")) {
    if (!vis(t) || /^(presentation|none)$/.test(t.getAttribute("role") || "")) continue;
    if (t.rows.length > 1 && !t.querySelector("th, [role=columnheader], [role=rowheader]")) add("table-headers", t, `${t.rows.length} rows, no th`);
  }

  // 1.4.10 at 320 px: the page itself never scrolls sideways. A box that
  // scrolls on its own (a wide table, D-0130's rule) is allowed.
  if (width <= 320) {
    const root = document.documentElement;
    if (root.scrollWidth > root.clientWidth + 1) {
      const wide = [...document.body.querySelectorAll("*")].filter(e => {
        const r = e.getBoundingClientRect();
        if (r.right <= root.clientWidth + 1 || !vis(e)) return false;
        for (let a = e.parentElement; a && a !== document.body; a = a.parentElement) {
          if (/(auto|scroll|hidden|clip)/.test(getComputedStyle(a).overflowX)) return false;
          if (a.getBoundingClientRect().right > root.clientWidth + 1) return false;   // report the outermost
        }
        return true;
      });
      if (!wide.length) add("reflow", null, `page ${root.scrollWidth}px wide at ${root.clientWidth}px`);
      for (const e of wide) add("reflow", e, `right edge ${Math.round(e.getBoundingClientRect().right)}px at ${root.clientWidth}px`);
    }
  }

  // 2.5.8 Target size (minimum): 24 by 24 CSS px, or a 24 px circle on its
  // centre that touches no other target. A link inside a line of text is
  // exempt; a checkbox's target includes its label.
  const targets = controls.filter(el => el.localName !== "iframe").map(el => {
    let r = el.getBoundingClientRect();
    const lab = el.labels?.[0] || null;
    if (lab && vis(lab)) {
      const l = lab.getBoundingClientRect();
      r = {left: Math.min(r.left, l.left), top: Math.min(r.top, l.top), right: Math.max(r.right, l.right), bottom: Math.max(r.bottom, l.bottom)};
    }
    const inline = el.localName === "a" && getComputedStyle(el).display === "inline"
      && [...el.parentElement.childNodes].some(n => n !== el && n.nodeType === 3 && n.textContent.trim());
    return {el, r: {left: r.left, top: r.top, right: r.right, bottom: r.bottom}, inline};
  }).filter(t => t.r.right - t.r.left > 0 && t.r.bottom - t.r.top > 0 && !hiddenBox(t.el));   // a skip link until focused
  const hitsRect = (cx, cy, rad, r) => {
    const dx = Math.max(r.left - cx, 0, cx - r.right), dy = Math.max(r.top - cy, 0, cy - r.bottom);
    return dx * dx + dy * dy < rad * rad;
  };
  for (const t of targets) {
    const w = t.r.right - t.r.left, h = t.r.bottom - t.r.top;
    if (t.inline || (w >= 24 && h >= 24)) continue;
    const cx = (t.r.left + t.r.right) / 2, cy = (t.r.top + t.r.bottom) / 2;
    const clash = targets.find(o => o !== t && !o.el.contains(t.el) && !t.el.contains(o.el) && (
      hitsRect(cx, cy, 12, o.r) ||
      ((o.r.right - o.r.left < 24 || o.r.bottom - o.r.top < 24) && !o.inline &&
        Math.hypot(cx - (o.r.left + o.r.right) / 2, cy - (o.r.top + o.r.bottom) / 2) < 24)));
    if (clash) add("target-size", t.el, `${Math.round(w)}x${Math.round(h)}px, within 12px of ${sel(clash.el)}`);
  }

  // 2.4.7 Focus visible: focus each control as a keyboard would and compare
  // what is drawn. Reads the element's own outline, box shadow, border,
  // background, colour and underline; a ring drawn by an ancestor or a
  // pseudo-element is missed and would be a false finding.
  const look = el => { const c = getComputedStyle(el);
    return [c.outlineStyle !== "none" && parseFloat(c.outlineWidth) > 0 ? c.outlineStyle + c.outlineWidth + c.outlineColor : "",
      c.boxShadow, c.borderColor, c.backgroundColor, c.color, c.textDecorationLine].join("|"); };
  for (const el of controls.slice(0, 400)) {
    if (el.localName === "iframe" || el.disabled) continue;
    const before = look(el);
    el.focus({preventScroll: true, focusVisible: true});
    if (document.activeElement !== el) continue;
    const after = look(el);
    el.blur();
    if (before === after) add("focus-visible", el, "focus changes nothing drawn on the element");
  }

  // 1.4.12 Text spacing: WCAG's four values, then any box that clips text
  // it did not clip before. A box that grows, or scrolls, passes.
  const clipped = () => new Set([...document.body.querySelectorAll("*")].filter(e => {
    const c = getComputedStyle(e);
    if (!/(hidden|clip)/.test(c.overflowX + c.overflowY) || !vis(e) || !e.textContent.trim()) return false;
    return e.scrollHeight > e.clientHeight + 2 || e.scrollWidth > e.clientWidth + 2;
  }));
  const was = clipped();
  const st = document.createElement("style");
  st.textContent = "* { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important; } p { margin-bottom: 2em !important; }";
  document.head.appendChild(st);
  for (const e of clipped()) if (!was.has(e) && !hiddenBox(e)) add("text-spacing", e, `clips at ${e.clientWidth}x${e.clientHeight}px`);
  st.remove();

  return found;
}

export async function auditPages(root, list, {themes = ["light", "dark"], widths = [1280, 320]} = {}) {
  const server = await serve(root);
  const base = `http://127.0.0.1:${server.address().port}/`;
  // The profile lives in the repo's gitignored build/, whatever folder is audited.
  const {cdp, close} = await launch(fileURLToPath(new URL("../build/a11y-chrome-profile", import.meta.url)));
  const findings = [];
  try {
    const {targetId} = await cdp.send("Target.createTarget", {url: "about:blank"});
    const {sessionId} = await cdp.send("Target.attachToTarget", {targetId, flatten: true});
    await cdp.send("Page.enable", {}, sessionId);
    const src = `(${AUDIT.toString()})`;
    for (const page of list) {
      for (const width of widths) {
        await cdp.send("Emulation.setDeviceMetricsOverride", {width, height: 900, deviceScaleFactor: 1, mobile: width < 600}, sessionId);
        for (const theme of themes) {
          await cdp.send("Emulation.setEmulatedMedia", {features: [{name: "prefers-color-scheme", value: theme}]}, sessionId);
          const loaded = cdp.event("Page.loadEventFired", sessionId);
          await cdp.send("Page.navigate", {url: base + page}, sessionId);
          await loaded;
          const r = await cdp.send("Runtime.evaluate", {expression: `${src}(${width})`, awaitPromise: true, returnByValue: true}, sessionId);
          if (r.exceptionDetails) throw new Error(`${page} ${theme} ${width}: ${r.exceptionDetails.exception?.description || r.exceptionDetails.text}`);
          for (const f of r.result.value) findings.push({rule: f.rule, wcag: RULES[f.rule], page, theme, width, target: f.target, detail: f.detail});
        }
      }
    }
  } finally {
    close();
    server.close();
  }
  return findings;
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const args = process.argv.slice(2);
  const root = args[0];
  if (!root || !fs.existsSync(root)) { console.error("usage: node tools/a11y_audit.mjs <site folder> [--page <path>]..."); process.exit(2); }
  const only = args.flatMap((a, i) => a === "--page" ? [args[i + 1]] : []);
  const list = only.length ? only : pages(root);
  const findings = await auditPages(root, list);
  process.stdout.write(JSON.stringify({pages: list, findings}, null, 1) + "\n");
}
