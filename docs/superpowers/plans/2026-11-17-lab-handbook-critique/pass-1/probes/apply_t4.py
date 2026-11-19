import json
b=json.load(open('probes/t4.json',encoding='utf-8'))
p='hb/tools/filters/media.lua'
s=open(p,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1, old
    s=s.replace(old,new)
old='''    Link = function(el)
      local id = el.target:match("^([%w%-]+)%-media/[^/]+$")
      if not id then return end
      if not url then error("media.lua: a link to a lab's file needs library-url: " .. el.target) end
      el.target = url .. "labs/" .. id .. "/" .. el.target
      return el
    end,
'''
rep(old, b[1])
anchor='''-- file's published address under `library-url` in every output, page and
-- download alike, so a saved Word, HTML or PDF file still reaches it.
'''
rep(anchor, anchor + b[2])
open(p,'w',encoding='utf-8',newline='\n').write(s)
