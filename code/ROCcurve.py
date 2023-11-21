import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
result_df = pd.read_csv(r"C:\Users\aswen\Desktop\Code\AIDAqc_Figures\input\Confusion_matrix_metrics.csv")
cm = 1/2.54
# Calculate Actual_Label

# Specify the font size for the plot
plt.figure(figsize=(18*cm, 4*cm), dpi=600)
sns.set_style('ticks')
sns.set(font='Times New Roman', style=None)  # Set font to Times New Roman and font size to 9
palette = 'Set3'

subset_df = result_df[result_df['Thresold_Human_Voters'] > 2]

# Create a Seaborn line plot
g = sns.relplot(
    data=subset_df, kind="line",
    x="Thresold_ML_Voters", y="Sensitivity-Recall", hue="sequence_name",
    dashes=False, markers=True, ci=0
)

# Set axis labels
g.set(xlabel="Threshold_ML_Voter", ylabel="hit-rate (TPR)")

# Save the figure as SVG and PNG
output_path = r"C:\Users\aswen\Desktop\Code\AIDAqc_Figures\figures"
output_filename = "Sensitivity_AIDAqc Voting Threshold"

# Save as SVG
g.savefig(f"{output_path}/{output_filename}.svg", format="svg")

# Save as PNG
g.savefig(f"{output_path}/{output_filename}.png", format="png")

plt.show()
