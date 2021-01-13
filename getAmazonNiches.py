# -*- coding: iso-8859-1 -*-
from selenium import webdriver
import time 
import json

driver = webdriver.Chrome(executable_path=r"C:\Flo\Webscraping\chromedriver.exe")

driver.get('https://merchreport.de/mba-nischenliste/')
driver.maximize_window()


all_niches = driver.find_elements_by_xpath('//div[contains(@class,"et_pb_row_5col")]//tr')
all_categories = driver.find_elements_by_xpath('//div[contains(@class,"et_pb_row_5col")]//h3')


results = []
categories = []

for niche in all_niches:
    results.append(niche.text)

for categorie in all_categories:
    categories.append(categorie.text)
    


with open('all-niches.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False)

with open('all-categories.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f, ensure_ascii=False)

driver.close()



