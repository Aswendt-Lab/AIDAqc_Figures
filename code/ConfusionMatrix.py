import pandas as pd
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support,ConfusionMatrixDisplay
import os
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt
# Load the CSV files



# Read data from the CSV file
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '..', 'input')
out_path = os.path.join(script_dir, '..', 'figures')




human_voters_df = pd.read_csv(os.path.join(file_path,"combined_Human_Voters_from_votings3_Final.csv"))
votings_df = pd.read_csv(os.path.join(file_path,"combined_votings3.csv"))
C = 0

# Create an empty DataFrame to store results
result_df = pd.DataFrame(columns=[
    'dataset_name', 'sequence_name', 'Thresold_ML_Voters', 'Thresold_Human_Voters',
    'TP', 'TN', 'FP', 'FN',"SUM" , 'Precision','Accuracy',
    'Prevalence', 'Sensitivity-Recall', 'Specificity', 'F1 Score',
    'Informedness', 'Markedness', 'Diagnostic Odds Ratio', 'Phi Coefficient',
    'Fowlkes-Mallows Index', 'Negative Predictive Value', 'Miss Rate',
    'Fall-out', 'False Discovery Rate', 'False Omission Rate', 'Positive Likelihood Ratio',
    'Negative Likelihood Ratio', 'Prevalence Threshold', 'Threat Score'
])

# Iterate over unique datasets
for dataset_name in human_voters_df['dataset_name'].unique():
    # Filter data for the current dataset
    human_data = human_voters_df[human_voters_df['dataset_name'] == dataset_name]
    voting_data = votings_df[votings_df['dataset'] == dataset_name]

    # Iterate over unique sequence names
    for sequence_name in human_data['SequenceType'].unique():

        # Filter data for the current sequence
        human_sequence_data = human_data[human_data['SequenceType'] == sequence_name]
        voting_sequence_data = voting_data[voting_data['SequenceType'] == sequence_name]
        voting_sequence_data["complete_image_path"] = voting_sequence_data.apply(
            lambda row: os.path.join(row['corresponding_img_Path'], row['corresponding_img']), axis=1)

        # Create a list to store rows for missing paths
        missing_rows = []
        missing_paths = set(human_sequence_data['Path']) - set(voting_sequence_data['complete_image_path'])
        for missing_path in missing_paths:
            # Get relevant information from human_voters_df based on the missing path
            relevant_info = human_voters_df[human_voters_df['Path'] == missing_path].iloc[0]

            # Create a new row with relevant information
            new_row = {'Pathes': relevant_info['Path'],
                       'corresponding_img': None,
                       'One_class_SVM': False,
                       'IsolationForest': False,
                       'LocalOutlierFactor': False,
                       ' EllipticEnvelope': False,
                       'statistical_method': False,
                       'Voting outliers (from 5)': None,
                       'dataset': relevant_info['dataset_name'],
                       'SequenceType': relevant_info['SequenceType'],
                       'complete_image_path': None
                       }

            # Append the new row to the list
            missing_rows.append(new_row)

        # Concatenate the list of new rows to the voting DataFrame
        voting_sequence_data_complemented = pd.concat([voting_sequence_data, pd.DataFrame(missing_rows)],
                                                      ignore_index=True)

        # Iterate over thresholds for Thresold_ML_Voters
        for Thresold_ML_Voters in range(1, 6):
            # Iterate over thresholds for Thresold_Human_Voters
            for Thresold_Human_Voters in range(1, 6):
                voting_sequence_data_complemented["Predictor"] = voting_sequence_data_complemented.iloc[:, 2:7].sum(
                    axis=1) >= Thresold_ML_Voters
                human_sequence_data["Predictor"] = human_sequence_data.iloc[:, [1] + list(range(4, 7))].sum(
                    axis=1) >= Thresold_Human_Voters

                # Extract labels from human voters
                human_labels = human_sequence_data[['Predictor']].values.flatten()

                # Extract labels from voting methods
                voting_labels = voting_sequence_data_complemented[['Predictor']].values.flatten()

                # Calculate confusion matrix
                try:
                    tn, fp, fn, tp = confusion_matrix(human_labels, voting_labels).ravel()
                    a = (tn, fp, fn, tp)
                except ValueError:
                    print("exception for: " + sequence_name + " + " + dataset_name)
                    C = 1 + C
                    continue

                # Calculate additional metrics
                prevalence = (tp + fn) / (tp + tn + fp + fn)
                accuracy = (tp + tn) / (tp + tn + fp + fn)
                sensitivity = recall = tp / (tp + fn)
                specificity = tn / (tn + fp)
                f1_score = 2 * tp / (2 * tp + fp + fn)
                informedness = sensitivity + specificity - 1
                markedness = precision = tp / (tp + fp)
                npv = tn / (tn + fn)
                miss_rate = fn / (tp + fn)
                fall_out = fp / (tn + fp)
                false_discovery_rate = fp / (tp + fp)
                false_omission_rate = fn / (tn + fn)
                positive_likelihood_ratio = sensitivity / (1 - specificity) if (1 - specificity) != 0 else float('inf')
                negative_likelihood_ratio = (1 - sensitivity) / specificity if specificity != 0 else float('inf')
                prevalence_threshold = (tp + fp) / (tp + tn + fp + fn)
                threat_score = 2 * tp / (2 * tp + fp + fn)
                # Calculate Phi Coefficient
                phi_coefficient = (tp * tn - fp * fn) / ((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))**0.5 if (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn) != 0 else 0
                
                # Calculate Fowlkes-Mallows Index
                fowlkes_mallows_index = (precision * recall)**0.5

                # Append the results to the result DataFrame
                result_df = pd.concat([result_df, pd.DataFrame({
                    'dataset_name': [dataset_name],
                    'sequence_name': [sequence_name],
                    'Thresold_ML_Voters': [Thresold_ML_Voters],
                    'Thresold_Human_Voters': [Thresold_Human_Voters],
                    'TP': [tp],
                    'TN': [tn],
                    'FP': [fp],
                    'FN': [fn],
                    "SUM":[tp+tn+fp+fn],
                    'Precision': [precision],
                    'Accuracy': [accuracy],
                    'Prevalence': [prevalence],
                    'Sensitivity-Recall': [sensitivity],
                    'Specificity': [specificity],
                    'F1 Score': [f1_score],
                    'Informedness': [informedness],
                    'Markedness': [markedness],
                    'Diagnostic Odds Ratio': [positive_likelihood_ratio],
                    'Phi Coefficient': [phi_coefficient],
                    'Fowlkes-Mallows Index': [fowlkes_mallows_index],
                    'Negative Predictive Value': [npv],
                    'Miss Rate': [miss_rate],
                    'Fall-out': [fall_out],
                    'False Discovery Rate': [false_discovery_rate],
                    'False Omission Rate': [false_omission_rate],
                    'Positive Likelihood Ratio': [positive_likelihood_ratio],
                    'Negative Likelihood Ratio': [negative_likelihood_ratio],
                    'Prevalence Threshold': [prevalence_threshold],
                    'Threat Score': [threat_score]
                })], ignore_index=True)

# Print the count of exceptions
print(C)

outpath = r"C:\Users\aswen\Desktop\Code\AIDAqc_Figures\input"
# Save the result DataFrame to a CSV file
#result_df.to_csv(os.path.join(outpath, 'Confusion_matrix_metrics.csv'), index=False)
