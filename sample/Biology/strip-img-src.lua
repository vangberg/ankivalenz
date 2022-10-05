function Image(img)
  img.src = img.src:match("^.+/(.+)$")
  return img
end