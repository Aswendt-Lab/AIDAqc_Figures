# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 11:34:11 2023

@author: arefks
"""

import os
import glob
import pandas as pd

# Step 1: Define the starting path and file pattern
start_path =  r"C:\Users\aswen\Desktop\Code\Validation3"
file_pattern = '*votin*.csv'

# Step 2: Find all matching CSV files in the specified directory and its subdirectories
csv_files = glob.glob(os.path.join(start_path, '*', file_pattern), recursive=True)

# Step 3: Initialize an empty DataFrame to store the extracted data
combined_df = pd.DataFrame()
combined_df1 = pd.DataFrame()


# Step 4: Loop through the CSV files and extract the specified columns
for csv_file in csv_files:
    try:
        df = pd.read_csv(csv_file)
        selected_columns = ["Pathes",	"corresponding_img"
                            ,	"One_class_SVM",
                            "IsolationForest",	"LocalOutlierFactor",
                            " EllipticEnvelope",	"statistical_method",
                            "Voting outliers (from 5)"]
        df = df[selected_columns]
        df["dataset"] = csv_file.split(os.sep)[-2]
        df["corresponding_img_Path"] = os.path.join(os.path.dirname(csv_file),"manual_slice_inspection")
        # Concatenate the current DataFrame with the combined DataFrame
        combined_df1 = pd.concat([combined_df1, df], ignore_index=True)
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")



combined_df = combined_df1
combined_df["SequenceType"] = combined_df["corresponding_img"].str.split("_").str[0]
# Step 5: Print the combined DataFrame
print(combined_df)

# Optionally, you can save the combined DataFrame to a CSV file
p = r"C:\Users\aswen\Desktop\Code\AIDAqc_Figures\input"
combined_df.to_csv(os.path.join(p,'combined_votings3.csv'), index=False)