#!/usr/bin/env python3

import requests

url =  'https://trail.elfu.org/trail/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://trail.elfu.org',
    'Referer': 'https://trail.elfu.org/trail/',
    'Cookie': 'trail-mix-cookie=1f23c2a213bd39ef41960edd1d09e0fda1bc07d1',
    }

data = {
    # The characters...
#    'playerid': 'VG',
    'playerid': 'JebediahSpringfield',
    'name0': 'Lila',
    'health0': 100,
    'cond0': 0,
    'cause0': '',
    'deathday0': 0,
    'deathmonth0': 0,
    'name1': 'Jo',
    'health1': 100,
    'cond1': 0,
    'cause1': '',
    'deathday1': 0,
    'deathmonth1': 0,
    'name2': 'Jessica',
    'health2': 100,
    'cond2': 0,
    'cause2': '',
    'deathday2': 0,
    'deathmonth2': 0,
    'name3': 'Jane',
    'health3': 100,
    'cond3': 0,
    'cause3': '',
    'deathday3': 0,
    'deathmonth3': 0,

    # Supplies

    'reindeer': 255,
    'runners': 29,
    'ammo': 35,
    'meds': 44,
    'food': 485,
    'money': 65535,

    # Status
    
    'pace': 1,
    'action': 'go',
    'distance': 7986,
    'curmonth':12,
    'curday': 25,

    'difficulty': 1,
    'hash': 'HASH'
    }


def submit_and_get_score():
    # Scoring:
    # score = 
    #   ( surviving_party_members * 1000 ) +
    #   ( reindeer * 400 ) +
    #   money + 
    #   ( days_left_until_christmas * 50 ) 
    #
    # total = difficulty (medium: 4, easy: 1) * score

    result = requests.post(url, headers=headers, data=data).content.decode('utf-8')

    score = -1
    ver_hash = ''

    if 'Total' in result:
        for l in result.split('\n'):
            if 'Total' in l:
                # e.g. ea022">86300</font>!</b></li>
                score = l.split('ea022">', 1)[1]
                score = score.split('<', 1)[0]
                score = int(score)
            if 'Verification' in l:
                # e.g.   <li>Verification hash: <font color="#9ea022">340a7074f20b2967727f12c2af6896a4</li>
                ver_hash = l.split('>')[2]
                ver_hash = ver_hash.split('<')[0]

    print(result)
    return(score, ver_hash)


submit_and_get_score()

