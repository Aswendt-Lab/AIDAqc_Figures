import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Read data from the CSV file
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '..', 'input', 'MUplot.csv')
out_path = os.path.join(script_dir, '..', 'figures')
df = pd.read_csv(file_path, header=None, names=['Shift (Voxel)', 'Severe motion', 'No motion'], skiprows=1)

# Set the seaborn style and palette
sns.set(style='ticks', palette='Set1')

# Set font properties
font_properties = {'family': 'Times New Roman', 'size': 8}
font_properties2 = {'family': 'Times New Roman', 'size': 6}

cm = 1/2.54  # centimeters in inches

# Create the plot
fig, ax = plt.subplots(figsize=(7.01*cm, 3.21*cm), dpi=300)
ax.plot(df['Shift (Voxel)'], df['Severe motion'], label='Severe motion', linewidth=1)  # Adjust the line width
ax.plot(df['Shift (Voxel)'], df['No motion'], label='No motion', linewidth=1, color='blue')  # Adjust the line width

# Set axis labels
ax.set_xlabel('Time Points (s)', **font_properties)
ax.set_ylabel('Mutual information (a.u)', **font_properties)

# Set axis ticks font and number of ticks
ax.tick_params(axis='both', which='both', width=0.5, color='gray', length=2)
ax.locator_params(axis='x', nbins=8)  # Set the number of ticks for the x-axis
ax.locator_params(axis='y', nbins=8)  # Set the number of ticks for the y-axis

for tick in ax.get_xticklabels():
    tick.set_fontname('Times New Roman')
    tick.set_fontsize(8)
for tick in ax.get_yticklabels():
    tick.set_fontname('Times New Roman')
    tick.set_fontsize(8)

# Set legend font and remove the legend border
legend = ax.legend(prop=font_properties2, frameon=False)

# Customize the border linewidth
ax.spines['top'].set_linewidth(0.5)     # Top border
ax.spines['right'].set_linewidth(0.5)   # Right border
ax.spines['bottom'].set_linewidth(0.5)  # Bottom border
ax.spines['left'].set_linewidth(0.5)   # Left border

# Adjust layout to include labels
plt.subplots_adjust(left=0.15, right=0.95, top=1.1, bottom=0.25)

# Save figures as PNG and SVG with 300 dpi
fig_path_png = os.path.join(out_path, 'MutualInformation.png')
fig_path_svg = os.path.join(out_path, 'MutualInformation.svg')

fig.savefig(fig_path_png, format='png', bbox_inches='tight')
fig.savefig(fig_path_svg, format='svg', bbox_inches='tight')

# Show the plot
plt.show()
