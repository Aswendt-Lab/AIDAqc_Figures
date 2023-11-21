import pandas as pd
from statsmodels.stats.inter_rater import fleiss_kappa
from statsmodels.stats.inter_rater import aggregate_raters

# Read the CSV file
csv_path = r"C:\Users\aswen\Desktop\Code\AIDAqc_Figures\input\combined_votings3.csv"
df = pd.read_csv(csv_path)

# Extract relevant columns
sequence_name_column = "sequence_name"
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
output_csv_path = r"C:\Users\aswen\Desktop\Code\AIDAqc_Figures\input\fleiss_kappa_results_ML_Voters.csv"
output_data = []

for seq_type, datasets in results_per_sequence_type.items():
    for dataset, kappa in datasets.items():
        output_data.append({'SequenceType': seq_type, 'Dataset': dataset, 'FleissKappa': kappa})

output_df = pd.DataFrame(output_data)
output_df.to_csv(output_csv_path, index=False)

print(f"\nResults saved to: {output_csv_path}")
