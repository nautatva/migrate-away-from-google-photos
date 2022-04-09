from datetime import datetime
import piexif
import os


# IMAGE_EXTENSIONS = ["jpg", "png", "jpeg"]
IMAGE_EXTENSIONS = [".jpg", ".png", ".jpeg"]


def update_exif_photo_taken_date(filepath:str, date:datetime):
    exif_dict = piexif.load(filepath)
    new_date = date.strftime("%Y:%m:%d %H:%M:%S")
    exif_dict['0th'][piexif.ImageIFD.DateTime] = new_date
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date
    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_date
    # print(exif_dict)
    exif_bytes = piexif.dump(exif_dict)
    piexif.remove(filepath)
    piexif.insert(exif_bytes, filepath)


def is_image(filepath:str) -> bool:
    file_name, file_extension = os.path.splitext(filepath)
    # print("extension", file_extension)
    if file_extension.lower() not in IMAGE_EXTENSIONS:
        return False
    statfile = os.stat(filepath)
    filesize = statfile.st_size
    if filesize == 0:
        return False

    # import filetype
    # if filetype.image(filename):
    #     return False

    # from PIL import Image
    # try:
    #     im = Image.load(filename)
    #     im.verify()
    # except Exception:
    #     pass

    return True
