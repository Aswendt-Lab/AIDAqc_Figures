import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as ticker
import os
# Load your Excel file into a Pandas DataFrame

# Read data from the CSV file
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '..', 'input')
out_path = os.path.join(script_dir, '..', 'figures')

csv_file = os.path.join(file_path,"Confusion_matrix_metrics.csv")

df = pd.read_csv(csv_file)

# Set the user-defined thresholds to get desired values
Thresold_Human_Voters = 4  # Replace with the user-set threshold value
Thresold_ML_Voters = 1

# Filter the DataFrame based on the user-set threshold
filtered_df = df[(df['Thresold_Human_Voters'] == Thresold_Human_Voters) &
                 (df['Thresold_ML_Voters'] == Thresold_ML_Voters) &
                (df['TP']+df['FN']  > 0)]
                 

filtered_df.loc[filtered_df["sequence_name"] == "anat","sequence_name"] = "Anatomical"
filtered_df.loc[filtered_df["sequence_name"] == "diff","sequence_name"] = "Diffusion"
filtered_df.loc[filtered_df["sequence_name"] == "func","sequence_name"] = "Functional"

cm = 1/2.54  # centimeters in inches
# Create two subplots for Kappa and F1 scores heatmaps
fig, axes = plt.subplots(1, 1, figsize=(20*cm, 4*cm), dpi=300)
sns.set_style('darkgrid')
# Specify the font properties
font_properties = fm.FontProperties(family='Times New Roman', size=8)
font_properties2 = fm.FontProperties(family='Times New Roman', size=10)
Title = ["(a) Fleiss kappa score: inter rater reliability "," (b) F1_score: raters vs AIDAqc"]
for i, metric in enumerate(['Sensitivity-Recall']):
    ax = axes
    pivot_df = filtered_df.pivot(index='sequence_name', columns='dataset_name', values=metric)
    pivot_df['mean'] = pivot_df.mean(axis=1)
    pivot_df['std'] = pivot_df.std(axis=1)
    t=Title[i]
    sns.heatmap(pivot_df, annot=True, fmt=".1f", cmap="YlGnBu", cbar=True, ax=ax)

    # Set font properties for labels, titles, and annotations
    ax.set_xticklabels(ax.get_xticklabels(), fontproperties=font_properties)
    ax.set_yticklabels(ax.get_yticklabels(), fontproperties=font_properties)
    ax.set_xlabel('Datasets', fontproperties=font_properties)
    ax.set_ylabel('Sequences', fontproperties=font_properties)
    #ax.set_title(f'{t} ', fontsize=10, fontproperties=font_properties2, fontweight='bold')
    ax.set(xlabel=None)
    # Set the color bar legend font size and font properties
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=8)
    cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(), fontproperties=font_properties)
    
    # Customize the color bar ticks (increase the number of ticks)
    cbar.ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    
    a = []
    for text in ax.texts:
        a.append(float(text.get_text()))
        
    

    for text in ax.texts:
        text.set_font("Times New Roman")
        text.set_size(8)
                
# Show the plots
plt.tight_layout()

output_path = out_path
output_filename = "HeatMap_Recall_ManualRater4_AIDAqc1"

# Save as SVG
#fig.savefig(f"{output_path}/{output_filename}.svg", format="svg")

# Save as PNG
#fig.savefig(f"{output_path}/{output_filename}.png", format="png")

plt.show()
#%% All Thresholds loops through
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as ticker
import os
# Load your Excel file into a Pandas DataFrame

# Read data from the CSV file
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '..', 'input')
out_path = os.path.join(script_dir, '..', 'figures')

csv_file = os.path.join(file_path,"Confusion_matrix_metrics.csv")

df = pd.read_csv(csv_file)

# Set the user-defined thresholds to get desired values

for Thresold_Human_Voters in df["Thresold_Human_Voters"].unique():
    for Thresold_ML_Voters in df["Thresold_ML_Voters"].unique():
        # Filter the DataFrame based on the user-set threshold
        filtered_df = df[(df['Thresold_Human_Voters'] == Thresold_Human_Voters) &
                         (df['Thresold_ML_Voters'] == Thresold_ML_Voters) &
                        (df['TP']+df['FN']  > 0)]
                         
        
        filtered_df.loc[filtered_df["sequence_name"] == "anat","sequence_name"] = "Anatomical"
        filtered_df.loc[filtered_df["sequence_name"] == "diff","sequence_name"] = "Diffusion"
        filtered_df.loc[filtered_df["sequence_name"] == "func","sequence_name"] = "Functional"
        
        cm = 1/2.54  # centimeters in inches
        # Create two subplots for Kappa and F1 scores heatmaps
        fig, axes = plt.subplots(1, 1, figsize=(20*cm, 5*cm), dpi=300)
        sns.set_style('darkgrid')
        # Specify the font properties
        font_properties = fm.FontProperties(family='Times New Roman', size=8)
        font_properties2 = fm.FontProperties(family='Times New Roman', size=10)
        Title = ["(a) Fleiss kappa score: inter rater reliability "," (b) F1_score: raters vs AIDAqc"]
        for i, metric in enumerate(['Sensitivity-Recall']):
            ax = axes
            pivot_df = filtered_df.pivot(index='sequence_name', columns='dataset_name', values=metric)
            pivot_df['mean'] = pivot_df.mean(axis=1)
            pivot_df['std'] = pivot_df.std(axis=1)
            t = "Human: " + str(Thresold_Human_Voters) + "|| AIDAqc:" +str(Thresold_ML_Voters) 
            sns.heatmap(pivot_df, annot=True, fmt=".2f", cmap="YlGnBu", cbar=True, ax=ax)
        
            # Set font properties for labels, titles, and annotations
            ax.set_xticklabels(ax.get_xticklabels(), fontproperties=font_properties)
            ax.set_yticklabels(ax.get_yticklabels(), fontproperties=font_properties)
            ax.set_xlabel('Datasets', fontproperties=font_properties)
            ax.set_ylabel('Sequences', fontproperties=font_properties)
            ax.set_title(f'{t} ', fontsize=10, fontproperties=font_properties2, fontweight='bold')
            ax.set(xlabel=None)
            # Set the color bar legend font size and font properties
            cbar = ax.collections[0].colorbar
            cbar.ax.tick_params(labelsize=8)
            cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(), fontproperties=font_properties)
            
            # Customize the color bar ticks (increase the number of ticks)
            cbar.ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
            
            a = []
            for text in ax.texts:
                a.append(float(text.get_text()))
                
            
        
            for text in ax.texts:
                text.set_font("Times New Roman")
                text.set_size(8)
                
                
        # Show the plots
        plt.tight_layout()
        
        plt.show()