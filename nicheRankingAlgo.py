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
all_products_global = []
all_niche_rankings = []

for categorie in niches:

    all_products = []
    niche_ranking = []

    # avg_price = 0
    # avg_bsr = 0
    # avg_rating_value = 0
    # avg_rating_count = 0


    url = f"https://www.amazon.com/-/de/s?k={categorie}+shirt&page=1&language=us&__mk_us_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1610205136&ref=sr_pg_1"
    print(url)

    driver.get(url)

    time.sleep(15)
    
    try:
        search_result = driver.find_element_by_xpath('//span[contains(@class,"template=RESULT_INFO_BAR")]//span[contains(@dir,"auto")][1]').text
        search_result_count = search_result.split(' ')

        if 'von mehr als' in search_result:
            search_result_count_value = search_result_count[4]
        else:
            search_result_count_value = search_result_count[2]    
        
        print(search_result_count_value)
    except:
        search_results = None

    # bewertung = xpath('//div[contains(@class,"a-size-small")]//span[contains(@class,"a-size-base")]')
    products = driver.find_elements_by_xpath('//div[contains(@data-component-type,"s-search-result")]')
    # print(product[0].get_attribute('innerHTML'))

    counter = 0

    for single_product in products:
        product_asin = products[counter].get_attribute('data-asin')
        innerHtml = single_product.get_attribute('innerHTML')
        soup = BeautifulSoup(innerHtml)

        #URL
        # try:
        product_link = soup.select('.s-result-item h2 a.a-text-normal')#.attrs['href']
            # product_link = product_link[0].attrs['href']
            # product_link = soup.select('.s-result-item h2 a.a-text-normal')
            # product_link = product_link[0].attrs['href']
        # except:
        #     product_link = None

        #TITLE
        try:
            product_title = soup.find('span', class_='a-size-base-plus a-color-base a-text-normal').get_text().strip()
        except:
            product_title = None

        #PRICE
        try:
            product_price = soup.find('span', class_='a-offscreen').get_text().strip()
            product_price = product_price[0:5]
            num, dec = product_price.split(',')
            product_price = float(''.join(num.split('.')) + '.' + dec)
        except:
            product_price = None

        #RANKING VALUE
        try:
            product_rating_value = soup.select('span[aria-label*=Sterne]') #soup.find(//span[contains(@aria-label,'Sterne')])
            product_rating_value = product_rating_value[0].get_text().strip()
            product_rating_value = product_rating_value.split(' ')[0]
            num, dec = product_rating_value.split(',')
            product_rating_value = float(''.join(num.split('.')) + '.' + dec)
        except:
            product_rating_value = None

        #RANKING COUNT
        try:
            product_rating_count = soup.select('.a-size-small .a-link-normal .a-size-base')
            product_rating_count = product_rating_count[0].get_text().strip()
            if '.' in product_rating_count:
                thousands, hundrets = product_rating_count.split('.')
                product_rating_count = int(''.join(thousands + hundrets))
        except:
            product_rating_count = None 

        #BSR
        try:
            product_bsr = soup.find('span', class_='extension-rank').get_text().strip()
            # product_bsr = product_bsr.split(,)
            thousands, hundrets = product_bsr.split(',')
            product_bsr = int(''.join(thousands + hundrets))
        except:
            product_bsr = None

        # print('\n############################')
        # print(product_link)
        # print(product_asin)
        # print(product_title)
        # print(product_price)
        # print(product_rating_value)
        # print(product_rating_count)
        # print(product_bsr)
        # print('############################\n')

        all_products.append({
            'Link': product_link,
            'Asin': product_asin,
            'Title': product_title,
            'Price': product_price,
            'Rating_value': product_rating_value,
            'Rating_count': product_rating_count,
            'BSR': product_bsr,

        })

        counter += 1
    
    all_products_global.append({f'{categorie}': all_products})



    #BUSINESS LOGIC

    price_sum = 0
    bsr_sum = 0
    rating_value_sum = 0
    rating_count_sum = 0

    products_with_bsr = 0
    products_with_rating_value = 0
    products_with_rating_count = 0

    for product in all_products:
        try:
            price_sum += product['Price']
        except:
            pass

        try:
            bsr_sum += product['BSR']
            products_with_bsr += 1    
        except:
            pass
        try:
            rating_value_sum += product['Rating_value']
            products_with_rating_value += 1
        except:
            pass
        try:
            rating_count_sum += product['Rating_count']
            products_with_rating_count += 1
        except:
            pass

    avg_price = round(price_sum/len(all_products),2)
    
    avg_bsr_relative = int(bsr_sum/products_with_bsr)
    avg_bsr_absolute = int(bsr_sum/len(all_products))
    products_with_bsr = ''.join(str(round((products_with_bsr/len(all_products))*100,2)) + '%')

    products_with_rating = ''.join(str(round((products_with_rating_value/len(all_products))*100,2)) + '%')

    avg_rating_value_relative = round(rating_value_sum/products_with_rating_value,2)
    avg_rating_value_absolute = round(rating_value_sum/len(all_products),2)

    avg_rating_count_relative = round(rating_count_sum/products_with_rating_count,2)
    avg_rating_count_absolute = round(rating_count_sum/len(all_products),2)

    niche_ranking.append({
        'ProductsCompetition': search_result_count_value,
        'Price': avg_price,
        'BSR': {
            'BSR relative': avg_bsr_relative,
            'BSR absolute': avg_bsr_absolute,
            'BSR percantage': products_with_bsr
        },
        'Rating Percantage': products_with_rating,
        'Rating Value': {
            'Rating Value relative': avg_rating_value_relative,
            'Rating Value absolute': avg_rating_value_absolute
        },
        'Rating Count': {
            'Rating Count relative': avg_rating_count_relative,
            'Rating Count absolute': avg_rating_count_absolute,
        }
    })

    all_niche_rankings.append({
        f'{categorie}': niche_ranking
    })







# print(all_products_global)
print(all_niche_rankings)



with open('niche_rankings.json', 'w', encoding='utf-8') as f:
    json.dump(all_niche_rankings, f, ensure_ascii=False)

# with open('all-products.json', 'w', encoding='utf-8') as f:
#     json.dump(all_products_global, f, ensure_ascii=False)

driver.close()




