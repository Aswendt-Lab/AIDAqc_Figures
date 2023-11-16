import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import numpy as np
import os

cm = 1/2.54  # centimeters in inches
# Specify the path to your Excel file
# Read data from the CSV file
script_dir = os.path.dirname(__file__)
excel_file_path = os.path.join(script_dir, '..', 'input', 'combined_data_anatF.csv')
out_path = os.path.join(script_dir, '..', 'figures')

# Read the data into a pandas DataFrame
df = pd.read_csv(excel_file_path)

# Set seaborn style
sns.set_style('white')

# Create a list to store correlation and p-value for each dataset
correlation_list = []
p_value_list = []

plt.figure(figsize=(10*cm,10*cm),dpi=300)
# Get unique values in the 'dataset' column
def extract_number(dataset):
    # Extract numeric part from the 'dataset' column
    # Assuming the numeric part is always at the beginning of the string
    # If it's not, you might need a more sophisticated method
    return int(''.join(filter(str.isdigit, dataset)))

df['sorting_key'] = df['dataset'].apply(extract_number)
df['SNR Chang'] = df['SNR Chang']#.apply(lambda x: np.power(10,x/20))
df['SNR Normal'] = df['SNR Normal']#.apply(lambda x: np.power(10,x/20))
df = df.sort_values(by=["sorting_key"],ascending=True)
datasets = df['dataset'].unique()
SS = int(np.ceil(np.sqrt(len(datasets))))
# Create subplots based on the number of datasets
fig, axes = plt.subplots(SS, SS, figsize=(18*cm, 18*cm), dpi=300, constrained_layout=True)

# Flatten the axes array to iterate over it
axes = axes.flatten()

for i, dataset in enumerate(datasets):
    # Filter the dataframe for the current dataset
    df_subset = df[df['dataset'] == dataset]

    # Calculate the correlation and p-value for the current dataset
    correlation, p_value = stats.spearmanr(df_subset['SNR Chang'], df_subset['SNR Normal'], nan_policy='omit', alternative='two-sided')
    
    # Append the correlation and p-value to the lists
    correlation_list.append(correlation)
    p_value_list.append(p_value)

    # Create a scatter plot for the current dataset
    ax = sns.scatterplot(data=df_subset, x='SNR Chang', y='SNR Normal', s=7, ax=axes[i],color="red")
    ax.set_title(f"{dataset}", weight='bold', fontsize=11, fontname='Times New Roman')

    # Set title and labels including the correlation and p-value
    ax.set_xlabel('SNR-Chang (db)', fontname='Times New Roman')
    ax.set_ylabel('SNR-Standard (db)', fontname='Times New Roman')
    for tick in ax.get_xticklabels():
        tick.set_fontname("Times New Roman")
        tick.set_fontsize(8)
    for tick in ax.get_yticklabels():
        tick.set_fontname("Times New Roman")
        tick.set_fontsize(8)        
    
    
    # Set xlim and ylim
    #ax.set_xlim(20.978242760551243, 88.420371212099)
    #ax.set_ylim(3.251536979292914, 43.47414376123412)

    # Remove borders
    ax.spines['top'].set_linewidth(0)
    ax.spines['right'].set_linewidth(0)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['left'].set_linewidth(0.5)
    

# Show the plot
plt.show()

# Print the correlation and p-value for each dataset
for i, dataset in enumerate(datasets):
    print(f"{dataset} - Correlation: {correlation_list[i]}, p-value: {p_value_list[i]}")
