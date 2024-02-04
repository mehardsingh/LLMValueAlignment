import pandas as pd
import os
import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

def row_normalize(matrix):
    # Compute mean and standard deviation of each row
    row_means = np.mean(matrix, axis=1)
    row_std = np.std(matrix, axis=1)

    # Subtract mean from each element and divide by standard deviation
    normalized_matrix = (matrix - row_means[:, np.newaxis]) / row_std[:, np.newaxis]

    return normalized_matrix

def plot_regional_alignment(country2region_fp, regional_alignment_dir, section2title_fp, out_dir, y_label, regions):
    with open(section2title_fp) as f:
        section2title = json.load(f)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    with open(country2region_fp, mode="r") as f:
        country2region = json.load(f)
    # regions = ["North America", "Latin America & Caribbean", "Europe", "Oceania", "East Asia & Pacific", "Eurasia or Eastern Europe", "North Africa & Middle East", "Sub-Saharan Africa", "South Asia"]
    if not regions:
        regions = set([v for k, v in country2region.items() if not v == "Other"])

    model_names = sorted(list(os.listdir(regional_alignment_dir)))

    sections = ["SectionsAvg", "AllQuestions"] + list(range(1, 14))
    for section in sections:
        title = section2title[str(section)] if str(section) in section2title else section
        heat_map = list()

        for model in model_names:
            model_alignments = list()
            for region in regions:
                if region == "Other":
                    continue
                regional_alignment_fp = os.path.join(regional_alignment_dir, model, f"{region.lower().replace(' ', '_')}.csv")
                regional_alignment_df = pd.read_csv(regional_alignment_fp)
                sections_avg_alignment = list(regional_alignment_df[regional_alignment_df["Section"] == str(section)]["Alignment"])[0]
                model_alignments.append(sections_avg_alignment)
                
            heat_map.append(model_alignments)

        heat_map = np.array(heat_map)

        normalized_matrix = row_normalize(heat_map)
        sns.heatmap(normalized_matrix.T, annot=True, fmt=".2f", cmap="RdBu")
        plt.xlabel("Models")
        plt.ylabel(y_label)
        plt.yticks(np.arange(heat_map.shape[1]) + 0.5, regions, rotation=0)
        plt.xticks(np.arange(heat_map.shape[0]) + 0.5, model_names, rotation=45, ha='right')
        plt.title(title)
        plt.tight_layout()

        plt.savefig(os.path.join(out_dir, f"section_{section}"))
        plt.clf()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--country2region_fp", type=str)
    parser.add_argument("--regional_alignment_dir", type=str)
    parser.add_argument("--out_dir", type=str)
    parser.add_argument("--section2title_fp", type=str)
    parser.add_argument("--y_label", type=str, default="Regions")
    parser.add_argument("--regions", nargs='+', type=str, default=None)
    args = parser.parse_args()

    plot_regional_alignment(args.country2region_fp, args.regional_alignment_dir, args.section2title_fp, args.out_dir, args.y_label, args.regions)

