#!/usr/bin/env python3

# Best score: 64800, 13f100399063a2317714dcfc93c87fa7

from bs4 import BeautifulSoup
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

    'reindeer': 2,
    'runners': 2,
    'ammo': 10,
    'meds': 2,
    'food': 100,
    'money': 1500,

    # Status
    
    'pace': 2,
    'action': 'go',
    'distance': 0,
    'curmonth': 9,
    'curday': 1,

    'difficulty': 2,
    'hash': 'bc573864331a9e42e4511de6f678aa83'
    }


# These were incremental values we found:
data['reindeer'] = 12
data['distance'] = 1086
data['food'] = 0
data['curmonth'] = 9
data['curday'] = 12
data['hash'] = '8e065119c74efe3a47aec8796964cf8b'


def get_distance_travelled(soup):
    try:
        return int(str(soup.p).split(' ')[12])
    except:
        return 0


def get_field(soup, field_name):
    try:
        return soup.find("input", {"name": field_name}).get('value')
    except AttributeError:
        print(soup)

    
def go():
    result = requests.post(url, headers=headers, data=data).content.decode('utf-8')
    
    soup = BeautifulSoup(result, 'html.parser')
    return soup

max_distance = 7
# Food:
#      Steady: 2 morsels/person/day
#      Strenuous: 3 morsels/person/day
#      Grueling: 4 morsels/person/day

while int(data['distance']) + max_distance < 8000:
    latest = go()
#    if get_distance_travelled(latest) > max_distance:
    if int(get_field(latest, 'runners')) < data['runners']:
        continue
    if int(get_field(latest, 'reindeer')) <= data['reindeer']:
        continue
        
    data['hash'] = get_field(latest, 'hash')
    data['distance'] = get_field(latest, 'distance')
    data['curmonth'] = get_field(latest, 'curmonth')
    data['curday'] = get_field(latest, 'curday')
    data['food'] = get_field(latest, 'food')
    data['reindeer'] = int(get_field(latest, 'reindeer'))
    data['runners'] = int(get_field(latest, 'runners'))

    print(data)
#        print(latest.find('div', {"id": "statusContainer"}))

print("Got there!", data)
