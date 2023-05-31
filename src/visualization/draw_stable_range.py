import os
import numpy as np
from matplotlib import pyplot as plt
from ..features.stable_range import get_good_points, parse_data


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


def main():
    for day in range(1, 2):
        create_directory(f"../../reports/figures/test/200903{day:02d}")
        for index in range(
            get_directory_size(f"../../data/interim/orbits/orbit_200903{day:02d}")
        ):
            x, y = parse_data(
                f"../../data/interim/orbits/orbit_200903{day:02d}/200903{day:02d}_{index:02d}.txt"
            )

            x = np.array(x)
            y = np.array(y)

            good_points, trendline = get_good_points(x, y)

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


if __name__ == "__main__":
    main()
