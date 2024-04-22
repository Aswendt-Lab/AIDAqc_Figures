import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import os


# Setting font and font size
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 8
# Function to read CSV files and store them in a dictionary
script_dir = os.path.dirname(__file__)
dirpath = os.path.dirname(script_dir)
out_path = os.path.join(dirpath, 'figures')
#os.mkdir(out_path)
file_address = os.path.join(dirpath, "input", "noise_and_motion", "caculated_features_func.csv")
# Load CSV file into a DataFrame
df = pd.read_csv(file_address)
# Filter data into two groups based on the presence of keywords in the FileAddress column
group_original = df[~df['FileAddress'].str.contains('mc.nii|motion_added', na=False)]
group_added_motion = df[df['FileAddress'].str.contains('motion_added', na=False)]

# Extract Displacement factor values for each group
dfactor_original = group_original['Displacement factor (std of Mutual information)']
dfactor_added_motion = group_added_motion['Displacement factor (std of Mutual information)']

# Perform t-test
ttest_dfactor_am_vs_original = ttest_ind(dfactor_added_motion, dfactor_original,equal_var=False)

# Print t-test result
print("\nT-test results for Displacement factor (Added Motion vs. Original):")
print("Statistic:", ttest_dfactor_am_vs_original.statistic)
print("P-value:", ttest_dfactor_am_vs_original.pvalue)

cm = 1/2.53
# Create boxplot for Displacement factor
plt.figure(figsize=(6*cm, 4*cm),dpi=300)  # Adjust the figure size as needed

# Combine the data into a list
data = [dfactor_added_motion,dfactor_original ]

# Create boxplot
sns.boxplot(data=data, fliersize=3 ,flierprops={"marker": "o"},showfliers=False,palette="Set2",width=0.6, boxprops={'zorder': 3}, linewidth=1)

# Add labels to the x-axis
plt.xticks([0, 1], ['Added motion', 'Original'], fontsize=8, fontname='Times New Roman')

# Add title and labels
plt.title('(c)', fontsize=10, fontweight='bold', fontname='Times New Roman', loc='left')
plt.xlabel('Group', fontsize=8, fontname='Times New Roman')
plt.ylabel('Motion Severity (a.u)', fontsize=8, fontname='Times New Roman')
plt.ylim([0,0.11])

# Save the plot
plt.savefig(os.path.join(out_path, "displacement_factor_comparison.svg"), format='svg' ,dpi=300, bbox_inches='tight')

# Show the plot
plt.show()
