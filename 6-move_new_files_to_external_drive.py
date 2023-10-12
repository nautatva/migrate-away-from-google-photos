# Compare the files in the source and destination directories
# and move any new files to the destination directory.
# This script is intended to be run as a cron job.
# The script will only move files that are not already in the destination directory.

import os
import shutil
from utils.common_utils import get_leaf_image_folder_paths


# Set the source and destination directories
directory_name = '3a-Fav photos'
source_dir = 'E:/Ext disk/' + directory_name
dest_dir = 'G:/' + directory_name

DRY_RUN = False
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
        if os.path.isdir(source_path):
            # Present in next loop of test
            continue
        dest_path = os.path.join(dest_dir, rel_path, item)

        # Check if the file is in the destination directory
        if not os.path.exists(dest_path):
            # If the file is not in the destination directory, copy it
            print("Moving", source_path)
            if not DRY_RUN:
                # If folder is not present, create it
                os.makedirs(os.path.join(dest_dir, rel_path), exist_ok=True)
                shutil.move(source_path, dest_path)
        else:
            # If the file is in the destination directory, Check if the date modified is the same
            source_time = os.path.getmtime(source_path)
            dest_time = os.path.getmtime(dest_path)
            if source_time == dest_time:
                # If the date modified is the same, delete the file in the source directory
                print("Deleting", source_path)
                if not DRY_RUN:
                    os.remove(source_path)
            elif source_time > dest_time:
                # If the date modified for source file is after the destination, move the file to the destination directory
                print("Moving the newer version", source_path, dest_path)
                # if not DRY_RUN:
                    # shutil.move(source_path, dest_path)
            else:
                print("Not moving, destination has the newer version", dest_path)
