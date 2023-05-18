import os
import xml.etree.ElementTree as ET
import shutil

# This script renames the files to their Alma unique ID (MMS ID).

# Path to the directory containing the grandparent folders
grandparent_dir = "/path/to/grandparent/directory"

# Path to the metadata XML file
matching_fields_file = "path/to/metadata/matching_fields.xml"

# Set the target directory path
target_dir = "path/to/target/directory"

# Create a dictionary to keep track of file names and their count
file_dict = {}

# Parse the XML file
tree = ET.parse(matching_fields_file)
root = tree.getroot()

# Loop through each grandparent folder
for grandparent_entry in os.scandir(grandparent_dir):
    if grandparent_entry.is_dir():
        grandparent_folder_name = grandparent_entry.name
        
        # Loop through each parent folder
        for child_entry in os.scandir(grandparent_entry.path):
            if child_entry.is_dir():
                parent_folder_name = child_entry.name
                
                # Loop through each file in the parent folder with an allowed file extension
                for file_entry in os.scandir(child_entry.path):
                    if file_entry.is_file() and file_entry.name.split(".")[-1] in ["pdf", "docx", "doc"]:
                        if not file_entry.name.endswith(".txt") and not file_entry.name.endswith(".jpg"):
                            # Find the dc:title in the XML file
                            title = grandparent_folder_name
                            for matching_field in root.findall(".//matching_field[@id='" + grandparent_folder_name + "']"):
                                identifier_element = matching_field.find(".//dc:identifier", namespaces={"dc": "http://purl.org/dc/elements/1.1/"})
                                if identifier_element is not None and identifier_element.text == grandparent_folder_name:
                                    title_element = matching_field.find(".//dc:title", namespaces={"dc": "http://purl.org/dc/elements/1.1/"})
                                    if title_element is not None:
                                        title = title_element.text
                                        break
                            
                            # Rename the file
                            file_extension = os.path.splitext(file_entry.name)[1]
                            new_file_name = title + file_extension
                            if new_file_name in file_dict:
                                # If the file name already exists in the dictionary, increment the count and add it to the new file name
                                count = file_dict[new_file_name]
                                new_file_name = f"{title}_{count}{file_extension}"
                                file_dict[new_file_name] += 1
                            else:
                                # If it doesn't, use the original file name
                                file_dict[new_file_name] = 1
                            new_file_path = os.path.join(target_dir, new_file_name)
                            
                            # Copy the file to the target directory
                            shutil.copy2(file_entry.path, new_file_path)
