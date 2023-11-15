#%% Plot all chang vs normal

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import numpy as np
import os


cm = 1/2.54  # centimeters in inches
# Specify the path to your Excel file
excel_file_path = r"C:\Users\aswen\Desktop\Code\AIDAqc_Figures\input\combined_data_anat.csv"
plt.figure(figsize=(10*cm,10*cm),dpi=300)
# Read the data into a pandas DataFrame
df = pd.read_csv(excel_file_path)

# Drop rows with NaN values in the specified columns
#df = df.dropna(subset=['SNR-Chang (dB)', 'SNR-Standard (dB)'])

df['SNR Chang'] = df['SNR Chang']#apply(lambda x: np.power(10,x/20))
df['SNR Normal'] = df['SNR Normal']#apply(lambda x: np.power(10,x/20))
df['names'] = df['FileAddress'].apply(lambda x:x.split("mri")[1].split(os.path.sep)[1])



plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 8
plt.title("All anatomical data",weight='bold', fontsize=10)

# Calculate the correlation and p-value between 'SNR-Chang' and 'SNR-Standard'
#correlation, p_value = stats.pearsonr(df['SNR-Chang (dB)'], df['SNR-Standard (dB)'])
correlation, p_value = stats.spearmanr(df['SNR Chang'], df['SNR Normal'], nan_policy='omit',alternative='two-sided')

# Set seaborn style
sns.set_style('whitegrid')


# Create a scatter plot
ax = sns.scatterplot(data=df, x='SNR Chang', y='SNR Normal', hue="names", palette="Spectral_r", s=7)
ax.set_title("All anatomical data", weight='bold', fontsize=11)

# Set title and labels including the correlation and p-value
plt.xlabel('SNR-Chang')
plt.ylabel('SNR-Standard')

# Calculate the correlation and p-value between 'SNR-Chang' and 'SNR-Standard'
correlation, p_value = stats.spearmanr(df['SNR Chang'], df['SNR Normal'], nan_policy='omit', alternative='two-sided')

# Set seaborn style
sns.set_style('whitegrid')

# Sort the dataframe by 'SNR Chang' in descending order
df_sorted = df.sort_values(by='SNR Chang', ascending=False)

# Exclude the top 3 highest values
top3_indices = df_sorted.head(1).index
df_filtered = df.drop(top3_indices)

# Set xlim and ylim excluding the top 3 highest values
ax.set_xlim(df_filtered['SNR Chang'].min(), df_filtered['SNR Chang'].max())
ax.set_ylim(df_filtered['SNR Normal'].min(), df_filtered['SNR Normal'].max())

ax.spines['top'].set_linewidth(0)  # Top border
ax.spines['right'].set_linewidth(0)  # Right border
ax.spines['bottom'].set_linewidth(0.5)  # Bottom border
ax.spines['left'].set_linewidth(0.5)  # Left border

# Move the legend outside the plot to the right side
legend = plt.legend(title="Dataset", loc='center left', bbox_to_anchor=(1, 0.5), fontsize=5, handlelength=0.5)
legend.get_title().set_fontfamily('Times New Roman')
for text in legend.get_texts():
    text.set_fontfamily('Times New Roman')

# Show the plot
plt.show()
