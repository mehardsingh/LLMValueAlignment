#!/bin/bash

#SBATCH --partition=spgpu
#SBATCH --gpus=1
#SBATCH --cpus-per-gpu=8
#SBATCH --mem-per-gpu=128GB
#SBATCH --account=mihalcea0
#SBATCH --time=00-08:00:00 

# set up job
module load python/3.9.12 cuda
pushd /home/mehars/LLMValueAlignment
source ./myenv/bin/activate

# run job
python src/probe_model/probe.py --dataset_fp wvs_data/questionaire/clean_wvs.csv --prompt_template_fp src/prompt_templates/llama2/pt1.txt --model_name meta-llama/Llama-2-7b-chat-hf --result_fp results/Llama-2-7b-chat-hf/results_pt1.csv
python src/probe_model/probe.py --dataset_fp wvs_data/questionaire/clean_wvs.csv --prompt_template_fp src/prompt_templates/llama2/pt2.txt --model_name meta-llama/Llama-2-7b-chat-hf --result_fp results/Llama-2-7b-chat-hf/results_pt2.csv