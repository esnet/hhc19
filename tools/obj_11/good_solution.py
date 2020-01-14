#!/usr/bin/env python3

import base64
from bs4 import BeautifulSoup
import codecs
from io import BytesIO
from PIL import Image
import pytesseract
import requests
import sys

domain = 'crate.elfu.org'

s = requests.Session()


def get_token(soup):
    """First link is: 
    <link href="css/styles.css/e56851a7-6697-49ef-badd-e86867e1b760" rel="stylesheet"/>"""
    href = soup.find('link').get('href')
    token = href.split('/')[-1]

    return token

def get_js(token):
    return s.get("https://" + domain + "/client.js/" + token).content.decode('utf-8')


def lock_1(js, token):
    """Printed to the console"""
    
    # Alternative
    offset = js.find(r'\x4a\x57\x50\x69\x6c\x6f\x73\x4b\x4a\x57\x4e')
    if offset < 0:
        raise ValueError("Could not find string in https://" + domain + "/client.js/" + token)
    end = js[offset:offset+1000].find("'")
    elem = js[offset:offset+end].encode('utf-8').decode('unicode_escape')
    try:
        data = base64.b64decode(elem).decode('utf-8').split('%c')[2].strip()
    except:
        raise ValueError("Unexpected format")
        
    return data


def lock_2(soup):
    """<div class="libra"><strong>A41VRDDQ</strong></div>"""
    
    return soup.find("div", {'class' : 'libra'}).find('strong').decode_contents()

def lock_3(token):
    """Image OCR"""
    return pytesseract.image_to_string(Image.open(BytesIO(s.get('https://' + domain + '/images/%s.png' % token).content)))

def lock_4(js, token):
    """Local storage"""

    array = js.split('[', 1)[1].split(']', 1)[0]
    # Strip first and last single-quote
    array = array.strip("'").rstrip("'")

    local_storage_offset = 0
    array_elems = array.split("','")
    for i in range(len(array_elems)):
    if array_elems[i].encode('utf-8').decode('unicode_escape') == '8J+bou+4j/Cfm6LvuI/wn5ui77iPW':
            local_storage_offset = i + 1
            break

    if not local_storage_offset:
        raise ValueError("Could not find local storage value in array")

    return base64.b64decode(array_elems[local_storage_offset].encode('utf-8').decode('unicode_escape')).decode('utf-8')


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
    main_page = s.get('https://' + domain + '/').content
    soup = BeautifulSoup(main_page, 'html.parser')

    if len(sys.argv) < 2:
        token = get_token(soup)
    else:
        token = sys.argv[1].split('/')[-1]
    js = get_js(token)

    codes = {
        '1': lock_1(js, token),
        '2': lock_2(soup),
        '3': lock_3(token),
        '4': lock_4(js, token),
        '5': lock_5(soup),
        '6': lock_6(soup),
        '7': lock_7(soup),
        '8': lock_8(soup),
        '9': lock_9(token),
        '10': lock_10(soup),
    }

    for k, v in codes.items():
        print(k, v, submit(token, v, k))

    data = {'seed': token, 'codes': codes}
    print(data)

    print(s.post('http://' + 'localhost:9000' + '/open', json=data).content)
    
    print("Image is at https://" + domain + "/images/scores/" + token + ".jpg")


if __name__ == '__main__':
    main()
