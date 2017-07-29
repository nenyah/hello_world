"""
file:google_translate.py
function: translate language via google translate
"""
import requests
import urllib

base_url = "http://api.microsofttranslator.com/V2/Ajax.svc//TranslateArray"
sentence = "Les lanières"

paraments = {
    'oncomplete': 'didtranslate',
    'appId': 'DB50E2E9FBE2E92B103E696DCF4E3E512A8826FB',
    'texts': urllib.parse.quote(sentence),
    'to': 'en'
}
headers = {'User-Agent':
           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19\
                   (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
r = requests.get(base_url, params=paraments, headers=headers)

import urllib.request
import sys
typ = sys.getfilesystemencoding()


def translate(querystr, to_l="zh", from_l="en"):
    '''for google tranlate by doom
    '''
    C_agent = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.165063 Safari/537.36 AppEngine-Google."}
    flag = 'class="t0">'
    tarurl = "http://translate.google.com/m?hl=%s&sl=%s&q=%s \
        " % (to_l, from_l, querystr.replace(" ", "+"))
    request = urllib.request.Request(tarurl, headers=C_agent)
    page = str(urllib.request.urlopen(request).read().decode(typ))
    target = page[page.find(flag) + len(flag):]
    target = target.split("<")[0]
    return target
print(translate("Hello world"))
