import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Load CSV file into a DataFrame
df = pd.read_csv(r"C:\Users\aswen\Desktop\TestingData\Aswendt_qc_data\proc_data\QC\calculated_features\caculated_features_func.csv")

# Filter data into two groups based on the presence of "mc.nii" in the FileAddress column
group_with_mc = df[df['FileAddress'].str.contains('mc.nii', na=False)]
group_without_mc = df[~df['FileAddress'].str.contains('mc.nii', na=False)]

# Extract SNR values for each group
tsnr_with = group_with_mc['tSNR (Averaged Brain ROI)']
dfactor_with = group_with_mc['Displacement factor (std of Mutual information)']

tsnr_without = group_without_mc['tSNR (Averaged Brain ROI)']
dfactor_without = group_without_mc['Displacement factor (std of Mutual information)']

# Perform t-tests
ttest_tsnr = ttest_ind(tsnr_with, tsnr_without)
ttest_dfactor = ttest_ind(dfactor_with, dfactor_without)

# Print t-test results
print("T-test results for tSNR:")
print("Statistic:", ttest_tsnr.statistic)
print("P-value:", ttest_tsnr.pvalue)

print("\nT-test results for Displacement factor:")
print("Statistic:", ttest_dfactor.statistic)
print("P-value:", ttest_dfactor.pvalue)

# Create boxplots for SNR and Displacement factor
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
sns.boxplot(data=[tsnr_with, tsnr_without], palette="Set1")
plt.title('tSNR')
plt.xticks(ticks=[0, 1], labels=['MotionCorrected', 'Original'])

plt.subplot(1, 2, 2)
sns.boxplot(data=[dfactor_with, dfactor_without], palette="Set2")
plt.title('Displacement factor')
plt.xticks(ticks=[0, 1], labels=['MotionCorrected', 'Original'])

plt.tight_layout()
plt.show()
