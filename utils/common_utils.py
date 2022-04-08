import os
from datetime import date, timedelta


def get_leaf_image_folder_paths(file_path:str) -> set:
    all_paths = []
    if os.path.isdir(file_path):
        all_paths.append(file_path)
        test = os.listdir(file_path)
        for item in test:
            all_paths.extend(get_leaf_image_folder_paths(os.path.join(file_path, item)))

    return set(all_paths)


def getDateRange(start_date:date, end_date:date):
    number_of_days = (end_date - start_date).days
    if (number_of_days == 0):
        return [start_date.date()]

    date_list = []
    for day in range(number_of_days):
        a_date = (start_date + timedelta(days=day))
        # .astimezone(timezone.utc)
        # a_date = a_date.strftime('$d-%m-%Y')
        date_list.append(a_date.date())
    return date_list
