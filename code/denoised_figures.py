import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Load CSV file into a DataFrame
df = pd.read_csv(r"C:\Users\aswen\Desktop\TestingData\Aswendt_qc_data\Hekmatyar\calculated_features\caculated_features_anat.csv")

# Filter data into two groups based on the presence of "denoised.nii" in the FileAddress column
group_with_denoised = df[df['FileAddress'].str.contains('denoised.nii', na=False)]
group_without_denoised = df[~df['FileAddress'].str.contains('denoised.nii', na=False)]

# Extract SNR values for each group
snr_chang_with = group_with_denoised['SNR Chang']
snr_normal_with = group_with_denoised['SNR Normal']

snr_chang_without = group_without_denoised['SNR Chang']
snr_normal_without = group_without_denoised['SNR Normal']

# Create boxplots for SNR Chang
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
sns.boxplot(data=[snr_chang_with, snr_chang_without], palette="Set1")
plt.title('SNR Chang')
plt.xticks(ticks=[0, 1], labels=['Denoised', 'Orginal'])

# Create boxplots for SNR Normal
plt.subplot(1, 2, 2)
sns.boxplot(data=[snr_normal_with, snr_normal_without], palette="Set2")
plt.title('SNR Normal')
plt.xticks(ticks=[0, 1], labels=['Denoised', 'Orginal'])

# Perform t-tests
ttest_chang = ttest_ind(snr_chang_with, snr_chang_without)
ttest_normal = ttest_ind(snr_normal_with, snr_normal_without)

print("T-test results for SNR Chang:")
print("Statistic:", ttest_chang.statistic)
print("P-value:", ttest_chang.pvalue)

print("\nT-test results for SNR Normal:")
print("Statistic:", ttest_normal.statistic)
print("P-value:", ttest_normal.pvalue)

plt.tight_layout()
plt.show()
