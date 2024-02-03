import sys
from map_data_ds import TLE
from map_data_ds import sod_to_hhmmss
from skyfield.api import load
import os
from radbelt import get_flux
from astropy import units as u
from astropy.coordinates import EarthLocation
from astropy.time import Time
from skyfield.api import Topos, load

sys.path.append("..")
from utility import read_text_file, create_folder, YEAR, MONTH, transform_date


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
            # cur_count_rate = sum(cur_data[5:-2])
            if cur_second < 0:
                continue

            cur_hhmmss = convert_hhmmss_to_date(sod_to_hhmmss(cur_second))
            time_ts = ts.utc(YEAR, MONTH, day, *cur_hhmmss)

            cur_long, cur_lat, days_from_epoch = cur_tle.get_geo_pos(time_ts)
            ra, dec, distance = cur_tle.get_radec(time_ts)
            print(
                "{:06.3f}   {:06.3f}   {:06.3f}   {:06.3f}   {:06.3f}   {:06.3f}   {:06.3f}".format(
                    cur_second,
                    cur_count_rate_25_100,
                    cur_count_rate_100_400,
                    cur_count_rate_400_640,
                    distance,
                    cur_lat,
                    cur_long,
                ),
                file=data,
            )

            # print(
            #     "{:06.3f}   {:06.3f}   {:06.3f}   {:06.3f}".format(
            #         cur_second, cur_count_rate, cur_lat, cur_long
            #     ),
            #     file=data,
            # )


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
                    start=min(orbit[0][-1], orbit[-1][-1]),
                    end=max(orbit[0][-1], orbit[-1][-1]),
                ),
                file=save_data,
            )
            columns = ["Time", "25-100", "100-400", "400-640", "R", "Lat", "Lon"]
            print(
                "{:>10}   {:>10}   {:>10}   {:>10}   {:>10}   {:>10}   {:>10}".format(
                    *columns
                ),
                file=save_data,
            )

            for line in orbit:
                print(
                    "{:10.3f}   {:10.3f}   {:10.3f}   {:10.3f}   {:10.3f}   {:10.3f}   {:10.3f}".format(
                        *line
                    ),
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


def calc_flux(latitude, longitude, elevation, date, earth_radius):
    surface_distance = (elevation - earth_radius) * u.km
    coords = EarthLocation(
        lon=longitude * u.deg, lat=latitude * u.deg, height=surface_distance
    )
    time = Time(transform_date(date))
    energy1 = 25 * u.keV
    res_flux = (get_flux(coords, time, energy1, "p", "max")) * 100
    return res_flux


def draw_belt(lat_lower_limit, lat_upper_limit, max_height, height_step, earth_radius):
    belt_geographical_points = []
    for lat in range(lat_lower_limit, lat_upper_limit):
        for radius in range(0, max_height, height_step):
            rightPart = [
                70,
                lat,
                radius + earth_radius,
                0,
                float(
                    str(
                        calc_flux(
                            lat, 70, radius + earth_radius, "20090312", earth_radius
                        )
                    ).split()[0]
                ),
            ]
            leftPart = [
                -70,
                lat,
                radius + earth_radius,
                0,
                float(
                    str(
                        calc_flux(
                            lat, -70, radius + earth_radius, "20090312", earth_radius
                        )
                    ).split()[0]
                ),
            ]
            belt_geographical_points.append(rightPart)
            belt_geographical_points.append(leftPart)
    with open("calc_data.txt", "w") as fout:
        for x in belt_geographical_points:
            print(*x, file=fout)


def main():
    save_data = "../../data/interim/day_count_rate.txt"
    tle_file = "../../data/interim/actual_tle.txt"

    # orbit_num = 3
    # get_ICRS_coordinates(
    #     day,
    #     f"../../data/interim/orbits/orbit_{date}/{date}_{orbit_num:02d}.txt",
    #     tle_file,
    #     f"../../data/interim/orbit_{date}_{orbit_num:02d}_data.txt",
    # )

    # for day in range(1, 32):
    #     print(day)
    #     date = f"{YEAR}{MONTH:02d}{day:02d}"
    #     get_day_count_rate(day, save_data, tle_file)
    #     split_day_count_rate(save_data, date)

    # draw_belt(-90, 90, 10000, 50, 6378)


if __name__ == "__main__":
    main()
