# todo: update exif and properties from exif
from datetime import datetime
import os
from pathlib import Path
from utils.common_utils import get_leaf_image_folder_paths
from utils.file_utils import update_file_with_date
from utils.file_utils import get_most_accurate_creation_date_from_file

folder = "G:/3-Photos/Albums/"
# folder = "E:/organize photos/test/"

albums = [get_leaf_image_folder_paths(os.path.join(folder, name)) for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]
# albums = [[os.path.join(folder, "Insti Aditya 40k ka convo 2022")]]


MAX_VIDEO_SIZE = 101 * 1024 * 1024



folders = []
for album in albums:
    folders.extend(album)
folders = set(folders)
print(folders)


def fix_meta_tags(file_path:str):
    """
        Fix inconsistent modified and created dates, taking exif and img name
    """
    if os.path.isdir(file_path):
        # Don't touch folder dates
        return

    item_pathlib = Path(file_path)
    item = item_pathlib.name.lower()

    if "Snapchat" in item:
        return

    if "aae" in item:
        return

    if "duplicate" in file_path:
        return

    # If size of item > max size, skip
    if item_pathlib.stat().st_size > MAX_VIDEO_SIZE:
        print("Video size is very big", file_path, item_pathlib.stat().st_size/1024/1024, "MB")
        return None

    min_date, change_required = get_most_accurate_creation_date_from_file(file_path, quick=True)

    if change_required > 0:
        update_file_with_date(file_path, min_date)


for folder in folders:
    print("Doing folder", folder)
    test = os.listdir(folder)
    for item in test:
        file_path = os.path.join(folder, item)
        if os.path.isdir(file_path):
            # Present in next loop of test
            continue
        # print(file_path)
        fix_meta_tags(file_path)
