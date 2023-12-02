import os
from pathlib import Path
from datetime import datetime
from utils.common_utils import get_leaf_image_folder_paths, is_json_key_present
from get_calendar_for_albums import get_calendar
# import shutil


album_folder = "G:/3-Photos/Albums"
albums = get_leaf_image_folder_paths(album_folder)
# albums = [name for name in os.listdir(album_folder) if os.path.isdir(os.path.join(album_folder, name))]
# albums = ["Palghar"]
rogue_folder = "D:/3-Photos/photos year sorted"

rogue_albums = [get_leaf_image_folder_paths(os.path.join(rogue_folder, name)) for name in os.listdir(rogue_folder) if os.path.isdir(os.path.join(rogue_folder, name))]
# rogue_albums = [[os.path.join(folder, "Shimla Manali with Fam")]]

SAME_DIRECTORY_STRUCUTRE = True


calendar = get_calendar(albums)

# Map dates to albums
date_desc = {}
for e in calendar:
    dates = calendar[e]
    for d in dates:
        if is_json_key_present(date_desc, d):
            # Album already present for this date, clash
            print("key already present for", d, date_desc[d], e)
        date_desc[d] = e

date_desc = {k: v for k, v in sorted(list(date_desc.items()))}
print()
print()


# ################## - ####################
# Now classify rogue images in albums
def classify(file_path:str, date_desc:dict) -> list:
    fileP = Path(file_path)
    m_date = datetime.fromtimestamp(fileP.stat().st_mtime).date()
    if is_json_key_present(date_desc, m_date):
        return date_desc[m_date]
    return None


rogue_folders = []
for album in rogue_albums:
    rogue_folders.extend(album)
rogue_folders = set(rogue_folders)
print(rogue_folders)


for folder in rogue_folders:
    print("Doing rogue folder", folder)
    test = os.listdir(folder)
    for item in test:
        file_path = os.path.join(folder, item)
        if os.path.isdir(file_path):
            # Present in next loop of test
            continue
        # print(file_path)
        album = classify(file_path, date_desc)
        if album is not None:
            print(file_path, "fits in", album)
            if SAME_DIRECTORY_STRUCUTRE:
                fit_folder = os.path.join(rogue_folder, "best_fit", album)
            else:
                fit_folder = os.path.join(album_folder, album, "best_fit3")

            if not os.path.exists(fit_folder):
                os.makedirs(fit_folder)
            new_photo_path = os.path.join(fit_folder, item)
            if os.path.exists(new_photo_path):
                print(new_photo_path, "already exists")
            else:
                os.rename(file_path, new_photo_path)
            # todo: Also move all relevant NAME (xx).AAE files
