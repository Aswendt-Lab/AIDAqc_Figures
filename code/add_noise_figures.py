import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import os

# Setting font and font size
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 8

# Load CSV file into a DataFrame
df = pd.read_csv(r"C:\Users\aswen\Desktop\TestingData\Aswendt_qc_data\proc_data\QC\calculated_features\caculated_features_anat.csv")
# Get the directory where the code file is located
code_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory of the code directory
parent_dir = os.path.dirname(code_dir)
outdir = os.path.join(parent_dir, "figures")
# Filter data into four groups based on the presence of "speckleNoisy.nii.gz", "saltPepperNoisy.nii.gz", "randomNoisy.nii.gz", and "original.nii.gz" in the FileAddress column
group_with_speckle_noise = df[df['FileAddress'].str.contains('speckleNoisy.nii.gz', na=False)]
group_with_salt_pepper_noise = df[df['FileAddress'].str.contains('saltPepperNoisy.nii.gz', na=False)]
group_with_random_noise = df[df['FileAddress'].str.contains('randomNoisy.nii.gz', na=False)]
group_with_original = df[~df['FileAddress'].str.contains('ois', na=False)]

# Extract SNR values for each group
snr_chang_with_speckle_noise = group_with_speckle_noise['SNR Chang']
snr_chang_with_salt_pepper_noise = group_with_salt_pepper_noise['SNR Chang']
snr_chang_with_random_noise = group_with_random_noise['SNR Chang']
snr_chang_with_original = group_with_original['SNR Chang']

snr_normal_with_speckle_noise = group_with_speckle_noise['SNR Normal']
snr_normal_with_salt_pepper_noise = group_with_salt_pepper_noise['SNR Normal']
snr_normal_with_random_noise = group_with_random_noise['SNR Normal']
snr_normal_with_original = group_with_original['SNR Normal']

cm = 1/2.5
# Create boxplots for SNR Chang
plt.figure(figsize=(18*cm, 6*cm))

plt.subplot(1, 2, 1)
sns.boxplot(data=[snr_chang_with_random_noise,
                  snr_chang_with_salt_pepper_noise,
                  snr_chang_with_speckle_noise, snr_chang_with_original], palette="Set2", fliersize=3 ,flierprops={"marker": "o"})
plt.title('(a)', fontsize=10, fontweight='bold')
plt.xticks(ticks=[0, 1, 2, 3], labels=['Random', 'Salt & Pepper', 'Speckle', 'Original'])

plt.subplot(1, 2, 2)
sns.boxplot(data=[snr_normal_with_random_noise,
                  snr_normal_with_salt_pepper_noise,
                  snr_normal_with_speckle_noise,
                  snr_normal_with_original], palette="Set2", fliersize=3 ,flierprops={"marker": "o"})
plt.title('(b)', fontsize=10, fontweight='bold')
plt.xticks(ticks=[0, 1, 2, 3], labels=['Random', 'Salt & Pepper', 'Speckle', 'Original'])

# Perform t-tests
ttest_chang_salt_pepper_noise_random_noise = ttest_ind(snr_chang_with_salt_pepper_noise, snr_chang_with_random_noise)
ttest_chang_speckle_noise_random_noise = ttest_ind(snr_chang_with_speckle_noise, snr_chang_with_random_noise)
ttest_chang_original_random_noise = ttest_ind(snr_chang_with_original, snr_chang_with_random_noise)
ttest_chang_original_salt_pepper_noise = ttest_ind(snr_chang_with_original, snr_chang_with_salt_pepper_noise)
ttest_chang_original_speckle_noise = ttest_ind(snr_chang_with_original, snr_chang_with_speckle_noise)

ttest_normal_salt_pepper_noise_random_noise = ttest_ind(snr_normal_with_salt_pepper_noise, snr_normal_with_random_noise)
ttest_normal_speckle_noise_random_noise = ttest_ind(snr_normal_with_speckle_noise, snr_normal_with_random_noise)
ttest_normal_original_random_noise = ttest_ind(snr_normal_with_original, snr_normal_with_random_noise)
ttest_normal_original_salt_pepper_noise = ttest_ind(snr_normal_with_original, snr_normal_with_salt_pepper_noise)
ttest_normal_original_speckle_noise = ttest_ind(snr_normal_with_original, snr_normal_with_speckle_noise)

print("T-test results for SNR Chang:")
print("Salt & Pepper Noise vs Random Noise - Statistic:", ttest_chang_salt_pepper_noise_random_noise.statistic, "P-value:", ttest_chang_salt_pepper_noise_random_noise.pvalue)
print("Speckle Noise vs Random Noise - Statistic:", ttest_chang_speckle_noise_random_noise.statistic, "P-value:", ttest_chang_speckle_noise_random_noise.pvalue)
print("Original vs Random Noise - Statistic:", ttest_chang_original_random_noise.statistic, "P-value:", ttest_chang_original_random_noise.pvalue)
print("Original vs Salt & Pepper Noise - Statistic:", ttest_chang_original_salt_pepper_noise.statistic, "P-value:", ttest_chang_original_salt_pepper_noise.pvalue)
print("Original vs Speckle Noise - Statistic:", ttest_chang_original_speckle_noise.statistic, "P-value:", ttest_chang_original_speckle_noise.pvalue)

print("\nT-test results for SNR Normal:")
print("Salt & Pepper Noise vs Random Noise - Statistic:", ttest_normal_salt_pepper_noise_random_noise.statistic, "P-value:", ttest_normal_salt_pepper_noise_random_noise.pvalue)
print("Speckle Noise vs Random Noise - Statistic:", ttest_normal_speckle_noise_random_noise.statistic, "P-value:", ttest_normal_speckle_noise_random_noise.pvalue)
print("Original vs Random Noise - Statistic:", ttest_normal_original_random_noise.statistic, "P-value:", ttest_normal_original_random_noise.pvalue)
print("Original vs Salt & Pepper Noise - Statistic:", ttest_normal_original_salt_pepper_noise.statistic, "P-value:", ttest_normal_original_salt_pepper_noise.pvalue)
print("Original vs Speckle Noise - Statistic:", ttest_normal_original_speckle_noise.statistic, "P-value:", ttest_normal_original_speckle_noise.pvalue)

# Adjust layout
plt.tight_layout()

# Save the plot as SVG
plt.savefig(os.path.join(outdir, "NoiseComparisons.svg"), format='svg', dpi=300)

plt.show()