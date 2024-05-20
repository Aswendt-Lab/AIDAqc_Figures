import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

cm = 1/2.54  # centimeters in inches

def read_csv_files(files):
    data_dict = {}
    for ff, file in enumerate(files):
        df = pd.read_csv(file)    
        data_type = "anat" if "anat" in file else ("diff" if "diff" in file else "func")
        data_dict[ff] = {data_type: df} 
    return data_dict

def compare_and_plot(data, column_name, group_column):
    sns.set_palette("Set2")  
    plt.figure(figsize=(9*cm, 6*cm))
    sns.boxplot(x=group_column, y=column_name, data=data)
    plt.xlabel(group_column)
    plt.ylabel(column_name)
    plt.title(f"Statistical Comparison of {column_name} by {group_column}")
    plt.tight_layout()
    plt.show()

Path = r"C:\Users\arefk\Desktop\Projects\AIDAqcOutput_of_all_Datasets"

anatomical_files = glob.glob(os.path.join(Path,"*/*/*caculated_features_anat.csv"), recursive=True)
structural_files = glob.glob(os.path.join(Path,"*/*/*caculated_features_diff.csv"), recursive=True)
functional_files = glob.glob(os.path.join(Path,"*/*/*caculated_features_func.csv"), recursive=True)

All_files = [anatomical_files, structural_files, functional_files]

anatomical_data = read_csv_files(anatomical_files)
structural_data = read_csv_files(structural_files)
functional_data = read_csv_files(functional_files)



All_Data = [anatomical_data, structural_data, functional_data]
All_type = ["anat", "diff", "func"]

features_to_compare = ["SpatRx", "SpatRy", "Slicethick"]

fig, axes = plt.subplots(3, 3, figsize=(18*cm, 18*cm), dpi=300)

for i, data in enumerate(All_Data):
    for j, feature in enumerate(features_to_compare):
        cc = 0
        temp = pd.DataFrame()
        Data_of_selected_feature = pd.DataFrame()
        temp_data = pd.DataFrame()

        for key in data:
            try:
                temp_data[feature] = data[key][All_type[i]][feature]
            except KeyError:
                continue
            temp_data["Dataset"] = All_files[i][cc].split(os.sep)[-3]
            cc = cc + 1
            Data_of_selected_feature = pd.concat([Data_of_selected_feature, temp_data], ignore_index=True)
            
        if not Data_of_selected_feature.empty:
            Data_of_selected_feature['sort'] = Data_of_selected_feature['Dataset'].str.extract('(\d+)', expand=True).astype(int)
            Data_of_selected_feature = Data_of_selected_feature.sort_values('sort')
            
            if feature == "SNR Normal":
                Data_of_selected_feature.rename(columns={"SNR Normal": "SNR-Standard (dB)"}, inplace=True)
                feature = "SNR-Standard (dB)"
            elif feature == "SNR Chang":
                Data_of_selected_feature.rename(columns={"SNR Chang": "SNR-Chang (dB)"}, inplace=True)
                feature = "SNR-Chang (dB)"    
            elif feature == "tSNR (Averaged Brain ROI)":
                Data_of_selected_feature.rename(columns={"tSNR (Averaged Brain ROI)": "tSNR (dB)"}, inplace=True)
                feature = "tSNR (dB)"
            elif feature == "Displacement factor (std of Mutual information)":
                Data_of_selected_feature.rename(columns={"Displacement factor (std of Mutual information)": "Motion severity (A.U)"}, inplace=True)
                feature = "Motion severity (A.U)"
                        
            # Assuming "Data_of_selected_feature" is your DataFrame
            if "94_m_Va" in Data_of_selected_feature["Dataset"].values and All_type[i]=="diff":
                # If the condition is met, select the rows where the condition is true and divide the first column by 20
                Data_of_selected_feature.loc[Data_of_selected_feature["Dataset"] == "94_m_Va", Data_of_selected_feature.columns[0]] /= 20
              
            sns.set_style('ticks')
            sns.set(font='Times New Roman', font_scale=0.9,style=None)
            palette = 'Set2'
            ax = sns.barplot(x="Dataset", y=feature, data=Data_of_selected_feature, ci=None, palette=palette, ax=axes[i, j])
            ax.set_xlabel('')
            ax.set_ylabel(f'{All_type[i]}-{feature} (mm)', fontweight='bold', fontsize=9)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=4.5, ha='right')  # Adjust tick labels
            ax.spines['top'].set_linewidth(0.5)  
            ax.spines['right'].set_linewidth(0.5)  
            ax.spines['bottom'].set_linewidth(0.5)  
            ax.spines['left'].set_linewidth(0.5)  
            ax.tick_params(axis='both', which='both', width=0.5, color='gray', length=2)
            ax.yaxis.grid(True)  # Add horizontal gridlines
            plt.tight_layout()


#%%
output_path = r"C:\Users\arefk\Desktop\Projects\AIDAqc_Figures\figures\PaperFigures\AswenSupplement1"

# Save as SVG
plt.savefig(output_path + ".svg", format='svg')

# Save as PNG
plt.savefig(output_path + ".png", dpi=300, format='png')
plt.show()
