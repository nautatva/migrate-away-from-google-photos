import os
from pathlib import Path
from pandas import DataFrame, Timestamp
from datetime import datetime
from utils.common_utils import get_leaf_image_folder_paths, get_date_range

album_folder = "G:/3-Photos/Albums"
# albums = [name for name in os.listdir(album_folder) if os.path.isdir(os.path.join(album_folder, name))]
albums = get_leaf_image_folder_paths(album_folder)

def get_calendar(albums: list):
    calendar = {}  # Album: time range
    print("Doing albums", albums)
    for album in albums:
        print(album)
        created_time = set([])
        # modified_time = set([])
        album_path = os.path.join(album_folder, album)

        print("album path", album_path)
        contents = os.listdir(album_path)
        if len(contents) == 0:
            print(album_path, "is empty")
            calendar[album_path] = []
            continue

        for item in contents:
            # Skip directory, they are present in next loop of iteration
            file_path = os.path.join(album_path, item)
            if os.path.isdir(file_path):
                continue

            # Skip snapchat files
            fileP = Path(file_path)
            if "snapchat" in fileP.name.lower():
                continue

            # Skip if extension is not in aae
            ext = fileP.suffix.lower()
            if ext in [".aae"]:
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
print(calendar)
# iterate over all the dates in the calendar map
# Map dates to albums
# If date is present in multiple albums, note down both albums
date_album = {}
for e in calendar:
    dates = calendar[e]
    for date in dates:
        als = []
        if date in date_album:
            als = date_album[date]
            if als is None:
                als = []
        else:
            als = []

        # als is now either [] or the all albums for that date
        if len(als) > 0:
            # Album already present for this date, clash
            print("key already present for", date, als, e)
        als.append(e)
        date_album[date] = als


# Print the date_album map with asc dates
# One date in one line
date_album_sorted = {k: v for k, v in sorted(list(date_album.items()))}
for date in date_album_sorted:
    print(date, date_album_sorted[date])

# print(date_album_sorted)
print()
print()
