// Manual layout check for the Quarto migration (phase 2). CI does not run it.
// Serve both builds from one origin, on a port not used before in the session
// (the pane caches per origin):
//   python -m http.server <port> --directory <absolute path to build>
// Open http://127.0.0.1:<port>/quarto-site/ in the browser pane and run this
// file's text with the pane's JavaScript tool. It loads every page of both
// builds in same-origin iframes at fixed sizes and returns JSON:
//   diffs        computed-style and box differences, old build versus Quarto
//   scroll375    each Quarto page's scrollWidth at 375 px (want <= 375)
//   banner1440   draft banner height, closed and open, at 1440 px
//   landing1440  the landing prose column's left and right gaps at 1440 px
//   contrast     WCAG ratios of the chrome text on its background
//   sim          the sim bar and page height at 1280x720
await (async () => {
  const LAB = "labs/ph211-team-building-handout/";
  const PAGES = ["index.html", "courses/index.html", "how-this-was-made/index.html",
    "sims/index.html", LAB + "modern/index.html", LAB + "faithful/index.html"];
  const SIM = "sims/modified-electric-force/index.html";
  const SEL = [".draft-banner", ".draft-banner summary", ".osu-strip", ".osu-strip a",
    ".osu-banner", ".osu-logo img", ".osu-sitename", ".osu-nav", ".osu-nav a", "main",
    "main h1", "main h2", "main p", "main li", ".hero", ".hero .lead", ".hero .button",
    ".link-cards li", ".lab-list > li", ".site-nav", ".site-nav a", ".doc-footer",
    ".site-foot", ".osu-foot", ".osu-foot a"];
  const PROPS = ["font-family", "font-size", "font-weight", "line-height", "color",
    "background-color", "margin-top", "margin-bottom", "padding-top", "padding-bottom"];
  const frame = (src, w, h) => new Promise(done => {
    const f = document.createElement("iframe");
    f.style.cssText = `position:absolute;left:-20000px;top:0;border:0;width:${w}px;height:${h}px`;
    f.onload = async () => { await f.contentDocument.fonts.ready; done(f); };
    f.src = src + "?m=" + Date.now();
    document.body.appendChild(f);
  });
  const css = el => el.ownerDocument.defaultView.getComputedStyle(el);
  const snap = doc => Object.fromEntries(SEL.map(s => {
    const el = doc.querySelector(s);
    if (!el) return [s, null];
    const r = el.getBoundingClientRect(), cs = css(el);
    return [s, Object.assign(Object.fromEntries(PROPS.map(p => [p, cs.getPropertyValue(p)])),
      {left: Math.round(r.left), width: Math.round(r.width), height: Math.round(r.height)})];
  }));
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
  const out = {diffs: {}, scroll375: {}, banner1440: {}, landing1440: null, contrast: {}, sim: null};
  for (const page of PAGES) {
    for (const [w, h] of [[1440, 900], [375, 812]]) {
      const a = await frame("/site/" + page, w, h), b = await frame("/quarto-site/" + page, w, h);
      const sa = snap(a.contentDocument), sb = snap(b.contentDocument), d = [];
      for (const s of SEL) {
        if (JSON.stringify(sa[s]) === JSON.stringify(sb[s])) continue;
        if (!sa[s] || !sb[s]) { d.push([s, sa[s] ? "missing in quarto" : "only in quarto"]); continue; }
        for (const k of Object.keys(sa[s])) if (sa[s][k] !== sb[s][k]) d.push([s, k, sa[s][k], sb[s][k]]);
      }
      if (d.length) out.diffs[page + " @" + w] = d;
      const q = b.contentDocument;
      if (w === 375) out.scroll375[page] = q.documentElement.scrollWidth;
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
      a.remove(); b.remove();
    }
  }
  const s = await frame("/quarto-site/" + SIM, 1280, 720), sd = s.contentDocument.documentElement;
  out.sim = {bar: Math.round(s.contentDocument.querySelector(".lib-bar").getBoundingClientRect().height),
             page: sd.scrollHeight, fits: sd.scrollHeight <= 720};
  s.remove();
  return JSON.stringify(out, null, 1);
})();
