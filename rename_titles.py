import os
import glob
import xml.etree.ElementTree as ET

# This script takes the MMS ID, locating the record in the .xml file and renames the file title to `dc:title- dc:creator.[extension]`

# Get list of files to process. folder_path is the target directory from `rename_move.py`
folder_path = "path/to/target/directory"
extensions = [".pdf", ".doc", ".docx"]
files = [f for ext in extensions for f in glob.glob(os.path.join(folder_path, "*" + ext))]

# Parse XML file making sure the `.xml` file is renamed to reflect below.
xml_file = os.path.join(folder_path, "matching_fields.xml")
tree = ET.parse(xml_file)
root = tree.getroot()

# Loop over each file
for file_path in files:
    # Get identifier from file name
    identifier = os.path.splitext(os.path.basename(file_path))[0]

    # Find record in XML file with matching identifier
    record = root.find(".//{{http://www.openarchives.org/OAI/2.0/oai_dc/}}dc[{{http://purl.org/dc/elements/1.1/}}identifier='{}']".format(identifier))

    if record is not None:
        # Get title from record and replace : with -
        title = record.find("{http://purl.org/dc/elements/1.1/}title").text.replace(":", "-")

        # Remove / from title
        title = title.replace("/", "")

        # Get creator from record and add it to the title
        creator = record.find("{http://purl.org/dc/elements/1.1/}creator").text
        title = f"{title} - {creator}"

        # Get file extension
        extension = os.path.splitext(file_path)[1]

        # Create new file name with title and extension
        new_file_name = title + extension

        # Rename file
        new_file_path = os.path.join(folder_path, new_file_name)
        os.rename(file_path, new_file_path)

        print(f"Renamed file {file_path} to {new_file_path}")
    else:
        print(f"Could not find record with identifier {identifier} in {xml_file}")
