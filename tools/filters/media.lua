-- Pictures and drawn figures in every output (four-items call 4.3; D-0117,
-- D-0118).
--
-- A picture (S12) is the original's file at Word's size and crop: its
-- `width` and `height` are Word's, in inches, and `crop` is Word's srcRect
-- (left, top, right, bottom, in thousandths of a percent). On a page it is
-- written as an <img> here, so Quarto never makes it a figure with its alt
-- text as a caption: the lab page runs this filter at `pre-ast`, before
-- Quarto's own figures (probed 2026-10-08). A cropped picture sits in a
-- span that shows only Word's part of it. In Word, Pandoc sizes it from the
-- same attributes, and tools/downloads.py writes the crop into the file.
--
-- A drawn figure (S13, class `drawn`) is made by the build (tools/media.py):
-- on a page its SVG is written inline, so its labels are text a screen
-- reader and find-in-page reach (D-0117, call 3); in Word it is the PNG
-- made from that SVG, at the SVG's size, its alt text Word's for the figure
-- and for each picture in it. A figure's `label` (D-0166) names the whole:
-- on a page the SVG becomes a group with that name, so a screen reader
-- hears what the drawing's arrows and shapes show before the pictures'
-- own alt text; in Word it leads the PNG's alt text.
--
-- A table (D-0130) is wrapped, in HTML only, in a `table-scroll` box the
-- theme scrolls sideways, so a table wider than a phone (PH 211 Lab 2's
-- eleven columns) scrolls in its box and the page itself never does (WCAG
-- 1.4.10); the box takes the keyboard's focus so the scroll is reachable
-- without a pointer (2.1.1). Word gets the table as Pandoc writes it.
--
-- Metadata: `media-dir`, the folder holding the lab's built media (needed
-- for a figure), and `media-prefix`, put before a picture's path on a page
-- that sits below the media folder's parent ("../" on labs/<id>/modern/).

local prefix, dir = "", nil

local function escape(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"))
end

local function basename(path)
  return path:match("([^/\\]+)$")
end

local function read(path)
  local fh = io.open(path, "rb")
  if not fh then error("media.lua: no file " .. path .. "; tools/media.py builds a lab's media") end
  local text = fh:read("a")
  fh:close()
  return text
end

local function figure_file(el, ext)
  if not dir then error("media.lua: a drawn figure needs media-dir") end
  local name = basename(el.src)
  if ext then name = name:gsub("%.svg$", ext) end
  return dir .. "/" .. name
end

local function inches(value, what)
  local n = value and tonumber(value:match("^([%d.]+)in$"))
  if not n then error("media.lua: a picture's " .. what .. " is Word's, in inches: " .. tostring(value)) end
  return n
end

local function picture_html(el)
  local alt = escape(pandoc.utils.stringify(el.caption))
  local src = escape(prefix .. el.src)
  local w = inches(el.attributes.width, "width") * 96
  local h = inches(el.attributes.height, "height") * 96
  local crop = el.attributes.crop
  -- Word's shape, even where it differs from the file's (aspect-ratio).
  if not crop then
    return string.format('<img src="%s" alt="%s" width="%d" height="%d" style="aspect-ratio:%.2f/%.2f">',
      src, alt, math.floor(w + 0.5), math.floor(h + 0.5), w, h)
  end
  local l, t, r, b = crop:match("^(%d+) (%d+) (%d+) (%d+)$")
  if not l then error("media.lua: crop is Word's srcRect, four integers: " .. crop) end
  l, t, r, b = l / 100000, t / 100000, r / 100000, b / 100000
  local sx, sy = 1 - l - r, 1 - t - b
  -- Word stretches the part it keeps to its size; percentages of the span,
  -- so the crop holds as the column narrows.
  return string.format(
    '<span class="picture-crop" style="width:%.2fpx;aspect-ratio:%.2f/%.2f">'
      .. '<img src="%s" alt="%s" style="width:%.4f%%;height:%.4f%%;left:-%.4f%%;top:-%.4f%%"></span>',
    w, w, h, src, alt, 100 / sx, 100 / sy, 100 * l / sx, 100 * t / sy)
end

local function figure_docx(el)
  local svg = read(figure_file(el))
  local w, h = svg:match('<svg[^>]-width="([%d.]+)" height="([%d.]+)"')
  local alts = { el.attributes.label or "", pandoc.utils.stringify(el.caption) }
  for alt in svg:gmatch('class="figure%-picture"[^>]-data%-alt="([^"]*)"') do
    table.insert(alts, alt)
  end
  local alt = table.concat(alts, " "):gsub("&quot;", '"'):gsub("&lt;", "<"):gsub("&gt;", ">")
    :gsub("&#x27;", "'"):gsub("&amp;", "&"):gsub("^%s+", ""):gsub("%s+$", "")
  return pandoc.Image({ pandoc.Str(alt) }, figure_file(el, ".png"), "",
    pandoc.Attr("", {}, { { "width", w .. "px" }, { "height", h .. "px" } }))
end

return {
  {
    Meta = function(meta)
      if meta["media-prefix"] then prefix = pandoc.utils.stringify(meta["media-prefix"]) end
      if meta["media-dir"] then dir = pandoc.utils.stringify(meta["media-dir"]) end
    end,
  },
  {
    Image = function(el)
      local drawn = el.classes:includes("drawn")
      if FORMAT:match("html") then
        if drawn then
          local svg = read(figure_file(el)):gsub("^%s*<%?xml[^>]*>%s*", ""):gsub("%s+$", "")
          local label = el.attributes.label
          if label then
            svg = svg:gsub("^<svg ", '<svg role="group" aria-label="' .. escape(label):gsub("%%", "%%%%") .. '" ', 1)
          end
          return pandoc.RawInline("html", svg)
        end
        return pandoc.RawInline("html", picture_html(el))
      elseif FORMAT == "docx" and drawn then
        return figure_docx(el)
      end
    end,
    Table = function(el)
      if FORMAT:match("html") then
        return pandoc.Div({ el }, pandoc.Attr("", { "table-scroll" }, { tabindex = "0" }))
      end
    end,
  },
}
