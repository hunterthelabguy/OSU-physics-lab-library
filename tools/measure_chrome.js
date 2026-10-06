// Manual layout check of the built site. CI does not run it.
// Serve build/ from one origin, on a port not used before in the session
// (the pane caches per origin):
//   python -m http.server <port> --directory <absolute path to build>
// Open http://127.0.0.1:<port>/quarto-site/ in the browser pane and run this
// file's text with the pane's JavaScript tool. It loads every page in
// same-origin iframes at fixed sizes and returns JSON:
//   scroll375    each page's scrollWidth and clientWidth at 375 px (no
//                sideways scroll when scrollWidth <= clientWidth)
//   banner1440   draft banner height, closed and open, at 1440 px
//   landing1440  the landing prose column's left and right gaps at 1440 px
//   contrast     WCAG ratios of the chrome text on its background
//   sim          the sim bar and page height at 1280x720
//   courses      the course index and course pages at 375, 1440 and 1920 px
//                (D-0069, D-0070): boxes of main, the h1, the intro, the
//                tiles, the tabs, the lab table and its columns, the
//                collapse, Download all and the footnote; the most lines any
//                description wraps to, with the collapse open; the header's
//                left edge beside a lab page's
// The old-build comparison it began with went with the old build (D-0061).
await (async () => {
  const LAB = "labs/ph211-team-building-handout/";
  const COURSES = ["courses/index.html", "courses/ph211/index.html",
    "courses/ph212/index.html", "courses/ph213/index.html"];
  const PAGES = ["index.html", "how-this-was-made/index.html", "sims/index.html",
    LAB + "modern/index.html", LAB + "faithful/index.html"].concat(COURSES);
  const SIM = "sims/modified-electric-force/index.html";
  const frame = (src, w, h) => new Promise(done => {
    const f = document.createElement("iframe");
    f.style.cssText = `position:absolute;left:-20000px;top:0;border:0;width:${w}px;height:${h}px`;
    f.onload = async () => { await f.contentDocument.fonts.ready; done(f); };
    f.src = src + "?m=" + Date.now();
    document.body.appendChild(f);
  });
  const css = el => el.ownerDocument.defaultView.getComputedStyle(el);
  const box = el => {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return {left: Math.round(r.left), width: Math.round(r.width), height: Math.round(r.height)};
  };
  // Line boxes of an element's text, counted by their tops (a cell's box
  // would count its padding too).
  const lines = el => {
    const r = el.ownerDocument.createRange();
    r.selectNodeContents(el);
    return new Set([...r.getClientRects()].map(x => Math.round(x.top))).size;
  };
  const lum = c => {
    const [r, g, b] = c.match(/[\d.]+/g).slice(0, 3).map(Number).map(v => {
      v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  const back = el => {
    for (; el; el = el.parentElement) {
      const c = css(el).backgroundColor;
      if (!/^rgba\(.*,\s*0\)$|^transparent$/.test(c)) return c;
    }
    return "rgb(255, 255, 255)";
  };
  const ratio = el => {
    if (!el) return null;
    const [a, b] = [lum(css(el).color), lum(back(el))].sort((x, y) => y - x);
    return Math.round((a + 0.05) / (b + 0.05) * 100) / 100;
  };
  const course = q => {
    const pending = q.querySelector(".lab-pending");
    if (pending) pending.open = true;
    const table = q.querySelector("main > .lab-table");
    const descs = [...q.querySelectorAll(".lab-table td.lab-desc")];
    const out = {
      main: box(q.querySelector("main")),
      h1: box(q.querySelector("main h1")),
      intro: box(q.querySelector("main > h1 + p")),
      tiles: [...q.querySelectorAll(".course-tile")].map(box),
      tabs: [...q.querySelectorAll(".course-tabs a")].map(box),
      table: box(table),
      columns: table && [...table.querySelectorAll("th")].map(th => [th.textContent, Math.round(th.getBoundingClientRect().width)]),
      rows: [...q.querySelectorAll("main > .lab-table tbody tr")].map(box),
      titleCells: [...q.querySelectorAll(".lab-table td.lab-title")].map(td => Math.round(td.getBoundingClientRect().width)),
      descMaxLines: descs.length ? Math.max(...descs.map(lines)) : null,
      descLongest: descs.length ? (d => ({chars: d.textContent.length, lines: lines(d)}))(
        descs.reduce((a, b) => b.textContent.length > a.textContent.length ? b : a)) : null,
      pendingSummary: pending && box(pending.querySelector("summary")),
      downloadAll: box(q.querySelector(".download-all-open")),
      footnote: box(q.querySelector("main > p.course-note:last-of-type")),
      header: box(q.querySelector(".osu-banner .osu-inner")),
    };
    if (pending) pending.open = false;
    return out;
  };
  const out = {scroll375: {}, banner1440: {}, landing1440: null, contrast: {}, sim: null, courses: {}};
  for (const page of PAGES) {
    for (const [w, h] of [[1920, 1080], [1440, 900], [375, 812]]) {
      const f = await frame("/quarto-site/" + page, w, h), q = f.contentDocument;
      const root = q.documentElement;
      if (w === 375) out.scroll375[page] = {scrollWidth: root.scrollWidth, clientWidth: root.clientWidth};
      if (COURSES.includes(page) || page === LAB + "modern/index.html")
        out.courses[page + " @" + w] = Object.assign({clientWidth: root.clientWidth}, course(q));
      if (w === 1440) {
        const banner = q.querySelector(".draft-banner"), det = banner.querySelector("details");
        const closed = Math.round(banner.getBoundingClientRect().height);
        det.open = true;
        const opened = Math.round(banner.getBoundingClientRect().height);
        det.open = false;
        out.banner1440[page] = {closed, opened};
        out.contrast[page] = {
          banner: ratio(q.querySelector(".draft-banner strong")),
          sitename: ratio(q.querySelector(".osu-sitename")),
          heroTitle: ratio(q.querySelector(".hero h1")),
          heroLead: ratio(q.querySelector(".hero .lead p")),
          heroButton: ratio(q.querySelector(".hero .button.primary")),
        };
        if (page === "index.html") {
          const r = q.querySelector("main > p").getBoundingClientRect();
          out.landing1440 = {selector: "main > p", left: Math.round(r.left), right: Math.round(w - r.right)};
        }
      }
      f.remove();
    }
  }
  const s = await frame("/quarto-site/" + SIM, 1280, 720), sd = s.contentDocument.documentElement;
  out.sim = {bar: Math.round(s.contentDocument.querySelector(".lib-bar").getBoundingClientRect().height),
             page: sd.scrollHeight, fits: sd.scrollHeight <= 720};
  s.remove();
  return JSON.stringify(out, null, 1);
})();
