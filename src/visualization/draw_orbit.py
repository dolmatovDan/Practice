import sys
import matplotlib.pyplot as plt
import numpy as np
import bisect
import os
import matplotlib as mpl
import matplotlib.patches as mpatches

sys.path.append("..")
from utility import (
    get_good_points,
    create_folder,
    get_folder_size,
    read_text_file,
    select_build_good_points,
)


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

    for data in lst_data[4:]:
        data = list(map(float, data.split()))
        lst_time.append(data[0])
        lst_lat.append(round(data[-2], 2))
        lst_count_rate.append(sum(data[1:4]))

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
    good_points, trendline, hull = get_good_points(x, y, 0)
    selected_x, selected_y = select_build_good_points(x, y, 0)
    colors = ["blue"] * len(x)
    # for i in range(len(x)):
    #     if y[i] in selected_y:
    #         colors[i] = "lightgreen"
    for i in range(len(x)):
        if good_points[i]:
            colors[i] = "lightgreen"
    return colors, trendline, hull


def colors_for_trendline(x, y):
    lower_bound = int(len(x) * 0.35)
    upper_bound = int(len(y) * 0.5)
    lower_bound_value = sorted(y)[lower_bound]
    upper_bound_value = sorted(y)[upper_bound - 1]
    colors = []
    for val in y:
        if lower_bound_value <= val <= upper_bound_value:
            colors.append("midnightblue")
        else:
            colors.append("lightblue")
    return colors


def draw_orbit(date, save_folder, data_folder):
    folder_size = get_folder_size(data_folder)

    for index in range(folder_size):
        print(index)
        data = get_day_data(f"{data_folder}/{date}_{index:02d}.txt")

        count_rate = data[0]
        lat = data[1]
        time = data[2]
        pair_time_lat = data[3]
        title_data = f"{data[4]}\n{data[5]}\n{data[6]}"

        fig, ax = plt.subplots(figsize=(24, 22))
        # fig, ax = plt.subplots(figsize=(16, 9))

        # ax1 = ax.twiny()

        colors, trendline, hull = get_colors(lat, count_rate)

        # ax.scatter(
        #     lat,
        #     count_rate,
        #     color=[
        #         "blue"
        #         if i > 0.35 * len(count_rate) and i < 0.5 * len(count_rate)
        #         else "lightblue"
        #         for i in range(len(count_rate))
        #     ],
        #     linewidth=1.25,
        #     s=15,
        # )
        # ax.scatter(
        #     np.linspace(0, 100, len(count_rate)),
        #     sorted(count_rate),
        #     color=[
        #         "lightgreen"
        #         if i > 0.35 * len(count_rate) and i < 0.5 * len(count_rate)
        #         else "blue"
        #         for i in range(len(count_rate))
        #     ],
        #     linewidth=1.25,
        #     s=15,
        # )

        # ax.scatter(lat, count_rate, color=colors, linewidth=1.25, s=15)
        ax.scatter(lat, count_rate, color="blue", linewidth=1.25, s=15)

        # ax.scatter(lat, count_rate, color="cornflowerblue", linewidth=1.25, s=15)
        # trendline_colors = colors_for_trendline(time, count_rate)
        # ax.scatter(
        #     lat, count_rate, color=trendline_colors, linewidth=1.25, s=15, alpha=1
        # )

        # for i in range(len(hull) - 1):
        #     plt.fill_between(
        #         [lat[i], lat[i + 1]],
        #         [hull[i][0], hull[i + 1][0]],
        #         [hull[i][1], hull[i + 1][1]],
        #         color="red",
        #         alpha=0.1,
        #     )
        # ax.plot(lat, trendline(lat), color="red", linewidth=3)

        # plt.annotate(
        #     title_data,
        #     (0, 0),
        #     (0, -70),
        #     xycoords="axes fraction",
        #     textcoords="offset points",
        #     va="top",
        #     fontsize=24,
        # )

        lat_lim_min = min(lat)
        lat_lim_max = max(lat)
        # print(lat_lim_min, lat_lim_max)

        time_ticks = np.arange(-80, 81, 20)

        ax.set_xlim([-80, 80])
        ax.set_xticks(time_ticks)
        # ax.set_xlim([0, 101])
        # ax.set_xticks(np.arange(0, 101, 10))

        # ax1.set_xlim([time_lim_min, time_lim_max])
        # ax1.set_xticks(time_ticks)

        # labels = get_lat_ticks(time_ticks, pair_time_lat)

        # ax1.set_xticklabels(labels)
        # ax1.tick_params(rotation=45, labelsize=30)

        ax.tick_params(rotation=45, labelsize=50)

        # help_x = np.arange(35, 51, 1)
        # ax.fill_between(
        #     help_x,
        #     np.full(16, 1e7),
        #     help_x,
        #     np.full(16, 1),
        #     color="red",
        #     alpha=0.2,
        # )
        ax.set_xlabel("Latitude, deg", fontsize=50)
        ax.set_ylabel("Count Rate, counts/sec", fontsize=50)

        # ax.set_yticks(np.arange(0, 20000, 1000))
        # ax.set_ylim([10, 20000])
        # ax.set_ylim([0, 1000])
        # ax.set_yticks(np.arange(0, 1000, 100))
        ax.set_ylim(3e2, 1e5)

        plt.semilogy()

        ax.grid(which="major", color=[0.4, 0.4, 0.4])
        ax.grid(which="minor", color=[0.7, 0.7, 0.7], linestyle="--")
        ax.minorticks_on()

        # ax1.set_xlabel("Latitude", fontsize=35)

        fig.savefig(f"{save_folder}/{date}_{index:02d}")
        plt.subplots_adjust(bottom=0.1)
        plt.close(fig)

        # plt.show()


# 20090303_02


def main():
    for day in range(15, 17):
        date = f"200903{day:02d}"
        save_folder = f"../../reports/figures/orbit_{date}"
        create_folder(save_folder)
        data_folder = f"../../data/interim/orbits/orbit_{date}"
        draw_orbit(date, save_folder, data_folder)
    # for orbit in range(4, 5):
    #     print(orbit)
    #     day = 12
    #     path = f"../../data/interim/orbits/orbit_200903{day:02d}/200903{day:02d}_{orbit:02d}.txt"
    #     data = read_text_file(path)
    #     data = [
    #         list(map(float, s.split()))
    #         for s in data.split("\n")[3:]
    #         if len(s.split()) > 0
    #     ]
    #     y = [a[-2] for a in data]
    #     x = [a[-1] for a in data]
    #     plt.plot(x, y)
    #     plt.ylim(-90, 90)
    #     plt.xlim(-180, 180)
    #     plt.show()


if __name__ == "__main__":
    main()
