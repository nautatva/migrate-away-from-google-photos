# cleans up duplicate heic and jpg files
# and moves them to a folder called "duplicates"


import os
from utils.common_utils import get_leaf_image_folder_paths, get_date_range, is_json_key_present


ios_folder = "E:/Ext disk/1-Phone/iPhone/DCIM"
folders = get_leaf_image_folder_paths(ios_folder)


# Find if there are any other files with the same name as a HEIC file
# If so, move the other file to a folder called "duplicates"
# This is because the HEIC file is the original and the other is a duplicate
# The other file is a duplicate because the HEIC file is a better quality image than JPEG or MOV or PNG

for folder in folders:    
    heic_available = []
    heic_not_found_yet = []
    heic_not_found_yet_ext = {}  # To store the extension of files that don't have a heic file yet

    print("Doing folder", folder)
    folder_name = os.path.basename(folder)
    if folder_name == "duplicates":
        print("Skipping duplicates folder, has " + str(len(os.listdir(folder))) + " files") 
        # Don't search in duplicates, they have already been moved here
        continue

    items = os.listdir(folder)
    for item in items:
        file_path = os.path.join(folder, item)
        if os.path.isdir(file_path):
            # Present in next loop of test
            continue
        name = os.path.splitext(item)[0]
        ext = os.path.splitext(item)[-1].lower()
        print(file_path, ext)

        # Check if this is a HEIC file
        # If there is an other file with the same name, move the other file to a folder called "duplicates"
        if ext == ".heic":
            if name in heic_not_found_yet:
                # Found a HEIC file with the same name as an other file
                heic_not_found_yet.remove(name)
                old_ext = heic_not_found_yet_ext[name]
                print("Found HEIC file for", name+old_ext)
                # Move the other file to a folder called "duplicates"
                old_file_path = os.path.join(folder, name+old_ext)
                new_file_path = os.path.join(folder, "duplicates", name+old_ext)
                os.makedirs(os.path.join(folder, "duplicates"), exist_ok=True)
                
                # Check if old_file_path is present
                if os.path.exists(old_file_path):
                    os.rename(old_file_path, new_file_path)
                else:
                    print("Old file not found", old_file_path)
            else:
                heic_available.append(name)
        elif ext == ".aae":
            # Ignore this file
            # Used to store edits in HEIC
            # print("Ignoring", file_path)
            continue
        else:
            if name in heic_available:
                # Found an other file with the same name as a HEIC file
                print("Found other file for", name+".heic")
                # Move the other file to a folder called "duplicates"
                new_file_path = os.path.join(folder, "duplicates", item)
                os.makedirs(os.path.join(folder, "duplicates"), exist_ok=True)
                
                # Check if old_file_path is present
                if os.path.exists(file_path):
                    os.rename(file_path, new_file_path)
                else:
                    print("File not found", file_path)
            else:
                heic_not_found_yet_ext[name] = ext
                heic_not_found_yet.append(name)
