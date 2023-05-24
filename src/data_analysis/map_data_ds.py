import sys
import time
import datetime

import numpy as np

from skyfield.api import load, utc, EarthSatellite

from src.visualization.draw_map import Plot


def sod_to_hhmmss(seconds):
    if seconds < 0 or seconds > 86400:
        print(f'Incorrect {seconds=}')
        sys.exit()

    hours = int(seconds / 3600)
    seconds -= 3600.0 * hours
    minutes = int(seconds / 60.0)
    seconds -= int(60.0 * minutes)

    return "{:02d}:{:02d}:{:06.3f}".format(hours, minutes, seconds)


class TLE:
    """
    TLE manipulation using EarthSatellite class from skyfield
    https://rhodesmill.org/skyfield/earth-satellites.html
    """

    def __init__(self, tle_file):
        self.tle_file = tle_file
        self.lst_sat, self.lst_epoch = self.read_tle(tle_file)

    def read_text_file(self, file_name):
        with open(file_name) as f:
            return f.read()

    def read_tle(self, file_name):
        str_tle = self.read_text_file(file_name)
        lst_lines = [s.strip() for s in str_tle.split('\n') if len(s.strip()) > 0]

        lst_tle = [(l1, l2) for l1, l2 in zip(lst_lines[:-1:2], lst_lines[1::2])]

        lst_sat = []
        lst_epoch = []
        for tle in lst_tle:
            sat = EarthSatellite(tle[0], tle[1], 'KORONAS-FOTON')
            lst_sat.append(sat)
            lst_epoch.append(sat.epoch)

        return lst_sat, lst_epoch

    def get_nearest_time(self, time_ts, lst_ts):
        """
        https://stackoverflow.com/questions/9706041/
            finding-index-of-an-item-closest-to-the-value-in-a-list-thats-not-entirely-sort
        """

        idx, val = min(enumerate(lst_ts), key=lambda x: abs(x[1] - time_ts))
        return idx, val

    def get_geo_pos(self, time_ts):
        """
        time_ts = ts.utc(2014, 1, 23, 11, 18, 7)
        """

        idx, t_epoch = self.get_nearest_time(time_ts, self.lst_epoch)

        days_from_epoch = time_ts - t_epoch
        # print('{:.3f} days away from epoch'.format(days_from_epoch))

        geoposition = self.lst_sat[idx].at(time_ts)

        cur_long = geoposition.subpoint().longitude.radians * 180 / np.pi
        cur_lat = geoposition.subpoint().latitude.radians * 180 / np.pi

        return cur_long, cur_lat, days_from_epoch


class KRF_BgTH:
    n_channels_1 = 12
    n_channels_2 = 12

    dt_res_1 = 1  # seconds
    dt_res_2 = 4  # seconds

    def __init__(self, path, date_start_ts, date_end_ts):

        # start and end dates; only year, mont, day fields are used
        self.t_i = date_start_ts.utc_datetime()
        self.t_f = date_end_ts.utc_datetime()

        self.lst_det_names = ['S1', 'S2']
        # self.lst_range_names = ['1', '2']

        # self.lst_det_names = ['S2',]
        self.lst_range_names = ['2', ]

        self.dic_count_data = {}

        for date in self.daterange(self.t_i, self.t_f):

            str_date = date.strftime('%Y%m%d')
            print(f'Reading task_data for {str_date}')
            for det in self.lst_det_names:
                for idx_range in self.lst_range_names:
                    self.dic_count_data[(str_date, det, idx_range)] = \
                        np.loadtxt(f'{path}/krf{str_date}_{idx_range}_{det}_bg.thr')

    def align_data(self):

        lst_dates = [s for s in self.daterange(self.t_i, self.t_f)]
        print('Size of lst_dates: ', len(lst_dates))

        if len(lst_dates) == 1:
            self.remove_negative_times(lst_dates[0])

        for i in range(len(lst_dates) - 1):

            str_date_cur = lst_dates[i].strftime('%Y%m%d')
            str_date_next = lst_dates[i + 1].strftime('%Y%m%d')

            for det in self.lst_det_names:
                for idx_range in self.lst_range_names:

                    data_cur = self.dic_count_data[(str_date_cur, det, idx_range)]
                    data_next = self.dic_count_data[(str_date_next, det, idx_range)]

                    # remove negative times form the first task_data set
                    if i == 0:
                        arr_bool = data_cur[:, 0] > - np.finfo(float).eps
                        data_cur = data_cur[arr_bool, :]

                    # append current task_data with negative time bins form the next task_data set
                    arr_bool = data_next[:, 0] < 0
                    data_cur_ = data_next[arr_bool, :]
                    data_cur_[:, 0] += 86400
                    data_cur_[:, 1] += 86400
                    data_cur = np.vstack([data_cur, data_cur_])

                    # remove negative times for the next task_data set
                    data_next = data_next[np.logical_not(arr_bool), :]

                    self.dic_count_data[(str_date_cur, det, idx_range)] = data_cur
                    self.dic_count_data[(str_date_next, det, idx_range)] = data_next

    def remove_negative_times(self, date_time):

        str_date = date_time.strftime('%Y%m%d')

        for det in self.lst_det_names:
            for idx_range in self.lst_range_names:
                data = self.dic_count_data[(str_date, det, idx_range)]
                arr_bool = data[:, 0] > - np.finfo(float).eps
                data = data[arr_bool, :]
                self.dic_count_data[(str_date, det, idx_range)] = data

    def daterange(self, start_date, end_date):

        for n in range(int((end_date - start_date).days + 1)):
            yield start_date + datetime.timedelta(n)

    def reduce_data(self, n_skip):
        """
        Leave only n_skip-th point in the task_data set
        """

        for date in self.daterange(self.t_i, self.t_f):
            str_date = date.strftime('%Y%m%d')
            for det in self.lst_det_names:
                for idx_range in self.lst_range_names:
                    data = self.dic_count_data[(str_date, det, idx_range)]
                    self.dic_count_data[(str_date, det, idx_range)] = data[::n_skip, :]

    def rebin_data(self, n_seconds):
        """
        Rebin task_data to n_seconds resolution
        n_seconds must be integer and divisible by the original resolution. 1 or 4 s
        """

        if n_seconds < self.dt_res_2:
            print(f'Cannot average range 2 on {n_seconds} s timescale')
            sys.exit()

        for date in self.daterange(self.t_i, self.t_f):
            str_date = date.strftime('%Y%m%d')
            for det in self.lst_det_names:
                for idx_range in self.lst_range_names:
                    print(f'Rebinning {str_date} {det} range {idx_range}')
                    data = self.dic_count_data[(str_date, det, idx_range)]

                    n_sum = n_seconds // int(data[0, 1] - data[0, 0])
                    n_bins = data.shape[0] // n_sum

                    print(f'{data.shape=}')
                    print(f'{n_bins=}')
                    print(f'{n_sum=}')

                    # print(task_data[:n_bins*n_sum,2:].reshape(n_bins, n_sum,-1)[:5,:])

                    arr_counts = data[:n_bins * n_sum, 2:].reshape(n_bins, n_sum, -1).mean(axis=1)
                    arr_start_times = data[:n_bins * n_sum:n_sum, 0]
                    # arr_end_times = task_data[n_sum:(n_bins+1)*n_sum+1:n_sum,0]
                    arr_end_times = data[n_sum - 1:(n_bins + 1) * n_sum:n_sum, 1]

                    print(data[:21, :2])
                    print(arr_start_times[:5])
                    print(arr_end_times[:5])
                    print(arr_counts[:5, :])

                    print(arr_start_times.shape)
                    print(arr_end_times.shape)
                    print(arr_counts.shape)
                    # sys.exit()

                    data_ = np.concatenate((
                        arr_start_times.reshape((arr_start_times.size, -1)),
                        arr_end_times.reshape((arr_end_times.size, -1)),
                        arr_counts), axis=1)

                    # print(data_[:5])
                    # sys.exit()

                    self.dic_count_data[(str_date, det, idx_range)] = data_

    def write_thr(self, data, file_name):

        print(f'Writing task_data {data.shape} to {file_name}')

        str_out = ''
        for i in range(data.shape[0]):
            str_out += '{:10.3f} {:10.3f} '.format(data[i, 0], data[i, 1])
            for j in range(data.shape[1] - 2):
                str_out += '{:5.0f} '.format(data[i, j + 2])
                # str_out += '{:9.3f} '.format(task_data[i,j+2])
            str_out += '\n'

        with open(file_name, 'w') as f:
            f.write(str_out)

    def write_data(self, path_out, str_sfx):

        for date in self.daterange(self.t_i, self.t_f):
            str_date = date.strftime('%Y%m%d')
            for det in self.lst_det_names:
                for idx_range in self.lst_range_names:
                    self.write_thr(self.dic_count_data[(str_date, det, idx_range)],
                                   f'{path_out}/krf{str_date}_{idx_range}_{det}_bg_{str_sfx}.thr')

    def get_count_rate(self, det, idx_range):

        lst_rate = []
        for date in self.daterange(self.t_i, self.t_f):
            str_date = date.strftime('%Y%m%d')
            str_date_dash = date.strftime('%Y-%m-%d')
            data = self.dic_count_data[(str_date, det, idx_range)]
            res = data[0, 1] - data[0, 0]

            lst_ = [['{:s}T{:s}'.format(str_date_dash, sod_to_hhmmss(t + res / 2)), arr_cnt.sum() / res] \
                    for t, arr_cnt in zip(data[:, 0], data[:, 2:])]
            lst_rate += lst_

        return lst_rate


def append_pos(lst_times_iso_rate, tle_data):
    ts = load.timescale()
    lst_out = []
    for rec in lst_times_iso_rate:
        d = datetime.datetime.strptime(rec[0], '%Y-%m-%dT%H:%M:%S.%f')
        d = d.replace(tzinfo=utc)
        time_ts = ts.from_datetime(d)
        geo_long, geo_lat, days_from_epoch = tle_data.get_geo_pos(time_ts)
        lst_out.append(rec + [geo_long, geo_lat, days_from_epoch])

    return lst_out


def make_plot(lst_times_iso_rate, det, idx_range):
    arr_x = [r[2] for r in lst_times_iso_rate]
    arr_y = [r[3] for r in lst_times_iso_rate]
    # arr_rate  = [r[1] for r in lst_times_iso_rate]
    arr_rate = np.log10([r[1] for r in lst_times_iso_rate])

    pl = Plot(det, idx_range, min(arr_rate), max(arr_rate))
    pl.draw_points(arr_x, arr_y, arr_rate)
    pl.save_plot()


def write_plot_data(lst_times_iso_rate, det, idx_range, path_plot_data):
    with open(f'{path_plot_data}/plot_data_S{det}_R{idx_range}.txt', 'w') as f:
        for i in range(len(lst_times_iso_rate)):
            f.write('{:s} {:10.3f} {:+10.3f} {:+10.3f}\n'.format(
                lst_times_iso_rate[i][0], lst_times_iso_rate[i][1], lst_times_iso_rate[i][2], lst_times_iso_rate[i][3]))


def main():
    path_data = '../data/task_data'
    path_data_aligned = './data_aligned'
    path_plot_data = '../data/plot_data'
    tle_file = '../data/tle/actual_tle.txt'

    ts = load.timescale()

    t_i = ts.utc(2009, 3, 1)
    t_f = ts.utc(2009, 3, 30)
    krf_data = KRF_BgTH(path_data, t_i, t_f)
    krf_data.align_data()

    str_sfx = 'al'
    # krf_data.write_data(path_data_aligned, str_sfx)

    # krf_data.reduce_data(10)
    n_seconds = 16
    krf_data.rebin_data(n_seconds)

    str_sfx = f'al_rb_{n_seconds}s'
    # krf_data.write_data(path_data_aligned, str_sfx)

    for det in [1, 2]:
        for idx_range in [2, ]:
            lst_times_iso_rate = krf_data.get_count_rate(f'S{det}', f'{idx_range}')

            tle_data = TLE(tle_file)

            lst_times_iso_rate = append_pos(lst_times_iso_rate, tle_data)
            # for r in lst_times_iso_rate:
            #    print(r)

            write_plot_data(lst_times_iso_rate, det, idx_range, path_plot_data)

            # make_plot(lst_times_iso_rate, det, idx_range)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("Total execution time: ")
    print("--- {:.3f} seconds ---".format(time.time() - start_time))
