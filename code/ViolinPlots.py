import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, f_oneway
import glob
import os
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests
import re

#% Function to read CSV files and store them in a dictionary
script_dir = os.path.dirname(__file__)
out_path = os.path.join(script_dir, '..', 'figures')
cm = 1/2.54  # centimeters in inches
def read_csv_files(files):
    data_dict = {}
    for ff,file in enumerate(files):
        df = pd.read_csv(file)    
        # Extract the data type from the file name (assuming the file name contains "anat", "diff", or "func")
        data_type = "anat" if "anat" in file else ("diff" if "diff" in file else "func")
        data_dict[ff] = {data_type:df} 
            
    return data_dict


# Function for statistical comparison and plotting
def compare_and_plot(data, column_name, group_column):
    sns.set_palette("Set2")  # Use colors for color-blind people
    plt.figure(figsize=(9*cm, 6*cm))
    sns.boxplot(x=group_column, y=column_name, data=data)
    plt.xlabel(group_column)
    plt.ylabel(column_name)
    plt.title(f"Statistical Comparison of {column_name} by {group_column}")
    plt.tight_layout()
    #plt.savefig(f"{column_name}_by_{group_column}_boxplot.png")
    plt.show()

#% List of CSV files for each data type
Path = r"C:\Users\arefk\Desktop\Projects\AIDAqcOutput_of_all_Datasets"

anat_files = [file for file in glob.glob(os.path.join(Path, "*/*/*caculated_features_anat.csv"), recursive=True) if "m_Rei" not in file and "7_m_Lo" not in file]
diff_files = [file for file in glob.glob(os.path.join(Path, "*/*/*caculated_features_diff.csv"), recursive=True) if "m_Rei" not in file and "7_m_Lo" not in file]
func_files = [file for file in glob.glob(os.path.join(Path, "*/*/*caculated_features_func.csv"), recursive=True) if "m_Rei" not in file and "7_m_Lo" not in file]

All_files = [anat_files,diff_files,func_files]

# Read the CSV files and store them in dictionaries
anat_data = read_csv_files(anat_files)
diff_data = read_csv_files(diff_files)
func_data = read_csv_files(func_files)
All_Data = [anat_data,diff_data,func_data]

All_type = ["anat","diff","func"]
#% data statistisc figure 7
BINS = [8,8,8]
features_to_compare = ["SNR Chang", "SNR Normal", "tSNR (Averaged Brain ROI)", "Displacement factor (std of Mutual information)"]

#features_to_compare = ["SpatRx", "SpatRy", "Slicethick"]


Data_of_selected_feature2 = pd.DataFrame()
for dd,data in enumerate(All_Data):
    for feature in features_to_compare:
        cc = 0
        temp = pd.DataFrame()
        Data_of_selected_feature = pd.DataFrame()
        temp_data = pd.DataFrame()

        for key in data:
            try:
                temp_data[feature] = data[key][All_type[dd]][feature]
            except KeyError:
                continue
            temp_data["Dataset"] = All_files[dd][cc].split(os.sep)[-3]
            cc = cc +1
            Data_of_selected_feature = pd.concat([Data_of_selected_feature, temp_data], ignore_index=True)
            #Data_of_selected_feature2 = pd.concat([Data_of_selected_feature2, temp_data], ignore_index=True)
            
            
            
        if not Data_of_selected_feature.empty:
            Data_of_selected_feature['sort'] = Data_of_selected_feature['Dataset'].str.extract('(\d+)', expand=True).astype(int)
            Data_of_selected_feature = Data_of_selected_feature.sort_values('sort')
            
            if feature == "SNR Normal":
                Data_of_selected_feature.rename(columns={"SNR Normal": "SNR-Standard (dB)"}, inplace=True)
                feature = "SNR-Standard (dB)"
            if feature == "SNR Chang":
                Data_of_selected_feature.rename(columns={"SNR Chang": "SNR-Chang (dB)"}, inplace=True)
                feature = "SNR-Chang (dB)"    
            elif feature == "tSNR (Averaged Brain ROI)":
                Data_of_selected_feature.rename(columns={"tSNR (Averaged Brain ROI)": "tSNR (dB)"}, inplace=True)
                feature = "tSNR (dB)"
            elif feature == "Displacement factor (std of Mutual information)":
                Data_of_selected_feature.rename(columns={"Displacement factor (std of Mutual information)": "Motion severity (a.u)"}, inplace=True)
                BINS[dd] = 10
                feature = "Motion severity (a.u)"
            
            
            #Data_of_selected_feature2["Vol"] = Data_of_selected_feature2["SpatRx"]*Data_of_selected_feature2["SpatRy"]*Data_of_selected_feature2["Slicethick"]
            
            #Data_of_selected_feature = Data_of_selected_feature.sort_values("Dataset",ascending=False)
            # creating boxplots
            if All_type[dd] == "anat":
                plt.figure(figsize=(21.3*cm,3.527*cm),dpi=600)
            else:
                plt.figure(figsize=(9.70*cm,3.527*cm),dpi=600)
                
            sns.set_style('ticks')
            sns.set(font='Times New Roman',style=None)  # Set font to Times New Roman and font size to 9
            palette = 'Set2'
            ax = sns.violinplot(x="Dataset", y=feature, data=Data_of_selected_feature, hue="Dataset", dodge=False,
                                palette=palette,
                                scale="width", inner=None,linewidth=1)
            patches = ax.patches
            #legend_colors = [patch.get_facecolor() for patch in patches[:]]

            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            for violin in ax.collections:
                bbox = violin.get_paths()[0].get_extents()
                x0, y0, width, height = bbox.bounds
                violin.set_clip_path(plt.Rectangle((x0, y0), width / 2, height, transform=ax.transData))
            
            sns.boxplot(x="Dataset", y=feature, data=Data_of_selected_feature, saturation=1, showfliers=False,
                        width=0.3, boxprops={'zorder': 3, 'facecolor': 'none'}, ax=ax, linewidth=1)
            old_len_collections = len(ax.collections)
            sns.stripplot(x="Dataset", y=feature, data=Data_of_selected_feature,size=1.1, hue="Dataset", palette=palette, dodge=False, ax=ax)
            for dots in ax.collections[old_len_collections:]:
                dots.set_offsets(dots.get_offsets() + np.array([0.12, 0]))
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
            #ax.legend_.remove()
            ax.locator_params(axis='y', nbins=BINS[dd])  # Set the number of ticks for the y-axis
            
            ax
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45,fontsize=8)
            ax.set_yticklabels(ax.get_yticklabels(),fontsize=8)
            
            
            #ax.set_yticks(np.linspace(ax.get_ylim()[0], ax.get_ylim()[1], BINS[dd]))


# =============================================================================
#             for label, color in zip(ax.get_xticklabels(), legend_colors):
#                 label.set_color(color)
# =============================================================================
            ax.set_xlabel('')
            ax.set_title(All_type[dd].capitalize(),weight='bold',fontsize=10)
            y_label = ax.set_ylabel(ax.get_ylabel(),fontsize=8)

# =============================================================================
            ax.xaxis.grid(True, linestyle='-', which='major', color='gray', linewidth=0)
            ax.xaxis.grid(True, linestyle='--', which='minor', color='gray', linewidth=0)
# 
            ax.yaxis.grid(True, linestyle='-', which='major', color='gray', linewidth=0)
            ax.yaxis.grid(True, linestyle='--', which='minor', color='gray', linewidth=0)        
# =============================================================================
            ax.spines['top'].set_linewidth(0.5)  # Top border
            ax.spines['right'].set_linewidth(0.5)  # Right border
            ax.spines['bottom'].set_linewidth(0.5)  # Bottom border
            ax.spines['left'].set_linewidth(0.5)  # Left border
                        # Set axis ticks font and number of ticks
            ax.tick_params(axis='both', which='both', width=0.5, color='gray', length=2)
            
            ax.tick_params(axis='both', which='both', width=0.5,color='gray',length=2)
            plt.xticks(ha='right')
            plt.savefig(os.path.join(out_path,feature+"_"+All_type[dd]+"withoutAbdominal.svg"), format='svg', bbox_inches='tight',transparent=False)
            plt.savefig(os.path.join(out_path,feature+"_"+All_type[dd]+"withoutAbdominal.png"),dpi=300 ,format='png', bbox_inches='tight',transparent=False)
            plt.show()