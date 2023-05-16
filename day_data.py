import sys
from main_ds import TLE
from skyfield.api import load, utc, EarthSatellite
import numpy as np
import os


def sod_to_hhmmss(seconds):
    if seconds < 0 or seconds > 86400:
        print(f'Incorrect {seconds=}')
        sys.exit()

    hours = int(seconds / 3600)
    seconds -= 3600.0 * hours
    minutes = int(seconds / 60.0)
    seconds -= int(60.0 * minutes)

    return "{:02d}:{:02d}:{:06.3f}".format(hours, minutes, seconds)


def convert_hhmmss_to_date(date):
    return list(map(float, date.split(':')))


def read_text_file(file_name):
    with open(file_name) as f:
        return f.read()


def create_directory(name):
    if os.path.isdir(name):
        print(f'Directory {name} already exists')
    else:
        path = './' + name
        os.mkdir(path)

def get_day_count_rate(day, save_data, tle_file):
    cur_tle = TLE(tle_file)
    ts = load.timescale()
    count_rate_data = './task_data/krf200903{:02d}_1_S1_bg.thr'.format(day)

    with open(count_rate_data, "r") as rate_data, open(save_data, "w") as data:
        for line in rate_data:
            cur_data = list(map(float, line.split()))
            cur_second = cur_data[0]
            cur_count_rate = sum(cur_data[5:-2])
            if cur_second < 0:
                continue

            cur_hhmmss = convert_hhmmss_to_date(sod_to_hhmmss(cur_second))
            time_ts = ts.utc(2009, 3, day, *cur_hhmmss)

            cur_long, cur_lat, days_from_epoch = cur_tle.get_geo_pos(time_ts)
            print("{:06.3f}   {:06.3f}   {:06.3f}   {:06.3f}".format(
                cur_second, cur_count_rate, cur_lat, cur_long), file=data)


def split_day_count_rate(day_count_rate, date):
    str_count_rate = read_text_file(day_count_rate)
    lst_count_rate = [list(map(float, s.split())) for s in str_count_rate.split('\n') if len(s.split()) > 0]

    # for i in range(5):
    #     print(lst_count_rate[i])
    lst_orbit = [[]]

    for line in lst_count_rate:
        cur_lat = line[2]

        if len(lst_orbit[-1]) <= 1:
            lst_orbit[-1].append(line)
        else:
            if (lst_orbit[-1][-1][2] - lst_orbit[-1][-2][2]) * (cur_lat - lst_orbit[-1][-1][2]) > 0 or \
                    len(lst_orbit[-1]) <= 5:  # need this condition, because otherwise several points are lost
                # 3 - max count of zero derivative in a row (5 > 3)
                lst_orbit[-1].append(line)
            else:
                lst_orbit.append([line])

    # for i in range(len(orbit)):
    #     print(len(orbit[i]))
    # print(len(orbit))
    # print(sum([len(x) for x in orbit]))

    dir_name = f'orbit_{date}'
    create_directory(dir_name)

    for index, orbit in enumerate(lst_orbit):
        file_name = os.path.join(f'{dir_name}', f'{date}_{index:02d}')
        with open(file_name, 'w') as save_data:
            print('Time range: [ {start}  {end} ]'.format(start=sod_to_hhmmss(orbit[0][0]),
                                                          end=sod_to_hhmmss(orbit[-1][0])), file=save_data)
            cnt_sec = orbit[-1][0] - orbit[0][0]
            cnt_min = cnt_sec // 60
            cnt_sec -= 60 * cnt_min
            print(f'Time range duration: {cnt_min} min, {cnt_sec} sec', file=save_data)
            print('Longitude range: [ {start}  {end} ]'.format(start=min(orbit[0][3], orbit[-1][3]),
                                                               end=max(orbit[0][3], orbit[-1][3])), file=save_data)

            for line in orbit:
                cur_second = line[0]
                cur_count_rate = line[1]
                cur_lat = line[2]
                cur_long = line[3]
                print("{:06.3f}   {:06.3f}   {:06.3f}   {:06.3f}".format(cur_second, cur_count_rate, cur_lat, cur_long),
                      file=save_data)


def main():
    # day = int(input())
    day = 12
    save_data = './day_count_rate.txt'
    tle_file = './actual_tle.txt'

    get_day_count_rate(day, save_data, tle_file)
    split_day_count_rate(save_data, f'200903{day:02d}')


if __name__ == '__main__':
    main()
