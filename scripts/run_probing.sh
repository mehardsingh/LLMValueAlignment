#!/bin/bash

# run job
# python src/probe_model/probe_all_prompts.py --dataset_fp wvs_data/questionaire/clean_wvs.csv --prompt_dir src/prompt_templates/Llama-2 --model_name meta-llama/Llama-2-7b-chat-hf --result_dir results/Llama-2-7b-chat-hf
# python src/probe_model/probe_all_prompts.py --dataset_fp wvs_data/questionaire/clean_wvs.csv --prompt_dir src/prompt_templates/Llama-2 --model_name meta-llama/Llama-2-13b-chat-hf --result_dir results/Llama-2-13b-chat-hf
# python src/probe_model/probe_all_prompts.py --dataset_fp wvs_data/questionaire/clean_wvs.csv --prompt_dir src/prompt_templates/without_system_prompt --model_name bigscience/bloomz-3b --result_dir results/bloomz-3b
# python src/probe_model/probe_all_prompts.py --dataset_fp wvs_data/questionaire/clean_wvs.csv --prompt_dir src/prompt_templates/without_system_prompt --model_name bigscience/bloomz-7b1 --result_dir results/bloomz-7b1
python src/probe_model/probe_all_prompts.py --dataset_fp wvs_data/questionaire/clean_wvs.csv --prompt_dir src/prompt_templates/without_system_prompt --model_name tiiuae/falcon-7b-instruct --result_dir results/falcon-7b-instruct
#python src/probe_model/probe_all_prompts.py --dataset_fp wvs_data/questionaire/clean_wvs.csv --prompt_dir src/prompt_templates/without_system_prompt --model_name tiiuae/falcon-40b-instruct --result_dir tiiuae/falcon-40b-instruct
#python src/probe_model/probe_all_prompts.py --dataset_fp wvs_data/questionaire/clean_wvs.csv --prompt_dir src/prompt_templates/Mistral --model_name mistralai/Mistral-7B-Instruct-v0.2 --result_dir results/Mistral-7B-Instruct-v0.2