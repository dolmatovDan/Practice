import os
import sys
import numpy as np
from matplotlib import pyplot as plt


sys.path.append("..")
from utility import (
    get_good_points,
    parse_data,
    read_text_file,
    create_folder,
    get_folder_size,
    YEAR,
    MONTH,
)


def main():
    for day in range(1, 2):
        date = f"{YEAR}{MONTH:02d}{day:02d}"
        create_folder(f"../../reports/figures/test/{date}")
        for index in range(get_folder_size(f"../../data/interim/orbits/orbit_{date}")):
            x, y = parse_data(
                f"../../data/interim/orbits/orbit_{date}/{date}_{index:02d}.txt"
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

            fig.savefig(f"../../reports/figures/test/{date}/{date}_{index:02d}.png")
            plt.close(fig)


if __name__ == "__main__":
    main()
