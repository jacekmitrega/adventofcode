import sys
sys.setrecursionlimit(5000)
import time


def input_grid(input_str):
    grid = [[char for char in line] for line in input_str.strip().splitlines()]
    sx, sy = len(grid[0]), len(grid)
    return grid, sx, sy


def parse_input_text(input_text):
    return input_grid(input_text)


def load_example_input():
    return parse_input_text("""
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
""")


def load_2nd_example_input():
    return parse_input_text("""
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
""")


def load_input():
    with open(f"input_{__file__.split('_')[-1].split('.')[0]}.txt", "r") as file:
        return parse_input_text(file.read())

directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
start_symbol, end_symbol, wall_symbol, path_symbol = "SE#."


def print_grid(path, visited, x, y, grid, sx, sy):
    import time
    print()
    for py, line in enumerate(grid):
        for px, char in enumerate(line):
            if (px, py) == (x, y):
                print('@', end='')
            elif char == 'E':
                if (px, py) in path:
                    print('!', end='')
                else:
                    print(char, end='')
            elif (px, py) in path:
                print('o', end='')
            elif (px, py) in visited:
                print(' ', end='')
            else:
                print(char, end='')
        print()
    time.sleep(1 / 20)


def min_path_and_score(paths, initial_dir):
    min_path = None
    min_score = float('inf')
    for p in paths:
        score = 0
        steps = list(zip(p, p[1:]))
        dir = initial_dir
        for (x1, y1), (x2, y2) in steps:
            dx = x2 - x1
            dy = y2 - y1
            dir_ch = directions.index(dir) - directions.index((dx, dy))
            if abs(dir_ch) in (1, 3):
                # 90 or -90 deg. turn
                score += 1000
            dir = dx, dy
            score += 1
        if score < min_score:
            min_score = score
            min_path = p
    return min_path, min_score


def find_path(path, visited, cache, x, y, dir, grid, sx, sy):
    # print_grid(path, visited, x, y, grid, sx, sy)

    if cached := cache.get((x, y, dir)):
        return cached

    paths = []
    for ndir in directions:
        dx, dy = ndir
        nx, ny = x + dx, y + dy
        if grid[ny][nx] == wall_symbol:
            continue  # don't run into walls
        elif (nx, ny) in visited:
            continue  # don't go back or run in circles
        elif grid[ny][nx] == end_symbol:
            # base case
            p_, s_ = min_path_and_score([path + [(nx, ny)]], (1, 0))
            print(s_)
            paths = [[(x, y), (nx, ny)]]
            break
        elif grid[ny][nx] == path_symbol:
            # recursive case
            min_path, min_score = find_path(path + [(nx, ny)], visited | {(nx, ny)}, cache, nx, ny, ndir, grid, sx, sy)
            if min_path:
                paths.append([(x, y)] + min_path)

    cache[(x, y, dir)] = min_path, min_score = min_path_and_score(paths, dir)
    return min_path, min_score


def calculate(grid, sx, sy):
    for start_y, line in enumerate(grid):
        if start_symbol in line:
            start_x = line.index(start_symbol)
            break

    min_path, min_score = find_path([(start_x, start_y)], {(start_x, start_y)}, {}, start_x, start_y, (1, 0), grid, sx, sy)
    # print_grid(min_path, set(), start_x, start_y, grid, sx, sy)

    return min_score


def task1(input):
    grid, sx, sy = input
    return calculate(grid, sx, sy)


if __name__ == "__main__":
    print(task1(load_example_input()))      # 7036
    print(task1(load_2nd_example_input()))  # 11048
    print(task1(load_input()))              # 122464 WRONG!!?!
