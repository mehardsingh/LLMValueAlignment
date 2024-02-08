from probe_utils import *
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import argparse

device = "cuda:0" if torch.cuda.is_available() else "cpu"

def get_all_filepaths(directory):
    file_paths = [os.path.join(directory, filename) for filename in os.listdir(directory) if os.path.isfile(os.path.join(directory, filename))]
    return file_paths

def probe_all_prompts(dataset_fp, prompt_dir, model_name, get_probs, result_dir):

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map='auto')

    prompt_fps = get_all_filepaths(prompt_dir)
    for i in range(len(prompt_fps)):
        prompt_fp = os.path.join(prompt_dir, f"pt{i+1}.txt")
        prompt_inputs, dataset = get_prompt_inputs(dataset_fp, prompt_fp)
        all_outputs, all_prompts, all_responses = query_model(model, tokenizer, prompt_inputs, get_probs)
        save_result(all_outputs, all_prompts, all_responses, dataset, os.path.join(result_dir, f"results_pt{i+1}.csv"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_fp", type=str)
    parser.add_argument("--prompt_dir", type=str)
    parser.add_argument("--model_name", type=str)
    parser.add_argument('--softmax', action=argparse.BooleanOptionalAction)
    parser.add_argument("--result_dir", type=str)
    args = parser.parse_args()

    probe_all_prompts(
        args.dataset_fp, 
        args.prompt_dir, 
        args.model_name, 
        args.softmax, 
        args.result_dir
    )