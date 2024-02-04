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

# python src/analysis/plot_alignment.py --in_align_fp analysis_metrics/alignment/alignment_Llama-2-7b-chat-hf.csv --out_align_fp analysis_metrics/alignment_plots/alignment_Llama-2-7b-chat-hf.png
# python src/analysis/plot_alignment.py --in_align_fp analysis_metrics/alignment/alignment_Llama-2-13b-chat-hf.csv --out_align_fp analysis_metrics/alignment_plots/alignment_Llama-2-13b-chat-hf.png
# python src/analysis/plot_alignment.py --in_align_fp analysis_metrics/alignment/alignment_bloomz-1b1.csv --out_align_fp analysis_metrics/alignment_plots/alignment_bloomz-1b1.png
# python src/analysis/plot_alignment.py --in_align_fp analysis_metrics/alignment/alignment_bloomz-1b7.csv --out_align_fp analysis_metrics/alignment_plots/alignment_bloomz-1b7.png
# python src/analysis/plot_alignment.py --in_align_fp analysis_metrics/alignment/alignment_bloomz-3b.csv --out_align_fp analysis_metrics/alignment_plots/alignment_bloomz-3b.png
# python src/analysis/plot_alignment.py --in_align_fp analysis_metrics/alignment/alignment_bloomz-7b1.csv --out_align_fp analysis_metrics/alignment_plots/alignment_bloomz-7b1.png
# python src/analysis/plot_alignment.py --in_align_fp analysis_metrics/alignment/alignment_falcon-7b-instruct.csv --out_align_fp analysis_metrics/alignment_plots/alignment_falcon-7b-instruct.png

# python src/analysis/compute_spearman.py --in_align_fp analysis_metrics/alignment/alignment_Llama-2-7b-chat-hf.csv --out_fp analysis_metrics/spearman_plots/spearman_Llama-2-7b-chat-hf.png
# python src/analysis/compute_spearman.py --in_align_fp analysis_metrics/alignment/alignment_Llama-2-13b-chat-hf.csv --out_fp analysis_metrics/spearman_plots/spearman_Llama-2-13b-chat-hf.png
# python src/analysis/compute_spearman.py --in_align_fp analysis_metrics/alignment/alignment_bloomz-1b1.csv --out_fp analysis_metrics/spearman_plots/spearman_bloomz-1b1.png
# python src/analysis/compute_spearman.py --in_align_fp analysis_metrics/alignment/alignment_bloomz-1b7.csv --out_fp analysis_metrics/spearman_plots/spearman_bloomz-1b7.png
# python src/analysis/compute_spearman.py --in_align_fp analysis_metrics/alignment/alignment_bloomz-3b.csv --out_fp analysis_metrics/spearman_plots/spearman_bloomz-3b.png
# python src/analysis/compute_spearman.py --in_align_fp analysis_metrics/alignment/alignment_bloomz-7b1.csv --out_fp analysis_metrics/spearman_plots/spearman_bloomz-7b1.png
# python src/analysis/compute_spearman.py --in_align_fp analysis_metrics/alignment/alignment_falcon-7b-instruct.csv --out_fp analysis_metrics/spearman_plots/spearman_falcon-7b-instruct.png

# continent alignment
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/continents --model Llama-2-7b-chat-hf --country2region src/analysis/country2continent.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/continents --model Llama-2-13b-chat-hf --country2region src/analysis/country2continent.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/continents --model bloomz-1b1 --country2region src/analysis/country2continent.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/continents --model bloomz-1b7 --country2region src/analysis/country2continent.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/continents --model bloomz-3b --country2region src/analysis/country2continent.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/continents --model bloomz-7b1 --country2region src/analysis/country2continent.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/continents --model falcon-7b-instruct --country2region src/analysis/country2continent.json

# # region alignment
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/regions --model Llama-2-7b-chat-hf --country2region src/analysis/country2region.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/regions --model Llama-2-13b-chat-hf --country2region src/analysis/country2region.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/regions --model bloomz-1b1 --country2region src/analysis/country2region.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/regions --model bloomz-1b7 --country2region src/analysis/country2region.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/regions --model bloomz-3b --country2region src/analysis/country2region.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/regions --model bloomz-7b1 --country2region src/analysis/country2region.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/regions --model falcon-7b-instruct --country2region src/analysis/country2region.json

# income alignment
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/income --model Llama-2-7b-chat-hf --country2region src/analysis/country2income.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/income --model Llama-2-13b-chat-hf --country2region src/analysis/country2income.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/income --model bloomz-1b1 --country2region src/analysis/country2income.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/income --model bloomz-1b7 --country2region src/analysis/country2income.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/income --model bloomz-3b --country2region src/analysis/country2income.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/income --model bloomz-7b1 --country2region src/analysis/country2income.json
# python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/income --model falcon-7b-instruct --country2region src/analysis/country2income.json

# quartile alignment
python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/quartile --model Llama-2-7b-chat-hf --country2region src/analysis/country2quartile.json
python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/quartile --model Llama-2-13b-chat-hf --country2region src/analysis/country2quartile.json
python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/quartile --model bloomz-1b1 --country2region src/analysis/country2quartile.json
python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/quartile --model bloomz-1b7 --country2region src/analysis/country2quartile.json
python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/quartile --model bloomz-3b --country2region src/analysis/country2quartile.json
python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/quartile --model bloomz-7b1 --country2region src/analysis/country2quartile.json
python src/analysis/compute_regional_alignment.py --regional_alignment_dir analysis_metrics/regional_alignment/quartile --model falcon-7b-instruct --country2region src/analysis/country2quartile.json

# python src/analysis/plot_regional_alignment2.py --country2region_fp src/analysis/country2continent.json --regional_alignment_dir analysis_metrics/regional_alignment/continents --out_dir analysis_metrics/regional_heatmaps/continent --section2title_fp wvs_data/section_name.json --y_label Continents
# python src/analysis/plot_regional_alignment2.py --country2region_fp src/analysis/country2region.json --regional_alignment_dir analysis_metrics/regional_alignment/regions --out_dir analysis_metrics/regional_heatmaps/region --section2title_fp wvs_data/section_name.json --y_label Regions
# python src/analysis/plot_regional_alignment2.py --country2region_fp src/analysis/country2income.json --regional_alignment_dir analysis_metrics/regional_alignment/income --out_dir analysis_metrics/regional_heatmaps/income --section2title_fp wvs_data/section_name.json --y_label "Avg. Income Level" --regions high upper-middle lower-middle low
python src/analysis/plot_regional_alignment2.py --country2region_fp src/analysis/country2quartile.json --regional_alignment_dir analysis_metrics/regional_alignment/quartile --out_dir analysis_metrics/regional_heatmaps/quartile --section2title_fp wvs_data/section_name.json --y_label "Income Quartile" --regions "Quartile 1" "Quartile 2" "Quartile 3" "Quartile 4"