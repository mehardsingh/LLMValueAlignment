from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import pandas as pd
import numpy as np
from tqdm import tqdm

device = "cuda:0" if torch.cuda.is_available() else "cpu"
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum(axis=0)

def get_prompt_inputs(dataset_fp, prompt_template_fp):
    with open(prompt_template_fp, mode="r") as f:
        prompt_template = f.read() 

    dataset = pd.read_csv(dataset_fp, dtype=str)
    prompt_inputs = list()

    for i in range(len(dataset)):
        question_info = dataset.iloc[i]

        question = question_info["Question"]
        answer_choices = list(question_info[letters])
        answer_choices = [ac for ac in answer_choices if pd.notna(ac)]
        answer_choices = [f"{letters[j]}. {answer_choices[j]}" for j in range(len(answer_choices)) if type(answer_choices[j]) == str]
        answer_choices_str = "\n".join(answer_choices)

        prompt = prompt_template.replace("[QUESTION]", question)
        prompt = prompt.replace("[ANSWER_CHOICES]", answer_choices_str)
        prompt_inputs.append({"ID": question_info["ID"], "prompt": prompt, "num_choices": len(answer_choices)})

    return prompt_inputs, dataset

def query_model(model_name, prompt_inputs, get_probs):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

    all_outputs = list()
    all_prompts = list()
    for prompt_input in tqdm(prompt_inputs):
        prompt = prompt_input["prompt"]
        num_choices = prompt_input["num_choices"]

        input = tokenizer(prompt, return_tensors="pt").to(device)

        with torch.no_grad():
            outputs = model(**input)
        
        next_token_logits = outputs.logits[0, -1, :]
        answer_choice_logits = list()

        for letter in letters[:num_choices] + ["Z"]:
            token_id = tokenizer.convert_tokens_to_ids(letter)
            token_logits = next_token_logits[token_id].item()
            answer_choice_logits.append(token_logits)

        output_nums = list(softmax(answer_choice_logits)) if get_probs else answer_choice_logits
        output_nums = output_nums[:len(output_nums) - 1] + [None] * (10 - len(output_nums) + 1) + [output_nums[-1]]

        all_outputs.append(output_nums)
        all_prompts.append(prompt)

    return all_outputs, all_prompts

def save_result(all_outputs, all_prompts, dataset, result_fp):
    response_options = letters + ["Z"]
    results = pd.DataFrame(all_outputs, columns=[f"{l}_out" for l in response_options])
    results = pd.concat([dataset, results], axis=1)
    results["Prompt"] = all_prompts
    results.to_csv(result_fp)