# python src/analysis/compute_alignment.py --llm_res_dir results/Llama-2-7b-chat-hf --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --output_fp analysis_metrics/alignment/alignment_Llama-2-7b-chat-hf.csv

from scipy.stats import wasserstein_distance as wd 
import pandas as pd
import math
import numpy as np
import json
from tqdm import tqdm
import argparse
import os
import ot

letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum(axis=0)

def compute_question_alignment(answer_dist1, answer_dist2, ordinal, hedge):
    num_vals = len(answer_dist1)

    if ordinal:
        if hedge:
            inner_cost_matrix = np.fromfunction(lambda i, j: np.abs(i - j), (num_vals-1, num_vals-1), dtype=np.float64)
            first_row = inner_cost_matrix[0]
            avg_val = np.mean(inner_cost_matrix[0])
            cost_matrix = np.zeros((num_vals, num_vals))
            cost_matrix[1:, 1:] = inner_cost_matrix
            cost_matrix[0, 1:] = np.abs(first_row - avg_val)
            cost_matrix[1:, 0] = np.abs(first_row - avg_val)
            # cost_matrix[0][1:] = np.abs(cost_matrix[0][1:] - np.mean(cost_matrix[0][1:]))
        else:
            # correct
            cost_matrix = np.fromfunction(lambda i, j: np.abs(i - j), (num_vals, num_vals), dtype=np.float64)
        
    else:
        cost_matrix = np.ones((num_vals, num_vals), dtype=np.float64)
        np.fill_diagonal(cost_matrix, 0) 

    distance = ot.emd2(np.array(answer_dist1, dtype=np.float64), np.array(answer_dist2, dtype=np.float64), cost_matrix)
    div = np.max(cost_matrix)
    question_alignment = 1 - (distance / div)
    # if not ordinal:
    #     print(question_alignment)
    return question_alignment

def compute_opinion_alignment(llm_responses, human_responses, ordinals, hedges):
    opinion_alignment = 0
    count = 0
    for i in range(len(llm_responses)):
        if human_responses[i] == None:
            continue
        else:
            opinion_alignment += compute_question_alignment(llm_responses[i], human_responses[i], ordinals[i], hedges[i])
            count += 1

    try:
        opinion_alignment /= count
    except Exception as e:
        opinion_alignment = np.nan

    return opinion_alignment

def load_llm_responses(llm_res_fp, section):
    llm_res_df = pd.read_csv(llm_res_fp)
    # llm_res_df = llm_res_df[llm_res_df["Ordinal"] == True]

    if section:
        llm_res_df = llm_res_df[llm_res_df["Section"] == section]

    out_cols = [f"{l}_out" for l in letters]
    cols = ["ID", "OneIndex", "Ordinal", "Hedge"] + out_cols
    llm_res_df = llm_res_df[cols]

    question_ids = list(llm_res_df["ID"])
    one_indices = list(llm_res_df["OneIndex"])
    ordinals = list(llm_res_df["Ordinal"])
    hedges = list(llm_res_df["Hedge"])

    llm_responses = list()
    for question_id in question_ids:
        response = llm_res_df[llm_res_df["ID"] == question_id][out_cols].values[0]
        response = [r for r in response if not math.isnan(r)]
        response = list(softmax(response))
        llm_responses.append(response)

    num_choices = [len(llm_responses[i]) for i in range(len(llm_responses))]

    return question_ids, one_indices, ordinals, hedges, llm_responses, num_choices

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

def get_all_country_alignment(llm_res_fp, country_res_fp, section):
    question_ids, one_indices, ordinals, hedges, llm_responses, num_choices = load_llm_responses(llm_res_fp, section)

    with open(country_res_fp) as f:
        country_responses_dict = json.load(f)

    countries = list(country_responses_dict.keys())
    alignments = list()
    for country in countries:
        country_response_dict = country_responses_dict[country]
        country_responses = load_country_responses(country_response_dict, question_ids, one_indices, num_choices)
        alignment = compute_opinion_alignment(llm_responses, country_responses, ordinals, hedges)
        alignments.append(alignment)

    return countries, alignments

# def save_all_prompts_alignment(llm_res_dir, country_res_fp, output_fp):
#     llm_res_fps = [os.path.join(llm_res_dir, filename) for filename in os.listdir(llm_res_dir) if os.path.isfile(os.path.join(llm_res_dir, filename))]

#     alignment_dict = dict()

#     for section in tqdm(range(0, 9)):
#         if section == 0:
#             section = None
#             col_name = "Overall"
#         else:
#             col_name = f"Section{section}"

#         all_prompt_alignments = list()
#         for i in range(len(llm_res_fps)):
#             llm_res_fp = llm_res_fps[i]

#             countries, alignments = get_all_country_alignment(llm_res_fp, country_res_fp, section)
#             all_prompt_alignments.append(alignments)

#         all_prompt_alignments = np.array(all_prompt_alignments)
#         all_prompt_alignments = np.mean(all_prompt_alignments, axis=0)

#         if not "Country" in alignment_dict:
#             alignment_dict["Country"] = countries
#         alignment_dict[col_name] = all_prompt_alignments
    
#     alignment_df = pd.DataFrame(alignment_dict)
#     alignment_df.to_csv(output_fp, index=False)

def save_all_prompts_alignment(llm_res_dir, country_res_fp, output_fp):
    llm_res_fps = [os.path.join(llm_res_dir, filename) for filename in os.listdir(llm_res_dir) if os.path.isfile(os.path.join(llm_res_dir, filename))]

    df_countries = list()
    df_prompts = list()
    df_sections = list()
    df_alignments = list()

    # go through sections
    for section in tqdm(range(0, 14)):
        if section == 0:
            section = None

        # go through prompts
        for i in range(len(llm_res_fps)):
            # llm_res_fp = llm_res_fps[i]
            llm_res_fp = os.path.join(llm_res_dir, f"results_pt{i+1}.csv")

            # get all countries & alignments
            countries, alignments = get_all_country_alignment(llm_res_fp, country_res_fp, section)

            N = len(countries)
            df_prompts += [f"pt{i+1}"] * N
            df_sections += [section if not section == None else "AllQuestions"] * N
            df_countries += countries
            df_alignments += alignments

    alignment_dict = {"Country": df_countries, "Prompt": df_prompts, "Section": df_sections, "Alignment": df_alignments}
    alignment_df = pd.DataFrame(alignment_dict)
    alignment_df.to_csv(output_fp, index=False)

def add_sections_average_col(output_fp):
    df = pd.read_csv(output_fp)
    df_removed = df[df['Section'] != 'AllQuestions']
    prompts = set(df_removed["Prompt"])

    results = list()
    for prompt in prompts:
        prompt_df = df_removed[df_removed["Prompt"] == prompt]
        result = prompt_df.groupby('Country')['Alignment'].mean().reset_index()
        result["Section"] = "SectionsAvg"
        result["Prompt"] = prompt
        results.append(result)

    appended = pd.concat([df] + results, ignore_index=True)
    appended.to_csv(output_fp, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm_res_dir", type=str)
    parser.add_argument("--country_res_fp", type=str)
    parser.add_argument("--output_fp", type=str)
    args = parser.parse_args()
        
    save_all_prompts_alignment(args.llm_res_dir, args.country_res_fp, args.output_fp)
    add_sections_average_col(args.output_fp)
