import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Load CSV file into a DataFrame
df = pd.read_csv(r"C:\Users\aswen\Desktop\TestingData\Aswendt_qc_data\proc_data\QC2\calculated_features\caculated_features_func.csv")

# Filter data into two groups based on the presence of keywords in the FileAddress column
group_original = df[~df['FileAddress'].str.contains('mc.nii|motion_added', na=False)]
group_added_motion = df[df['FileAddress'].str.contains('motion_added', na=False)]

# Extract Displacement factor values for each group
dfactor_original = group_original['Displacement factor (std of Mutual information)']
dfactor_added_motion = group_added_motion['Displacement factor (std of Mutual information)']

# Perform t-test
ttest_dfactor_am_vs_original = ttest_ind(dfactor_added_motion, dfactor_original)

# Print t-test result
print("\nT-test results for Displacement factor (Added Motion vs. Original):")
print("Statistic:", ttest_dfactor_am_vs_original.statistic)
print("P-value:", ttest_dfactor_am_vs_original.pvalue)

# Create boxplot for Displacement factor
plt.figure(figsize=(6, 6))

sns.boxplot(data=[dfactor_original, dfactor_added_motion], palette="Set2")
plt.title('Displacement factor (Added Motion vs. Original)')
plt.xticks(ticks=[0, 1], labels=['Original', 'Added Motion'])

plt.tight_layout()
plt.show()
