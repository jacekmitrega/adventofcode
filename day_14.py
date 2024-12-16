def parse_input_text(input_text):
    robots = []
    for line in input_text.strip().splitlines():
        p, v = line.split(' ')
        px, py = map(int, p.split('=')[1].split(','))
        vx, vy = [int(s) for s in v.split('=')[1].split(',')]
        robots.append((px, py, vx, vy))
    return robots

def load_example_input():
    return parse_input_text("""
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""), 11, 7

def load_input():
    with open(f"input_{__file__.split('_')[-1].split('.')[0]}.txt", "r") as file:
        return parse_input_text(file.read()), 101, 103


def calculate1(robots, sx, sy):
    secs = 100
    tl = 0
    tr = 0
    bl = 0
    br = 0
    for i, (px, py, vx, vy) in enumerate(robots):
        robots[i] = ((px + secs*vx) % sx, (py + secs*vy) % sy, vx, vy)
    tl = sum(1 for x, y, _, _ in robots if x < sx//2 and y < sy//2)
    tr = sum(1 for x, y, _, _ in robots if x > sx//2 and y < sy//2)
    bl = sum(1 for x, y, _, _ in robots if x < sx//2 and y > sy//2)
    br = sum(1 for x, y, _, _ in robots if x > sx//2 and y > sy//2)
    return tl * tr * bl * br

def print_robots(robots, sx, sy):
    print()
    for y in range(sy):
        row = []
        for x in range(sx):
            if (x, y) in {(px, py) for px, py, _, _ in robots}:
                row.append('#')
            else:
                row.append('.')
        print(''.join(row))
    print()

def find_horizontal_line(robots, sx, sy):
    for y in range(sy):
        row = []
        robotset = {(px, py) for px, py, _, _ in robots}
        for x in range(sx):
            if (x, y) in robotset:
                row.append('#')
            else:
                row.append('.')
        printable_row = ''.join(row)
        if '###############################' in printable_row:
            return True
    return False

def calculate2(robots, sx, sy):
    secs = 0
    for _ in range(20000):
        secs += 1
        for i, (px, py, vx, vy) in enumerate(robots):
            robots[i] = ((px + vx) % sx, (py + vy) % sy, vx, vy)

        if find_horizontal_line(robots, sx, sy):
            print(secs)
            print_robots(robots, sx, sy)
            print(secs)
            return secs


def task1(input):
    return calculate1(*input)

def task2(input):
    return calculate2(*input)


print(task1(load_example_input()))  # 12
print(task1(load_input()))          # 218619120

task2(load_input())                 # 7055
