function Math (m)
  local startDelimiter = m.mathtype == 'InlineMath' and '$' or '$$'
  local endDelimiter = m.mathtype == 'InlineMath' and '$' or '$$'
  local escaped = string.gsub(m.text, "\\", "\\\\")
  return pandoc.RawInline('html', startDelimiter .. m.text .. endDelimiter)
end