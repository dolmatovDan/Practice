import ephem
import sys
import numpy as np
from skyfield.api import load, EarthSatellite


def read_tle(file_name):
    with open(file_name) as f:
        return f.read()


def get_time(sat):
    ts = load.timescale()
    cur_date = sat.epoch.utc_jpl().split()
    # print(cur_date)

    cur_time = list(map(float, cur_date[2].split(':')))
    cur_day = cur_date[1].split('-')
    res_arr = [int(cur_day[0]), 3, int(cur_day[2]), cur_time[0], cur_time[1], cur_time[2]]
    #                           ^ - month number

    return ts.utc(*res_arr)


def get_sat(file_name):
    str_tle = read_tle(file_name)
    lst_lines = [s.strip() for s in str_tle.split('\n') if len(s.strip()) > 0]

    lst_tle = [(l1, l2) for l1, l2 in zip(lst_lines[:-1:2], lst_lines[1::2])]

    lst_sat = []
    for tle in lst_tle:
        lst_sat.append(EarthSatellite(tle[0], tle[1], 'KORONAS-FOTON'))

    return lst_sat


def get_count_speed_in_day(file_name, sat, day):
    res = []
    with open(file_name, 'r') as data:
        prev_second = -2e15  # -INF
        for line in data:
            cur_second = float(line.split()[0])
            if cur_second - prev_second >= 10:
                cur_day = day
                cnt_second = 0
                ts = load.timescale()

                if cur_second < 0:
                    cur_day -= 1
                    cnt_second = 24 * 60 * 60 + cur_second
                else:
                    cnt_second = cur_second

                date = cur_day + cur_second / (24 * 60 * 60)
                time = ts.utc(2009, 3, date)
                # print(time.utc_strftime(), day, cur_second)

                geoposition = sat.at(time)

                cur_long = geoposition.subpoint().longitude.radians * 180 / np.pi
                cur_lat = geoposition.subpoint().latitude.radians * 180 / np.pi

                cur_count_speed = sum(list(map(float, line.split())))

                res.append([cur_long, cur_lat, cur_count_speed])

                prev_second = cur_second
    return res


def main():
    with open('actual_tle.txt', 'r') as actual_tle, \
            open('plot_data/plot_data_1_S1.txt', 'w') as plot_data_1_S1, \
            open('plot_data/plot_data_1_S2.txt', 'w') as plot_data_1_S2, \
            open('plot_data/plot_data_2_S1.txt', 'w') as plot_data_2_S1, \
            open('plot_data/plot_data_2_S2.txt', 'w') as plot_data_2_S2:

        lst_sat = get_sat('actual_tle.txt')
        prev_day = -1
        for sat in lst_sat:
            cur_day = int(get_time(sat).utc_jpl().split()[1].split('-')[-1])
            if cur_day == prev_day:
                continue
            str_day = str(cur_day)
            if len(str_day) == 1:
                str_day = '0' + str_day

            res = get_count_speed_in_day(f'./data/krf200903{str_day}_1_S1_bg.thr', sat, cur_day)
            for data in res:
                print(' '.join(map(str, data)), file=plot_data_1_S1)

            res = get_count_speed_in_day(f'./data/krf200903{str_day}_1_S2_bg.thr', sat, cur_day)
            for data in res:
                print(' '.join(map(str, data)), file=plot_data_1_S2)

            res = get_count_speed_in_day(f'./data/krf200903{str_day}_2_S1_bg.thr', sat, cur_day)
            for data in res:
                print(' '.join(map(str, data)), file=plot_data_2_S1)

            res = get_count_speed_in_day(f'./data/krf200903{str_day}_2_S2_bg.thr', sat, cur_day)
            for data in res:
                print(' '.join(map(str, data)), file=plot_data_2_S2)

            prev_day = cur_day
            print('ok', cur_day)


main()
