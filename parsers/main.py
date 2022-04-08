from pathlib import Path
from datetime import datetime
import re


# Use this for easy addition of patterns
patterns = {
    "%Y%m%d_%H%M%S": re.compile(r'^.*(\d{8}_\d{6}).*?$')
}


def parse_date_from_file_name(file_path:str) -> datetime:
    # try this https://github.com/scrapinghub/dateparser
    fileP = Path(file_path).name
    pattern = re.compile(r'^.*(\d{8}_\d{6}).*?$')
    m8 = re.match(pattern, fileP)
    if m8:
        date_time = m8.group(1)
        # Check which formats can be used
        return datetime.strptime(date_time, "%Y%m%d_%H%M%S")

    pattern = re.compile(r'^.*(\d{6}_\d{6}).*?$')
    m6 = re.match(pattern, fileP)
    if m6 and not m8:
        date_time = m6.group(1)
        # Check which formats can be used
        return datetime.strptime(date_time, "%y%m%d_%H%M%S")

    pattern = re.compile(r'^.*(\d{6}_\d{6}).*?$')
    m6 = re.match(pattern, fileP)
    if m6 and not m8:
        date_time = m6.group(1)
        # Check which formats can be used
        return datetime.strptime(date_time, "%y%m%d_%H%M%S")

    pattern = re.compile(r'^.*(\d{14}).*?$')
    m8 = re.match(pattern, fileP)
    if m8:
        date_time = m8.group(1)
        # Check which formats can be used
        try:
            return datetime.strptime(date_time, "%Y%m%d%H%M%S")
        except Exception:
            pass

    pattern = re.compile(r'^.*(\d{8}).*?$')
    m8 = re.match(pattern, fileP)
    if m8:
        date_time = m8.group(1)
        # Check which formats can be used
        try:
            return datetime.strptime(date_time, "%Y%m%d")
        except Exception:
            pass

    pattern = re.compile(r'^.*(\d{6}).*?$')
    m6 = re.match(pattern, fileP)
    if m6 and not m8:
        date_time = m6.group(1)
        # Check which formats can be used
        try:
            return datetime.strptime(date_time, "%y%m%d")
        except Exception:
            pass

    # todo: "Photo 03-07-21, 5 59 09 PM.jpg"
    # pattern = re.compile(r'^.*(\d{2}-\d{2}-\d{2}, ).*?$')
    # m6 = re.match(pattern, fileP)
    # if m6 and not m8:
    #     date_time = m6.group(1)
    #     # Check which formats can be used
    #     try:
    #         return datetime.strptime(date_time, "%y%m%d")
    #     except Exception:
    #         pass

    # all_date_regex = r'^.*(((20[012]\d|19\d\d)|(1\d|2[0123]))-((0[0-9])|(1[012]))-((0[1-9])|([12][0-9])|(3[01])))|(((0[1-9])|([12][0-9])|(3[01]))-((0[0-9])|(1[012]))-((20[012]\d|19\d\d)|(1\d|2[0123])))|(((20[012]\d|19\d\d)|(1\d|2[0123]))\/((0[0-9])|(1[012]))\/((0[1-9])|([12][0-9])|(3[01])))|(((0[0-9])|(1[012]))\/((0[1-9])|([12][0-9])|(3[01]))\/((20[012]\d|19\d\d)|(1\d|2[0123])))|(((0[1-9])|([12][0-9])|(3[01]))\/((0[0-9])|(1[012]))\/((20[012]\d|19\d\d)|(1\d|2[0123])))|(((0[1-9])|([12][0-9])|(3[01]))\.((0[0-9])|(1[012]))\.((20[012]\d|19\d\d)|(1\d|2[0123])))|(((20[012]\d|19\d\d)|(1\d|2[0123]))\.((0[0-9])|(1[012]))\.((0[1-9])|([12][0-9])|(3[01]))).*?$'

    return None
