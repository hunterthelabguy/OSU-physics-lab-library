-- A `::: landscape` block prints on a landscape page of its own, as Word
-- prints PH 212 Lab 6's rubric (pass 4). In Word, a section-break marker
-- goes on each side of the block: the first ends the portrait section
-- before it, the second ends the block's own landscape section.
-- tools/downloads.py fills each marker from the document's own section
-- (its page, margins and footer), so nothing here repeats
-- tools/reference.docx. On the page and in the PDF the block stays a Div;
-- the theme's print rules give it its landscape page.

local function marker(orientation)
  return pandoc.RawBlock("openxml",
    "<w:p><w:pPr><w:sectPr><!--section:" .. orientation .. "--></w:sectPr></w:pPr></w:p>")
end

function Div(el)
  if FORMAT ~= "docx" or not el.classes:includes("landscape") then
    return nil
  end
  local out = { marker("portrait") }
  for _, block in ipairs(el.content) do
    table.insert(out, block)
  end
  table.insert(out, marker("landscape"))
  return out
end
