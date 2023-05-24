import matplotlib.pyplot as plt
import numpy as np
import bisect


DATE = 20090301

def get_lat_ticks(times, pair_time_lat):
    tick_labels = []
    for time in times:
        pos = pair_time_lat[1][bisect.bisect_left(pair_time_lat[0], time)]
        tick_labels.append(str(pos))
    return tick_labels


def read(name):
    with open(f"orbits/orbit_{DATE}/{name}") as file:
        time = []
        lat = []
        count_rate = []
        pair_time_lat = [[], []]

        str_time_range = file.readline()
        str_time_duration = file.readline()
        str_long_range = file.readline()

        points_color = []

        for line in file:
            point = list(map(float, line.split()))
            time.append(point[0])
            lat.append(round(point[-2], 2))
            count_rate.append(sum(point[1:4]))
            if sum(point[1:4]) > 500 and sum(point[1:4]) < 2000:
                points_color.append('lightgreen')
            else:
                points_color.append('blue')

            pair_time_lat[0].append(point[0])
            pair_time_lat[1].append(point[-2])

        return [count_rate, lat, time, pair_time_lat, str_time_range, str_time_duration, str_long_range, points_color]


def main():
    for index in range(31):
        data = read(f"{DATE}_{index:02d}.txt")

        count_rate = data[0]
        lat = data[1]
        time = data[2]
        pair_time_lat = data[3]
        title_data = f"{data[4]}{data[5]}{data[6]}"
        points_color = data[7]

        fig, ax = plt.subplots(figsize=(24, 18))

        ax1 = ax.twiny()

        # plt.scatter(time, countRate, s=0.5)
        # print(len(time), len(count_rate), len(points_color))
        ax.scatter(time, count_rate, color=points_color, linewidth=1.25, s=15)

        plt.annotate(title_data, (0, 0), (0, -70), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=18)

        min_elem = min(time)
        max_elem = max(time)

        ticks_time = np.arange(int(min(time)), int(max(time)), 100)

        ax.set_xlim([min_elem, max_elem])
        ax.set_xticks(ticks_time)

        ax1.set_xlim([min_elem, max_elem])
        ax1.set_xticks(ticks_time)

        labels = get_lat_ticks(ticks_time, pair_time_lat)

        ax1.set_xticklabels(labels)
        ax1.tick_params(rotation=45, labelsize=17)

        ax.tick_params(rotation=45, labelsize=17)
        ax.set_xlabel("Time (s)", fontsize=35)
        ax.set_ylabel("Count Speed", fontsize=35)
        ax.set_yticks(np.arange(0, 20000, 1000))


        plt.semilogy()

        ax.set_ylim([10, 20000])
        ax.grid(which="major", color=[0.4, 0.4, 0.4])
        ax.grid(which="minor", color=[0.7, 0.7, 0.7], linestyle='--')
        ax.minorticks_on()

        ax1.set_xlabel("Latitude", fontsize=35)

        fig.savefig(f"plots/orbit_{DATE}/{DATE}_{index:02d}.png")
        plt.close(fig)


if __name__ == '__main__':
    main()
