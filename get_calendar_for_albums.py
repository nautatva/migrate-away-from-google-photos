import os
from pathlib import Path
from pandas import DataFrame, Timestamp
from datetime import datetime
from utils.common_utils import get_leaf_image_folder_paths, get_date_range

album_folder = "G:/3-Photos/Albums"
albums = [name for name in os.listdir(album_folder) if os.path.isdir(os.path.join(album_folder, name))]
# albums = get_leaf_image_folder_paths(album_folder)

def get_calendar(albums: list):
    calendar = {}  # Album: time range
    print("Doing albums", albums)
    for album in albums:
        print(album)
        created_time = set([])
        # modified_time = set([])
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
                created_time.add(m_date)
                # created_time.append(pathlib.Path(file_path).stat().st_ctime)

        if len(created_time) == 0:
            continue

        df = DataFrame({'DATE': [Timestamp(x) for x in created_time]})
        # print(df)

        qa = df['DATE'].quantile(0.15)  # lower 10%
        qb = df['DATE'].quantile(0.85)  # higher 10%

        print("Dates are ", qa, qb)

        dates = get_date_range(qa, qb)
        print("Done album", album, "with dates starting", qa, "and ending", qb)
        print()
        if len(dates) > 15:
            print(album, "len greater than 15")
            print(df)
            continue
        
        print(album, "Added to calendar")
        calendar[album] = dates
        # print (s)
        # s.plot()
    return calendar

calendar = get_calendar(albums)
# print(calendar)
# Print calendar in ascending order of dates
for album in sorted(calendar, key=lambda k: calendar.get(k, [0])[0]):
    print(album, calendar[album])
print()
print()
