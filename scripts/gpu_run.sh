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
python src/probe_model/probe_all_prompts.py --dataset_fp wvs_data/questionaire/clean_wvs.csv --prompt_dir src/prompt_templates/Llama-2-7b-chat-hf --model_name meta-llama/Llama-2-7b-chat-hf --result_dir results/Llama-2-7b-chat-hf