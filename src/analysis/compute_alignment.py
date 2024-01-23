# python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt1.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --section 2 --output_fp country_opinion_alignments_pt1_s2.csv

from scipy.stats import wasserstein_distance as wd 
import pandas as pd
import math
import numpy as np
import json
from tqdm import tqdm
import argparse

# TODO: hedging

letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum(axis=0)

def compute_wasserstein_dist(answer_dist1, answer_dist2):
    answer_choice_values = list(range(len(answer_dist1)))
    distance = wd(answer_choice_values, answer_choice_values, u_weights=answer_dist1, v_weights=answer_dist2)
    return distance

def compute_question_alignment(answer_dist1, answer_dist2):
    distance = compute_wasserstein_dist(answer_dist1, answer_dist2)
    return 1 - (distance / (len(answer_dist1) - 1))

def compute_opinion_alignment(llm_responses, human_responses):
    opinion_alignment = 0
    count = 0
    for i in range(len(llm_responses)):
        if human_responses[i] == None:
            continue
        else:
            opinion_alignment += compute_question_alignment(llm_responses[i], human_responses[i])
            count += 1

    opinion_alignment /= count
    return opinion_alignment

def load_llm_responses(llm_res_fp, section):
    llm_res_df = pd.read_csv(llm_res_fp)
    llm_res_df = llm_res_df[llm_res_df["Ordinal"] == True]

    if section:
        llm_res_df = llm_res_df[llm_res_df["Section"] == section]

    out_cols = [f"{l}_out" for l in letters]
    cols = ["ID", "OneIndex"] + out_cols
    llm_res_df = llm_res_df[cols]

    question_ids = list(llm_res_df["ID"])
    one_indices = list(llm_res_df["OneIndex"])
    llm_responses = list()
    for question_id in question_ids:
        response = llm_res_df[llm_res_df["ID"] == question_id][out_cols].values[0]
        response = [r for r in response if not math.isnan(r)]
        response = list(softmax(response))
        llm_responses.append(response)

    num_choices = [len(llm_responses[i]) for i in range(len(llm_responses))]

    return question_ids, one_indices, llm_responses, num_choices

def load_country_responses(country_response_dict, question_ids, one_indices, num_choices):
    country_responses = list()
    for i in range(len(question_ids)):
        question_id = question_ids[i]
        question_response = country_response_dict[question_id]
        question_response = {int(key): value for key, value in question_response.items()}

        min_answer = 1 if one_indices[i] else 0
        question_response_all_choices = {key: 0 for key in range(min_answer, min_answer + num_choices[i])}
        question_response = {key: value for key, value in question_response.items() if key >= min_answer} # remove all answer choices < min_answer
        question_response_all_choices.update(question_response)
    
        question_response_all_choices = [question_response_all_choices[key] for key in sorted(question_response_all_choices.keys())] # sort by answer choice
        question_response_all_choices = [r / sum(question_response_all_choices) for r in question_response_all_choices] if not sum(question_response_all_choices) == 0 else None
        country_responses.append(question_response_all_choices)

    return country_responses

def save_all_alignment_scores(llm_res_fp, country_res_fp, section, output_fp):
    question_ids, one_indices, llm_responses, num_choices = load_llm_responses(llm_res_fp, section)

    with open(country_res_fp) as f:
        country_responses_dict = json.load(f)

    countries = list(country_responses_dict.keys())
    alignments = list()
    for country in tqdm(countries):
        country_response_dict = country_responses_dict[country]
        country_responses = load_country_responses(country_response_dict, question_ids, one_indices, num_choices)
        alignment = compute_opinion_alignment(llm_responses, country_responses)
        alignments.append(alignment)

    alignment_df = pd.DataFrame({'Country': countries, 'Alignment': alignments})
    alignment_df.to_csv(output_fp, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm_res_fp", type=str)
    parser.add_argument("--country_res_fp", type=str)
    parser.add_argument("--section", type=int, default=None)
    parser.add_argument("--output_fp", type=str)
    args = parser.parse_args()
        
    save_all_alignment_scores(args.llm_res_fp, args.country_res_fp, args.section, args.output_fp)
