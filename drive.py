import re
# This script simply strips the file id from the URL and places it in the lh3 space.
def convert_drive_link(url):
    match = re.search(r"(?<=\/d\/|id=)([\w-]+)", url)
    if match:
        file_id = match.group(1)
        return f"https://lh3.googleusercontent.com/d/{file_id}"
    else:
        return url

# Example usage
url = "https://drive.google.com/file/d/[fileID]/view?usp=share_link"
lh_url = convert_drive_link(url)
print(lh_url)
