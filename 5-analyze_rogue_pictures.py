import os
from pathlib import Path
import pandas as pd
from datetime import datetime
from utils.common_utils import get_leaf_image_folder_paths, get_date_range, is_json_key_present
# import shutil


album_folder = "D:/3-Photos/Albums"
albums = [name for name in os.listdir(album_folder) if os.path.isdir(os.path.join(album_folder, name))]
# albums = ["Palghar"]
rogue_folder = "D:/3-Photos/photos year sorted"

rogue_albums = [get_leaf_image_folder_paths(os.path.join(rogue_folder, name)) for name in os.listdir(rogue_folder) if os.path.isdir(os.path.join(rogue_folder, name))]
# rogue_albums = [[os.path.join(folder, "Shimla Manali with Fam")]]

calendar = {}  # Album: time range

for album in albums:
    print(album)
    created_time = []
    modified_time = []
    directory = os.path.join(album_folder, album)
    directories = get_leaf_image_folder_paths(directory)
    print("directories", directories)
    for sub_folder in directories:
        print("sub folder", sub_folder)
        test = os.listdir(sub_folder)
        if len(test) == 0:
            print(sub_folder, "is empty")
            calendar[sub_folder] = []
            continue

        for item in test:
            file_path = os.path.join(sub_folder, item)
            if os.path.isdir(file_path):
                # Present in next loop of test
                continue
            # print(file_path)
            fileP = Path(file_path)
            if "snapchat" in fileP.name.lower():
                continue
            m_date = datetime.fromtimestamp(fileP.stat().st_mtime).date()
            modified_time.append(m_date)
            # created_time.append(pathlib.Path(file_path).stat().st_ctime)

    if len(modified_time) == 0:
        continue

    df = pd.DataFrame({'DATE': [pd.Timestamp(x) for x in modified_time]})
    # print(df)

    qa = df['DATE'].quantile(0.15)  # lower 10%
    qb = df['DATE'].quantile(0.85)  # higher 10%

    print(qa, qb)

    dates = get_date_range(qa, qb)
    if len(dates) > 15:
        print(album, "len greater than 15")
        # calendar[album] = [qa, qb]
        print(df)
        continue
    calendar[album] = dates
    # print (s)
    # s.plot()

print(calendar)
print()
print()

date_desc = {}
for e in calendar:
    dates = calendar[e]
    for d in dates:
        if is_json_key_present(date_desc, d):
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
            fit_folder = os.path.join(album_folder, album, "best_fit2")
            if not os.path.exists(fit_folder):
                os.makedirs(fit_folder)
            new_photo_path = os.path.join(fit_folder, item)
            if os.path.exists(new_photo_path):
                print(new_photo_path, "already exists")
            else:
                os.rename(file_path, new_photo_path)
