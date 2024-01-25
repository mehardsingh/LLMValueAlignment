module load python/3.9.12 cuda
pushd /home/mehars/LLMValueAlignment
source ./myenv/bin/activate

python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt1.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --section 1 --output_fp analysis_metrics/Llama-2-7b-chat-hf/by_section/alignment_pt1_s1.csv
python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt1.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --section 2 --output_fp analysis_metrics/Llama-2-7b-chat-hf/by_section/alignment_pt1_s2.csv
python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt1.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --section 3 --output_fp analysis_metrics/Llama-2-7b-chat-hf/by_section/alignment_pt1_s3.csv
python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt1.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --section 4 --output_fp analysis_metrics/Llama-2-7b-chat-hf/by_section/alignment_pt1_s4.csv
python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt1.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --section 5 --output_fp analysis_metrics/Llama-2-7b-chat-hf/by_section/alignment_pt1_s5.csv
python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt1.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --section 6 --output_fp analysis_metrics/Llama-2-7b-chat-hf/by_section/alignment_pt1_s6.csv
python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt1.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --section 7 --output_fp analysis_metrics/Llama-2-7b-chat-hf/by_section/alignment_pt1_s7.csv
python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt1.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --section 8 --output_fp analysis_metrics/Llama-2-7b-chat-hf/by_section/alignment_pt1_s8.csv
python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt1.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --output_fp analysis_metrics/Llama-2-7b-chat-hf/overall/alignment_pt1.csv

python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt2.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --section 1 --output_fp analysis_metrics/Llama-2-7b-chat-hf/by_section/alignment_pt2_s1.csv
python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt2.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --section 2 --output_fp analysis_metrics/Llama-2-7b-chat-hf/by_section/alignment_pt2_s2.csv
python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt2.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --section 3 --output_fp analysis_metrics/Llama-2-7b-chat-hf/by_section/alignment_pt2_s3.csv
python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt2.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --section 4 --output_fp analysis_metrics/Llama-2-7b-chat-hf/by_section/alignment_pt2_s4.csv
python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt2.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --section 5 --output_fp analysis_metrics/Llama-2-7b-chat-hf/by_section/alignment_pt2_s5.csv
python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt2.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --section 6 --output_fp analysis_metrics/Llama-2-7b-chat-hf/by_section/alignment_pt2_s6.csv
python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt2.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --section 7 --output_fp analysis_metrics/Llama-2-7b-chat-hf/by_section/alignment_pt2_s7.csv
python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt2.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --section 8 --output_fp analysis_metrics/Llama-2-7b-chat-hf/by_section/alignment_pt2_s8.csv
python src/analysis/compute_alignment.py --llm_res_fp results/Llama-2-7b-chat-hf/results_pt2.csv --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --output_fp analysis_metrics/Llama-2-7b-chat-hf/overall/alignment_pt2.csv