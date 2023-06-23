import sys

sys.path.append("..")
from utility import (
    get_good_points,
    read_text_file,
    get_folder_size,
    YEAR,
    MONTH,
    get_mean_range,
)


def get_stable_range_boundaries(arr_x, arr_y):
    is_good, trendline = get_good_points(arr_x, arr_y)
    min_count_rate, max_count_rate = float("inf"), float("-inf")
    good_points = []
    for good, val in zip(is_good, arr_y):
        if good:
            good_points.append(val)
    return good_points


def get_file_stable_range_boundaries(filename):
    str_data = read_text_file(filename)
    lst_data = [s.split() for s in str_data.split("\n") if len(s.split()) > 0][3:]
    lst_data = [list(map(float, s)) for s in lst_data]

    lst_count_rate_25_100 = [s[1] for s in lst_data]
    lst_count_rate_100_400 = [s[2] for s in lst_data]
    lst_count_rate_400_640 = [s[3] for s in lst_data]

    lst_time = [s[0] for s in lst_data]

    good_25_100 = get_stable_range_boundaries(lst_time, lst_count_rate_25_100)
    good_100_400 = get_stable_range_boundaries(lst_time, lst_count_rate_100_400)
    good_400_640 = get_stable_range_boundaries(lst_time, lst_count_rate_400_640)

    return [good_25_100, good_100_400, good_400_640]


def get_day_mean_stable_range_boundaries(date):
    folder_size = get_folder_size(f"../../data/interim/orbits/orbit_{date}")
    cnt_boundaries = 3
    stable_range_boundaries = [[] for i in range(cnt_boundaries)]
    for index in range(folder_size):
        cur_file = f"../../data/interim/orbits/orbit_{date}/{date}_{index:02d}.txt"
        cur_boundaries = get_file_stable_range_boundaries(cur_file)
        for i in range(cnt_boundaries):
            stable_range_boundaries[i] += cur_boundaries[i]
    return stable_range_boundaries


def main():
    date = f"{YEAR}{MONTH:02d}"
    cnt_boundaries = 3
    stable_range_total = [[] for i in range(cnt_boundaries)]
    for day in range(1, 32):
        print(day)
        cur_stable_ranges = get_day_mean_stable_range_boundaries(f"{date}{day:02d}")
        for i in range(cnt_boundaries):
            stable_range_total[i] += cur_stable_ranges[i]
    for i in range(cnt_boundaries):
        print(get_mean_range(stable_range_total[i]))

    # for i in range(cnt_boundaries):
    #     print(len(stable_range_total[i]))


if __name__ == "__main__":
    main()
