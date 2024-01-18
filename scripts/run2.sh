#!/bin/bash

#SBATCH --partition=spgpu
#SBATCH --gpus=1
#SBATCH --cpus-per-gpu=8
#SBATCH --mem-per-gpu=128GB
#SBATCH --account=mihalcea0
#SBATCH --time=00-08:00:00 

# set up job
module load python cuda
pushd /home/mehars/LLMValueAlignment
source .venv/bin/activate

pip install torch
pip install transformers
pip install datasets
pip install tqdm
pip install numpy
# pip install evaluate
# pip install scikit-learn
# pip install peft

# run job
python test.py