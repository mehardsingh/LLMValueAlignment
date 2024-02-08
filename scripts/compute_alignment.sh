#!/bin/bash

model_list=(
    "Llama-2-7b-chat-hf"
    "Llama-2-13b-chat-hf"
    "bloomz-3b"
    "bloomz-7b1"
    "falcon-7b-instruct"
)

  for model in "${model_list[@]}"
  do
    echo "Processing $model"
    python src/alignment/compute_alignment.py --result_dir results/$model \
      --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json \
      --output_fp analysis_metrics/alignment/alignment_$model.csv
  done