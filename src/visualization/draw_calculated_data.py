import sys
from matplotlib import pyplot as plt

sys.path.append("..")
from utility import read_text_file


def main():
    file_path = "../../data/interim/calculated orbits/orbit_20090312/20090312_03.txt"
    str_data = read_text_file(file_path)
    data = [
        list(map(float, s.split()[:2]))
        for s in str_data.split("\n")
        if len(s.split()) > 0
    ]
    x = [a[0] for a in data]
    y = [a[1] for a in data]
    plt.scatter(x, y, s=10)
    plt.show()


if __name__ == "__main__":
    main()
