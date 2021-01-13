from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import time 
import json



chrome_options = Options()
chrome_options.add_extension(r'C:\Flo\Amazon MBA\Python Scripts\ds-amazon-quick-view.crx')

desired_capabilities = DesiredCapabilities.CHROME.copy()
desired_capabilities['chrome.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r"C:\Flo\Webscraping\chromedriver.exe", desired_capabilities=desired_capabilities)
driver.minimize_window()

# with open('all-niches.json') as json_file:
#     niches = json.load(json_file)

# header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
niches = ['Fußball', 'Bmx', 'Baseball']

results = []

for categorie in niches:

    url = f"https://www.amazon.com/-/de/s?k={categorie}+shirt&page=1&language=us&__mk_us_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1610205136&ref=sr_pg_1"
    print(url)

    driver.get(url)

    time.sleep(15)
    
    try:
        search_result = driver.find_element_by_xpath('//span[contains(@class,"template=RESULT_INFO_BAR")]//span[contains(@dir,"auto")][1]').text
        print(search_result)
        search_result_count = search_result.split(' ')

        if 'von mehr als' in search_result:
            search_result_count_value = search_result_count[4]
        else:
            search_result_count_value = search_result_count[2]    
        
        print(search_result_count_value)
    except:
        search_results = None

    # bewertung = xpath('//div[contains(@class,"a-size-small")]//span[contains(@class,"a-size-base")]')
    whole_products = driver.find_elements_by_xpath('//div[contains(@data-component-type,"s-search-result")]')
    whole_product_asin = whole_products[0].get_attribute('data-asin')
    # print(whole_product[0].get_attribute('innerHTML'))

    for single_product in whole_products:
        innerHtml = single_product.get_attribute('innerHTML')
        soup = BeautifulSoup(innerHtml)

        #URL
        # try:
        whole_product_link = soup.select('.s-result-item h2 a.a-text-normal')#.attrs['href']
            # whole_product_link = whole_product_link[0].attrs['href']
            # whole_product_link = soup.select('.s-result-item h2 a.a-text-normal')
            # whole_product_link = whole_product_link[0].attrs['href']
        # except:
        #     whole_product_link = None

        #TITLE
        try:
            whole_product_title = soup.find('span', class_='a-size-base-plus a-color-base a-text-normal').get_text().strip()
        except:
            whole_product_title = None

        #PRICE
        try:
            whole_product_price = soup.find('span', class_='a-offscreen').get_text().strip()
        except:
            whole_product_price = None

        #RANKING VALUE
        try:
            whole_product_rating_value = soup.select('span[aria-label*=Sterne]') #soup.find(//span[contains(@aria-label,'Sterne')])
            whole_product_rating_value = whole_product_rating_value[0].get_text().strip()
            whole_product_rating_value = whole_product_rating_value.split(' ')[0]
        except:
            whole_product_rating_value = None

        #RANKING COUNT
        try:
            whole_product_rating_count = soup.select('.a-size-small .a-link-normal .a-size-base')
            whole_product_rating_count = whole_product_rating_count[0].get_text().strip()
        except:
            whole_product_rating_count = None 

        #BSR
        try:
            whole_product_bsr = soup.find('span', class_='extension-rank').get_text().strip()
        except:
            whole_product_bsr = None

        print('\n############################')
        print(whole_product_link)
        print(whole_product_asin)
        print(whole_product_title)
        print(whole_product_price)
        print(whole_product_rating_value)
        print(whole_product_rating_count)
        print(whole_product_bsr)
        print('############################\n')


# with open('all-niches.json', 'w', encoding='utf-8') as f:
#     json.dump(results, f, ensure_ascii=False)

# with open('all-categories.json', 'w', encoding='utf-8') as f:
#     json.dump(categories, f, ensure_ascii=False)

# driver.close()




