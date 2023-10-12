
import os
import sys
import re
from utils.common_utils import get_leaf_image_folder_paths

# Set the source and destination directories
# source_dir = 'E:/Ext disk/3-Photos'
source_dir = 'G:/3-Photos'

DRY_RUN = True
folders = get_leaf_image_folder_paths(source_dir)

# # Get the list of files in the source directory
# source_files = os.listdir(source_dir)

# # Get the list of files in the destination directory
# dest_files = os.listdir(dest_dir)

# Loop through the source files
for folder in folders:
    print("Doing folder", folder)
    # folder_name = os.path.basename(folder)
    rel_path = os.path.relpath(folder, source_dir)
    items = os.listdir(folder)
    for item in items:
        source_path = os.path.join(folder, item)
        try:
            print(source_path, source_path.encode('utf-8'))
        except UnicodeEncodeError:    
            print("folder", folder)
            printable_str = re.sub(r'\W+', '', item)
            print("No unicode present for", item.encode('utf-8'))
