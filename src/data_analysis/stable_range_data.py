import os


def read_text_file(file_name):
    with open(file_name) as f:
        return f.read()
    
    
def create_directory(name):
    if os.path.isdir(name):
        print(f'Directory {name} already exists')
    else:
        path = './' + name
        os.mkdir(path)


def get_directory_size(dir_name):
    return len([name for name in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, name))])


def get_stable_file_count_rate_range(file_name):
    str_count_rate = read_text_file(file_name)
    lst_count_rate = [list(map(float, s.split())) for s in str_count_rate.split('\n')[3:] if len(s.split()) > 0]
    range_duration = len(lst_count_rate)

    good_lower_bound = 500
    good_upper_bound = 2000
    cnt_good_points = 0 # count_rate from good_lower_bound to good_upper_bound

    for line in lst_count_rate:
        cur_count_rate = sum(line[1:4])
        if cur_count_rate > good_lower_bound and cur_count_rate < good_upper_bound:
            cnt_good_points += 1
    return cnt_good_points / range_duration


def get_stable_day_count_rate_range(date):
    dir_name = f'orbit_{date}'
    dir_name = os.path.join('../data/orbits', dir_name)

    res = 0
    cnt_files = get_directory_size(dir_name)

    with open('../data/stable_range.txt', "w") as save_data:
        for index in range(cnt_files):
            file_name = f'{date}_{index:02d}.txt'
            file_name = os.path.join(dir_name, file_name)
            cur_range_duration = get_stable_file_count_rate_range(file_name)
            res += cur_range_duration

            # print(f'{index:02d}   {cur_range_duration:05.3f}', file=save_data)

    res /= cnt_files
    return res

def main():
    sum_stable_range = 0
    for day in range(1, 32):
        cur_date = f'200903{day:02d}'
        stable_day_count_rate_range = get_stable_day_count_rate_range(cur_date)
        sum_stable_range += stable_day_count_rate_range
        
    mean_stable_range = sum_stable_range / 31
    print(mean_stable_range)

if __name__ == '__main__':
    main()