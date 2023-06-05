import numpy as np
from matplotlib import pyplot as plt
import os


def read_text_file(file):
    with open(file, "r") as f:
        return f.read()


def create_directory(name):
    if os.path.isdir(name):
        print(f"Directory {name} already exists")
    else:
        path = "./" + name
        os.mkdir(path)


def get_directory_size(dir_name):
    return len(
        [
            name
            for name in os.listdir(dir_name)
            if os.path.isfile(os.path.join(dir_name, name))
        ]
    )


def get_trendline(x, y):
    equation = np.polyfit(x, y, 1)
    trendline = np.poly1d(equation)
    return trendline


def parse_data(file_name):
    str_data = read_text_file(file_name)
    lst_data = [s for s in str_data.split("\n") if len(s.split()) > 0]
    x = []
    y = []
    for data in lst_data[3:]:
        data = list(map(float, data.split()))
        y.append(sum(data[1:5]))
        x.append(data[0])
    return x, y


def get_good_points(arr_x, arr_y):
    df = []
    for x, y in zip(arr_x, arr_y):
        df.append([x, y])
    df.sort(key=lambda x: x[1])

    lower_bound = int(len(arr_x) * 0.4)
    upper_bound = int(len(arr_x) * 0.5)
    definitely_good_points = df[lower_bound:upper_bound]
    good_x, good_y = zip(*definitely_good_points)

    trendline = get_trendline(good_x, good_y)

    is_good = [False] * len(arr_x)

    for index, (x, y) in enumerate(zip(arr_x, arr_y)):
        dif = abs(trendline(x) - y)
        if dif / abs(trendline(x)) < 0.5:
            is_good[index] = True

    return is_good, trendline


def get_good_points_from_file(file_name):
    x, y = parse_data(file_name)
    return get_good_points(x, y)


def get_stable_file_count_rate_range(file_name):
    cnt_good_points = 0

    arr_x, arr_y = parse_data(file_name)
    arr_x = np.array(arr_x)
    arr_y = np.array(arr_y)

    good_points, trendline = get_good_points(arr_x, arr_y)

    for point in good_points:
        if point:
            cnt_good_points += 1
    return cnt_good_points / len(arr_x)


def get_stable_day_count_rate_range(day):
    dir_name = f"../../data/interim/orbits/orbit_200903{day:02d}"
    dir_size = get_directory_size(dir_name)

    sum_stable_range = 0
    for index in range(dir_size):
        file_name = f"{dir_name}/200903{day:02d}_{index:02d}.txt"
        cur_stable_range = get_stable_file_count_rate_range(file_name)
        sum_stable_range += cur_stable_range

    return sum_stable_range / dir_size


def main():
    mean_stable_range = 0
    for day in range(1, 32):
        cur_stable_range = get_stable_day_count_rate_range(day)
        mean_stable_range += cur_stable_range
    print(mean_stable_range / 31)


if __name__ == "__main__":
    main()
