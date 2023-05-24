from itertools import chain

import numpy as np

import matplotlib

matplotlib.use('agg')

matplotlib.rcParams["figure.figsize"] = [11.693, 8.268]

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from mpl_toolkits.basemap import Basemap


class Plot:

    def __init__(self, det, idx_range, r_min, r_max):
        self.det = det
        self.idx_range = idx_range
        self.label = f'Скорость счета S{det} в диапазоне {idx_range}'

        self.const = 100

        self.create_layout(r_min, r_max)
        self.draw_map()

    def create_layout(self, r_min, r_max):
        self.ax = plt.subplot()
        self.ax.set_title(self.label, fontsize=14)

        self.norm = matplotlib.colors.Normalize(vmin=r_min, vmax=r_max)
        self.cmap = matplotlib.cm.coolwarm

        self.cbar = plt.colorbar(
            matplotlib.cm.ScalarMappable(norm=self.norm, cmap=self.cmap),
            label="lg (cкорость счета, отсч./с)",
            ax=self.ax
        )
        # self.cbar.set_ticks([i * 10000 for i in range(0, 270)])

    def draw_map(self):
        self.m = Basemap(
            projection='cyl', resolution='c',
            llcrnrlat=-90, urcrnrlat=90,
            llcrnrlon=-180, urcrnrlon=180
        )

        self.m.drawcoastlines(color=[0.5, 0.5, 0.5], zorder=0.5)
        self.m.drawmapboundary(fill_color=[1, 1, 1], zorder=0)

        # self.m.etopo(scale=0.5, alfa=0) #Another way of drawing
        # self.m.shadedrelief(scale=0.2)

        self.lats = self.m.drawparallels(np.arange(-180, 180, 30), labels=[1, 0, 0, 0])
        self.lons = self.m.drawmeridians(np.arange(-180, 180, 60), labels=[0, 0, 0, 1])

        """
        self.lat_lines = chain(*(tup[1][0] for tup in self.lats.items()))
        self.lon_lines = chain(*(tup[1][0] for tup in self.lons.items()))

        self.all_lines = chain(self.lat_lines, self.lon_lines)

        for line in self.all_lines:
            line.set(linestyle='-', alpha=1, color='black')
        """

    def draw_points(self, arr_x, arr_y, arr_rate):
        plt.scatter(arr_x, arr_y, c=self.norm(arr_rate), s=5, zorder=1, cmap=self.cmap)

    def save_plot(self):
        plt.savefig(f'plot_S{self.det}_R{self.idx_range}.png')


def test_map():
    det, idx_range = 1, 1

    arr_x = np.linspace(-180, 180, num=100)
    arr_y = np.linspace(-90, 90, num=100)

    arr_rate = np.linspace(0, 5000, num=100)

    pl = Plot(det, idx_range, 0, max(arr_rate))
    pl.draw_points(arr_x, arr_y, arr_rate)
    pl.save_plot()


def read_plot_data(det, idx_range, path_plot_data):
    with open(f'{path_plot_data}/plot_data_S{det}_R{idx_range}.txt') as f:
        lines = f.read().split('\n')
        lst_times_iso_rate = []
        for l in lines:
            lst = l.split()
            if len(lst) == 0:
                break
            lst_times_iso_rate.append([lst[0], float(lst[1]), float(lst[2]), float(lst[3])])

    return lst_times_iso_rate


def plot_data():
    path_plot_data = '../data/plot_data'

    det, idx_range = 2, 1

    lst_times_iso_rate = read_plot_data(det, idx_range, path_plot_data)

    arr_x = [r[2] for r in lst_times_iso_rate]
    arr_y = [r[3] for r in lst_times_iso_rate]
    # arr_rate  = [r[1] for r in lst_times_iso_rate]
    arr_rate = np.log10([r[1] for r in lst_times_iso_rate])

    pl = Plot(det, idx_range, min(arr_rate), max(arr_rate))
    pl.draw_points(arr_x, arr_y, arr_rate)
    pl.save_plot()


if __name__ == '__main__':
    # test_map()
    plot_data()