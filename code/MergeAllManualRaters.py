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
start_path = r"C:\Users\aswen\Desktop\Code\Validation3"
file_pattern_all_images = os.path.join(start_path, "*", "manual_slice_inspection", "*.png")
manual_slice_inspection_image_files = glob.glob(file_pattern_all_images, recursive=True)

file_pattern_all_raters = os.path.join(start_path, "*", "validation*", "*.png")
validators_image_files = glob.glob(file_pattern_all_raters, recursive=True)

# Step 2: Create DataFrames
column_names = ["Path", "dataset_name", "validator_name"]

manual_slice_inspection_df = pd.DataFrame(
    [
        [file_path, path_elements[-3] if len(path_elements) >= 3 else None, path_elements[-2] if len(path_elements) >= 2 else None]
        for file_path in manual_slice_inspection_image_files
        for path_elements in [file_path.split(os.sep)]
    ],
    columns=column_names,
)

validators_df = pd.DataFrame(
    [
        [file_path, path_elements[-3] if len(path_elements) >= 3 else None, path_elements[-2] if len(path_elements) >= 2 else None]
        for file_path in validators_image_files
        for path_elements in [file_path.split(os.sep)]
    ],
    columns=column_names,
)

# Get unique dataset names and validators
unique_datasets = manual_slice_inspection_df["dataset_name"].unique()


def process_dataset(dataset_name):
    ma_subset = manual_slice_inspection_df[manual_slice_inspection_df["dataset_name"] == dataset_name]
    va_subset = validators_df[validators_df["dataset_name"] == dataset_name]

    results = []

    for index, ma_row in ma_subset.iterrows():
        ma_path = ma_row["Path"]
        ma_image = Image.open(ma_path).convert('RGB')
        ma_image_array = np.array(ma_image)

        result_row = {"Path": ma_path}
        is_same_all = []
        for _, va_row in va_subset.iterrows():
            va_path = va_row["Path"]
            va_image = Image.open(va_path).convert('RGB')
            va_image_array = np.array(va_image)

            diff_image = abs(ma_image_array - va_image_array)
            threshold = 1e-6  # You can adjust this threshold based on your needs
            is_same = np.sum(diff_image) < threshold
            is_same_all.append(is_same)

            result_row[va_row["validator_name"]] = is_same
            result_row["dataset_name"] = dataset_name
            result_row["SequenceType"] = ma_path.split(os.sep)[-1].split("_")[0]

        validator_names = va_subset[is_same_all].validator_name
        for v in validator_names:
            result_row[v] = True
        results.append(result_row)
        #print(C)
    
    print("finished: " + dataset_name)
    return results

# Get the number of available CPUs
num_cpus = os.cpu_count()

# Create a ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor(max_workers=num_cpus) as executor:
    # Process datasets in parallel
    all_results = list(executor.map(process_dataset, unique_datasets))

# Concatenate the results into the final DataFrame
result_df = pd.concat([pd.DataFrame(results) for results in all_results], ignore_index=True)

# Fill NaN values with False
result_df = result_df.fillna(False)

# Optionally, you can save the combined DataFrame to a CSV file
output_path = r"C:\Users\aswen\Desktop\Code\AIDAqc_Figures\input"
result_df.to_csv(os.path.join(output_path, "combined_Human_Voters_from_votings3_Final.csv"), index=False)
