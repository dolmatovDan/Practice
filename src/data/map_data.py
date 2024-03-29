import os
import numpy as np
from skyfield.api import load, EarthSatellite


def read_tle(file_name):
    with open(file_name) as f:
        return f.read()


def get_time(sat):
    ts = load.timescale()
    cur_date = sat.epoch.utc_jpl().split()
    # print(cur_date)

    cur_time = list(map(float, cur_date[2].split(":")))
    cur_day = cur_date[1].split("-")
    res_arr = [
        int(cur_day[0]),
        3,
        int(cur_day[2]),
        cur_time[0],
        cur_time[1],
        cur_time[2],
    ]

    return ts.utc(*res_arr)


def get_sat(file_name):
    str_tle = read_tle(file_name)
    lst_lines = [s.strip() for s in str_tle.split("\n") if len(s.strip()) > 0]

    lst_tle = [(l1, l2) for l1, l2 in zip(lst_lines[:-1:2], lst_lines[1::2])]

    lst_sat = []
    for tle in lst_tle:
        lst_sat.append(EarthSatellite(tle[0], tle[1], "KORONAS-FOTON"))

    return lst_sat


def get_count_rate_in_day(file_name, sat, day):
    res = []
    ts = load.timescale()
    with open(file_name, "r") as data:
        prev_second = -2e15  # -INF
        for line in data:
            cur_second = float(line.split()[0])
            if cur_second - prev_second >= 10:
                cur_day = day
                cnt_second = 0

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

                cur_data = list(map(float, line.split()))
                cur_count_rate = sum(cur_data[5:-2])
                cur_count_rate_25_100 = sum(cur_data[5:8])
                cur_count_rate_100_400 = sum(cur_data[8:11])
                cur_count_rate_400_640 = sum(cur_data[11:-2])

                res.append(
                    [
                        sum(cur_data[2:]),
                        cur_lat,
                        cur_long,
                    ]
                )

                prev_second = cur_second
    return res


def main():
    with open(
        "../../data/interim/map_data/plot_data_1_S1.txt", "w"
    ) as plot_data_1_S1, open(
        "../../data/interim/map_data/plot_data_1_S2.txt", "w"
    ) as plot_data_1_S2, open(
        "../../data/interim/map_data/plot_data_2_S1.txt", "w"
    ) as plot_data_2_S1, open(
        "../../data/interim/map_data/plot_data_2_S2.txt", "w"
    ) as plot_data_2_S2:
        lst_sat = get_sat("../../data/interim/actual_tle.txt")
        prev_day = -1
        for sat in lst_sat:
            cur_day = int(get_time(sat).utc_jpl().split()[1].split("-")[-1])
            if cur_day == prev_day:
                continue
            str_day = str(cur_day)
            if len(str_day) == 1:
                str_day = "0" + str_day

            res = get_count_rate_in_day(
                f"../../data/raw/task_data/krf200903{str_day}_1_S1_bg.thr", sat, cur_day
            )
            for data in res:
                print(
                    "{:06.3f}   {:06.3f}   {:06.3f}".format(*data),
                    file=plot_data_1_S1,
                )

            res = get_count_rate_in_day(
                f"../../data/raw/task_data/krf200903{str_day}_1_S2_bg.thr", sat, cur_day
            )
            for data in res:
                print(
                    "{:06.3f}   {:06.3f}   {:06.3f}".format(*data),
                    file=plot_data_1_S2,
                )

            res = get_count_rate_in_day(
                f"../../data/raw/task_data/krf200903{str_day}_2_S1_bg.thr", sat, cur_day
            )
            for data in res:
                print(
                    "{:06.3f}   {:06.3f}   {:06.3f}".format(*data),
                    file=plot_data_2_S1,
                )

            res = get_count_rate_in_day(
                f"../../data/raw/task_data/krf200903{str_day}_2_S2_bg.thr", sat, cur_day
            )
            for data in res:
                print(
                    "{:06.3f}   {:06.3f}   {:06.3f}".format(*data),
                    file=plot_data_2_S2,
                )

            prev_day = cur_day
            print("ok", cur_day)


if __name__ == "__main__":
    main()
