import sys
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib.animation import FuncAnimation, writers

sys.path.append("..")
from utility import read_text_file, get_good_points, get_folder_size


def get_colors(x, y):
    good_points, trendline, hull = get_good_points(x, y, 0)
    colors = ["blue"] * len(x)
    for i in range(len(x)):
        if good_points[i]:
            colors[i] = "lightgreen"
    return colors, trendline


def parse_calculated_data(file_name):
    str_data = read_text_file(file_name)
    lst_data = [s.split() for s in str_data.split("\n")[1:] if len(s.split()) > 0]
    res_x = np.array([])
    res_y = np.array([])
    for data in lst_data:
        cur_lat = float(data[-2])
        cur_flux = float(data[1]) + float(data[2])
        res_x = np.append(res_x, [cur_lat])
        res_y = np.append(res_y, [cur_flux])
    return res_x, res_y


def parse_measured_data(file_name):
    str_data = read_text_file(file_name)
    lst_data = [s.split() for s in str_data.split("\n")[4:] if len(s.split()) > 0]
    res_x = np.array([])
    res_y = np.array([])
    for data in lst_data:
        cur_lat = float(data[-2])
        cur_count_rate = float(data[1])
        res_x = np.append(res_x, [cur_lat])
        res_y = np.append(res_y, [cur_count_rate])
    return res_x, res_y


def main():
    # orbits = [4]
    # orbits = [4, 5, 6]
    orbits = np.arange(2, 3, 1)
    for orbit in orbits:
        x = np.array([])
        measured_y = np.array([])
        calculated_y = np.array([])
        measured_data_path = (
            f"../../data/interim/orbits/orbit_20090312/20090312_{orbit:02d}.txt"
        )
        calculated_data_path = f"../../data/interim/calculated orbits/orbit_20090312/20090312_{orbit:02d}.txt"
        cur_x, cur_y = parse_measured_data(measured_data_path)
        x = np.append(x, cur_x)
        measured_y = np.append(measured_y, cur_y)

        cur_x, cur_y = parse_calculated_data(calculated_data_path)
        calculated_y = np.append(calculated_y, cur_y)
        fig, ax = plt.subplots(figsize=(24, 22))

        ax.tick_params(rotation=45, labelsize=50)

        ax.set_ylim(1, 1e9)
        ax.set_xlim(-80, 81)
        ax.set_xticks(np.arange(-80, 81, 20))
        colors, trendline = get_colors(cur_x, measured_y)

        plt.semilogy()

        ax.grid(which="major", color=[0.4, 0.4, 0.4])
        ax.grid(which="minor", color=[0.7, 0.7, 0.7], linestyle="--")
        ax.minorticks_on()
        # plt.plot(x, measured_y + 1, linewidth=3)
        ax.set_xlabel("Latitude, deg", fontsize=50)
        ax.set_ylabel("Counts/sec", fontsize=50)
        plt.semilogy()

        # (line,) = ax.plot(0, 0, linewidth=5, color="#f97306")

        # def animation_frame(i):
        #     line.set_xdata(x[:i])
        #     line.set_ydata(calculated_y[:i] + 1)
        #     return (line,)

        # ax.legend(["Electron flow"], loc="upper left", fontsize=40)
        # animation = FuncAnimation(
        #     fig, func=animation_frame, frames=np.arange(1, len(x), 35), interval=10
        # )
        # Writer = writers["ffmpeg"]
        # writer = Writer(fps=20, metadata={"artist": "Me"}, bitrate=1800)

        # animation.save("Line Graph Animation.gif", writer)
        # plt.show()

        # plt.scatter(
        #     x,
        #     measured_y + 1,
        #     color=["blue" if x > 0 else "lightgreen" for x in calculated_y],
        # )
        # plt.scatter(
        #     x,
        #     measured_y + 1,
        #     color=colors,
        # )
        plt.plot(x, calculated_y + 1, linewidth=5, color="#f97306")
        leg = plt.legend(
            [
                # "Count rate",
                "Proton and electron flux",
            ],
            loc="upper left",
            fontsize=40,
        )
        # leg.legendHandles[0].set_color("white")
        plt.savefig(
            f"../../reports/figures/data_match/orbits/orbit_20090312/20090312_{orbit:02d}.png"
        )
        plt.close()


if __name__ == "__main__":
    main()
    # x_data = []
    # y_data = []

    # fig, ax = plt.subplots()
    # ax.set_xlim(0, 105)
    # ax.set_ylim(0, 12)
    # (line,) = ax.plot(0, 0)

    # def animation_frame(i):
    #     x_data.append(i * 10)
    #     y_data.append(i)

    #     line.set_xdata(x_data)
    #     line.set_ydata(y_data)
    #     return (line,)

    # animation = FuncAnimation(
    #     fig, func=animation_frame, frames=np.arange(0, 2, 0.1), interval=10
    # )
    # plt.show()
