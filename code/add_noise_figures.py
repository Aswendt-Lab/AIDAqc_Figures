import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import os

# Setting font and font size
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 8

# Load CSV file into a DataFrame
script_dir = os.path.dirname(__file__)
dirpath = os.path.dirname(script_dir)
out_path = os.path.join(dirpath, 'figures')
#os.mkdir(out_path)
file_address = os.path.join(dirpath, "input", "noise_and_motion", "caculated_features_anat.csv")
# Load CSV file into a DataFrame
df = pd.read_csv(file_address)

outdir = os.path.join(dirpath, "figures")
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

cm = 1/2.53
# Create boxplot for Displacement factor
plt.figure(figsize=(12 * cm, 5 * cm), dpi=300)  # Adjust the figure size as needed

plt.subplot(1, 2, 1)
sns.boxplot(data=[snr_chang_with_random_noise,
                  snr_chang_with_salt_pepper_noise,
                  snr_chang_with_speckle_noise, snr_chang_with_original], palette="Set2", fliersize=3,
            flierprops={"marker": "o"},width=0.6, boxprops={'zorder': 3}, linewidth=1,showfliers=False,)
plt.title('(a)', fontsize=10, fontweight='bold', loc="left")
plt.xticks(ticks=[0, 1, 2, 3], labels=['Gaussian ', 'S&P', 'Speckle', 'Original'])
plt.xlabel('Noise type', fontsize=8, fontname='Times New Roman')
plt.ylabel('SNR Chang (dB)', fontsize=8, fontname='Times New Roman')

plt.ylim([18,57])

plt.subplot(1, 2, 2)
sns.boxplot(data=[snr_normal_with_random_noise,
                  snr_normal_with_salt_pepper_noise,
                  snr_normal_with_speckle_noise,
                  snr_normal_with_original], palette="Set2", fliersize=3,
            flierprops={"marker": "o"}, saturation=1, showfliers=False,
                        width=0.6, boxprops={'zorder': 3}, linewidth=1)

plt.title('(b)', fontsize=10, fontweight='bold', loc="left")
plt.xticks(ticks=[0, 1, 2, 3], labels=['Gaussian ', 'S&P', 'Speckle', 'Original'])
plt.xlabel('Noise type', fontsize=8, fontname='Times New Roman')
plt.ylabel('SNR Standard (dB)', fontsize=8, fontname='Times New Roman')

plt.ylim([10,42])


# Remove rows with NaN values from SNR Chang datasets
snr_chang_with_speckle_noise = snr_chang_with_speckle_noise.dropna()
snr_chang_with_salt_pepper_noise = snr_chang_with_salt_pepper_noise.dropna()
snr_chang_with_random_noise = snr_chang_with_random_noise.dropna()

# Perform Welch's t-tests for SNR Chang between Original and each noise type
ttest_welch_chang_original_vs_salt_pepper = ttest_ind(snr_chang_with_original, snr_chang_with_salt_pepper_noise, equal_var=False)
ttest_welch_chang_original_vs_speckle = ttest_ind(snr_chang_with_original, snr_chang_with_speckle_noise, equal_var=False)
ttest_welch_chang_original_vs_random = ttest_ind(snr_chang_with_original, snr_chang_with_random_noise, equal_var=False)

# Perform Welch's t-tests for SNR Normal between Original and each noise type
ttest_welch_normal_original_vs_salt_pepper = ttest_ind(snr_normal_with_original, snr_normal_with_salt_pepper_noise, equal_var=False)
ttest_welch_normal_original_vs_speckle = ttest_ind(snr_normal_with_original, snr_normal_with_speckle_noise, equal_var=False)
ttest_welch_normal_original_vs_random = ttest_ind(snr_normal_with_original, snr_normal_with_random_noise, equal_var=False)

# Adjust p-values for multiple comparisons using Bonferroni correction
alpha = 0.05
num_comparisons = 3  # Number of comparisons
alpha_adjusted = alpha / num_comparisons

p_values_chang = [ttest_welch_chang_original_vs_salt_pepper.pvalue, ttest_welch_chang_original_vs_speckle.pvalue, ttest_welch_chang_original_vs_random.pvalue]
reject_null_chang = [p < alpha_adjusted for p in p_values_chang]

p_values_normal = [ttest_welch_normal_original_vs_salt_pepper.pvalue, ttest_welch_normal_original_vs_speckle.pvalue, ttest_welch_normal_original_vs_random.pvalue]
reject_null_normal = [p < alpha_adjusted for p in p_values_normal]

# Print adjusted p-values
print("Adjusted p-values for SNR Chang:")
print("Original vs Salt & Pepper:", ttest_welch_chang_original_vs_salt_pepper.pvalue, "Reject Null:", reject_null_chang[0])
print("Original vs Speckle:", ttest_welch_chang_original_vs_speckle.pvalue, "Reject Null:", reject_null_chang[1])
print("Original vs Random:", ttest_welch_chang_original_vs_random.pvalue, "Reject Null:", reject_null_chang[2])

print("\nAdjusted p-values for SNR Normal:")
print("Original vs Salt & Pepper:", ttest_welch_normal_original_vs_salt_pepper.pvalue, "Reject Null:", reject_null_normal[0])
print("Original vs Speckle:", ttest_welch_normal_original_vs_speckle.pvalue, "Reject Null:", reject_null_normal[1])
print("Original vs Random:", ttest_welch_normal_original_vs_random.pvalue, "Reject Null:", reject_null_normal[2])
# Adjust layout
plt.tight_layout()

# Save the plot as SVG
plt.savefig(os.path.join(outdir, "NoiseComparisons.svg"), format='svg', dpi=300)

plt.show()