import os
import shutil

# This script moves .pdf, .docx, and .doc files from subdirectories into a single directory.

# Set the source directory and target directory paths
RootDir1 = "/path_to_folders_with_files"
TargetFolder = "/path_to_target_folder"

# Create a dictionary to keep track of file names and their count
file_dict = {}

# Loop through all files in the source directory and its subdirectories
for root, dirs, files in os.walk(os.path.normpath(RootDir1), topdown=False):
    for name in files:
        # Check if the file has a pdf, docx or doc extension
        if name.endswith('.pdf') or name.endswith('.docx') or name.endswith('.doc'):
            print("Found")
            # Get the source file path
            source_path = os.path.join(root, name)
            # Split the filename and extension
            filename, ext = os.path.splitext(name)
            
            # Check if the file name already exists in the dictionary
            if name in file_dict:
                # If it does, increment the count and add it to the new file name
                count = file_dict[name]
                new_name = f"{filename}_{count}{ext}"
                file_dict[name] += 1
            else:
                # If it doesn't, use the original file name
                new_name = name
                # Initialize the count to 1 in the dictionary
                file_dict[name] = 1
            
            # Get the target file path
            target_path = os.path.join(TargetFolder, new_name)
            # Copy the file to the target directory
            shutil.copy2(source_path, target_path)

# Credit goes to [jblasco's post on Stack Exchange](https://stackoverflow.com/questions/18383384/python-copy-files-to-a-new-directory-and-rename-if-file-name-already-exists) and ChatGPT's adaptation and comments
