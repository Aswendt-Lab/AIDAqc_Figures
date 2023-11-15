import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, f_oneway
import glob
import os
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests
import re

# Set font to Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

script_dir = os.path.dirname(__file__)
p_address = os.path.join(script_dir, '..', 'input', 'AIDAqc_Testdaten_PieChart.csv')
p_save = os.path.join(script_dir, '..', 'figures')

# Load the CSV data into a pandas DataFrame
data = pd.read_csv(p_address)

# Clean up the 'Scanner' column to extract the field strength (including decimals)
def extract_field_strength(scanner):
    match = re.search(r'(\d+(\.\d+)?)T', scanner)
    if match:
        return f"{match.group(1)}T"
    else:
        return None

data['Scanner'] = data['Scanner'].apply(extract_field_strength)
cm = 1/2.54  # centimeters in inches

# Set up the figure and axes using subplots
fig, axes = plt.subplots(1, 4, figsize=(22*cm, 10*cm), dpi=300)

rrr = 1.1
# Species pie chart
species_counts = data['Species'].value_counts()
axes[0].pie(species_counts, labels=species_counts.index, autopct='%1.1f%%', startangle=180, pctdistance=0.75,radius=rrr)
#axes[0].set_title('(a) Species', weight='bold', fontsize=10)

# Field strength pie chart
scanner_counts = data['Scanner'].value_counts()
axes[1].pie(scanner_counts, labels=scanner_counts.index, autopct='%1.1f%%', startangle=180, pctdistance=0.70,radius=rrr)
#axes[1].set_title('(b) Field strength', weight='bold', fontsize=10)

# Sequence type pie chart
sequences_data = data['Sequences'].str.split(', ', expand=True)
sequences_melted = sequences_data.melt(value_name='Sequence').dropna()['Sequence']
sequence_counts = sequences_melted.value_counts()
axes[2].pie(sequence_counts, labels=sequence_counts.index, autopct='%1.1f%%', startangle=180, pctdistance=0.65,radius=rrr)
#axes[2].set_title('(c) Sequence type', weight='bold', fontsize=10)

# Data format pie chart
format_counts = data['Data format'].value_counts()
axes[3].pie(format_counts, labels=format_counts.index, autopct='%1.1f%%', startangle=180,radius=rrr)
#axes[3].set_title('(d) Data format', weight='bold', fontsize=10)

# Turn off axes for all subplots
for ax in axes:
    ax.axis('off')

# Adjust layout and save the figure
#plt.tight_layout()
plt.savefig(os.path.join(p_save , "All_Pie_Charts" + ".svg"), format='svg', bbox_inches='tight')
plt.savefig(os.path.join(p_save , "All_Pie_Charts" + ".png"), format='png', bbox_inches='tight')

plt.show()
