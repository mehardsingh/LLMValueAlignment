import pandas as pd
from collections import Counter
from tqdm import tqdm
import json
import argparse


def main():
    wvs_gt = pd.read_csv("filtered_wvs_gt.csv")
    with open("country_codes/code2country.json", 'r') as json_file:
        code2country = json.load(json_file)
        print(code2country)
        code2country = {int(key): value for key, value in code2country.items()}

    country_ids = set(wvs_gt["B_COUNTRY"])
    question_ids = [col for col in wvs_gt.columns if not col == "B_COUNTRY"]
    
    wvs_gt_dict = dict()
    for country_id in tqdm(country_ids):
        try:
            country = code2country[country_id]
        except Exception as _:
            country = "Unknown"
        
        wvs_gt_dict[country] = dict()
        country_answers = wvs_gt[wvs_gt["B_COUNTRY"] == country_id][question_ids]
        
        for question_id in question_ids:
            country_question_answers = list(country_answers[question_id])
            country_question_answer_freq = dict(Counter(country_question_answers))
            wvs_gt_dict[country][question_id] = country_question_answer_freq

    with open("wvs_gt_by_country.json", 'w') as json_file:
        json.dump(wvs_gt_dict, json_file, indent=4)

    




if __name__ == "__main__":
    main()

