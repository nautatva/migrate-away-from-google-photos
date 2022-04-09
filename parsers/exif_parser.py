from PIL import Image, ExifTags
from datetime import datetime
from utils.common_utils import is_json_key_present
from utils.image_utils import is_image


def extract_exif_date_taken(filename:str) -> datetime:
    if not is_image(filename):
        # Cannot update exif if not image
        return None

    try:
        image = Image.open(filename)
        image_exif = image._getexif()
    except Exception:
        print("Exception in file", filename)
        return None
    if image_exif:
        # Make a map with tag names
        exif = {ExifTags.TAGS[k]: v for k, v in image_exif.items() if k in ExifTags.TAGS and type(v) is not bytes}

        # json = safe_serialize(exif, indent=4)  # Spares the non-serializable data like GPSInfo (byte in dict)
        try:
            if is_json_key_present(exif, "DateTimeOriginal"):
                date_str = exif['DateTimeOriginal']
                return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
        except Exception:
            pass
    else:
        print('Unable to get date from exif for %s' % filename)

    return None
