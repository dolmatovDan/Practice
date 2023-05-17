import matplotlib.pyplot as plt
import numpy as np
import bisect
import os


def read_text_file(file_name):
    with open(file_name) as f:
        return f.read()


def parse_data(file_name):
    str_data = read_text_file(file_name)
    lst_data = [s.split() for s in str_data.split('\n') if len(s.split()) > 0]

    time_range = lst_data[0]
    time_range_duration = lst_data[1]
    long_range = lst_data[2]

    lst_lat = []
    lst_time = []
    lst_count_rate = []
    
    for i in range(3, len(lst_data)):
        cur_data = lst_data[i]
        cur_count_rate = list(map(float, cur_data[1:-2]))
        cur_second = float(cur_data[0])
        cur_lat = float(cur_data[-2])

        lst_lat.append(cur_lat)
        lst_time.append(cur_second)
        lst_count_rate.append(cur_count_rate)
    
    return [time_range, time_range_duration, long_range, lst_time, lst_lat, [sum(a) for a in lst_count_rate]]


def plot_data(x1, x2, y, description):
    fig, ax1 = plt.subplots(figsize=(16, 9))
    ax1.plot(x1, y)
    ax2 = ax1.secondary_xaxis('top')
    
    ax1.set_xlim(np.arange(min(x1), max(x1), 100))
    ax1.set_ylim(np.arange(0, 100001, 10000))

    plt.show()



def main():
    # day = int(input())
    day = 12
    dir_plot_data = './orbit_20090312/'
    for index in range(1):
        plot_data_name = os.path.join(dir_plot_data, f'20090312_{index:02d}.txt')
        data = parse_data(plot_data_name)
        plot_data(data[3], data[4], data[5], data[0:3])


if __name__ == "__main__":
    main()
