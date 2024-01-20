# python src/probe_model/probe.py --dataset_fp wvs_data/questionaire/clean_wvs.csv --prompt_template_fp src/prompt_templates/llama2/pt2.txt --model_name meta-llama/Llama-2-7b-chat-hf --get_probs True --result_fp results/llama2-7b-chat/results_pt2.csv

from probe_utils import *
import argparse

def main(dataset_fp, prompt_template_fp, model_name, get_probs, result_fp):
    prompt_inputs, dataset = get_prompt_inputs(dataset_fp, prompt_template_fp)
    all_outputs, all_prompts = query_model(model_name, prompt_inputs, get_probs)
    save_result(all_outputs, all_prompts, dataset, result_fp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_fp", type=str)
    parser.add_argument("--prompt_template_fp", type=str)
    parser.add_argument("--model_name", type=str)
    parser.add_argument("--get_probs", type=bool)
    parser.add_argument("--result_fp", type=str)
    args = parser.parse_args()

    main(
        args.dataset_fp, 
        args.prompt_template_fp, 
        args.model_name, 
        args.get_probs, 
        args.result_fp
    )