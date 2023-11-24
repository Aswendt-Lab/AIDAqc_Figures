import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from matplotlib import rcParams

# Set font to Times New Roman
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman']
rcParams['font.size'] = 8

# Load your Excel file into a Pandas DataFrame
# ... (your existing code)
# Read data from the CSV file
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '..', 'input')
out_path = os.path.join(script_dir, '..', 'figures')

csv_file = os.path.join(file_path, "Confusion_matrix_metrics.csv")

df = pd.read_csv(csv_file)

df.loc[df["sequence_name"] == "anat", "sequence_name"] = "Anatomical"
df.loc[df["sequence_name"] == "diff", "sequence_name"] = "Diffusion"
df.loc[df["sequence_name"] == "func", "sequence_name"] = "Functional"

# Set the user-defined thresholds to get desired values
Thresold_Human_Voters_random = 1  # Replace with the user-set threshold value
Thresold_ML_Voters_random = 1

# Filter the DataFrame based on the user-set threshold
filtered_df_random = df[(df['Thresold_Human_Voters'] == Thresold_Human_Voters_random) &
                        (df['Thresold_ML_Voters'] == Thresold_ML_Voters_random) &
                        (df['TP'] + df['FN'] > 0)
                        & (df['sequence_name'] == "Anatomical")]

# Set the user-defined thresholds to get desired values
Thresold_Human_Voters_Good = 1  # Replace with the user-set threshold value
Thresold_ML_Voters_Good = 3

# Filter the DataFrame based on the user-set threshold
filtered_df_Good = df[(df['Thresold_Human_Voters'] == Thresold_Human_Voters_Good) &
                      (df['Thresold_ML_Voters'] == Thresold_ML_Voters_Good) &
                      (df['TP'] + df['FN'] > 0)]

# Add Filter_Type column
filtered_df_random['Filter_Type'] = 0
filtered_df_Good['Filter_Type'] = 1

# Concatenate the two filtered dataframes
concatenated_df = pd.concat([filtered_df_random, filtered_df_Good])
custom_palette = ["#DBE3EF","#3A67B8"]
# Create plot for Anatomical
g = sns.catplot(
    data=concatenated_df[concatenated_df['sequence_name'] == 'Anatomical'], kind="bar",
    x="dataset_name", y="Sensitivity-Recall", hue="Filter_Type",
    palette=custom_palette, alpha=1, height=5, aspect=(18/5)  # Adjust the height and aspect ratio
)
cm = 1/2.54

# Customize the plot as needed
g.set(title='Accuracy Comparison - Anatomical', xlabel='Dataset Name', ylabel='Accuracy')
g.fig.set_dpi(300)  # Set DPI
g.fig.set_size_inches(18*cm, 18*cm)  # Set size in inches

# Customize x-axis ticks
plt.xticks(rotation=45)

# Add borders to the top and right side of the plot
sns.despine()

# Rename the legend
g._legend.set_title('Threshold Type')
plt.tight_layout()

plt.show()
#%%
# Filter the DataFrame based on the user-set threshold
filtered_df_random = df[(df['Thresold_Human_Voters'] == Thresold_Human_Voters_random) &
                        (df['Thresold_ML_Voters'] == Thresold_ML_Voters_random) &
                        (df['TP'] + df['FN'] > 0)
                        & (df['sequence_name'] == "Diffusion")]

# Set the user-defined thresholds to get desired values
Thresold_Human_Voters_Good = 1  # Replace with the user-set threshold value
Thresold_ML_Voters_Good = 2
sns.color_palette("light:b", as_cmap=True)
# Filter the DataFrame based on the user-set threshold
filtered_df_Good = df[(df['Thresold_Human_Voters'] == Thresold_Human_Voters_Good) &
                      (df['Thresold_ML_Voters'] == Thresold_ML_Voters_Good) &
                      (df['TP'] + df['FN'] > 0)]

# Add Filter_Type column
filtered_df_random['Filter_Type'] = 0
filtered_df_Good['Filter_Type'] = 1

# Concatenate the two filtered dataframes
concatenated_df = pd.concat([filtered_df_random, filtered_df_Good])
custom_palette = ["#F8E6DC","#F66900"]
# Create plot for Diffusion
g = sns.catplot(
    data=concatenated_df[concatenated_df['sequence_name'] == 'Diffusion'], kind="bar",
    x="dataset_name", y="Sen", hue="Filter_Type",
    palette=custom_palette, alpha=.6, height=5, aspect=(18/5)  # Adjust the height and aspect ratio
)
# Customize the plot as needed
g.set(title='Accuracy Comparison - Diffusion', xlabel='Dataset Name', ylabel='Accuracy')
g.fig.set_dpi(300)  # Set DPI
g.fig.set_size_inches(18*cm, 5*cm)  # Set size in inches

# Customize x-axis ticks
plt.xticks(rotation=45)

# Add borders to the top and right side of the plot
sns.despine()

# Rename the legend
g._legend.set_title('Threshold Type')
plt.tight_layout()

plt.show()
#%%
# Filter the DataFrame based on the user-set threshold
filtered_df_random = df[(df['Thresold_Human_Voters'] == Thresold_Human_Voters_random) &
                        (df['Thresold_ML_Voters'] == Thresold_ML_Voters_random) &
                        (df['TP'] + df['FN'] > 0)
                        & (df['sequence_name'] == "Functional")]

# Set the user-defined thresholds to get desired values
Thresold_Human_Voters_Good = 1  # Replace with the user-set threshold value
Thresold_ML_Voters_Good = 2

# Filter the DataFrame based on the user-set threshold
filtered_df_Good = df[(df['Thresold_Human_Voters'] == Thresold_Human_Voters_Good) &
                      (df['Thresold_ML_Voters'] == Thresold_ML_Voters_Good) &
                      (df['TP'] + df['FN'] > 0)]

# Add Filter_Type column
filtered_df_random['Filter_Type'] = 0
filtered_df_Good['Filter_Type'] = 1

# Concatenate the two filtered dataframes
concatenated_df = pd.concat([filtered_df_random, filtered_df_Good])

# Create plot for Functional
g = sns.catplot(
    data=concatenated_df[concatenated_df['sequence_name'] == 'Functional'], kind="bar",
    x="dataset_name", y="Sensitivity-Recall", hue="Filter_Type",
    palette={0: "#DDEEE1", 1: "#376D43"}, alpha=.6, height=5, aspect=(18/5)  # Adjust the height and aspect ratio
)

# Customize the plot as needed
g.set(title='Accuracy Comparison - Functional', xlabel='Dataset Name', ylabel='Accuracy')
g.fig.set_dpi(300)  # Set DPI
g.fig.set_size_inches(18*cm, 5*cm)  # Set size in inches

# Customize x-axis ticks
plt.xticks(rotation=45)

# Add borders to the top and right side of the plot
sns.despine()

# Rename the legend
g._legend.set_title('Threshold Type')
plt.tight_layout()


plt.show()
