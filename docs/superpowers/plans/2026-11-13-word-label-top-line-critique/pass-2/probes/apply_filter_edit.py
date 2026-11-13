p = 'tools/filters/questions.lua'
s = open(p, encoding='utf-8', newline='').read()
assert '\r\n' not in s
new = r'''-- .question { padding: .9rem 1.1rem .1rem; border-left: 4px; margin: 1.5rem 0 }:
-- the padding as cell margins, the rule as a 3 pt left border on the text
-- column's edge, and an empty paragraph after it for the bottom margin,
-- which also keeps two boxes in a row from joining into one table.
-- D-0180: the label sits directly before the table, since Word's Navigation
-- pane leaves out any heading in a table cell, drawn as the box's top line
-- by direct formatting (questions and checkpoints differ in colour): the
-- rule as its left border, the tint as its shading and as top and right
-- borders, so the shading reaches the box's edges. Spaces and indents land
-- the rule and the tint's edge on the box's, measured in Word's render at
-- 300 dpi (spec 2026-11-13, section 3).
-- The cell's top margin under the label: the box's top padding, twips(.9)
-- = 203, plus Question Label's space after, 79, as before, less the
-- label's top border (0.5 pt, 10) and its space (9 pt, 180).
local CELL_TOP = 92

local function word_label(text, level, rule, fill)
  return pandoc.RawBlock("openxml", '<w:p><w:pPr><w:pStyle w:val="QuestionLabel' .. level .. '"/>'
    .. '<w:pBdr><w:top w:val="single" w:sz="4" w:space="9" w:color="' .. fill .. '"/>'
    .. '<w:left w:val="single" w:sz="24" w:space="9" w:color="' .. rule .. '"/>'
    .. '<w:right w:val="single" w:sz="4" w:space="11" w:color="' .. fill .. '"/></w:pBdr>'
    .. '<w:shd w:val="clear" w:color="auto" w:fill="' .. fill .. '"/>'
    .. '<w:spacing w:before="0" w:after="0"/><w:ind w:left="238" w:right="258" w:firstLine="10"/></w:pPr>'
    .. '<w:r><w:t xml:space="preserve">' .. text .. '</w:t></w:r></w:p>')
end

local function word_box(text, level, blocks, rule, fill, kind)
  if not rule or not fill then
    error("the Word " .. kind .. " box needs its colours; tools/downloads.py passes them")
  end
  local side = twips(1.1)
  local open = '<w:tbl><w:tblPr><w:tblW w:w="' .. TEXT_WIDTH .. '" w:type="dxa"/>'
    .. '<w:tblInd w:w="' .. side .. '" w:type="dxa"/><w:tblBorders>'
    .. '<w:top w:val="nil"/><w:left w:val="single" w:sz="24" w:space="0" w:color="' .. rule .. '"/>'
    .. '<w:bottom w:val="nil"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/>'
    .. '</w:tblBorders><w:tblLayout w:type="fixed"/><w:tblCellMar>'
    .. '<w:top w:w="' .. CELL_TOP .. '" w:type="dxa"/><w:left w:w="' .. side .. '" w:type="dxa"/>'
    .. '<w:bottom w:w="' .. twips(.1) .. '" w:type="dxa"/><w:right w:w="' .. side .. '" w:type="dxa"/>'
    .. '</w:tblCellMar><w:tblLook w:val="0000"/></w:tblPr>'
    .. '<w:tblGrid><w:gridCol w:w="' .. TEXT_WIDTH .. '"/></w:tblGrid>'
    .. '<w:tr><w:trPr><w:cantSplit/></w:trPr><w:tc><w:tcPr><w:tcW w:w="' .. TEXT_WIDTH .. '" w:type="dxa"/>'
    .. '<w:shd w:val="clear" w:color="auto" w:fill="' .. fill .. '"/></w:tcPr>'
  local gap = '<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="' .. twips(1.5)
    .. '" w:lineRule="exact"/></w:pPr></w:p>'
  local out = { word_label(text, level, rule, fill), pandoc.RawBlock("openxml", open) }
  for _, b in ipairs(blocks) do table.insert(out, b) end
  table.insert(out, pandoc.RawBlock("openxml", "</w:tc></w:tr></w:tbl>"))
  table.insert(out, pandoc.RawBlock("openxml", gap))
  return out
end
'''
i = s.index('-- .question { padding')
j = s.index('return {\n  {\n    Meta')
s = s[:i] + new + '\n' + s[j:]

old = '''        local label = pandoc.Div({ pandoc.Para({ pandoc.Str(text) }) },
          pandoc.Attr("", { kind .. "-label" }, { ["custom-style"] = "Question Label " .. level }))
        table.insert(el.content, 1, label)
        local prefix = kind == "question" and "box" or "checkpoint"
        return word_box(el.content, colours[prefix .. "-rule"], colours[prefix .. "-fill"], kind), false
'''
assert old in s
s = s.replace(old, '''        local prefix = kind == "question" and "box" or "checkpoint"
        return word_box(text, level, el.content, colours[prefix .. "-rule"], colours[prefix .. "-fill"], kind), false
''')

old = '''-- label takes the Question Label N style of tools/reference.docx, N its
-- level, 3 to 5 (D-0176). Any other output would carry a style name into
-- the page as an attribute, so it is never set there.'''
assert old in s
s = s.replace(old, '''-- label, in the Question Label N style of tools/reference.docx (N its level,
-- 3 to 5; D-0176), sits directly before the box as its top line (D-0180).
-- Any other output would carry a style name into the page as an attribute,
-- so it is never set there.''')
open(p, 'w', encoding='utf-8', newline='').write(s)
