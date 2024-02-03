import sys
import numpy as np
from matplotlib import pyplot as plt

sys.path.append("..")
from utility import get_good_points, MONTH, YEAR, get_folder_size, read_text_file


def get_mean_stable_range(time, count_rate):
    is_good, trendline = get_good_points(time, count_rate)
    return sum(is_good) / len(is_good)


def get_mean_day_stable_range(date):
    cur_folder = f"../../data/interim/orbits/orbit_{date}"
    folder_size = get_folder_size(cur_folder)
    values = []
    for orbit in range(folder_size):
        cur_file = cur_folder + f"/{date}_{orbit:02d}.txt"
        str_data = read_text_file(cur_file)
        lst_data = [
            list(map(float, s.split()))
            for s in str_data.split("\n")[4:]
            if len(s.split()) > 0
        ]
        lst_count_rate = [sum(s[1:4]) for s in lst_data]
        lst_time = [s[0] for s in lst_data]
        values.append(get_mean_stable_range(lst_time, lst_count_rate))
    return np.mean(values)


def get_month_stable_range():
    stable_range_values = []
    for day in range(1, 32):
        date = f"{YEAR}{MONTH:02d}{day:02d}"
        stable_range_values.append(get_mean_day_stable_range(date))
    return stable_range_values


def main():
    x = np.arange(1, 32, 1)
    y = get_month_stable_range()
    plt.ylim((0, 1))
    plt.yticks(np.arange(0, 1.05, 0.1))
    plt.plot(x, y, markersize=10, marker=".")
    plt.show()


if __name__ == "__main__":
    main()
