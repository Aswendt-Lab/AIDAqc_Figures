import pandas as pd
from statsmodels.stats.inter_rater import fleiss_kappa
from statsmodels.stats.inter_rater import aggregate_raters
import os
# Read the CSV file
csv_path = r"C:\Users\aswen\Desktop\Code\AIDAqc_Figures\input\combined_Human_Voters_from_votings3.csv"
df = pd.read_csv(csv_path)

# Extract relevant columns
path_column = "Path"
validation_columns = ["validation_adam", "validation_giovanna", "validation_joanes", "validation_pboehmsturm", "validation_Susanne"]
dataset_column = "dataset_name"



# Create a DataFrame for ratings
data = {
    'Path': df[path_column],
    'Dataset': df[dataset_column],
    'SequenceType': df['SequenceType'],
    'Methods': df[validation_columns].apply(tuple, axis=1)
}
ratings_df = pd.DataFrame(data)

# Define sequence types
sequence_types = ["anat", "func", "diff"]

results_per_sequence_type = {}

for seq_type in sequence_types:
    seq_type_ratings = ratings_df[ratings_df['SequenceType']==seq_type]
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
output_csv_path = r"C:\Users\aswen\Desktop\Code\AIDAqc_Figures\input\fleiss_kappa_results_Human_Voters_new_structure.csv"
output_data = []

for seq_type, datasets in results_per_sequence_type.items():
    for dataset, kappa in datasets.items():
        output_data.append({'SequenceType': seq_type, 'Dataset': dataset, 'FleissKappa': kappa})

output_df = pd.DataFrame(output_data)
output_df.to_csv(output_csv_path, index=False)

print(f"\nResults saved to: {output_csv_path}")
