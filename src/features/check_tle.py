import sys
import numpy as np
from skyfield.api import load, EarthSatellite

sys.path.append("..")
from utility import MONTH, YEAR, get_month_range


def read_tle():
    with open("../../data/raw/tle.txt") as f:
        return f.read()


def get_time(sat):
    ts = load.timescale()
    cur_date = sat.epoch.utc_jpl().split()
    cur_time = list(map(float, cur_date[2].split(":")))
    cur_day = cur_date[1].split("-")
    res_arr = [
        int(cur_day[0]),
        MONTH,
        int(cur_day[2]),
        cur_time[0],
        cur_time[1],
        cur_time[2],
    ]
    return ts.utc(*res_arr)


def get_sat():
    str_tle = read_tle()
    lst_lines = [s.strip() for s in str_tle.split("\n") if len(s.strip()) > 0]

    lst_tle = [(l1, l2) for l1, l2 in zip(lst_lines[:-1:2], lst_lines[1::2])]

    lst_sat = []

    month_range = get_month_range(MONTH, YEAR)
    month_day_min = month_range[0]
    month_day_max = month_range[1]
    for tle in lst_tle:
        day = float(tle[0].split()[3][2:])
        if day >= month_day_min and day <= month_day_max:
            lst_sat.append(
                (EarthSatellite(tle[0], tle[1], "KORONAS-FOTON"), tle[0], tle[1])
            )

    return lst_sat


def main():
    lst_sat = get_sat()
    cnt_bad = 0
    with open("../../data/interim/actual_tle.txt", "w") as actual_tle:
        print(
            lst_sat[0][1], lst_sat[0][2], file=actual_tle, sep="\n"
        )  # this tle is fine
        for i in range(1, len(lst_sat) - 1):
            cur_sat = lst_sat[i][0]
            prev_sat = lst_sat[i - 1][0]
            next_sat = lst_sat[i + 1][0]

            cur_time = get_time(cur_sat)

            geocentric1 = prev_sat.at(cur_time)
            geocentric2 = cur_sat.at(cur_time)
            geocentric3 = next_sat.at(cur_time)

            r1 = np.array(geocentric1.position.km)
            r2 = np.array(geocentric2.position.km)
            r3 = np.array(geocentric3.position.km)

            dR12 = np.sum((r1 - r2) ** 2) ** 0.5
            dR32 = np.sum((r3 - r2) ** 2) ** 0.5

            error_value = 1000
            if dR12 < error_value or dR32 < error_value:
                # tle is fine
                print(lst_sat[i][1], lst_sat[i][2], file=actual_tle, sep="\n")
            else:
                """
                2009-Mar-02 15:49:41.7772 UTC
                2009-Mar-10 15:15:40.5988 UTC

                Bad tle!
                """
                cnt_bad += 1
        print(
            lst_sat[-1][1], lst_sat[-1][2], file=actual_tle, sep="\n"
        )  # this tle is fine
    # print(cnt_bad)


if __name__ == "__main__":
    main()
