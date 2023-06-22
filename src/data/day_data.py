import sys
from map_data_ds import TLE
from map_data_ds import sod_to_hhmmss
from skyfield.api import load
import os

sys.path.append("..")
from utility import read_text_file, create_folder, YEAR, MONTH


def convert_hhmmss_to_date(date):
    return list(map(float, date.split(":")))


def get_day_count_rate(day, save_data, tle_file):
    ts = load.timescale()
    cur_tle = TLE(tle_file)
    count_rate_data = f"../../data/raw/task_data/krf200903{day:02d}_1_S1_bg.thr"

    with open(count_rate_data, "r") as rate_data, open(save_data, "w") as data:
        for line in rate_data:
            cur_data = list(map(float, line.split()))
            cur_second = cur_data[0]
            cur_count_rate_25_100 = sum(cur_data[5:8])
            cur_count_rate_100_400 = sum(cur_data[8:11])
            cur_count_rate_400_640 = sum(cur_data[11:-2])
            cur_count_rate = sum(cur_data[5:-2])
            if cur_second < 0:
                continue

            cur_hhmmss = convert_hhmmss_to_date(sod_to_hhmmss(cur_second))
            time_ts = ts.utc(YEAR, MONTH, day, *cur_hhmmss)

            cur_long, cur_lat, days_from_epoch = cur_tle.get_geo_pos(time_ts)
            print(
                "{:06.3f}   {:06.3f}   {:06.3f}   {:06.3f}".format(
                    cur_second,
                    cur_count_rate,
                    cur_lat,
                    cur_long,
                ),
                file=data,
            )

            # print("{:06.3f}   {:06.3f}   {:06.3f}   {:06.3f}".format(
            #     cur_second, cur_count_rate, cur_lat, cur_long), file=data)


def split_day_count_rate(day_count_rate, date):
    str_count_rate = read_text_file(day_count_rate)
    lst_count_rate = [
        list(map(float, s.split()))
        for s in str_count_rate.split("\n")
        if len(s.split()) > 0
    ]

    # for i in range(5):
    #     print(lst_count_rate[i])
    lst_orbit = [[]]

    for line in lst_count_rate:
        cur_lat = line[-2]

        if len(lst_orbit[-1]) <= 1:
            lst_orbit[-1].append(line)
        else:
            prev_lat_delta = lst_orbit[-1][-1][-2] - lst_orbit[-1][-2][-2]
            cur_lat_delta = cur_lat - lst_orbit[-1][-1][-2]
            if (prev_lat_delta) * (cur_lat_delta) > 0 or len(
                lst_orbit[-1]
            ) <= 5:  # need this condition, because otherwise several points are lost
                # 3 - max count of zero derivative in a row (5 > 3)
                lst_orbit[-1].append(line)
            else:
                lst_orbit.append([line])

    # for i in range(len(lst_orbit)):
    #     print(len(lst_orbit[i]))
    # print(len(lst_orbit))
    # print(sum([len(x) for x in lst_orbit]))

    folder_name = f"orbit_{date}"
    folder_name = os.path.join("../../data/interim/orbits", folder_name)
    create_folder(folder_name)

    for index, orbit in enumerate(lst_orbit):
        file_name = os.path.join(f"{folder_name}", f"{date}_{index:02d}.txt")
        with open(file_name, "w") as save_data:
            print(
                "Time range: [ {start}  {end} ]".format(
                    start=sod_to_hhmmss(orbit[0][0]), end=sod_to_hhmmss(orbit[-1][0])
                ),
                file=save_data,
            )
            cnt_sec = orbit[-1][0] - orbit[0][0]
            cnt_min = cnt_sec // 60
            cnt_sec -= 60 * cnt_min
            print(f"Time range duration: {cnt_min} min, {cnt_sec} sec", file=save_data)
            print(
                "Longitude range: [ {start}  {end} ]".format(
                    start=min(orbit[0][3], orbit[-1][3]),
                    end=max(orbit[0][3], orbit[-1][3]),
                ),
                file=save_data,
            )

            for line in orbit:
                print(
                    "{:06.3f}   {:06.3f}   {:06.3f}   {:06.3f}".format(*line),
                    file=save_data,
                )


def get_ICRS_coordinates(day, data_file, tle_file, save_file):
    str_data = read_text_file(data_file)
    lst_data = [
        list(map(float, s.split()))
        for s in str_data.split("\n")[3:]
        if len(s.split()) > 0
    ]

    ts = load.timescale()
    cur_tle = TLE(tle_file)

    with open(save_file, "w") as save_data:
        for data in lst_data:
            cur_second = data[0]
            cur_hhmmss = convert_hhmmss_to_date(sod_to_hhmmss(cur_second))
            time_ts = ts.utc(YEAR, MONTH, day, *cur_hhmmss)
            ra, dec, distance = cur_tle.get_radec(time_ts)
            lat, long, days_from_epoch = cur_tle.get_geo_pos(time_ts)
            print(
                f"{cur_second}   {ra._degrees:.03f}   {dec._degrees:.03f}   {distance:.03f}",
                file=save_data,
            )


def main():
    save_data = "../../data/interim/day_count_rate.txt"
    tle_file = "../../data/interim/actual_tle.txt"

    day = 12
    date = f"{YEAR}{MONTH:02d}{day:02d}"
    orbit_num = 3
    get_ICRS_coordinates(
        day,
        f"../../data/interim/orbits/orbit_{date}/{date}_{orbit_num:02d}.txt",
        tle_file,
        f"../../data/interim/orbit_{date}_{orbit_num:02d}_data.txt",
    )
    # get_day_count_rate(day, save_data, tle_file)
    # split_day_count_rate(save_data, date)


if __name__ == "__main__":
    main()
