# python src/preprocess/create_code_dicts.py --country_codes_fp wvs_data/country_codes/country_codes_messy.txt --code2country_fp wvs_data/country_codes/code2country.json --country2code_fp wvs_data/country_codes/country2code.json

import json
import argparse

def main(country_codes_fp, code2country_fp, country2code_fp):
    with open(country_codes_fp, mode="r", encoding='utf-8-sig') as f:
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

    with open(code2country_fp, 'w') as json_file:
        json.dump(code2country, json_file, indent=4)

    with open(country2code_fp, 'w') as json_file:
        json.dump(country2code, json_file, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--country_codes_fp", type=str)
    parser.add_argument("--code2country_fp", type=str)
    parser.add_argument("--country2code_fp", type=str)
    args = parser.parse_args()