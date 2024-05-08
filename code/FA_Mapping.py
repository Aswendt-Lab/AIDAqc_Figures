import glob
import os
import pandas as pd
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

# Set font properties
rcParams['font.family'] = 'times new roman'
rcParams['font.size'] = 8

# Define file paths
path = r"C:\Users\aswen\Desktop\TestingData\Aswendt_qc_rsfmri_plot\proc_data"
csv_voting_path =r"C:\Users\aswen\Desktop\TestingData\Aswendt_qc_rsfmri_plot\QC\votings.csv"

# Function to read CSV files and store them in a dictionary
script_dir = os.path.dirname(__file__)  # Use this line if running from a script file
out_path = os.path.join(script_dir, '..', 'figures',"PaperFigures",'supplement_figure_6')
if not os.path.exists(out_path):
    os.mkdir(out_path)

# Read CSV file for voting
df_voting = pd.read_csv(csv_voting_path, delimiter=",")

# Find DWI files
SearchP = os.path.join(path, "**", "dwi", "*dwi.nii.gz")
BetFiles = glob.glob(SearchP, recursive=True)

for bb in BetFiles:
    temp = os.path.dirname(bb)
    SearchFA = os.path.join(temp, "**", "fa_flipped.nii.gz")
    try:
        FA = glob.glob(SearchFA, recursive=True)[0]
    except IndexError:
        continue
    title = os.path.basename(bb).replace("_dwi.nii.gz","")
    # Load DWI and FA images
    dwi_img = nib.load(bb)
    fa_img = nib.load(FA)

    # Rotate images 90 degrees
    dwi_data_rotated = np.rot90(dwi_img.get_fdata(), k=-1)
    fa_data_rotated = np.rot90(fa_img.get_fdata(), k=-1)

        # Plot images
    fig, axes = plt.subplots(1, 2, figsize=(8/2.54, 6/2.54))  # Size in inches converted to centimeters
    fig.subplots_adjust(wspace=-0.1)  # Adjust the horizontal space between subplots to 0
    fig.suptitle(title)  # Add title
    axes[0].imshow(dwi_data_rotated[:, :, dwi_data_rotated.shape[-2] // 2+5, dwi_data_rotated.shape[-1] // 2], cmap='gray')
    axes[0].text(0.5, 0.05, 'DWI', color='white', fontweight='bold', ha='center', transform=axes[0].transAxes)
    axes[0].axis('off')  # Turn off axes
    
    axes[1].imshow(np.fliplr(fa_data_rotated[:, :, fa_data_rotated.shape[-1] // 2+5]), cmap='gray')  # Flip left to right
    axes[1].text(0.5, 0.05, 'FA Map', color='white', fontweight='bold', ha='center', transform=axes[1].transAxes)
    axes[1].axis('off')  # Turn off axes
    
        
    # Find corresponding entry in CSV_voting
    df_bb_voting = df_voting[df_voting['Pathes'] == bb]
    if not df_bb_voting.empty:
        voting_value = df_bb_voting['Voting outliers (from 5)'].values[0]
        if voting_value>1:
        
            axes[0].text(5, 15, f'Majority Votes: {voting_value}', color='red', fontweight='bold')
        else:
            axes[0].text(5, 15, f'Majority Votes: {voting_value}', color='yellow', fontweight='bold')
    
    
    else:
        voting_value = 0
        axes[0].text(5, 15, f'Majority Votes: {voting_value}', color='white', fontweight='bold')
    
    plt.savefig(os.path.join(out_path, os.path.basename(bb).replace(".nii.gz", "").replace("Underscore", "_") + ".svg"), transparent=True, bbox_inches='tight')
    plt.show()
