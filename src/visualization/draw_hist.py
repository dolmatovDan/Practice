from matplotlib import pyplot as plt


def read_text_file(file):
    with open(file, "r") as f:
        return f.read()


def draw_hist(data, name):
    fig, ax = plt.subplots()
    ax.hist(data, bins=int(len(data) ** 0.5), density=True)
    fig.savefig(name)
    plt.close(fig)


def parse_day_data(file_name):
    str_data = read_text_file(file_name)
    lst_data = [
        list(map(float, s.split())) for s in str_data.split("\n") if len(s.split()) > 0
    ]
    lst_val = []
    for line in lst_data:
        lst_val.append(sum(line[1:4]))
    return lst_val


def parse_month_data(file_name):
    str_data = read_text_file(file_name)
    lst_data = [
        list(map(float, s.split())) for s in str_data.split("\n") if len(s.split()) > 0
    ]
    lst_val = []
    for line in lst_data:
        lst_val.append(sum(line[0:3]))
    return lst_val


def main():
    # for day in range(1, 32):
    #     file = f'./day_count_rates/count_rate_200903{day:02d}.txt'
    #     lst_count_rate = parse_day_data(file)
    # draw_hist(lst_count_rate, f'./day_hist/hist_200903{day:02d}.png')

    file = "../../data/interim/month_count_rate.txt"
    lst_count_rate = parse_month_data(file)
    draw_hist(lst_count_rate, "./month_hist.png")


if __name__ == "__main__":
    main()
