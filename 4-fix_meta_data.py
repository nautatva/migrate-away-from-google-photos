# todo: update exif and properties from exif
from datetime import datetime
import os
from pathlib import Path
from parsers.file_name_parser import parse_date_from_file_name
from parsers.exif_parser import extract_exif_date_taken
from utils.common_utils import get_leaf_image_folder_paths
from utils.file_utils import update_file_with_date

folder = "G:/3-Photos/Albums/"

albums = [get_leaf_image_folder_paths(os.path.join(folder, name)) for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]
# albums = [[os.path.join(folder, "Insti Aditya 40k ka convo 2022")]]

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

    # Check modified/created/exif dates and get the earliest
    dates = []
    modified = datetime.fromtimestamp(item_pathlib.stat().st_mtime)
    dates.append(modified)

    created = datetime.fromtimestamp(item_pathlib.stat().st_ctime)
    dates.append(created)

    exif_date = extract_exif_date_taken(file_path)
    if exif_date is not None:
        dates.append(exif_date)

    item = item_pathlib.name
    file_date = None
    if "Snapchat" not in item:
        # Not a snapchat file (false positive dates)
        file_date = parse_date_from_file_name(file_path)
        if file_date is not None:
            dates.append(file_date)

    min_date = min(dates)
    max_date = max(dates)
    number_of_days = (max_date - min_date).days
    if number_of_days == 0:
        # No need to set anything
        return
    elif number_of_days > 0:
        print("Dates are inconsistent", file_path, min_date, max_date, "All dates", dates)
        required_date = min_date
        if file_date is not None:
            # Actually found the date, best scenario
            print("Found date in file name itself", file_path, file_date)
            required_date = file_date
        else:
            # Modified date is ahead of created date
            print("Old dates", file_path, created, modified, exif_date)

        update_file_with_date(file_path, required_date)


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
