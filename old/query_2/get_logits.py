from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import transformers
import torch
import json
import pandas as pd
import numpy as np
from tqdm import tqdm

def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum(axis=0)

prompt_num = 2
with open(f"query_2/prompt_template{prompt_num}.txt", mode="r") as f:
    prompt_template = f.read() 

dataset = pd.read_csv("data/wvs_dataset2.csv", dtype=str)
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
prompt_inputs = list()

for i in range(len(dataset)):
    question_info = dataset.iloc[i]

    question = question_info["Question"]
    answer_choices = list(question_info[letters])
    answer_choices = [ac for ac in answer_choices if pd.notna(ac)]
    answer_choices = [f"{letters[j]}. {answer_choices[j]}" for j in range(len(answer_choices)) if type(answer_choices[j]) == str]
    answer_choices_str = "\n".join(answer_choices)

    prompt = prompt_template.replace("[Q]", question)
    prompt = prompt.replace("[ANSWER_CHOICES]", answer_choices_str)
    prompt_inputs.append({"ID": question_info["ID"], "prompt": prompt, "num_choices": len(answer_choices)})

device = "cuda:0" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf").to(device)

all_probs = list()
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

    # probs = list(softmax(answer_choice_logits))
    probs = answer_choice_logits
    probs = probs[:len(probs) - 1] + [None] * (10 - len(probs) + 1) + [probs[-1]]
    all_probs.append(probs)
    all_prompts.append(prompt)

response_options = letters + ["Z"]
results = pd.DataFrame(all_probs, columns=[f"{l}_prob" for l in response_options])
results = pd.concat([dataset, results], axis=1)
results["Prompt"] = all_prompts
results.to_csv(f"query_2/logits{prompt_num}''.csv")