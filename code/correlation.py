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
csv_voting_path = r"C:\Users\aswen\Desktop\TestingData\Aswendt_qc_rsfmri_plot\QC\votings.csv"

# Function to read CSV files and store them in a dictionary
script_dir = os.path.dirname(__file__)  # Use this line if running from a script file
out_path = os.path.join(script_dir, '..', 'figures', 'supplement9')

if not os.path.exists(out_path):
    os.mkdir(out_path)

# Read CSV file for voting
#df_voting = pd.read_csv(csv_voting_path, delimiter=",")

# Find rs-fMRI files
search_pattern = os.path.join(path, "**", "func", "rs-fMRI_niiData", "*_mcf_f.nii.gz")
rs_files = glob.glob(search_pattern, recursive=True)

for rs_file in rs_files:
    temp_dir = os.path.dirname(os.path.dirname(rs_file))
    mask_search_pattern = os.path.join(temp_dir, "*AnnoSplit_parental.nii.gz")
    mask_files = glob.glob(mask_search_pattern, recursive=True)
    

    mask_file = mask_files[0]
    
    # Load rs-fMRI data
    rs_img = nib.load(rs_file)
    rs_data = rs_img.get_fdata()
    
    # Load mask data
    mask_img = nib.load(mask_file)
    mask_data = mask_img.get_fdata()
    
    # Convert mask_data to 4D
    mask_data_4d = np.expand_dims(mask_data, axis=3)

    # Initialize a list to store average time series
    average_all = []

      # Initialize a list to store average time series for each region
    average_all_all = []
    
    # Iterate over unique values in mask_data_4d
    unique_regions = np.unique(mask_data_4d)
    for mm in unique_regions:
        # Initialize a list to store average time series for the current region
        average_all = []
        # Mask out the region in rs_data
        masked_data = rs_data * (mask_data_4d == mm)
        for t in range(masked_data.shape[3]):
            masked_data_t = masked_data[:, :, :, t]
            masked_data_nonzero = masked_data_t[masked_data_t != 0]
            average = np.mean(masked_data_nonzero)
            average_all.append(average)
        # Append the average time series for the current region to the list
        average_all_all.append(average_all)
    
    # Convert the list of average time series for each region into a matrix
    average_matrix = np.array(average_all_all)

    # Initialize a list to store average time series for specific regions
    average_all_specific = []

    # Specify regions of interest
    regions_of_interest = [329,1080, 2329, 3080]
    region_names = ["L_MOs","L_HIP","R_MOs","R_HIP"]
    
    
    for sts in regions_of_interest:    
        BigMaskData = rs_data * (mask_data_4d == sts)
        BigMaskDataaverage_all =  []
        for t in range(BigMaskData.shape[3]):
            BigMaskData_t = BigMaskData[:, :, :, t]
            BigMaskData_t_nonzero = BigMaskData_t[BigMaskData_t != 0]
            BigMaskDataaverage = np.mean(BigMaskData_t_nonzero)
            BigMaskDataaverage_all.append(BigMaskDataaverage)
        # Calculate average time series for the masked region
        average_all_specific.append(BigMaskDataaverage_all)
    average_all_specific_matrix = np.array(average_all_specific)
    # Plot the average time series for specific regions and the correlation matrix side by side
    cm = 1/2.53
    plt.figure(figsize=(9.5*cm, 5*cm))

    # Plot average time series subplot
    ax1 = plt.subplot(1, 2, 1)
    for idx, sts in enumerate(regions_of_interest):
        ax1.plot(average_all_specific_matrix[idx], label=f'Region {sts}')
    ax1.set_xlabel('Repetition')
    ax1.set_ylabel('Mean Signal (a.u)')
    ax1.set_title('')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # Calculate Pearson correlation coefficient matrix
    correlation_matrix = np.corrcoef(average_matrix)

    # Plot correlation matrix subplot
    ax2 = plt.subplot(1, 2, 2)
    im = ax2.imshow(correlation_matrix, cmap='viridis', interpolation='nearest')
    plt.colorbar(im, ax=ax2, label='Correlation')
    ax2.set_xlabel('Regions')
    ax2.set_ylabel('Regions')
    ax2.set_title('')
    ax2.axis('on')
    ax2.set_xticks([])
    ax2.set_yticks([])

    # Save the figure
    pp = os.path.basename(rs_file).replace(".nii.gz","")
    pptt = pp.replace("_mcf_f","")
    ppttx = pptt.replace("_EPI","") 
    plt.suptitle(f'{ppttx}')
    plt.tight_layout()
    plt.savefig(os.path.join(out_path, f"{ppttx}.svg"), format='svg', transparent=True, dpi=100)
    
    # Show the figure
    plt.show()
