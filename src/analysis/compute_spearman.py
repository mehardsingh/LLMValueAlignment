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

    for i in range(num_prompts):
        p1_df =  alignment_df[alignment_df["Prompt"] == f"pt{i+1}"]
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_align_fp", type=str)
    parser.add_argument("--out_fp", type=str)
    args = parser.parse_args()

    save_spearman(args.in_align_fp, args.out_fp)

