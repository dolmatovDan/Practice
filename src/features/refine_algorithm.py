import sys

sys.path.append("..")
from utility import read_text_file


def main():
    data_path = "../../data/interim/stable_data.txt"
    save_path = "../../data/interim/refined_stable_data.txt"
    str_data = read_text_file(data_path)
    lst_data = [
        list(map(float, s.split())) for s in str_data.split("\n") if len(s.split()) > 0
    ]
    Bx = 2
    By = 2
    addx = 90
    addy = 180
    totalx = 170
    totaly = 360
    grid = [[] for i in range(totalx // Bx + 5)]
    for i in range(totalx // By + 5):
        for j in range((totaly // By + 5)):
            grid[i].append([])
    cnt = 0
    for line in lst_data:
        cnt += 1
        lat = line[-2] + addx
        lon = line[-1] + addy
        grid[int(lat // Bx)][int(lon // By)].append(line)
    sm = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            sm += len(grid[i][j])

    df = []
    for i in range(len(grid)):
        # print(i)
        for j in range(len(grid[0])):
            sm += len(grid[i][j])
            cnt = [0, 0]
            for line in grid[i][j]:
                cnt[int(line[0])] += 1
            if sum(cnt) > 0 and cnt[0] / sum(cnt) < 0.7:
                for k in range(len(grid[i][j])):
                    grid[i][j][k][0] = 1
            for line in grid[i][j]:
                df.append(line)

    with open(save_path, "w") as save_file:
        for line in df:
            print(
                "{:10.3f}   {:10.3f}   {:10.3f}   {:10.3f}   {:10.3f}   {:10.3f}".format(
                    *line
                ),
                file=save_file,
            )


if __name__ == "__main__":
    main()
