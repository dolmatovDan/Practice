from matplotlib.animation import FuncAnimation, writers
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.basemap import Basemap
from itertools import chain
import matplotlib.colors as mcolors
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

plt.rcParams["figure.dpi"] = 140


class Plot:
    def __init__(self, plot_num, start, finish):
        self.label = [
            "Count rate for S1 detector",
            "Скорость счета для нижнего датчика в " "первом диапазоне",
            "Скорость счета для верхнего датчика во втором диапазоне",
            "Скорость счета для нижнего датчика " "во втором диапазоне",
        ][plot_num - 1]
        self.filename = [
            "../../data/interim/map_data/plot_data_1_S1.txt",
            "../../data/interim/map_data/plot_data_1_S2.txt",
            "../../data/interim/map_data/plot_data_2_S1.txt",
            "../../data/interim/map_data/plot_data_2_S2.txt",
        ][plot_num - 1]
        self.ax = plt.subplot()
        self.start = start
        self.finish = finish
        self.const = [1e5, 262275, 269610, 274050][plot_num - 1]
        self.m = Basemap(
            projection="cyl",
            resolution="c",
            llcrnrlat=-90,
            urcrnrlat=90,
            llcrnrlon=-180,
            urcrnrlon=180,
        )
        self.m.drawcoastlines(color=[0.5, 0.5, 0.5], zorder=0.5)
        self.m.drawmapboundary(fill_color=[1, 1, 1], zorder=0)
        self.scale = 0.2
        # m.etopo(scale=0.5, alfa=0) # Another way of drawing
        self.draw_map()
        self.norm = matplotlib.colors.Normalize(vmin=0, vmax=self.const)
        self.cmap = matplotlib.cm.coolwarm
        # plt.set_cmap("coolwarm")
        # self.cbar = plt.colorbar(
        #     matplotlib.cm.ScalarMappable(norm=self.norm, cmap=self.cmap),
        # )
        # self.cbar.set_label(r"$log_{10} (count\;rate,\;counts/sec)$", fontsize=15)
        # self.cbar.set_ticks(np.arange(0, 5.1, 0.5))
        # self.ax.set_title(
        #     self.label, fontsize=20, fontfamily="serif", fontstyle="italic"
        # )
        self.draw_points()

    def draw_map(self):
        self.m.shadedrelief(scale=self.scale)
        self.lats = self.m.drawparallels(np.arange(-180, 180, 30), labels=[1, 0, 0, 0])
        self.lons = self.m.drawmeridians(np.arange(-180, 180, 60), labels=[0, 0, 0, 1])
        self.lat_lines = chain(*(tup[1][0] for tup in self.lats.items()))
        self.lon_lines = chain(*(tup[1][0] for tup in self.lons.items()))
        self.all_lines = chain(self.lat_lines, self.lon_lines)
        for line in self.all_lines:
            line.set(linestyle="-", alpha=1, color="black")

    def draw_points(self):
        x = []
        y = []
        t = []
        self.const = np.log10(1e5)
        with open(self.filename) as file:
            step = 0
            for line in file:
                if self.start < step < self.finish:
                    lst1 = list(map(float, line.split()))
                    cur_count_rates = lst1[0:1]
                    cur_count_rates.sort()
                    t.append(
                        plt.cm.coolwarm(
                            (np.log10(sum(cur_count_rates) + 1) - 1.5) / self.const
                        )
                    )
                    # if lst1[0] == 1:
                    #     t.append("lightcoral")
                    # else:
                    #     t.append("cornflowerblue")
                    x.append(lst1[-1])
                    y.append(lst1[-2])
                step += 1

        plt.scatter(x, y, c=t, s=0.1, zorder=1, alpha=1)
        # fig, ax = plt.subplots()
        # (line,) = ax.plot(0, 0, linewidth=5, color="#f97306")

        # def animation_frame(i):
        #     line.set_xdata(x[:i])
        #     line.set_ydata(np.array(y[:i]) + 1)
        #     return (line,)

        # ax.legend(["Proton flow"], loc="upper left", fontsize=40)
        # animation = FuncAnimation(
        #     fig, func=animation_frame, frames=np.arange(1, len(x), 50), interval=10
        # )
        # Writer = writers["ffmpeg"]
        # writer = Writer(fps=20, metadata={"artist": "Me"}, bitrate=1800)

        # animation.save("Line Graph Animation.gif", writer)
        # plt.show()

    def draw_plot(self):
        # plt.savefig("../../reports/figures/count_rate_map.png")
        # self.ax.xaxis.set_major_locator(MultipleLocator(60))
        # self.ax.yaxis.set_major_locator(MultipleLocator(60))

        # Change minor ticks to show every 5. (20/4 = 5)
        # self.ax.xaxis.set_minor_locator(AutoMinorLocator(4))
        # self.ax.yaxis.set_minor_locator(AutoMinorLocator(4))

        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])

        # Turn grid on for both major and minor ticks and style minor slightly
        # differently.
        plt.grid(which="major", color="#000000", linestyle="--")
        plt.grid(which="minor", color="#000000", linestyle="--")
        plt.grid()
        plt.show()


print(
    "Give the plot number (1 is 1_S1, 2 is 1_S2, 3 is 2_S1, 4 is 2_S2), and data range (start, finish)"
)
plot_data = list(map(int, input().split()))
satellite_map = Plot(plot_data[0], plot_data[1], plot_data[2])
satellite_map.draw_plot()
