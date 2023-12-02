import os
from pathlib import Path
from pandas import DataFrame, Timestamp
from datetime import datetime
from utils.common_utils import get_leaf_image_folder_paths, get_date_range
from utils.file_utils import get_most_accurate_creation_date_from_file

album_folder = "G:/3-Photos/Albums"
# albums = [name for name in os.listdir(album_folder) if os.path.isdir(os.path.join(album_folder, name))]
albums = get_leaf_image_folder_paths(album_folder)



def check_continuous_dates(dates_set):
    media_dates_set = set(dates_set)
    sorted_dates = sorted(media_dates_set)
    
    # Iterate through the sorted dates and check for continuity
    for i in range(len(sorted_dates) - 1):
        current_date = sorted_dates[i]
        next_date = sorted_dates[i + 1]
        
        # Check if the next date is not consecutive to the current date
        if (next_date - current_date).days != 1:
            return False  # Dates are not continuous
    
    return True  # Dates are continuous

def get_calendar(albums: list):
    calendar = {}  # Album: time range
    print("Doing albums", albums)
    skipped_date_albums = {}
    long_albums = {}
    for album in albums:
        print(album)
        media_dates = []
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

            m_date, change_required = get_most_accurate_creation_date_from_file(file_path)
            media_dates.append(m_date)
            # media_dates.append(pathlib.Path(file_path).stat().st_ctime)

        if len(media_dates) == 0:
            continue

        # Get set of dates
        # Check if dates are continuous
        if not check_continuous_dates(media_dates):
            print("Dates are not continuous for album", album)
            skipped_date_albums[album] = sorted(set(media_dates))
            continue
        

        df = DataFrame({'DATE': [Timestamp(x) for x in media_dates]})
        # print(df)

        qa = df['DATE'].quantile(0.05)  # lower 10%
        qb = df['DATE'].quantile(0.95)  # higher 10%

        print("Dates are ", qa, qb)

        dates = get_date_range(qa, qb)
        print("Done album", album, "with dates starting", qa, "and ending", qb)
        print()
        if len(dates) > 15:
            print(album, "len greater than 15")
            print(df)
            long_albums[album] = sorted(set(media_dates))
            continue
        
        print(album, "Added to calendar")
        calendar[album] = dates
        # print (s)
        # s.plot()
    return calendar, skipped_date_albums, long_albums


calendar, skipped_date_albums, long_albums = get_calendar(albums)
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
print("############################# CALENDAR ITERNARY PRINTED BELOW #############################")
date_album_sorted = {k: v for k, v in sorted(list(date_album.items()))}
for date in date_album_sorted:
    print(date, date_album_sorted[date])

print("############################# ALBUMS WHICH TOO LONG TO BE INCLUDED IN THE CALENDAR #############################")
print(long_albums)

print("############################# ALBUMS WHICH HAVE DATES SKIPPED IN BETWEEN #############################")
print(skipped_date_albums)
