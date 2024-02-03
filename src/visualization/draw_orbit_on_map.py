import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.basemap import Basemap
from itertools import chain
import matplotlib.colors as mcolors
from cycler import cycler

colors = cycler(color=plt.get_cmap("tab20").colors)
# print(colors)

plt.rcParams["figure.dpi"] = 200

sys.path.append("..")
from utility import get_folder_size, read_text_file


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
        self.const = [np.log10(100000), 262275, 269610, 274050][plot_num - 1]
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
        plt.set_cmap("coolwarm")
        plt.tick_params(labelsize=200)
        self.cbar = plt.colorbar(
            matplotlib.cm.ScalarMappable(norm=self.norm, cmap=self.cmap),
        )
        self.cbar.set_label(r"$log_{10} (Count\;Rate,\;counts/sec)$", fontsize=13)
        self.cbar.set_ticks(np.arange(0, 5.1, 1))
        # self.ax.set_title(self.label, fontsize=15, fontfamily="serif")
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
        self.const = np.log10(10000)
        date = "20090312"
        folder = f"../../data/interim/orbits/orbit_{date}"
        # for orbit, color_palette in zip(range(20), colors):
        #     str_data = read_text_file(
        #         f"../../data/interim/orbits/orbit_{date}/{date}_{orbit:02d}.txt"
        #     )
        #     lst_data = [
        #         list(map(float, s.split()))
        #         for s in str_data.split("\n")[3:]
        #         if len(s.split()) > 0
        #     ]
        #     print(orbit, color_palette)
        #     for data in lst_data:
        #         x.append(data[-1])
        #         y.append(data[-2])
        #         t.append(color_palette["color"])
        with open(self.filename) as file:
            step = 0
            for line in file:
                if self.start < step < self.finish:
                    lst1 = list(map(float, line.split()))
                    cur_count_rates = lst1[0:3]
                    cur_count_rates.sort()
                    cur_count_rates[1] += 1
                    t.append(
                        plt.cm.coolwarm(
                            (np.log10(sum(cur_count_rates)) - 1.5) / self.const
                        )
                    )
                    x.append(lst1[-1])
                    y.append(lst1[-2])
                step += 1
        # for orbit, color_palette in zip(range(20, 31), colors):
        #     str_data = read_text_file(
        #         f"../../data/interim/orbits/orbit_{date}/{date}_{orbit:02d}.txt"
        #     )
        #     lst_data = [
        #         list(map(float, s.split()))
        #         for s in str_data.split("\n")[3:]
        #         if len(s.split()) > 0
        #     ]
        #     print(orbit, color_palette)
        #     for data in lst_data:
        #         x.append(data[-1])
        #         y.append(data[-2])
        #         t.append(color_palette["color"])
        plt.scatter(x, y, c=t, s=0.1, zorder=1, alpha=0.2)
        plt.tick_params(labelsize=100)
        plt.plot(x[750:1040], y[750:1040], c="black", linewidth=2, zorder=1)

    def draw_plot(self):
        # plt.savefig("../../reports/figures/count_rate_map.png")
        plt.show()


print(
    "Give the plot number (1 is 1_S1, 2 is 1_S2, 3 is 2_S1, 4 is 2_S2), and data range (start, finish)"
)
plot_data = list(map(int, input().split()))
satellite_map = Plot(plot_data[0], plot_data[1], plot_data[2])
satellite_map.draw_plot()
