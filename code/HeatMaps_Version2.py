# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 17:50:28 2023

@author: arefk
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# Load your Excel file into a Pandas DataFrame

# Read data from the CSV file
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '..', 'input')
out_path = os.path.join(script_dir, '..', 'figures')

csv_file = os.path.join(file_path, "Confusion_matrix_metrics.csv")

df = pd.read_csv(csv_file)

# Set the user-defined thresholds to get desired values
Threshold_Human_Voters = 3  # Replace with the user-set threshold value
Threshold_ML_Voters = 1

# Filter the DataFrame based on the user-set threshold
filtered_df = df[(df['Thresold_Human_Voters'] == Threshold_Human_Voters) &
                 (df['Thresold_ML_Voters'] == Threshold_ML_Voters) &
                 (df['TP'] > 0)]

# Specify the columns you want to include in the heatmap
columns_to_include = ['TP', 'TN', 'FP', 'FN', 'Sensitivity-Recall', 'Specificity', 'Precision', 'Accuracy', 'F1 Score']

cm = 1 / 2.54  # centimeters in inches

# Create a subplot for the heatmap
fig, ax = plt.subplots(figsize=(20 * cm, 10 * cm), dpi=300)

# Specify the font properties
font_properties = fm.FontProperties(family='Times New Roman', size=10)

# Pivot the DataFrame to have "sequence_name" as columns and "dataset_name" as index
pivot_df = filtered_df.pivot(index='sequence_name', columns='dataset_name')

# Filter the pivot DataFrame to include only the specified columns
pivot_df = pivot_df[columns_to_include]

# Calculate the average for each "dataset_name"
avg_df = pivot_df.mean(level=0, axis=1)

# Plot the heatmap without color coding
sns.heatmap(avg_df, annot=True, fmt=".1f", cmap="Blues", cbar=False, ax=ax)

# Set font properties for labels, titles, and annotations
ax.set_xticklabels(ax.get_xticklabels(), fontproperties=font_properties)
ax.set_yticklabels(ax.get_yticklabels(), fontproperties=font_properties)
ax.set_xlabel('Sequences', fontproperties=font_properties)
ax.set_ylabel('Datasets', fontproperties=font_properties)

# Set the font properties for the cell annotations
for text in ax.texts:
    text.set_font("Times New Roman")
    text.set_size(8)

# Show the plot
plt.tight_layout()
plt.show()
