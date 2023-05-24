import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib
from itertools import chain
import matplotlib.colors as mcolors


class Plot:
    def __init__(self, plotNum, start, finish):
        self.label = ['Скорость счета для верхнего датчика в первом диапазоне', 'Скорость счета для нижнего датчика в '
                                                                                'первом диапазоне',
                      'Скорость счета для верхнего датчика во втором диапазоне', 'Скорость счета для нижнего датчика '
                                                                                 'во втором диапазоне'][plotNum - 1]
        self.filename = ['./plot_data/plot_data_1_S1.txt', 'plot_data_1_S2.txt', 'plot_data_2_S1.txt', 'plot_data_2_S2.txt'][plotNum - 1]
        self.ax = plt.subplot()
        self.start = start
        self.finish = finish
        self.const = [np.log10(100000), 262275, 269610, 274050][plotNum - 1]
        self.m = Basemap(projection='cyl', resolution='c',
                         llcrnrlat=-90, urcrnrlat=90,
                         llcrnrlon=-180, urcrnrlon=180)
        self.m.drawcoastlines(color=[0.5, 0.5, 0.5], zorder=0.5)
        self.m.drawmapboundary(fill_color=[1, 1, 1], zorder=0)
        self.scale = 0.2
        # m.etopo(scale=0.5, alfa=0) # Another way of drawing
        self.draw_map()
        self.norm = matplotlib.colors.Normalize(vmin=2, vmax=self.const)
        self.cmap = matplotlib.cm.coolwarm
        plt.set_cmap('coolwarm')
        self.cbar = plt.colorbar(matplotlib.cm.ScalarMappable(norm=self.norm, cmap=self.cmap), label="Скорость счета")
        self.cbar.set_ticks(np.arange(2, 5.1, 0.5))
        self.ax.set_title(self.label, fontsize=20, fontfamily='serif',
                          fontstyle='italic')
        self.draw_points()

    def draw_map(self):
        self.m.shadedrelief(scale=self.scale)
        self.lats = self.m.drawparallels(np.arange(-180, 180, 30), labels=[1, 0, 0, 0])
        self.lons = self.m.drawmeridians(np.arange(-180, 180, 60), labels=[0, 0, 0, 1])
        self.lat_lines = chain(*(tup[1][0] for tup in self.lats.items()))
        self.lon_lines = chain(*(tup[1][0] for tup in self.lons.items()))
        self.all_lines = chain(self.lat_lines, self.lon_lines)
        for line in self.all_lines:
            line.set(linestyle='-', alpha=1, color='black')

    def draw_points(self):
        x = []
        y = []
        t = []
        self.const = np.log10(100000)
        el = 200000000
        with open(self.filename) as file:
            counter = 0
            for line in file:
                if self.start < counter < self.finish:
                    lst1 = list(map(float, line.split()))
                    cur_count_rates = lst1[0:3]
                    cur_count_rates.sort()
                    if cur_count_rates[1] > 0:
                        el = min(el, np.log10(sum(cur_count_rates)))
                        t.append(plt.cm.coolwarm((np.log10(sum(cur_count_rates)) - 2) / self.const))
                        x.append(lst1[-1])
                        y.append(lst1[-2])
                counter += 1
        plt.scatter(x, y, c=t, s=1, zorder=1, alpha=0.5)
        # print(sorted(ar))
        print(el)
    def draw_plot(self):
        plt.show()


print("Give the plot number (1 is 1_S1, 2 is 1_S2, 3 is 2_S1, 4 is 2_S2), and data range (start, finish)")
plot_data = list(map(int, input().split()))
satellite_map = Plot(plot_data[0], plot_data[1], plot_data[2])
satellite_map.draw_plot()