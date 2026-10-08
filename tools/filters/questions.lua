-- Numbers graded-question blocks and checkpoints and labels them, per theme.
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
-- theme=faithful: the original look. The question keeps its bold, prefixed
--   with "N)" exactly as the Word original numbered it.
-- theme=modern: the block becomes a labeled block ("Question N"), and all its
--   bold is removed so that bold means emphasis again (ledger 29; D-0101,
--   S4). For Word only, the question's label and paragraphs name the Question
--   Label and Question styles of tools/reference.docx (D-0057); any other
--   output would carry the name into the page as an attribute, so it is never
--   set there.

local theme = "modern"
local questions, checkpoints = 0, 0

local function unbold(el)
  return el:walk({ Strong = function(s) return s.content end })
end

return {
  {
    Meta = function(meta)
      -- Quarto reserves `theme` for its page theme, so the presentation
      -- travels as `theme-name` there; the Pandoc build still sends `theme`.
      local v = meta["theme-name"] or meta.theme
      if v then theme = pandoc.utils.stringify(v) end
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

      if theme == "faithful" and kind == "question" then
        local prefix = pandoc.Strong({ pandoc.Str(n .. ")"), pandoc.Space() })
        table.insert(first.content, 1, prefix)
        return el
      end

      if theme ~= "faithful" then el = unbold(el) end
      local text = (kind == "question" and "Question " or "Checkpoint ") .. n
      local label = pandoc.Div({ pandoc.Para({ pandoc.Str(text) }) },
        pandoc.Attr("", { kind .. "-label" }))
      if FORMAT == "docx" and kind == "question" then
        label.attributes["custom-style"] = "Question Label"
        el.attributes["custom-style"] = "Question"
      end
      table.insert(el.content, 1, label)
      return el
    end,
  },
}
