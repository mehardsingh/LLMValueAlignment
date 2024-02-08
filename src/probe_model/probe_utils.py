from transformers import pipeline
import torch
import pandas as pd
import numpy as np
import logging

logging.basicConfig(filename='probe.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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

def query_model(model, tokenizer, prompt_inputs, get_probs):
    logging.info("Inside query_model()")

    generator = pipeline("text-generation", model=model, tokenizer=tokenizer, )
    all_inputs_responses = generator([p["prompt"] for p in prompt_inputs], max_new_tokens=10)
    all_inputs_responses = [r[0]["generated_text"] for r in all_inputs_responses]

    all_responses = list()
    for i in range(len(all_inputs_responses)):
        input_response = all_inputs_responses[i]
        prompt = prompt_inputs[i]["prompt"]
        response = input_response[len(prompt):].strip()
        all_responses.append(response)

    logging.info("got text responses")

    all_outputs = list()
    all_prompts = list()

    for i in range(len(prompt_inputs)):
        prompt_input = prompt_inputs[i]
        prompt = prompt_input["prompt"]
        num_choices = prompt_input["num_choices"]

        input = tokenizer(prompt, return_tensors="pt").to("cuda")

        with torch.no_grad():
            outputs = model(**input)
        
        next_token_logits = outputs.logits[0, -1, :]
        answer_choice_logits = list()

        for letter in letters[:num_choices] + ["Z"]:
            token_id = tokenizer.convert_tokens_to_ids(letter)
            token_logits = next_token_logits[token_id].item()
            answer_choice_logits.append(token_logits)

        logging.info("got next_token logits")

        output_nums = list(softmax(answer_choice_logits)) if get_probs else answer_choice_logits
        output_nums = output_nums[:len(output_nums) - 1] + [None] * (10 - len(output_nums) + 1) + [output_nums[-1]]

        logging.info("got outputs")

        all_outputs.append(output_nums)
        all_prompts.append(prompt)

        logging.info("appending")

    logging.info("got all outputs")

    return all_outputs, all_prompts, all_responses

def save_result(all_outputs, all_prompts, all_responses, dataset, result_fp):
    response_options = letters + ["Z"]
    results = pd.DataFrame(all_outputs, columns=[f"{l}_out" for l in response_options])
    results = pd.concat([dataset, results], axis=1)

    results["Prompt"] = all_prompts
    results["TextResponse"] = all_responses
    
    results.to_csv(result_fp)
    logging.info(f"Saved to {result_fp}")