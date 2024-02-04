import pandas as pd
import json
import os
import argparse

# models = ["Llama-2-7b-chat-hf", "Llama-2-13b-chat-hf", "bloomz-1b1", "bloomz-1b7", "bloomz-3b", "bloomz-7b1", "falcon-7b-instruct"]

def compute_regional_alignment(regional_alignment_dir, model, country2region):
    directory = os.path.join(regional_alignment_dir, model)
    
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(country2region, mode="r") as f:
        country2group = json.load(f)

    df = pd.read_csv(f"analysis_metrics/alignment/alignment_{model}.csv")

    df['Region'] = df['Country'].apply(lambda x: country2group[x])
    df = df[["Region", "Section", "Alignment"]]

    regional_alignment_df = df.groupby(['Region', 'Section']).mean().reset_index()

    regions = set(regional_alignment_df["Region"])
    for region in regions:
        region_folder = region.lower().replace(" ", "_")
        regional_alignment_df[regional_alignment_df["Region"] == region].to_csv(os.path.join(directory, f"{region_folder}.csv"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--regional_alignment_dir", type=str)
    parser.add_argument("--model", type=str)
    parser.add_argument("--country2region", type=str)
    args = parser.parse_args()
        
    compute_regional_alignment(args.regional_alignment_dir, args.model, args.country2region)
