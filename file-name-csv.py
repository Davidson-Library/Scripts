import os
import csv

# This script recursively goes through a folder/subfolder path and finds all the files, then writes them to a CSV file.
def get_files_recursive(folder_path):
    file_names = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_names.append(os.path.join(root, file))
    return file_names

def write_to_csv(file_names):
    with open('file_names.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Name'])
        for name in file_names:
            writer.writerow([name])

# Provide the path to the root folder
root_folder_path = '/folder_path'

# Get all files recursively
file_names = get_files_recursive(root_folder_path)

# Write to CSV
write_to_csv(file_names)