import sys

sys.path.append("..")
from utility import get_folder_size, read_text_file, YEAR, MONTH


def day_find_orbit_by_value(channel_num, need_count_rate, date, error=0):
    folder_size = get_folder_size(f"../../data/interim/orbits/orbit_{date}")
    for index in range(folder_size):
        str_data = read_text_file(
            f"../../data/interim/orbits/orbit_{date}/{date}_{index:02d}.txt"
        )
        lst_data = [s.split() for s in str_data.split("\n") if len(s.split()) > 0][3:]
        lst_data = [list(map(float, s)) for s in lst_data]

        for data in lst_data:
            if abs(data[channel_num] - need_count_rate) <= error:
                return True, f"{date}_{index:02d}.txt"
    return False, ""


def find_orbit_by_value(channel_num, need_count_rate, error=0):
    for day in range(1, 32):
        find, name = day_find_orbit_by_value(
            channel_num, need_count_rate, f"{YEAR}{MONTH:02d}{day:02d}"
        )
        if find:
            return True, name
    return False, ""


def main():
    print(find_orbit_by_value(3, 63))
    print(find_orbit_by_value(3, 182))


if __name__ == "__main__":
    main()
