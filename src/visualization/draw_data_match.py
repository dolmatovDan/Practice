import sys
from matplotlib import pyplot as plt
import numpy as np

sys.path.append("..")
from utility import read_text_file


def parse_calculated_data(file_name):
    str_data = read_text_file(file_name)
    lst_data = [s.split() for s in str_data.split("\n") if len(s.split()) > 0]
    res_x = np.array([])
    res_y = np.array([])
    for data in lst_data:
        cur_time = float(data[0])
        cur_flux = float(data[1])
        res_x = np.append(res_x, [cur_time])
        res_y = np.append(res_y, [cur_flux])
    return res_x, res_y


def parse_measured_data(file_name):
    str_data = read_text_file(file_name)
    lst_data = [s.split() for s in str_data.split("\n")[3:] if len(s.split()) > 0]
    res_x = np.array([])
    res_y = np.array([])
    for data in lst_data:
        cur_time = float(data[0])
        cur_count_rate = float(data[1])
        res_x = np.append(res_x, [cur_time])
        res_y = np.append(res_y, [cur_count_rate])
    return res_x, res_y


def main():
    x = np.array([])
    measured_y = np.array([])
    calculated_y = np.array([])
    orbits = [15]
    # orbits = [4, 5, 6]
    for orbit in orbits:
        measured_data_path = (
            f"../../data/interim/orbits/orbit_20090312/20090312_{orbit:02d}.txt"
        )
        calculated_data_path = f"../../data/interim/calculated orbits/orbit_20090312/20090312_{orbit:02d}.txt"
        cur_x, cur_y = parse_measured_data(measured_data_path)
        x = np.append(x, cur_x)
        measured_y = np.append(measured_y, cur_y)

        cur_x, cur_y = parse_calculated_data(calculated_data_path)
        calculated_y = np.append(calculated_y, cur_y)
    plt.plot(x, measured_y + 1)
    plt.plot(x, calculated_y + 1)
    plt.semilogy()
    plt.show()


if __name__ == "__main__":
    main()
