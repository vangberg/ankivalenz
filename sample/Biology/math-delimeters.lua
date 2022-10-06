function Math (m)
  local startDelimiter = m.mathtype == 'InlineMath' and '\\\\(' or '\\\\['
  local endDelimiter = m.mathtype == 'InlineMath' and '\\\\)' or '\\\\]'
  return pandoc.RawInline('html', startDelimiter .. m.text .. endDelimiter)
end