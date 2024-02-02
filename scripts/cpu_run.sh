module load python/3.9.12 cuda
pushd /home/mehars/LLMValueAlignment
source ./myenv/bin/activate

# python src/analysis/compute_alignment.py --llm_res_dir results/Llama-2-7b-chat-hf --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --output_fp analysis_metrics/alignment/alignment_Llama-2-7b-chat-hf.csv
# python src/analysis/compute_alignment.py --llm_res_dir results/Llama-2-13b-chat-hf --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --output_fp analysis_metrics/alignment/alignment_Llama-2-13b-chat-hf.csv
# python src/analysis/compute_alignment.py --llm_res_dir results/bloomz-1b1 --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --output_fp analysis_metrics/alignment/alignment_bloomz-1b1.csv
# python src/analysis/compute_alignment.py --llm_res_dir results/bloomz-1b7 --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --output_fp analysis_metrics/alignment/alignment_bloomz-1b7.csv
# python src/analysis/compute_alignment.py --llm_res_dir results/bloomz-3b --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --output_fp analysis_metrics/alignment/alignment_bloomz-3b.csv
# python src/analysis/compute_alignment.py --llm_res_dir results/bloomz-7b1 --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --output_fp analysis_metrics/alignment/alignment_bloomz-7b1.csv
# python src/analysis/compute_alignment.py --llm_res_dir results/falcon-7b-instruct --country_res_fp wvs_data/gt_responses/wvs_gt_by_country.json --output_fp analysis_metrics/alignment/alignment_falcon-7b-instruct.csv

python src/analysis/plot_alignment.py --in_align_fp analysis_metrics/alignment/alignment_Llama-2-7b-chat-hf.csv --out_align_fp analysis_metrics/alignment_plots/alignment_Llama-2-7b-chat-hf.png
python src/analysis/plot_alignment.py --in_align_fp analysis_metrics/alignment/alignment_Llama-2-13b-chat-hf.csv --out_align_fp analysis_metrics/alignment_plots/alignment_Llama-2-13b-chat-hf.png
python src/analysis/plot_alignment.py --in_align_fp analysis_metrics/alignment/alignment_bloomz-1b1.csv --out_align_fp analysis_metrics/alignment_plots/alignment_bloomz-1b1.png
python src/analysis/plot_alignment.py --in_align_fp analysis_metrics/alignment/alignment_bloomz-1b7.csv --out_align_fp analysis_metrics/alignment_plots/alignment_bloomz-1b7.png
python src/analysis/plot_alignment.py --in_align_fp analysis_metrics/alignment/alignment_bloomz-3b.csv --out_align_fp analysis_metrics/alignment_plots/alignment_bloomz-3b.png
python src/analysis/plot_alignment.py --in_align_fp analysis_metrics/alignment/alignment_bloomz-7b1.csv --out_align_fp analysis_metrics/alignment_plots/alignment_bloomz-7b1.png
python src/analysis/plot_alignment.py --in_align_fp analysis_metrics/alignment/alignment_falcon-7b-instruct.csv --out_align_fp analysis_metrics/alignment_plots/alignment_falcon-7b-instruct.png

python src/analysis/compute_spearman.py --in_align_fp analysis_metrics/alignment/alignment_Llama-2-7b-chat-hf.csv --out_fp analysis_metrics/spearman_plots/spearman_Llama-2-7b-chat-hf.png
python src/analysis/compute_spearman.py --in_align_fp analysis_metrics/alignment/alignment_Llama-2-13b-chat-hf.csv --out_fp analysis_metrics/spearman_plots/spearman_Llama-2-13b-chat-hf.png
python src/analysis/compute_spearman.py --in_align_fp analysis_metrics/alignment/alignment_bloomz-1b1.csv --out_fp analysis_metrics/spearman_plots/spearman_bloomz-1b1.png
python src/analysis/compute_spearman.py --in_align_fp analysis_metrics/alignment/alignment_bloomz-1b7.csv --out_fp analysis_metrics/spearman_plots/spearman_bloomz-1b7.png
python src/analysis/compute_spearman.py --in_align_fp analysis_metrics/alignment/alignment_bloomz-3b.csv --out_fp analysis_metrics/spearman_plots/spearman_bloomz-3b.png
python src/analysis/compute_spearman.py --in_align_fp analysis_metrics/alignment/alignment_bloomz-7b1.csv --out_fp analysis_metrics/spearman_plots/spearman_bloomz-7b1.png
python src/analysis/compute_spearman.py --in_align_fp analysis_metrics/alignment/alignment_falcon-7b-instruct.csv --out_fp analysis_metrics/spearman_plots/spearman_falcon-7b-instruct.png
