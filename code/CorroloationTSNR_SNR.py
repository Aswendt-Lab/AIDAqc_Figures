import pandas as pd
import os


# Read data from the CSV file
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '..', 'input')
out_path = os.path.join(script_dir, '..', 'figures')

func_df = pd.read_csv(os.path.join(file_path, 'combined_data_func.csv'))
struct_df = pd.read_csv(os.path.join(file_path, 'combined_data_struct.csv'))
anat_df = pd.read_csv(os.path.join(file_path, 'combined_data_anat.csv'))


# Step 4: Sort all dataframes based on the FileAddress column
func_df.sort_values(by='FileAddress', inplace=True)
struct_df.sort_values(by='FileAddress', inplace=True)
anat_df.sort_values(by='FileAddress', inplace=True)

# Step 5: Process the FileAddress column
def process_file_address(file_address):
    elements = file_address.split('\\')  # Use '\\' to split on backslash
    return '\\'.join(elements[:-1])  # Use '\\' to join elements with backslash

func_df['FileAddress'] = func_df['FileAddress'].apply(process_file_address)
anat_df['FileAddress'] = anat_df['FileAddress'].apply(process_file_address)

# Step 6: Create a new dataframe
common_file_addresses = set(anat_df['FileAddress']).intersection(set(func_df['FileAddress']))
result_data = []

for file_address in common_file_addresses:
    anat_rows = anat_df[anat_df['FileAddress'] == file_address]
    func_rows = func_df[func_df['FileAddress'] == file_address]
    
    # Calculate the average of 'SNR Chang' and 'tSNR (Averaged Brain ROI)' values, ignoring NaNs
    avg_snr_chang = anat_rows['SNR Normal'].mean() #Here you have to set what kind of SNR you want to plot
    avg_tsnr_avg_brain_roi = func_rows['tSNR (Averaged Brain ROI)'].mean()
    
    result_data.append({
        'Common FileAddress': file_address,
        'Average SNR Chang': avg_snr_chang,
        'Average tSNR (Averaged Brain ROI)': avg_tsnr_avg_brain_roi
    })

# Create the result DataFrame
result_df = pd.DataFrame(result_data)

# Print the result
print(result_df)


import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy.stats import spearmanr

# Calculate the correlation coefficient and p-value
corr, p_value = pearsonr(result_df['Average SNR Chang'], result_df['Average tSNR (Averaged Brain ROI)'])
# corr, p_value = spearmanr(result_df['Average SNR Chang'], result_df['Average tSNR (Averaged Brain ROI)'])
sns.set_style('ticks')
# Set the font style to Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

# Define the centimeters to inches conversion
cm = 1/2.54  # centimeters in inches

# Create the plot

#plt.figure(figsize=(4.5*cm, 5*cm), dpi=100)

# Create the plot with a specified figure size
h = 5 * cm
width = 9.5 * cm
aspect = width / h
fig =sns.lmplot(x='Average SNR Chang', y='Average tSNR (Averaged Brain ROI)',
                data=result_df, palette='Set2',height=h,aspect = aspect,ci=100,scatter_kws={'s': 8,'color': '#4C72B0','edgecolor':'w','linewidths':.3},line_kws={'lw': 2, 'color': '#4682b4'})
plt.rcParams['figure.dpi'] = 300

plt.xlabel('Anatomical SNR-standard (dB)', fontsize=8)
plt.ylabel('Functional tSNR (dB)', fontsize=8)

# Set font size for tick labels
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

# Add correlation coefficient and p-value to the plot
# plt.text(0.1, 0.9, f'r: {corr:.2f}', transform=plt.gca().transAxes, fontsize=8)
# plt.text(0.1, 0.85, f'p-value: {p_value:}', transform=plt.gca().transAxes, fontsize=8)
ax = plt.gca()
# Remove right and upper bordersax = plt.gca()
# Set font size for tick labels
ax.tick_params(axis='both', which='both', labelsize=8)
# Explicitly set the visibility of top and right spines
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
# Customize the border linewidth
ax.spines['top'].set_linewidth(0.5)     # Top border
ax.spines['right'].set_linewidth(0.5)   # Right border
ax.spines['bottom'].set_linewidth(0.5)  # Bottom border
ax.spines['left'].set_linewidth(0.5)   # Left border
ax.locator_params(axis='y', nbins=8)
ax.locator_params(axis='x', nbins=16)

# Add horizontal lines from yticks

ax.tick_params(axis='both', which='both', width=0.5, color='gray', length=2)
#ax.set_title("(b) SNR structural vs anatomical", weight='bold', fontsize=10)

# Save the figure as PNG and SVG
fig_path_png = os.path.join(out_path, 'AnatVSFuncAllDataCorr.png')
fig_path_svg = os.path.join(out_path, 'AnatVSFuncAllDataCorr.svg')

fig.savefig(fig_path_png, format='png', bbox_inches='tight')
fig.savefig(fig_path_svg, format='svg', bbox_inches='tight')

plt.show()