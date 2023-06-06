import os
import datetime
import calendar


def read_text_file(file):
    with open(file, "r") as f:
        return f.read()


def create_folder(name):
    if os.path.isdir(name):
        print(f"folder {name} already exists")
    else:
        path = "./" + name
        os.mkdir(path)


def get_folder_size(dir_name):
    return len(
        [
            name
            for name in os.listdir(dir_name)
            if os.path.isfile(os.path.join(dir_name, name))
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
