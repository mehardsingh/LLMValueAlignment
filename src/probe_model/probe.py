# depracated, check for correctness if using this
# python src/probe_model/probe.py --dataset_fp wvs_data/questionaire/clean_wvs.csv --prompt_template_fp src/prompt_templates/llama2/pt2.txt --model_name meta-llama/Llama-2-7b-chat-hf --get_probs True --result_fp results/llama2-7b-chat/results_pt2.csv

from probe_utils import *
from transformers import AutoTokenizer, AutoModelForCausalLM
import argparse

device = "cuda:0" if torch.cuda.is_available() else "cpu"

def probe_model(dataset_fp, prompt_template_fp, model_name, get_probs, result_fp):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

    prompt_inputs, dataset = get_prompt_inputs(dataset_fp, prompt_template_fp)
    all_outputs, all_prompts, all_responses = query_model(model, tokenizer, device, prompt_inputs, get_probs)
    save_result(all_outputs, all_prompts, all_responses, dataset, result_fp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_fp", type=str)
    parser.add_argument("--prompt_template_fp", type=str)
    parser.add_argument("--model_name", type=str)
    parser.add_argument('--softmax', action=argparse.BooleanOptionalAction)
    parser.add_argument("--result_fp", type=str)
    args = parser.parse_args()

    probe_model(
        args.dataset_fp, 
        args.prompt_template_fp, 
        args.model_name, 
        args.softmax, 
        args.result_fp
    )