import json
import argparse

with open("country_codes/country_codes_messy.txt", mode="r", encoding='utf-8-sig') as f:
    country_codes_messy = f.readlines()

countries = list()
codes = list()

for line in country_codes_messy:
    line = line.strip()
    elems = line.split(" ")
    elems = [e.strip() for e in elems if not e.isspace()]
    
    code = int(elems[0])
    country = " ".join(elems[1:])

    countries.append(country)
    codes.append(code)

country2code = dict(zip(countries, codes))
code2country = dict(zip(codes, countries))

with open("code2country.json", 'w') as json_file:
    json.dump(code2country, json_file, indent=4)

with open("country2code.json", 'w') as json_file:
    json.dump(country2code, json_file, indent=4)