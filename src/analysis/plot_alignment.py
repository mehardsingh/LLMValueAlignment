# python src/analysis/plot_alignment.py --in_align_fp analysis_metrics/alignment/alignment_Llama-2-7b-chat-hf2.csv --out_align_fp align_map.png

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import argparse

def plot_alignment(in_align_fp, out_align_fp, section="SectionsAvg", prompt=None):
    alignment_df = pd.read_csv(in_align_fp)
    alignment_df = alignment_df[alignment_df["Section"] == section]

    if prompt:
        alignment_df = alignment_df[alignment_df["Prompt"] == prompt]

    alignment_df = alignment_df[["Country", "Alignment"]]
    alignment_df = alignment_df.groupby('Country')['Alignment'].mean().reset_index()
    alignment_df.columns = ['Country', 'Alignment']

    alignment_dict = alignment_df.set_index('Country')['Alignment'].to_dict()

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    world['value'] = world['name'].map(alignment_dict)
    world = world[world['name'] != 'Antarctica']

    # vmin = min(alignment_dict.values()) - 0.025
    # vmax = max(alignment_dict.values()) + 0.025
    vmin = 0.55
    vmax = 0.85

    fig, ax = plt.subplots(1, 1, figsize=(20, 15))
    world.plot(column='value', cmap='Purples', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True, vmin=vmin, vmax=vmax, missing_kwds={'color': 'white'})
    ax.set_title('Opinion Alignment World Map')

    plt.show()
    plt.savefig(out_align_fp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_align_fp", type=str)
    parser.add_argument("--out_align_fp", type=str)
    args = parser.parse_args()
        
    plot_alignment(args.in_align_fp, args.out_align_fp)

