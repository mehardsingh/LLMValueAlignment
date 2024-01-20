# python src/preprocess/save_country_aggs.py --wvs_gt_fp wvs_data/gt_responses/WVS_Cross-National_Wave_7_csv_v5_0.csv --filtered_fp wvs_data/gt_responses/filtered_WVS_Cross-National_Wave_7_csv_v5_0.csv --code2country_fp wvs_data/country_codes/code2country.json --output_fp wvs_data/gt_responses/wvs_gt_by_country.json

import pandas as pd
from collections import Counter
from tqdm import tqdm
import json
import argparse

def filter_gt(wvs_gt_fp, filtered_fp):
    wvs_gt = pd.read_csv(wvs_gt_fp)
    cols = ["B_COUNTRY"] + [col for col in wvs_gt.columns if col.startswith('Q') and not col == "Q_MODE"]
    wvs_gt = wvs_gt[cols]
    wvs_gt.to_csv(filtered_fp, index=False)

def aggregate_country_gt(filtered_fp, code2country_fp, output_fp):
    wvs_gt = pd.read_csv(filtered_fp)
    with open(code2country_fp, 'r') as json_file:
        code2country = json.load(json_file)
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

    with open(output_fp, 'w') as json_file:
        json.dump(wvs_gt_dict, json_file, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--wvs_gt_fp", type=str)
    parser.add_argument("--filtered_fp", type=str)
    parser.add_argument("--code2country_fp", type=str)
    parser.add_argument("--output_fp", type=str)
    args = parser.parse_args()

    filter_gt(args.wvs_gt_fp, args.filtered_fp)
    aggregate_country_gt(args.filtered_fp, args.code2country_fp, args.output_fp)

