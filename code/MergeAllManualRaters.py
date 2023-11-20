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
import concurrent.futures
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

# Assuming you already have manual_slice_inspection_df and validators_df DataFrames

# Get unique dataset names and validators
unique_datasets = manual_slice_inspection_df['dataset_name'].unique()
unique_validators =  validators_df['validator_name'].unique()

# Create a result DataFrame
result_column_names = ['Path'] + list(unique_validators)
result_df = pd.DataFrame(columns=result_column_names)

# Function to process a dataset
def process_dataset(dataset_name):
    ma_subset = manual_slice_inspection_df[manual_slice_inspection_df['dataset_name'] == dataset_name]
    va_subset = validators_df[validators_df['dataset_name'] == dataset_name]
    
    results = []
    
    for index, ma_row in ma_subset.iterrows():
        ma_path = ma_row['Path']
        ma_image = Image.open(ma_path)
        ma_image_array = np.array(ma_image)
        
        result_row = {'Path': ma_path}
        
        for _, va_row in va_subset.iterrows():
            va_path = va_row['Path']
            va_image = Image.open(va_path)
            va_image_array = np.array(va_image)
            
            diff_image = ma_image_array - va_image_array
            is_same = np.sum(diff_image) == 0
            
            result_row[va_row['validator_name']] = is_same
        
        results.append(result_row)
    
    return results


# Get the max number of CPUs
max_cpus = min(os.cpu_count(), len(unique_datasets))

# Create a ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor(max_cpus) as executor:
    # Process datasets in parallel
    results_list = list(executor.map(process_dataset, unique_datasets))

# Concatenate the results into the final DataFrame
result_df = pd.concat([pd.DataFrame(result_list) for result_list in results_list], ignore_index=True)

# Optionally, you can save the combined DataFrame to a CSV file
p = r"C:\Users\aswen\Desktop\Code\AIDAqc_Figures\input"
result_df.to_csv(os.path.join(p,'results_df_to_check.csv'), index=False)
# Display the result DataFrame
print(result_df.head())





