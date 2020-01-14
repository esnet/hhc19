#!/usr/bin/env python3
#
#   NOTE
#
#   This is aggressively optimized, to the point that something
#   changed server-side, and this broke during the competition.
#
###############################################################


import base64
from bs4 import BeautifulSoup
import binascii
import datetime
from io import BytesIO
from multiprocessing.dummy import Pool
from PIL import Image
import pytesseract
import requests
import sys
import time

domain = 'crate.elfu.org'
domain = 'sleighworkshopdoor.elfu.org'


from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

# This is the 2.11 Requests cipher string, containing 3DES.
CIPHERS = (
    'ECDH+AES256'
)


class AESCCMAdapter(HTTPAdapter):
    """
    A TransportAdapter that re-enables 3DES support in Requests.
    """
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(AESCCMAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(AESCCMAdapter, self).proxy_manager_for(*args, **kwargs)

s = requests.Session()
s.mount('https://' + domain, AESCCMAdapter())

s = requests.Session()

def get_token(soup):
    """First link is: 
    <link href="css/styles.css/e56851a7-6697-49ef-badd-e86867e1b760" rel="stylesheet"/>"""
    href = soup.find('link').get('href')
    token = href.split('/')[-1]

    return token

def get_js(token):
    # If length is 52351, lock 1 is at: 11151, lock 4 is at 111
    with s.get("https://" + domain + "/client.js/" + token) as r:
        if r.raw.headers['Content-Length'] != '52351':
            raise ValueError("Don't bother. len=", r.raw.headers['Content-Length'])
        return r.content.decode('utf-8')


def lock_1(js, token):
    """Printed to the console"""

    # Our padding is weird, so we add hex for =
    encoded = js[11183:11247].replace('\\x', '') + '3d'
    decoded = binascii.unhexlify(encoded)
    # %cCYDSHREW %
    return ('1', base64.b64decode(decoded)[2:10].decode('utf-8'))
    # # Alternative
    # offset = js.find(r'\x4a\x57\x50\x69\x6c\x6f\x73\x4b\x4a\x57\x4e')
    # if offset < 0:
    #     raise ValueError("Could not find string in https://" + domain + "/client.js/" + token)
    # print("Offset is", offset)
    # end = js[offset:offset+1000].find("'")
    # print("End is", end)
    # elem = js[offset:offset+end].encode('utf-8').decode('unicode_escape')
    # try:
    #     data = base64.b64decode(elem).decode('utf-8').split('%c')[2].strip()
    # except:
    #     raise ValueError("Unexpected format")
        
    # return data


def lock_2(soup):
    """<div class="libra"><strong>A41VRDDQ</strong></div>"""
    
    return soup.find("div", {'class' : 'libra'}).find('strong').decode_contents()

def lock_3(token):
    """Image OCR"""
    return pytesseract.image_to_string(Image.open(BytesIO(s.get('https://' + domain + '/images/%s.png' % token).content)))

def lock_4(js, token):
    """Local storage"""

    encoded = js[12443:12491].replace('\\x', '') + '3d'
    decoded = binascii.unhexlify(encoded)
    # %cCYDSHREW %
    return ('4', base64.b64decode(decoded).decode('utf-8'))
    
def lock_5(soup):
    """Title"""
    return soup.find('title').decode_contents()[-8:]

def lock_6(soup):
    """Text perspective"""

    # This has some child divs, but the answer is always in the same order:
    divs = [x.decode_contents() for x in soup.find("div", {'class': 'hologram'}).find('div').children]
    result = ""
    for i in [3, 0, 4, 6, 5, 2, 7, 1]:
        result += divs[i]
        
    return result

def lock_7(soup):
    """
    <style>
    .instructions { font-family: 'U2N9FUQA', 'Beth Ellen', cursive; }
    </style>
    """
    style_inner_html = soup.find('style').decode_contents()
    # This returns something like ".instructions { font-family: 'VFYFYI08', 'Beth Ellen', cursive; }"
    return style_inner_html.split("'")[1]

def lock_8(soup):
    """.eggs event handler. Always VERONICA?"""
    return "VERONICA"

def lock_9(token):
    """Active chakras"""
    css = s.get("https://" + domain + "/css/styles.css/" + token).content.decode('utf-8')
    result = ""
    for l in css.split('\n'):
        if l.startswith("  content:"):
            result += l.split("'")[1]
    return result

def lock_10(soup):
    """Always hardcoded, but needs the right elements"""
    return "KD29XJ37"

def submit(token, code, lock_no):

    result = s.post('https://' + domain + '/unlock', json={'seed': token, 'code': code, 'id': lock_no})
    return result.json()


def main():
#   main_page_start = datetime.datetime.now()
    main_page = s.get('https://' + domain + '/').content
    soup = BeautifulSoup(main_page, 'html.parser')

    if len(sys.argv) < 2:
        token = get_token(soup)
    else:
        token = sys.argv[1].split('/')[-1]

    data = {'seed': token}
    data['codes'] = {
        '2': lock_2(soup),
        '3': lock_3(token),
        '5': lock_5(soup),
        '6': lock_6(soup),
        '7': lock_7(soup),
        '8': lock_8(soup),
        '9': lock_9(token),
        '10': lock_10(soup),
    }

    for k, v in data['codes'].items():
        print(k, v, submit(token, v, k))

    js = get_js(token)

    pool = Pool(4)
    lock_futures = []
    lock_futures.append(pool.apply_async(lock_1, [js, token]))
    lock_futures.append(pool.apply_async(lock_4, [js, token]))
    
    for future in lock_futures:
        k, v = future.get()
        data['codes'][k] = v
        pool.apply_async(submit, [token, k, v])

    result = s.post('https://' + domain + '/open', json=data, verify=False).json()
    if result:
        print("RESULT: Success", result)
    else:
        result = s.post('https://' + domain + '/open', json=data, verify=False).json()
        if result:
            print("RESULT: Success", result)

if __name__ == '__main__':
    main()
