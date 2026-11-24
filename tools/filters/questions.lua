-- Numbers graded-question blocks and checkpoints and labels them.
--
-- Question ids are descriptors (ledger 14); the number a reader sees comes
-- from document order at render time, so reordering a lab renumbers safely.
-- `.restart` on a question starts the count again at 1, where Word restarts
-- the lab's question list (S9, a second week). A `.checkpoint` block is a
-- numbered item needing no answer (D-0109, D-0110): "Checkpoint N" on its own
-- count, so the questions keep Word's numbers. A question or checkpoint must
-- open with a paragraph; anything else fails the render (D-0082).
-- tools/check_numbers.py reads these labels against Word's (D-0102).
--
-- The block becomes a labeled block ("Question N"), and all its bold is
-- removed so that bold means emphasis again (ledger 29; D-0101, S4). The
-- faithful presentation, which kept the bold and printed "N)", is retired
-- (D-0108). In Word the block is a one-cell table with the page's rule down
-- the left and its tint behind (D-0082), so stem, parts, bullets and hints
-- sit in one box: Pandoc's custom-style never reaches list items (D-0057's
-- probe). The table is raw OpenXML around Pandoc's own paragraphs; its
-- colours come from themes/modern.css by way of tools/downloads.py
-- (`box-rule`, `box-fill`, `checkpoint-rule`, `checkpoint-fill`), and the
-- label takes the Question Label style of tools/reference.docx. Any other
-- output would carry a style name into the page as an attribute, so it is
-- never set there.

local questions, checkpoints = 0, 0
local colours = {}

local function unbold(el)
  return el:walk({ Strong = function(s) return s.content end })
end

-- themes/modern.css lengths in rem, as twips of Word's 12 pt body, the
-- proportion tools/make_reference_docx.py keeps (body 1.0625rem = 12 pt).
local function twips(rem) return math.floor(rem / 1.0625 * 12 * 20 + 0.5) end
-- Letter less 0.75 in margins each side, tools/reference.docx's page.
local TEXT_WIDTH = 10080

-- .question { padding: .9rem 1.1rem .1rem; border-left: 4px; margin: 1.5rem 0 }:
-- the padding as cell margins, the rule as a 3 pt left border on the text
-- column's edge, and an empty paragraph after it for the bottom margin,
-- which also keeps two boxes in a row from joining into one table. The same
-- gap goes before a box that follows a table: Word joins two tables that
-- touch, and Pandoc separates its own tables but cannot see the box (D-0179).
local GAP = '<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="' .. twips(1.5)
  .. '" w:lineRule="exact"/></w:pPr></w:p>'

local function word_box(blocks, rule, fill, kind)
  if not rule or not fill then
    error("the Word " .. kind .. " box needs its colours; tools/downloads.py passes them")
  end
  local side = twips(1.1)
  local open = '<w:tbl><w:tblPr><w:tblW w:w="' .. TEXT_WIDTH .. '" w:type="dxa"/>'
    .. '<w:tblInd w:w="' .. side .. '" w:type="dxa"/><w:tblBorders>'
    .. '<w:top w:val="nil"/><w:left w:val="single" w:sz="24" w:space="0" w:color="' .. rule .. '"/>'
    .. '<w:bottom w:val="nil"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/>'
    .. '</w:tblBorders><w:tblLayout w:type="fixed"/><w:tblCellMar>'
    .. '<w:top w:w="' .. twips(.9) .. '" w:type="dxa"/><w:left w:w="' .. side .. '" w:type="dxa"/>'
    .. '<w:bottom w:w="' .. twips(.1) .. '" w:type="dxa"/><w:right w:w="' .. side .. '" w:type="dxa"/>'
    .. '</w:tblCellMar><w:tblLook w:val="0000"/></w:tblPr>'
    .. '<w:tblGrid><w:gridCol w:w="' .. TEXT_WIDTH .. '"/></w:tblGrid>'
    .. '<w:tr><w:trPr><w:cantSplit/></w:trPr><w:tc><w:tcPr><w:tcW w:w="' .. TEXT_WIDTH .. '" w:type="dxa"/>'
    .. '<w:shd w:val="clear" w:color="auto" w:fill="' .. fill .. '"/></w:tcPr>'
  local out = { pandoc.RawBlock("openxml", open) }
  for _, b in ipairs(blocks) do table.insert(out, b) end
  table.insert(out, pandoc.RawBlock("openxml", "</w:tc></w:tr></w:tbl>"))
  table.insert(out, pandoc.RawBlock("openxml", GAP))
  return out
end

return {
  {
    Meta = function(meta)
      for _, key in ipairs({ "box-rule", "box-fill", "checkpoint-rule", "checkpoint-fill" }) do
        if meta[key] then colours[key] = pandoc.utils.stringify(meta[key]) end
      end
    end,
  },
  {
    Div = function(el)
      local kind
      if el.classes:includes("question") then
        kind = "question"
      elseif el.classes:includes("checkpoint") then
        kind = "checkpoint"
      else
        return nil
      end
      local first = el.content[1]
      if not first or first.t ~= "Para" then
        local name = el.identifier ~= "" and ("#" .. el.identifier) or "without an id"
        error(kind .. " " .. name .. " must open with a paragraph, not "
          .. (first and first.t or "nothing"))
      end

      local n
      if kind == "checkpoint" then
        checkpoints = checkpoints + 1
        n = checkpoints
      else
        if el.classes:includes("restart") then questions = 0 end
        questions = questions + 1
        n = questions
      end

      el = unbold(el)
      local text = (kind == "question" and "Question " or "Checkpoint ") .. n
      local label = pandoc.Div({ pandoc.Para({ pandoc.Str(text) }) },
        pandoc.Attr("", { kind .. "-label" }))
      table.insert(el.content, 1, label)
      if FORMAT == "docx" then
        label.attributes["custom-style"] = "Question Label"
        local prefix = kind == "question" and "box" or "checkpoint"
        return word_box(el.content, colours[prefix .. "-rule"], colours[prefix .. "-fill"], kind)
      end
      return el
    end,
  },
  {
    -- After the boxes are written: a box (raw, opening "<w:tbl>") right
    -- after a Pandoc table gets the gap before it too (D-0179).
    Blocks = function(blocks)
      if FORMAT ~= "docx" then return nil end
      local out, inserted = {}, false
      for i, b in ipairs(blocks) do
        local prev = blocks[i - 1]
        if prev and prev.t == "Table" and b.t == "RawBlock" and b.format == "openxml"
            and b.text:sub(1, 7) == "<w:tbl>" then
          table.insert(out, pandoc.RawBlock("openxml", GAP))
          inserted = true
        end
        table.insert(out, b)
      end
      if inserted then return out end
      return nil
    end,
  },
}
