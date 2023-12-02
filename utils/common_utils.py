import os
from datetime import date, timedelta
import json


def get_leaf_image_folder_paths(file_path:str) -> set:
    # Lists all leaf folders that contain images
    # Recursively searches for folders
    all_paths = []
    if os.path.isdir(file_path):
        all_paths.append(file_path)
        test = os.listdir(file_path)
        for item in test:
            all_paths.extend(get_leaf_image_folder_paths(os.path.join(file_path, item)))

    return set(all_paths)


def get_date_range(start_date:date, end_date:date):
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


def safe_serialize(obj, *args, **kwargs):
    return json.dumps(obj, default=lambda o: f"<<non-serializable: {type(o).__qualname__}>>", *args, **kwargs)


def merge_iterables(iter1, iter2):
    # TODO: make a function with *args instead of fixed args
    final_list = []
    if iter1 is None:
        return iter2
    if iter2 is None:
        return iter1
    for e in iter1:
        final_list.append(e)
    for e in iter2:
        final_list.append(e)

    return final_list


def is_json_key_present(json:dict, key) -> bool:
    # TODO: Add in common_utils PyPi
    try:
        json[key]
    except KeyError:
        return False

    return True
