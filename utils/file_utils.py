import filedate
from datetime import datetime
from utils.image_utils import is_image, update_exif_photo_taken_date


def update_file_with_date(file_path:str, date:datetime):
    if date is None:
        return
    if date < datetime(2002,1,1):
        print("date too old, check manually", file_path)
        return

    if date > datetime.now():
        print("date in future not possible", file_path)
        return

    print("Doing", file_path, date)

    # if is_image(file_path):
    #     update_exif_photo_taken_date(file_path, date)
    filedate.File(file_path).set(
        created=date,
        modified=date
    )
