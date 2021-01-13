import json

with open('all-niches.json') as json_file:
    niches = json.load(json_file)

with open('all-categories.json') as json_file:
    categories = json.load(json_file)

final_result = []
element = {}

for categorie in categories:
    for niche in niches:
        if categorie == niche:
            element = {f'categorie': }
            