local function esc(s)
  local map = {
    ['\\'] = '\\textbackslash{}', ['%'] = '\\%', ['#'] = '\\#',
    ['&'] = '\\&', ['$'] = '\\$', ['{'] = '\\{', ['}'] = '\\}',
    ['~'] = '\\textasciitilde{}', ['^'] = '\\textasciicircum{}',
    ['_'] = '\\_'
  }
  local out = s:gsub('.', function(c) return map[c] or c end)
  -- points de coupure après ces caractères
  out = out:gsub('([_/%.%-%(%):@,=])', '%1\\allowbreak{}')
  return out
end

function Code(el)
  if FORMAT:match('latex') and #el.text >= 10
     and not el.text:find('%s') then
    return pandoc.RawInline('latex', '\\texttt{' .. esc(el.text) .. '}')
  end
end

function Pandoc(doc)
  if FORMAT:match('latex') then
    local def = [[
\makeatletter
\providecommand{\code}[1]{{\urlstyle{tt}\path{#1}}}
\g@addto@macro{\UrlBreaks}{\do\_\do\-\do\(\do\)\do\:}
\makeatother
]]
    table.insert(doc.blocks, 1, pandoc.RawBlock('latex', def))
  end
  return doc
end