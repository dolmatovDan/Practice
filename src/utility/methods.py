import os
import datetime
import calendar
from copy import deepcopy


def read_text_file(file):
    with open(file, "r") as f:
        return f.read()


def create_folder(name):
    if os.path.isdir(name):
        print(f"Folder {name} already exists")
    else:
        path = name
        os.mkdir(path)


def get_folder_size(folder_name):
    return len(
        [
            name
            for name in os.listdir(folder_name)
            if os.path.isfile(os.path.join(folder_name, name))
        ]
    )


def get_month_range(month, year):
    """
    Return month first day and month last day since year beginning
    For example: (60, 91)
    """
    first_day = datetime.date(year, month, 1)
    days_per_month_count = calendar.monthrange(year, month)[1]
    last_day = datetime.date(year, month, days_per_month_count)

    first_jan = datetime.date(year, 1, 1)

    first_day_diff = first_day - first_jan
    last_day_diff = last_day - first_jan

    return (first_day_diff.days + 1, last_day_diff.days + 1)


def get_mean_range(arr):
    arr_copy = deepcopy(arr)
    arr_copy.sort()
    low = len(arr_copy) // 100 * 5
    high = len(arr_copy) // 100 * 95
    return arr_copy[low], arr_copy[high]

def transform_date(date):
    """
    20090312 -> 2009-03-12
    """
    year = date[:4]
    month = date[4:6]
    day = date[6:]
    return f"{year}-{month}-{day}"