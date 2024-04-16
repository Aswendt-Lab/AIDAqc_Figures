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
path = r"C:\Users\arefk\Desktop\Projects\testData\proc_data"
csv_voting_path = r"C:\Users\arefk\Desktop\Projects\testData\proc_data2\QC\votings.csv"

# Read CSV file for voting
df_voting = pd.read_csv(csv_voting_path, delimiter=";")

# Find DWI files
SearchP = os.path.join(path, "**", "dwi", "*dwi.nii.gz")
BetFiles = glob.glob(SearchP, recursive=True)

for bb in BetFiles:
    temp = os.path.dirname(bb)
    SearchFA = os.path.join(temp, "**", "fa_flipped.nii.gz")
    FA = glob.glob(SearchFA, recursive=True)[0]

    # Load DWI and FA images
    dwi_img = nib.load(bb)
    fa_img = nib.load(FA)

    # Rotate images 90 degrees
    dwi_data_rotated = np.rot90(dwi_img.get_fdata(), k=-1)
    fa_data_rotated = np.rot90(fa_img.get_fdata(), k=-1)

    # Plot images
    fig, axes = plt.subplots(1, 2)
    axes[0].imshow(dwi_data_rotated[:, :, dwi_data_rotated.shape[-2] // 2+3, dwi_data_rotated.shape[-1] // 2], cmap='gray')
    axes[0].set_title('Original', fontweight='bold')
    axes[1].imshow(fa_data_rotated[:, :, fa_data_rotated.shape[-1] // 2+3], cmap='gray')
    axes[1].set_title('FA Map', fontweight='bold')

    # Find corresponding entry in CSV_voting
    df_bb_voting = df_voting[df_voting['Pathes'] == bb]
    if not df_bb_voting.empty:
        voting_value = df_bb_voting['Voting outliers (from 5)'].values[0]
    else:
        voting_value = 0
    axes[0].text(10, 30, f'Voting Outliers: {voting_value}', color='blue', fontweight='bold')

    plt.show()
