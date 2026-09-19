-- Numbers graded-question blocks and labels them, per theme.
--
-- Question ids are descriptors (ledger 14); the number a reader sees comes
-- from document order at render time, so reordering a lab renumbers safely.
--
-- theme=faithful: the original look. The question keeps its bold, prefixed
--   with "N)" exactly as the Word original numbered it.
-- theme=modern: the question becomes a labeled block ("Question N"), and its
--   bold is removed so that bold means emphasis again (ledger 29).

local theme = "modern"
local count = 0

local function unbold(inlines)
  return pandoc.walk_inline(pandoc.Span(inlines), {
    Strong = function(s) return s.content end,
  }).content
end

return {
  {
    Meta = function(meta)
      if meta.theme then theme = pandoc.utils.stringify(meta.theme) end
    end,
  },
  {
    Div = function(el)
      if not el.classes:includes("question") then return nil end
      count = count + 1
      local first = el.content[1]
      if not first or first.t ~= "Para" then return nil end

      if theme == "faithful" then
        local prefix = pandoc.Strong({ pandoc.Str(count .. ")"), pandoc.Space() })
        table.insert(first.content, 1, prefix)
      else
        first.content = unbold(first.content)
        local label = pandoc.Para({ pandoc.Str("Question " .. count) })
        label = pandoc.Div({ label }, pandoc.Attr("", { "question-label" }))
        table.insert(el.content, 1, label)
      end
      return el
    end,
  },
}
