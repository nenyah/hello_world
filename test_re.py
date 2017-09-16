html = """test <img data-ratio="1" data-s="300,640" data-src="http://mmbiz.qpic.cn/mmbiz/44k1ricUO477PbiaLKJ8GicfEnaZgaIeCPENv5ydYukw5y1qUYTOLfPEAAeDA0vMfvrf9ZgBwRB1eWicL9lDTk1NLA/0?wx_fmt=jpeg" data-type="jpeg" data-w=""/><br/></p><p><br/></p><p><span style="color: rgb(142, 201, 101); font-weight: bold; line-height: 22.4px; text-align: center; font-size: 14px; background-color: rgb(255, 255, 255);">黄昏下，他和她....</span></p><p><img data-ratio="1" data-s="300,640" data-src="http://mmbiz.qpic.cn/mmbiz/44k1ricUO477PbiaLKJ8GicfEnaZgaIeCPEC8OuwcnZibNia9z2tbeT5bF6YkoB9fJIsp7kPzHZIKPnLmdlfWHCQsGQ/0?wx_fmt=jpeg" data-type="jpeg" data-w="" style="line-height: 1.6; white-space: normal;"/> test1"""
import re
p = re.compile(r'^<img.*"(http.*fmt=.*)";.*/>$', re.M)
# m = re.match(pattern, html)


def build_img(m):
    return '<img src="' + m.group(1) + '" />'
print(p.sub(build_img, html))
