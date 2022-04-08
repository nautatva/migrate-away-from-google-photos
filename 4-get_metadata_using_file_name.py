import filedate
import os
import pathlib
from datetime import datetime
from parsers.main import parse_date_from_file_name
from utils.common_utils import get_leaf_image_folder_paths


folder = "D:/3-Photos/Albums"
albums = [get_leaf_image_folder_paths(os.path.join(folder, name)) for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]
# albums = [[os.path.join(folder, "Bhua_s 25th anniversary!!")]]
folders = []
for album in albums:
    folders.extend(album)


def updateFileWithDate(file_path:str, date:datetime):
    if date is None:
        return

    modified = datetime.fromtimestamp(pathlib.Path(file_path).stat().st_mtime)
    # modified_date = modified.date()

    number_of_days = (modified - date).days
    if number_of_days == 0:
        pass
    elif number_of_days > 0:
        # Date is earlier
        print("All ok", file_path, date, modified)
        filedate.File(file_path).set(
            created=date,
            modified=date
        )
    else:
        if (((modified - date).total_seconds()) / 60 > 1):
            print("Check", file_path, date, modified)


def updateFileWithOlderDates(file_path:str):
    """
        Fix inconsistent modified and created dates
    """
    if os.path.isdir(file_path):
        # Don't touch folder dates
        return

    modified = datetime.fromtimestamp(pathlib.Path(file_path).stat().st_mtime)
    modified_date = modified.date()
    created = datetime.fromtimestamp(pathlib.Path(file_path).stat().st_ctime)
    created_date = created.date()

    number_of_days = (modified_date - created_date).days
    if number_of_days == 0:
        # No need to set anything
        return
    elif number_of_days > 0:
        # Modified date is ahead of created date
        # Change modified date
        print("1", file_path, modified, created)
        updateFileWithDate(file_path, created)
    else:
        # Created date ahead of modified date
        # Change created date
        print("2", file_path, modified, created)
        updateFileWithDate(file_path, modified)


for folder in folders:
    print(folder)
    test = os.listdir(folder)
    for item in test:
        file_path = os.path.join(folder, item)
        if os.path.isdir(file_path):
            # Present in next loop of test
            continue
        # print(file_path)
        if "Snapchat" in item:
            continue
        file_date = parse_date_from_file_name(file_path)
        if file_date is None:
            # print("implement regex for file " + file_path)
            pass
        else:
            print(item, file_date)
            updateFileWithDate(file_path, file_date)
