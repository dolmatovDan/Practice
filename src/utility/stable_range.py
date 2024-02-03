import numpy as np
from matplotlib import pyplot as plt
import os
import sys
from radbelt import get_flux


sys.path.append("..")
from .methods import read_text_file, get_folder_size
from .constants import YEAR, MONTH


def get_trendline(x, y):
    equation = np.polyfit(x, y, 1)
    trendline = np.poly1d(equation)
    return trendline


def parse_data(file_name):
    str_data = read_text_file(file_name)
    lst_data = [s for s in str_data.split("\n") if len(s.split()) > 0]
    x = []
    y = []
    for data in lst_data[4:]:
        data = list(map(float, data.split()))
        y.append(sum(data[1:4]))
        x.append(data[0])
    return x, y


# def get_good_points(arr_x, arr_y):
#     df = []
#     for x, y in zip(arr_x, arr_y):
#         df.append([x, y])
#     df.sort(key=lambda x: x[1])

#     lower_bound = int(len(arr_x) * 0.35)
#     upper_bound = int(len(arr_x) * 0.5)
#     definitely_good_points = df[lower_bound:upper_bound]
#     good_x, good_y = zip(*definitely_good_points)

#     trendline = get_trendline(good_x, good_y)

#     is_good = [False] * len(arr_x)

#     for index, (x, y) in enumerate(zip(arr_x, arr_y)):
#         dif = abs(trendline(x) - y)
#         if (dif < 0.7 * abs(trendline(x)) and trendline(x) > y) or (
#             dif < 0.35 * abs(trendline(x)) and trendline(x) <= y
#         ):
#             is_good[index] = True

#     return is_good, trendline


def select_build_good_points(arr_x, arr_y, index):
    arr_x = [arr_x[i] for i in range(len(arr_x)) if arr_y[i] > 0 and arr_y[i] < 5e3]
    arr_y = [arr_y[i] for i in range(len(arr_y)) if arr_y[i] > 0 and arr_y[i] < 5e3]

    hist, bin_edges = np.histogram(arr_y, bins=int(len(arr_x) ** 0.5))
    # print(len(arr_x), hist.max())

    fig, ax = plt.subplots(figsize=(10, 8))
    hh = ax.hist(arr_y, bins=int(len(arr_x) ** 0.5))
    hh[-1].patches[hist.argmax()].set_color("lightgreen")

    ax.set_xlabel("Count Rate, counts/sec", fontsize=20)
    ax.set_ylabel("Number of points", fontsize=20)
    ax.set_xticks(np.arange(1e3, 5e3 + 1, 1e3))
    ax.tick_params(labelsize=20)
    ax.grid()
    fig.savefig(f"../../reports/figures/hist/{index}.png")
    plt.close()

    target = hist.argmax()
    target_points = [
        arr_y[i]
        for i in range(len(arr_y))
        if bin_edges[target] <= arr_y[i] < bin_edges[target + 1]
    ]

    y_mean = np.mean(target_points)
    sigma = y_mean**0.5
    # print(index, y_mean - sigma * 3, y_mean, y_mean + sigma * 3)
    # print(bin_edges)
    selected_x = []
    selected_y = []

    for x, y in zip(arr_x, arr_y):
        if y_mean - sigma * 3 <= y <= y_mean + sigma * 3:
            # if bin_edges[target] <= y < bin_edges[target + 1]:
            selected_x.append(x)
            selected_y.append(y)
    return selected_x, selected_y


def get_good_points(arr_x, arr_y, index):
    good_x, good_y = select_build_good_points(arr_x, arr_y, index)
    trendline = get_trendline(good_x, good_y)
    hull = []

    is_good = [False] * len(arr_x)

    for index, (x, y) in enumerate(zip(arr_x, arr_y)):
        sigma = abs(trendline(x)) ** 0.5
        c = 10
        hull.append((trendline(x) - sigma * c, trendline(x) + sigma * c))
        if trendline(x) - sigma * c <= y <= trendline(x) + sigma * c:
            is_good[index] = True

    return is_good, trendline, hull


def get_good_points_from_file(file_name, index):
    x, y = parse_data(file_name)
    return get_good_points(x, y, index)


def get_stable_file_count_rate_range(file_name, index):
    cnt_good_points = 0

    arr_x, arr_y = parse_data(file_name)
    arr_x = np.array(arr_x)
    arr_y = np.array(arr_y)

    good_points, trendline = get_good_points(arr_x, arr_y, index)

    for point in good_points:
        if point:
            cnt_good_points += 1
    return cnt_good_points / len(arr_x)


def get_stable_day_count_rate_range(date):
    folder_name = f"../../data/interim/orbits/orbit_{date}"
    folder_size = get_folder_size(folder_name)

    sum_stable_range = 0
    for index in range(folder_size):
        file_name = f"{folder_name}/{date}_{index:02d}.txt"
        cur_stable_range = get_stable_file_count_rate_range(file_name, index)
        sum_stable_range += cur_stable_range

    return sum_stable_range / folder_size


def main():
    mean_stable_range = 0
    for day in range(1, 2):
        date = f"{YEAR}{MONTH:02d}{day:02d}"
        cur_stable_range = get_stable_day_count_rate_range(date)
        mean_stable_range += cur_stable_range
        print(day, cur_stable_range)
    print(mean_stable_range / 31)
    # str_data = read_text_file(
    #     "../../data/interim/orbits/orbit_20090301/20090301_02.txt"
    # )
    # lst_data = [
    #     list(map(float, s.split()))
    #     for s in str_data.split("\n")[4:]
    #     if len(s.split()) > 0
    # ]
    # arr_x = [s[-2] for s in lst_data]
    # arr_y = [sum(s[1:4]) for s in lst_data]
    # select_build_good_points(arr_x, arr_y)


if __name__ == "__main__":
    main()
