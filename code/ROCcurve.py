import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

# Read data from the CSV file
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '..', 'input')
out_path = os.path.join(script_dir, '..', 'figures')

# Load the data 
result_df = pd.read_csv(os.path.join(file_path, 'Confusion_matrix_metrics.csv'))
cm = 1/2.54

# Calculate Actual_Label

# Specify the font size for the plot
sns.set_style('ticks')
sns.set(font='Times New Roman', style=None)  # Set font to Times New Roman and font size to 9
palette = 'Set1'

subset_df = result_df[(result_df['TP']+result_df['FN'] > 0)]

# Create a Seaborn line plot
g = sns.relplot(
    data=subset_df, kind="line",
    x="Thresold_ML_Voters", y="Sensitivity-Recall", hue="sequence_name",
    dashes=False, markers=True, ci=30,
    height=5*cm, aspect=2 # Adjust the aspect to achieve the desired width of 9 cm
)

# Access the individual axes
axes = g.axes.flatten()
axes[0].set_xlabel("AIDAqc Voting Threshold", fontsize=8)
axes[0].set_ylabel("Sensitivity", fontsize=8)

# Loop through each axis and customize spines and tick parameters
for ax in axes:
    ax.tick_params(axis='both', which='both', labelsize=8)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)
    ax.spines['top'].set_linewidth(0.5)
    ax.spines['right'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['left'].set_linewidth(0.5)
g._legend.set_title("")
g._legend.set_fontsize(8)
# Save the figure as SVG and PNG
output_path = out_path
output_filename = "Sensitivity_AIDAqc_Voting_Threshold"

# Save as SVG
g.savefig(f"{output_path}/{output_filename}.svg", format="svg")

# Save as PNG
g.savefig(f"{output_path}/{output_filename}.png", format="png")

plt.show()
#%%
# Create a Seaborn line plot
g = sns.relplot(
    data=subset_df, kind="line",
    x="Thresold_Human_Voters", y="Sensitivity-Recall", hue="sequence_name",
    dashes=False, markers=True, ci=30,
    height=5*cm, aspect=2 # Adjust the aspect to achieve the desired width of 9 cm
)

# Access the individual axes
# Access the individual axes
axes = g.axes.flatten()
axes[0].set_xlabel("Manual-rater Voting Threshold", fontsize=8)
axes[0].set_ylabel("Sensitivity", fontsize=8)

# Loop through each axis and customize spines and tick parameters
for ax in axes:
    ax.tick_params(axis='both', which='both', labelsize=8)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)
    ax.spines['top'].set_linewidth(0.5)
    ax.spines['right'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['left'].set_linewidth(0.5)
g._legend.set_title("")
g._legend.set_fontsize(8)  # Set legend label size to 8 points

# Save the figure as SVG and PNG
output_path = out_path
output_filename = "Sensitivity_ManualRater_Voting_Threshold"

# Save as SVG
g.savefig(f"{output_path}/{output_filename}.svg", format="svg")

# Save as PNG
g.savefig(f"{output_path}/{output_filename}.png", format="png")

plt.show()
