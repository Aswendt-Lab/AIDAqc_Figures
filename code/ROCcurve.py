import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import os

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

# Function to print mean, std, max, and mean for "sequencetype"
def print_statistics(data, x, y, hue):
    mean_values = data.groupby(hue).agg({y: 'mean'}).reset_index()
    std_values = data.groupby(hue).agg({y: 'std'}).reset_index()
    max_values = data.groupby(hue).agg({y: 'max'}).reset_index()

    for i, seq_type in enumerate(mean_values[hue]):
        print(f"Sequence Type: {seq_type}")
        print(f"Mean {y}: {mean_values[y][i]:.2f}")
        print(f"Standard Deviation {y}: {std_values[y][i]:.2f}")
        print(f"Maximum {y}: {max_values[y][i]:.2f}")
        print("\n")

# Create a 2x3 subplot
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(19*cm, 8*cm))

# Plot for "Accuracy" vs. "Thresold_Human_Voters"
sns.lineplot(
    data=subset_df, 
    x="Thresold_Human_Voters", y="Accuracy", hue="sequence_name",
    dashes=False, markers=True, ci=30,
    ax=axes[0, 0]
)
axes[0, 0].set_xlabel("Manual-rater Voting Threshold", fontsize=8)
axes[0, 0].set_ylabel("Accuracy", fontsize=8)
axes[0, 0].yaxis.set_major_locator(MaxNLocator(nbins=5))  # Set major y ticks
axes[0, 0].get_legend().remove()
print("Statistics for Accuracy vs. Thresold_Human_Voters:")
print_statistics(subset_df, "Thresold_Human_Voters", "Accuracy", "sequence_name")

# Plot for "Specificity" vs. "Thresold_Human_Voters"
sns.lineplot(
    data=subset_df, 
    x="Thresold_Human_Voters", y="Specificity", hue="sequence_name",
    dashes=False, markers=True, ci=30,
    ax=axes[0, 1]
)
axes[0, 1].set_xlabel("Manual-rater Voting Threshold", fontsize=8)
axes[0, 1].set_ylabel("Specificity", fontsize=8)
axes[0, 1].get_legend().remove()  # Remove legend for subsequent plots
axes[0, 1].yaxis.set_major_locator(MaxNLocator(nbins=5))  # Set major y ticks
print("Statistics for Specificity vs. Thresold_Human_Voters:")
print_statistics(subset_df, "Thresold_Human_Voters", "Specificity", "sequence_name")

# Plot for "Sensitivity-Recall" vs. "Thresold_Human_Voters"
sns.lineplot(
    data=subset_df, 
    x="Thresold_Human_Voters", y="Sensitivity-Recall", hue="sequence_name",
    dashes=False, markers=True, ci=30,
    ax=axes[0, 2]
)
axes[0, 2].set_xlabel("Manual-rater Voting Threshold", fontsize=8)
axes[0, 2].set_ylabel("Sensitivity", fontsize=8)
axes[0, 2].get_legend().remove()  # Remove legend for subsequent plots
axes[0, 2].yaxis.set_major_locator(MaxNLocator(nbins=5))  # Set major y ticks
print("Statistics for Sensitivity-Recall vs. Thresold_Human_Voters:")
print_statistics(subset_df, "Thresold_Human_Voters", "Sensitivity-Recall", "sequence_name")

# Plot for "Accuracy" vs. "Thresold_ML_Voters"
sns.lineplot(
    data=subset_df, 
    x="Thresold_ML_Voters", y="Accuracy", hue="sequence_name",
    dashes=False, markers=True, ci=30,
    ax=axes[1, 0]
)
axes[1, 0].set_xlabel("AIDAqc Voting Threshold", fontsize=8)
axes[1, 0].set_ylabel("Accuracy", fontsize=8)
axes[1, 0].yaxis.set_major_locator(MaxNLocator(nbins=5))  # Set major y ticks
axes[1, 0].get_legend().remove()
print("Statistics for Accuracy vs. Thresold_ML_Voters:")
print_statistics(subset_df, "Thresold_ML_Voters", "Accuracy", "sequence_name")

# Plot for "Specificity" vs. "Thresold_ML_Voters"
sns.lineplot(
    data=subset_df, 
    x="Thresold_ML_Voters", y="Specificity", hue="sequence_name",
    dashes=False, markers=True, ci=30,
    ax=axes[1, 1]
)
axes[1, 1].set_xlabel("AIDAqc Voting Threshold", fontsize=8)
axes[1, 1].set_ylabel("Specificity", fontsize=8)
axes[1, 1].get_legend().remove()  # Remove legend for subsequent plots
axes[1, 1].yaxis.set_major_locator(MaxNLocator(nbins=5))  # Set major y ticks
print("Statistics for Specificity vs. Thresold_ML_Voters:")
print_statistics(subset_df, "Thresold_ML_Voters", "Specificity", "sequence_name")

# Plot for "Sensitivity-Recall" vs. "Thresold_ML_Voters"
sns.lineplot(
    data=subset_df, 
    x="Thresold_ML_Voters", y="Sensitivity-Recall", hue="sequence_name",
    dashes=False, markers=True, ci=30,
    ax=axes[1, 2]
)
axes[1, 2].set_xlabel("AIDAqc Voting Threshold", fontsize=8)
axes[1, 2].set_ylabel("Sensitivity", fontsize=8)
#axes[1, 2].get_legend().remove()  # Add legend for the last plot only
axes[1, 2].yaxis.set_major_locator(MaxNLocator(nbins=5))  # Set major y ticks
print("Statistics for Sensitivity-Recall vs. Thresold_ML_Voters:")
print_statistics(subset_df, "Thresold_ML_Voters", "Sensitivity-Recall", "sequence_name")
axes[1, 2].legend(fontsize=8,frameon=False)

# Customize spines and tick parameters
for ax in axes.flatten():
    ax.tick_params(axis='both', which='both', labelsize=8)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)
    ax.spines['top'].set_linewidth(0.5)
    ax.spines['right'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['left'].set_linewidth(0.5)

# Adjust layout manually
plt.tight_layout()

# Save the figure as SVG and PNG
output_path = out_path
output_filename = "Subplots_Sensitivity_Accuracy_Specificity_2x3"

# Save as SVG
plt.savefig(f"{output_path}/{output_filename}.svg", format="svg")

# Save as PNG
plt.savefig(f"{output_path}/{output_filename}.png", format="png")

plt.show()
