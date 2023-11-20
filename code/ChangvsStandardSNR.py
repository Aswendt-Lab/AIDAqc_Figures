#%% Plot all chang vs normal

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import numpy as np
import os

sns.set_style('ticks')
cm = 1/2.54  # centimeters in inches
# Specify the path to your Excel file
# Read data from the CSV file
script_dir = os.path.dirname(__file__)
excel_file_path = os.path.join(script_dir, '..', 'input', 'combined_data_anat.csv')
out_path = os.path.join(script_dir, '..', 'figures')


plt.figure(figsize=(10*cm,10*cm),dpi=300)
# Read the data into a pandas DataFrame
df = pd.read_csv(excel_file_path)

# Drop rows with NaN values in the specified columns
#df = df.dropna(subset=['SNR-Chang (dB)', 'SNR-Standard (dB)'])
# Custom sorting key function
def extract_number(dataset):
    # Extract numeric part from the 'dataset' column
    # Assuming the numeric part is always at the beginning of the string
    # If it's not, you might need a more sophisticated method
    return int(''.join(filter(str.isdigit, dataset)))

df['sorting_key'] = df['dataset']#.apply(extract_number)
df['SNR Chang'] = df['SNR Chang']#.apply(lambda x: np.power(10,x/20))
df['SNR Normal'] = df['SNR Normal']#.apply(lambda x: np.power(10,x/20))
df = df.sort_values(by=["sorting_key"],ascending=True)


plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 8
#plt.title("All anatomical data",weight='bold', fontsize=10)

# Calculate the correlation and p-value between 'SNR-Chang' and 'SNR-Standard'
#correlation, p_value = stats.pearsonr(df['SNR-Chang (dB)'], df['SNR-Standard (dB)'])
# Set seaborn style
Wanted_datasets = ["117_m_Ra","94_m_Va","7_m_Se","7_rab_Mu","7_h_He"]

# Filter DataFrame based on Wanted_datasets
filtered_df = df[df['dataset'].isin(Wanted_datasets)]

#

# Your DataFrame and plot
ax = sns.scatterplot(data=filtered_df, x='SNR Chang', y='SNR Normal', hue="dataset", palette= "Set1", s=20)

#ax.set_title("All anatomical data", weight='bold', fontsize=11)

# Set title and labels including the correlation and p-value
plt.xlabel('SNR-Chang (db)', fontname='Times New Roman', fontsize=8)
plt.ylabel('SNR-Standard (db)', fontname='Times New Roman', fontsize=8)

# Calculate the correlation and p-value between 'SNR-Chang' and 'SNR-Standard'
correlation, p_value = stats.spearmanr(df['SNR Chang'], df['SNR Normal'], nan_policy='omit', alternative='two-sided')


# Sort the dataframe by 'SNR Chang' in descending order
df_sorted = df.sort_values(by='SNR Chang', ascending=False)

# Exclude the top 3 highest values
top3_indices = df_sorted.head(1).index
df_filtered = df.drop(top3_indices)


ax.spines['top'].set_linewidth(0.5)  # Top border
ax.spines['right'].set_linewidth(0.5)  # Right border
ax.spines['bottom'].set_linewidth(0.5)  # Bottom border
ax.spines['left'].set_linewidth(0.5)  # Left border
ax.set_xlim(15,50)
ax.set_ylim(10,50)

# Move the legend outside the plot to the right side
legend = plt.legend(title="Dataset", loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8, handlelength=0.5)
legend.get_title().set_fontfamily('Times New Roman')
for text in legend.get_texts():
    text.set_fontfamily('Times New Roman')

fig_path_png = os.path.join(out_path, 'StandardVSchangtogether.png')
fig_path_svg = os.path.join(out_path, 'StandardVSchangtogether.svg')

plt.savefig(fig_path_png, format='png', bbox_inches='tight')
plt.savefig(fig_path_svg, format='svg', bbox_inches='tight')

# Show the plot
plt.show()

