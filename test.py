import json

with open('all-products.json',encoding='utf-8') as json_file:
    all_products = json.load(json_file)


all_products = all_products[0]['Fußball']
# print(all_products)

all_products_without_null = []

for product in all_products:
    if product['BSR'] is not None:
        all_products_without_null.append(product)

all_products_without_null = sorted(all_products_without_null, key=lambda i: i['BSR'])

print(all_products_without_null[0:5])


with open('test-best-products.json', 'w', encoding='utf-8') as f:
    json.dump(all_products_without_null, f, ensure_ascii=False)

