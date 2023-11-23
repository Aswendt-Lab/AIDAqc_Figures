import pandas as pd
from statsmodels.stats.inter_rater import fleiss_kappa
from statsmodels.stats.inter_rater import aggregate_raters
import os
import numpy

# Read data from the CSV file
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '..', 'input')
out_path = os.path.join(script_dir, '..', 'figures')

# Read the CSV file
df = pd.read_csv(os.path.join(file_path,"combined_votings3.csv"))

# Extract relevant columns
sequence_name_column = "SequenceType"
dataset_column = "dataset"
corresponding_img_column = "corresponding_img"
method_columns = ["One_class_SVM", "IsolationForest", "LocalOutlierFactor", " EllipticEnvelope", "statistical_method"]

sequence_name = df[sequence_name_column]
dataset_names = df[dataset_column]
corresponding_imgs = df[corresponding_img_column]
methods_data = df[list(method_columns)]

# Create a DataFrame for ratings
data = {
    sequence_name_column: sequence_name,
    'Dataset': dataset_names,
    'CorrespondingImg': corresponding_imgs,
    'Methods': methods_data.apply(tuple, axis=1)
}
ratings_df = pd.DataFrame(data)

# Define sequence types
sequence_types = ["anat", "func", "diff"]

results_per_sequence_type = {}

for seq_type in sequence_types:
    seq_type_ratings = ratings_df[ratings_df['CorrespondingImg'].str.startswith(seq_type)]
    unique_datasets = seq_type_ratings['Dataset'].unique()

    results_per_dataset = {}

    for dataset in unique_datasets:
        dataset_ratings = seq_type_ratings[seq_type_ratings['Dataset'] == dataset]
        try:
            # Convert the ratings data to a format expected by fleiss_kappa
            ratings_matrix, _ = aggregate_raters(list(dataset_ratings['Methods'].values), n_cat=None)

            # Calculate Fleiss' Kappa
            kappa = fleiss_kappa(ratings_matrix, method='fleiss')
            results_per_dataset[dataset] = kappa
        except ValueError:
            print(f"\nValue Error: Fleiss' Kappa could not be calculated for dataset {dataset} and sequence type {seq_type}.")

    results_per_sequence_type[seq_type] = results_per_dataset

# Save results to CSV file
output_csv_path = os.path.join(file_path, "fleiss_kappa_results_ML_Voters.csv")
output_data = []

for seq_type, datasets in results_per_sequence_type.items():
    for dataset, kappa in datasets.items():
        output_data.append({'SequenceType': seq_type, 'Dataset': dataset, 'FleissKappa': kappa})

output_df = pd.DataFrame(output_data)
output_df.to_csv(output_csv_path, index=False)

print(f"\nResults saved to: {output_csv_path}")
#%% Create Heat map of it
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as ticker
import os
# Load your Excel file into a Pandas DataFrame
filtered_df = output_df
filtered_df.loc[filtered_df["SequenceType"] == "anat","SequenceType"] = "Anatomical"
filtered_df.loc[filtered_df["SequenceType"] == "diff","SequenceType"] = "Diffusion"
filtered_df.loc[filtered_df["SequenceType"] == "func","SequenceType"] = "Functional"

sns.set_style("darkgrid")
cm = 1/2.54  # centimeters in inches
# Create two subplots for Kappa and F1 scores heatmaps
fig, axes = plt.subplots(1, 1, figsize=(20*cm, 5*cm), dpi=300)
#sns.set_style('whitegrid')
# Specify the font properties
font_properties = fm.FontProperties(family='Times New Roman', size=8)
font_properties2 = fm.FontProperties(family='Times New Roman', size=10)
Title = ["(a) Fleiss kappa score: inter rater reliability "," (b) F1_score: raters vs AIDAqc"]
for i, metric in enumerate(['FleissKappa']):
    ax = axes
    pivot_df = filtered_df.pivot(index='SequenceType', columns='Dataset', values=metric)
    pivot_df['mean'] = pivot_df.mean(axis=1)
    pivot_df['std'] = pivot_df.std(axis=1)
    t=Title[i]
    sns.heatmap(pivot_df, annot=True, fmt=".1f", cmap="YlGnBu", cbar=True, ax=ax)

    # Set font properties for labels, titles, and annotations
    ax.set_xticklabels(ax.get_xticklabels(), fontproperties=font_properties)
    ax.set_yticklabels(ax.get_yticklabels(), fontproperties=font_properties)
    ax.set_xlabel('Datasets', fontproperties=font_properties)
    ax.set_ylabel('Sequences', fontproperties=font_properties)
    #ax.set_title(f'{t} ', fontsize=10, fontproperties=font_properties2, fontweight='bold')
    ax.set(xlabel=None)
    # Set the color bar legend font size and font properties
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=8)
    cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(), fontproperties=font_properties)
    
    # Customize the color bar ticks (increase the number of ticks)
    cbar.ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    
    a = []
    for text in ax.texts:
        a.append(float(text.get_text()))
        
    

    for text in ax.texts:
        text.set_font("Times New Roman")
        text.set_size(8)
        
        
# Show the plots
plt.tight_layout()


# Save the figure as PNG and SVG
fig_path_png = os.path.join(out_path, 'FleissKappa_AIDAqc_Raters_InterraterVariability.png')
fig_path_svg = os.path.join(out_path, 'FleissKappa_AIDAqc_Raters_InterraterVariability.svg')

fig.savefig(fig_path_png, format='png', bbox_inches='tight')
fig.savefig(fig_path_svg, format='svg', bbox_inches='tight')
plt.show()


