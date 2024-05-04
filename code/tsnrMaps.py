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

# Function to read CSV files and store them in a dictionary
script_dir = os.path.dirname(__file__)  # Use this line if running from a script file
out_path = os.path.join(script_dir, '..', 'figures', 'supplement_figure_6')
if not os.path.exists(out_path):
    os.mkdir(out_path)

# Read CSV file for voting
df_voting = pd.read_csv(csv_voting_path)

# Find DWI files
SearchP = os.path.join(path, "**", "func", "*EPI.nii.gz")
BetFiles = glob.glob(SearchP, recursive=True)

for bb in BetFiles:
    temp = os.path.dirname(bb)
    Searchmask = os.path.join(temp, "**", "*AnnoSplit_parental.nii.gz")
    mask = glob.glob(Searchmask, recursive=True)[0]
    SearchBet = os.path.join(temp, "**", "*Bet.nii.gz")
    Bet = glob.glob(SearchBet, recursive=True)[0]
    
    # Load 4D DWI file
    dwi_img = nib.load(bb)
    dwi_data = dwi_img.get_fdata()
    
    # Load 3D Bet image
    bet_img = nib.load(Bet)
    bet_data = bet_img.get_fdata()
    
    # Load 3D mask image
    mask_img = nib.load(mask)
    mask_data = mask_img.get_fdata()
    
    # Plotting
    fig, axes = plt.subplots(2, 4, figsize=(4.72, 3.54), dpi=300)  # 12 cm wide, DPI=300
    plt.subplots_adjust(wspace=0, hspace=0)  # Reduce space between subplots
    
    # First row: 4 equally distributed slices from the middle of the Bet image
    middle_slice = bet_data.shape[2] // 2
    for i, ax in enumerate(axes[0]):
        slice_data = np.rot90(bet_data[..., middle_slice + 2*i], k=-1)
        ax.imshow(slice_data, cmap='gray')
        ax.set_xticks([])  # Remove x ticks
        ax.set_yticks([])  # Remove y ticks
    
    # Second row: same slices for the mask image
    for i, ax in enumerate(axes[1]):
        slice_data = np.rot90(mask_data[..., middle_slice + 2*i], k=-1)
        ax.imshow(slice_data, cmap='gray')
        ax.set_xticks([])  # Remove x ticks
        ax.set_yticks([])  # Remove y ticks
    
    # Third row: Time course plot
    time_points = dwi_data.shape[-1]
    selected_voxels = [485, 2485, 353, 2353, 985, 2985,329,2329,198,2198,1080,3080]
    bigmask = np.zeros_like(mask_data)
    for ss in selected_voxels:
        bigmask += (mask_data == ss)
    
    region_mean = []
    for tt in range(20, dwi_data.shape[-1]):  # Skip the first 20 seconds
        tempdwi = dwi_data[..., tt]
        region_mean.append(np.mean(tempdwi[bigmask != 0]))
    
    fig, ax = plt.subplots(figsize=(2.36, 1.77), dpi=300)  # 6 cm wide, DPI=300
    ax.plot(range(20, time_points), region_mean, label='Merged Region')
    ax.set_xlabel('Time Points')
    ax.set_ylabel('Average Intensity')
    plt.tight_layout()
    plt.show()
