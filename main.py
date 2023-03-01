import ephem
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

class Item:
    def __init__(self, long: str, lat: str, day: int, count_speed1_up: int = 0, count_speed1_down: int = 0,
                 count_speed2_up: int = 0, count_speed2_down: int = 0):
        self.long = long
        self.lat = lat
        self.day = day
        self.count_speed1_up = count_speed1_up
        self.count_speed1_up = count_speed1_down
        self.count_speed2_up = count_speed2_up
        self.count_speed2_up = count_speed2_down

    def print_values(self):
        print(f"long: {self.long}")
        print(f"lat: {self.lat}")
        print(f"day: {self.day}")
        print(f"count_speed1_up: {self.count_speed1_up}")
        print(f"count_speed1_down: {self.count_speed1_down}")
        print(f"count_speed2_up: {self.count_speed2_up}")
        print(f"count_speed2_down: {self.count_speed2_down}")

def get_count_speed(file_name: str, second: int) -> int:
    result = 0
    with open(file_name, "r") as data:
        content = data.readlines()
        start = float(content[0].split()[0])
        end = float(content[-1].split()[0]) - start
        # if end < second:
        #     print("ERROR", start, end, second, file_name) # ther're some erros!!!!!!!
        left = -1
        right = len(content) - 1
        while right > left + 1:
            mid = (left + right) // 2
            if float(content[mid].split()[0]) - start >= second:
                right = mid
            else:
                left = mid
        pos = right
        energy_window = list(map(int, content[pos].split()[2:]))
        result = sum(energy_window)
    return result

df = dict()
with open('tle.txt', "r") as TLE:
    line1 = "ISS (ZARYA)"
    cnt = 0
    for line2 in TLE:
        line3 = TLE.readline()
        day = float(line2.split()[3][2:])
        if day >= 60 and day <= 91:
            second = int((day - int(day)) * 24 * 60 * 60)
            iss = ephem.readtle(line1, line2, line3)
            iss.compute(f'2009/3/{int(day)}')
            cords = ('%s %s' % (iss.sublong, iss.sublat)).split()
            df[second] = Item(cords[0], cords[1], int(day) - 59)

for second, it in df.items():
    cur_day = str(it.day)
    if len(cur_day) == 1:
        cur_day = '0' + cur_day
    name1_up = f'data\\krf200903{cur_day}_1_S1_bg.thr'
    name1_down = f'data\\krf200903{cur_day}_1_S2_bg.thr'

    name2_up = f'data\\krf200903{cur_day}_2_S1_bg.thr'
    name2_down = f'data\\krf200903{cur_day}_2_S2_bg.thr'

    it.count_speed1_up = get_count_speed(name1_up, second)
    it.count_speed1_down = get_count_speed(name1_down, second)

    it.count_speed2_up = get_count_speed(name2_up, second)
    it.count_speed2_down = get_count_speed(name2_down, second)


# debug
# cnt = 0
# for key, val in df.items():
#     print(f"key: {key}")
#     val.print_values()
#     print("________________")

fig = plt.figure()
ax = plt.axes(projection='3d')
xline = []
yline = []
zline = []
for key, val in df.items():
    xline.append(int(val.long[:val.long.find(':')]))
    yline.append(int(val.lat[:val.lat.find(':')]))
    zline.append(val.count_speed1_down + val.count_speed1_up + val.count_speed2_down + val.count_speed2_up)

ax.scatter3D(xline, yline, zline, 'gray')
plt.show()
