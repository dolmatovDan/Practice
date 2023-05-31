import numpy as np
from matplotlib import pyplot as plt
import os


def read_text_file(file):
    with open(file, "r") as f:
        return f.read()


def create_directory(name):
    if os.path.isdir(name):
        print(f"Directory {name} already exists")
    else:
        path = "./" + name
        os.mkdir(path)


def get_directory_size(dir_name):
    return len(
        [
            name
            for name in os.listdir(dir_name)
            if os.path.isfile(os.path.join(dir_name, name))
        ]
    )


def get_trendline(x, y):
    equation = np.polyfit(x, y, 1)
    trendline = np.poly1d(equation)
    return trendline


def parse_data(file_data):
    str_data = read_text_file(file_data)
    lst_data = [s for s in str_data.split("\n") if len(s.split()) > 0]
    x = []
    y = []
    for data in lst_data[3:]:
        data = list(map(float, data.split()))
        y.append(sum(data[1:5]))
        x.append(data[0])
    return x, y


def get_good_points(arr_x, arr_y):
    df = []
    for x, y in zip(arr_x, arr_y):
        df.append([x, y])
    df.sort(key=lambda x: x[1])

    lower_bound = int(len(arr_x) * 0.4)
    upper_bound = int(len(arr_x) * 0.5)
    definitely_good_points = df[lower_bound:upper_bound]
    good_x, good_y = zip(*definitely_good_points)

    trendline = get_trendline(good_x, good_y)

    is_good = [False] * len(arr_x)

    for index, (x, y) in enumerate(zip(arr_x, arr_y)):
        dif = abs(trendline(x) - y)
        if dif / trendline(x) < 0.5:
            is_good[index] = True

    return is_good, trendline


def main():
    mean_range = 0
    for day in range(1, 32):
        res = 0
        create_directory(f"../../reports/figures/test/200903{day:02d}")
        for index in range(
            get_directory_size(f"../../data/interim/orbits/orbit_200903{day:02d}")
        ):
            cnt_points = 0
            cnt_good = 0
            x, y = parse_data(
                f"../../data/interim/orbits/orbit_200903{day:02d}/200903{day:02d}_{index:02d}.txt"
            )
            x = np.array(x)
            y = np.array(y)
            good_points, trendline = get_good_points(x, y)
            for xx in good_points:
                if xx:
                    cnt_good += 1
                cnt_points += 1
            res += cnt_good / cnt_points
            colors = []
            for i in range(len(good_points)):
                if good_points[i]:
                    colors.append("lightgreen")
                else:
                    colors.append("blue")

            fig, ax = plt.subplots()
            ax.scatter(x, y, c=colors, s=1)
            ax.plot(x, trendline(x), "r", linewidth=0.5)

            fig.savefig(
                f"../../reports/figures/test/200903{day:02d}/200903{day:02d}_{index:02d}.png"
            )
            plt.close(fig)

        mean_range += res / get_directory_size(
            f"../../data/interim/orbits/orbit_200903{day:02d}"
        )
    print(mean_range / 31)


if __name__ == "__main__":
    main()
