# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 11:34:11 2023

@author: arefks
"""

import os
import glob
import pandas as pd
from PIL import Image
import numpy as np
# Step 1: Define the starting path and file pattern
start_path =  r"C:\Users\aswen\Desktop\Code\Validation3"
file_pattern_all_images = os.path.join(start_path,"*","manual_slice_inspection",'*.png')
manual_slice_inspection_image_files = glob.glob(file_pattern_all_images, recursive=True)


file_pattern_all_raters = os.path.join(start_path,"*","validation*",'*.png')
validators_image_files = glob.glob(file_pattern_all_raters, recursive=True)
# Step 2: Create DataFrames
def create_dataframe(file_list, column_names):
    data = []
    for file_path in file_list:
        path_elements = file_path.split(os.sep)
        dataset_name = path_elements[-3] if len(path_elements) >= 3 else None
        validator_name = path_elements[-2] if len(path_elements) >= 2 else None
        data.append([file_path, dataset_name, validator_name])
    return pd.DataFrame(data, columns=column_names)

# Create DataFrames
column_names = ['Path', 'dataset_name', 'validator_name']

manual_slice_inspection_df = create_dataframe(manual_slice_inspection_image_files, column_names)
validators_df = create_dataframe(validators_image_files, column_names)


# Iterate over unique datasets
for dataset_name in unique_datasets:
    # Filter DataFrames based on the current dataset
    ma_subset = manual_slice_inspection_df[manual_slice_inspection_df['dataset_name'] == dataset_name]
    va_subset = validators_df[validators_df['dataset_name'] == dataset_name]
    
    # Iterate over manual_slice_inspection images
    for index, ma_row in ma_subset.iterrows():
        ma_path = ma_row['Path']
        ma_image = Image.open(ma_path)
        ma_image_array = np.array(ma_image)
        
        # Initialize result row
        result_row = {'Path': ma_path}
        
        # Iterate over validators
        for _, va_row in va_subset.iterrows():
            va_path = va_row['Path']
            va_image = Image.open(va_path)
            va_image_array = np.array(va_image)
            
            # Calculate the difference
            diff_image = ma_image_array - va_image_array
            
            # Check if the difference is zero
            is_same = np.sum(diff_image) == 0
            
            # Update the result row
            result_row[va_row['validator_name']] = is_same
            
        # Append the result row to the result DataFrame
        result_df = result_df.append(result_row, ignore_index=True)


















file_pattern_voting_images = 
# Step 2: Find all matching CSV files in the specified directory and its subdirectories
image_files = glob.glob(os.path.join(start_path, '*', file_pattern), recursive=True)

# Step 3: Initialize an empty DataFrame to store the extracted data
combined_df = pd.DataFrame()
combined_df1 = pd.DataFrame()


# Step 4: Loop through the CSV files and extract the specified columns
for image_file in image_files:
    try:
        df = pd.read_csv(image_file)
        selected_columns = ["Pathes",	"sequence_name",	"corresponding_img",
                            "sequence_name",	"One_class_SVM",
                            "IsolationForest",	"LocalOutlierFactor",
                            " EllipticEnvelope",	"statistical_method",
                            "Voting outliers (from 5)"]
        df = df[selected_columns]
        df["dataset"] = csv_file.split(os.sep)[-2]
        # Concatenate the current DataFrame with the combined DataFrame
        combined_df1 = pd.concat([combined_df1, df], ignore_index=True)
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")



combined_df = combined_df1
# Step 5: Print the combined DataFrame
print(combined_df)

# Optionally, you can save the combined DataFrame to a CSV file
p = r"C:\Users\aswen\Desktop\Code\AIDAqc_Figures\input"
combined_df.to_csv(os.path.join(p,'combined_votings3.csv'), index=False)