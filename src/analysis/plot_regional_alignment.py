import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



def get_section_dataframe(section, normalized=False): 
    data = []
    
    folder_path = 'analysis_metrics/regional_alignment'
    # Iterate over all the files in the folder
    for model_name in os.listdir(folder_path):
        model_path = os.path.join(folder_path, model_name)
        
        for continent_name in os.listdir(model_path):
            continent_file = os.path.join(model_path, continent_name)
            try:
                with open(continent_file, 'r') as file:
                    model_data = file.readlines()
                    score = float(model_data[section].split(',')[-1].replace('\n', ''))
                    
                    data.append((model_name, continent_name[:-4], score))
            except:
                print(f"Error reading file {continent_file}")
                
    df = pd.DataFrame(data, columns=["model", "continent", "score"])
    df['normalized_score'] = df.groupby('model')['score'].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
    
    if normalized:
        average_by_continent = df.groupby('continent')['normalized_score'].mean().reset_index()
        average_by_continent = average_by_continent.assign(model='Average')
        df = pd.concat([df, average_by_continent])
    else:
        average_by_continent = df.groupby('continent')['score'].mean().reset_index()
        average_by_continent = average_by_continent.assign(model='Average')
        df = pd.concat([df, average_by_continent])

        average_by_model = df.groupby('model')['score'].mean().reset_index()
        average_by_model = average_by_model.assign(continent='Average')
        df = pd.concat([df, average_by_model])
    return df


def get_heatmap(section, normalized=False):
    """
    Create and save a heatmap for all models and continents. Section_name is to be used as the title of the plot
    """
    
    df = get_section_dataframe(section, normalized)
    idx_section = json.load(open('wvs_data/section_name.json', 'r'))
    section_name = idx_section[str(section)]
    
    fig = plt.figure(figsize=(10, 8))
        
    if normalized:
        # Reshape the dataframe to have the models as columns and continents as rows
        heatmap_data = df.pivot(index='continent', columns='model', values='normalized_score')
        plt.title(f'{section_name} (score normalized for each model)')
    else:
        heatmap_data = df.pivot(index='continent', columns='model', values='score')
        plt.title(section_name)
        
    # sns.heatmap(heatmap_data, cmap='flare',vmin=0.75, vmax=0.85)
    sns.heatmap(heatmap_data, cmap='flare')

    plt.xlabel('Model')
    plt.ylabel('Continent')
    
    plt.savefig(f'analysis_metrics/alignment_heatmaps/{section}-{section_name}.png', dpi=300)
    # plt.show()


def main():
    get_heatmap(-1, normalized=True)
    
    for i in range(1,8):
        get_heatmap(i, normalized=True)


if __name__=="__main__":
    main()