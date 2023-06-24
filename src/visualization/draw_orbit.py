import sys
import matplotlib.pyplot as plt
import numpy as np
import bisect
import os
import matplotlib as mpl

sys.path.append("..")
from utility import get_good_points, create_folder, get_folder_size, read_text_file


def get_lat_ticks(times, pair_time_lat):
    tick_labels = []
    for time in times:
        pos = pair_time_lat[1][bisect.bisect_left(pair_time_lat[0], time)]
        tick_labels.append(str(pos))
    return tick_labels


def get_day_data(name):
    str_data = read_text_file(name)
    lst_data = [s for s in str_data.split("\n") if len(s.split()) > 0]
    lst_time = []
    lst_lat = []
    lst_count_rate = []
    lst_pair_time_lat = [[], []]

    str_time_range = lst_data[0]
    str_time_duration = lst_data[1]
    str_long_range = lst_data[2]

    for data in lst_data[3:]:
        data = list(map(float, data.split()))
        lst_time.append(data[0])
        lst_lat.append(round(data[-2], 2))
        lst_count_rate.append(data[3])

        lst_pair_time_lat[0].append(data[0])
        lst_pair_time_lat[1].append(data[-2])

    return [
        lst_count_rate,
        lst_lat,
        lst_time,
        lst_pair_time_lat,
        str_time_range,
        str_time_duration,
        str_long_range,
    ]


def get_colors(x, y):
    good_points, trendline = get_good_points(x, y)
    colors = ["blue"] * len(x)
    for i in range(len(x)):
        if good_points[i]:
            colors[i] = "lightgreen"
    return colors


def draw_orbit(date, save_folder, data_folder):
    folder_size = get_folder_size(data_folder)

    for index in range(folder_size):
        data = get_day_data(f"{data_folder}/{date}_{index:02d}.txt")

        count_rate = data[0]
        lat = data[1]
        time = data[2]
        pair_time_lat = data[3]
        title_data = f"{data[4]}\n{data[5]}\n{data[6]}"

        fig, ax = plt.subplots(figsize=(24, 16))

        ax1 = ax.twiny()

        colors = get_colors(time, count_rate)

        ax.scatter(time, count_rate, color=colors, linewidth=1.25, s=15)

        plt.annotate(
            title_data,
            (0, 0),
            (0, -70),
            xycoords="axes fraction",
            textcoords="offset points",
            va="top",
            fontsize=18,
        )

        time_lim_min = min(time)
        time_lim_max = max(time)

        time_ticks = np.arange(int(min(time)), int(max(time)), 100)

        ax.set_xlim([time_lim_min, time_lim_max])
        ax.set_xticks(time_ticks)

        ax1.set_xlim([time_lim_min, time_lim_max])
        ax1.set_xticks(time_ticks)

        labels = get_lat_ticks(time_ticks, pair_time_lat)

        ax1.set_xticklabels(labels)
        ax1.tick_params(rotation=45, labelsize=17)

        ax.tick_params(rotation=45, labelsize=17)

        ax.set_xlabel("Time (s)", fontsize=35)
        ax.set_ylabel("Count Speed", fontsize=35)
        # ax.set_yticks(np.arange(0, 20000, 1000))
        # ax.set_ylim([10, 20000])
        ax.set_ylim([0, 1000])
        ax.set_yticks(np.arange(0, 1000, 100))

        # plt.semilogy()

        ax.grid(which="major", color=[0.4, 0.4, 0.4])
        ax.grid(which="minor", color=[0.7, 0.7, 0.7], linestyle="--")
        ax.minorticks_on()

        ax1.set_xlabel("Latitude", fontsize=35)

        fig.savefig(f"{save_folder}/{date}_{index:02d}")
        plt.close(fig)


def main():
    date = "20090301"
    save_folder = f"../../reports/figures/orbit_{date}"
    create_folder(save_folder)
    data_folder = f"../../data/interim/orbits/orbit_{date}"
    draw_orbit(date, save_folder, data_folder)


if __name__ == "__main__":
    main()
