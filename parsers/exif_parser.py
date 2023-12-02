from PIL import Image, ExifTags
from datetime import datetime
from utils.common_utils import is_json_key_present
from utils.image_utils import is_image
from utils.common_utils import safe_serialize
from pillow_heif import register_heif_opener
import subprocess
import os

register_heif_opener()

CUSTOM_EXIF_DATA_EXTENSION = [".mp4", ".mov"]

def extract_exif_date_taken(filename:str) -> datetime:
    if not is_image(filename):
        # Cannot update exif if not image
        file_name, file_extension = os.path.splitext(filename)
        if file_extension.lower() in CUSTOM_EXIF_DATA_EXTENSION:
            map = extract_exif_data(filename)
            return custom_min_date_extractor(map)
        else:
            print("Exif parsing not supported", filename)
            return None

    try:
        image = Image.open(filename)
        image_exif = image.getexif()
    except Exception  as e:
        print("Exception in file", filename, e)
        return None
    if image_exif:
        # Make a map with tag names
        exif = {ExifTags.TAGS[k]: v for k, v in image_exif.items() if k in ExifTags.TAGS and type(v) is not bytes}

        # json = safe_serialize(exif, indent=4)  # Spares the non-serializable data like GPSInfo (byte in dict)
        # print("All exif", json)
        date_str = get_key_from_exif_dict(exif, "DateTime")
        if date_str is None:
            date_str = get_key_from_exif_dict(exif, "DateTimeOriginal")
        return date_str
    else:
        print('Unable to get date from exif for %s' % filename)
    return None

def get_key_from_exif_dict(exif:dict, key:str):
    if is_json_key_present(exif, key):
        date_str = exif[key]
        return getDateTimeFromString(date_str)
    return None

def getDateTimeFromString(date_str:str):
    try:
        str1, str2 = date_str.split("+")
        return datetime.strptime(str1, '%Y:%m:%d %H:%M:%S')
    except Exception:
        pass
    return None


def custom_min_date_extractor(map:dict):
    min_date = datetime.now()
    tag = None
    for k,v in map.items():
        if "date" in k.lower():
            value = getDateTimeFromString(v)
            # print(k, value)
            if value is not None:
                min_date = min(min_date, value)
                tag = k

    # media_create_date = get_key_from_exif_dict(map, "Creation Date")
    # print('media_create_date', media_create_date)
    # if media_create_date is not None and min_date < media_create_date:
        # print("Using Media Create Date", media_create_date, "Check min date from", k)
        # return media_create_date

    return min_date

def extract_exif_data(video_path):
    process = subprocess.Popen(["exiftool", video_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    exif_data = {}

    for line in out.decode("utf-8").splitlines():
        key, value = line.split(": ", 1)
        exif_data[key] = value
        # print(key, value)

    return exif_data