import os
import pandas as pd
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import argparse

def save_spearman(in_align_fp, out_fp):
    alignment_df = pd.read_csv(in_align_fp)
    alignment_df = alignment_df[alignment_df["Section"] == "SectionsAvg"]

    num_prompts = alignment_df['Prompt'].nunique()
    spearman_heatmap = np.zeros((num_prompts, num_prompts))

    # A temporary fix
    prompt_idx = {0:1, 1:3, 2:5, 3:7, 4:9, 5:2, 6:4, 7:6, 8:8, 9:10, 10:11, 11:12, 12:13, 13:14, 14:15}

    for i in range(num_prompts):
        # p1_df =  alignment_df[alignment_df["Prompt"] == f"pt{i+1}"]
        p1_df = alignment_df[alignment_df["Prompt"] == f"pt{prompt_idx[i]}"]
        p1_df = p1_df[["Country", "Alignment"]]
        p1_df = p1_df.groupby('Country')['Alignment'].mean().reset_index()
        p1_df.columns = ['Country', 'Alignment']
        p1_alignment_scores = list(p1_df["Alignment"])

        for j in range(num_prompts):
            p2_df =  alignment_df[alignment_df["Prompt"] == f"pt{j+1}"]
            p2_df = p2_df[["Country", "Alignment"]]
            p2_df = p2_df.groupby('Country')['Alignment'].mean().reset_index()
            p2_df.columns = ['Country', 'Alignment']
            p2_alignment_scores = list(p2_df["Alignment"])

            spearman_heatmap[i][j] = spearmanr(p1_alignment_scores, p2_alignment_scores).statistic

    # Create heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(spearman_heatmap, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Spearman Correlation Coefficients')
    plt.xlabel(f'Prompts 1 to {num_prompts}')
    plt.ylabel(f'Prompts 1 to {num_prompts}')

    # plt.xticks(ticks=range(1, num_prompts + 1), labels=range(1, num_prompts + 1))
    # plt.yticks(ticks=range(1, num_prompts + 1), labels=range(1, num_prompts + 1))

    plt.xticks(ticks=[i + 0.5 for i in range(num_prompts)], labels=range(1, num_prompts + 1))
    plt.yticks(ticks=[i + 0.5 for i in range(num_prompts)], labels=range(1, num_prompts + 1))

    plt.savefig(out_fp)


def write_average_alignment(folder_path):

    # Get all CSV files in the folder
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    # Iterate over each CSV file
    dfs = []
    for file in csv_files:
        file_path = os.path.join(folder_path, file)

        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Append the DataFrame to the list
        dfs.append(df)

    # Concatenate all DataFrames into a single DataFrame
    concatenated_df = pd.concat(dfs)

    # Group the rows by the first three columns and calculate the average for each group
    grouped_df = concatenated_df.groupby(['Country', 'Prompt', 'Section']).mean()

    grouped_df.to_csv(os.path.join(folder_path, 'alignment_all_models.csv'), index=True, header=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_align_fp", type=str)
    parser.add_argument("--out_fp", type=str)
    args = parser.parse_args()

    if not args.in_align_fp and not args.out_fp:
        folder_path = "analysis_metrics"
        write_average_alignment(os.path.join(folder_path, "alignment"))
        save_spearman(os.path.join(folder_path, "alignment", "alignment_all_models.csv"),
                      os.path.join(folder_path, "spearman_plots" ,"spearman_all_models.png"))
    else:
        save_spearman(args.in_align_fp, args.out_fp)

