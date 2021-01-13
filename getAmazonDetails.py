from bs4 import BeautifulSoup
from lxml import etree 
from time import gmtime, strftime

import re
import requests
import json
import lxml
import urllib.request  as urllib2
import time

with open('all-niches.json') as json_file:
    niches = json.load(json_file)

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
results = []

for categorie in niches:


    url = f"https://www.amazon.com/-/de/s?k={categorie}+shirt&page=1&language=us&__mk_us_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1610205136&ref=sr_pg_1"
    print(url)


    r = requests.get(url, headers=header).text
    tree = lxml.etree.fromstring(r, parser=lxml.etree.HTMLParser())

    try:
        search_result = tree.xpath('//span[contains(@class,"template=RESULT_INFO_BAR")]//span[contains(@dir,"auto")][1]/text()')
        print(search_result)
    except: 
        print('not found')
        search_result = ''

    results.append({f'{categorie}': search_result})

print(results)



