import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '..', 'input', 'Ghostplot.csv')
out_path = os.path.join(script_dir,'..','figures')
df = pd.read_csv(file_path, header=None, names=['Shift (Voxel)', 'Severe motion', 'No motion'], skiprows=1)

# Set the seaborn style and palette
sns.set(style='ticks', palette='Set1')

# Set font properties
font_properties = {'family': 'Times New Roman', 'size': 8}
font_properties2 = {'family': 'Times New Roman', 'size': 8}

cm = 1/2.54  # centimeters in inches

# Create the first plot (No ghost)
fig1, ax1 = plt.subplots(figsize=(5.2*cm, 4.91*cm), dpi=300)
ax1.plot(df['Shift (Voxel)'], df['No motion'], label='No ghost', linewidth=1, color='red')
ax1.set_xlabel('Shift (Voxel)', **font_properties)
ax1.set_ylabel('Mutual Information (a.u)', **font_properties)
ax1.tick_params(axis='both', which='both', width=0.5, color='gray', length=2)
ax1.locator_params(axis='x', nbins=8)  # Set the number of ticks for the x-axis
ax1.locator_params(axis='y', nbins=8)  # Set the number of ticks for the y-axis

for tick in ax1.get_xticklabels():
    tick.set_fontname('Times New Roman')
    tick.set_fontsize(8)
for tick in ax1.get_yticklabels():
    tick.set_fontname('Times New Roman')
    tick.set_fontsize(8)

ax1.spines['top'].set_linewidth(0.5)     # Top border
ax1.spines['right'].set_linewidth(0.5)   # Right border
ax1.spines['bottom'].set_linewidth(0.5)  # Bottom border
ax1.spines['left'].set_linewidth(0.5)   # Left border
ax1.xaxis.grid(True, linestyle='-', which='major', color='gray', linewidth=0)
ax1.xaxis.grid(True, linestyle='--', which='minor', color='gray', linewidth=0)
ax1.yaxis.grid(True, linestyle='-', which='major', color='gray', linewidth=0)
ax1.yaxis.grid(True, linestyle='--', which='minor', color='gray', linewidth=0)        
plt.tight_layout()
# Create the second plot (Ghost)
fig2, ax2 = plt.subplots(figsize=(5.2*cm, 4.91*cm), dpi=300)
ax2.plot(df['Shift (Voxel)'], df['Severe motion'], label='Ghost', linewidth=1, color='blue')
ax2.set_xlabel('Shift (Voxel)', **font_properties)
ax2.set_ylabel('Mutual Information (a.u)', **font_properties)
ax2.tick_params(axis='both', which='both', width=0.5, color='gray', length=2)
ax2.locator_params(axis='x', nbins=8)  # Set the number of ticks for the x-axis
ax2.locator_params(axis='y', nbins=8)  # Set the number of ticks for the y-axis

for tick in ax2.get_xticklabels():
    tick.set_fontname('Times New Roman')
    tick.set_fontsize(8)
for tick in ax2.get_yticklabels():
    tick.set_fontname('Times New Roman')
    tick.set_fontsize(8)

ax2.spines['top'].set_linewidth(0.5)     # Top border
ax2.spines['right'].set_linewidth(0.5)   # Right border
ax2.spines['bottom'].set_linewidth(0.5)  # Bottom border
ax2.spines['left'].set_linewidth(0.5)   # Left border

ax2.xaxis.grid(True, linestyle='-', which='major', color='gray', linewidth=0)
ax2.xaxis.grid(True, linestyle='--', which='minor', color='gray', linewidth=0)
ax2.yaxis.grid(True, linestyle='-', which='major', color='gray', linewidth=0)
ax2.yaxis.grid(True, linestyle='--', which='minor', color='gray', linewidth=0)
plt.tight_layout()
# Save figures as SVG and PNG with 300 dpi
fig1_path = os.path.join(out_path, 'GhostingPlotHighMotion.svg')
fig2_path = os.path.join(out_path, 'GhostingPlotLowMotion.svg')
fig3_path = os.path.join(out_path, 'GhostingPlotHighMotion.png')
fig4_path = os.path.join(out_path, 'GhostingPlotLowMotion.png')

fig1.savefig(fig1_path, format='svg')
fig2.savefig(fig2_path, format='svg')


fig1.savefig(fig3_path, format='png')
fig2.savefig(fig4_path, format='png')

# Show the plots
plt.show()
