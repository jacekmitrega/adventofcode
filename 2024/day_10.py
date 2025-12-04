"""
>>> task1(load_example_input())
36

>>> task1(load_input())
593

>>> task2(load_example_input())
81

>>> task2(load_input())
1192

"""

import functools


def parse_input_str(input_str):
    return input_str.strip()

@functools.cache
def load_example_input():
    return parse_input_str("""
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""")

@functools.cache
def load_input():
    with open(f'input_{__file__.split('_')[-1].split('.')[0]}.txt', 'r') as file:
        return parse_input_str(file.read())

@functools.cache
def input_grid(input_str, cell_type=str):
    grid = [[cell_type(char) for char in line] for line in input_str.strip().splitlines()]
    sx, sy = len(grid[0]), len(grid)
    return grid, sx, sy

def descent(grid, scoring_grid, sx, sy, peak, x, y):
    scoring_grid[y][x][0].add(peak)
    scoring_grid[y][x][1] += 1
    valid_steps = [
        (x+dx, y+dy)
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0))
        if (
            (0 <= x+dx < sx) and (0 <= y+dy < sy)
            and grid[y+dy][x+dx] == grid[y][x] - 1
        )
    ]
    for nx, ny in valid_steps:
        descent(grid, scoring_grid, sx, sy, peak, nx, ny)

def get_scoring_grid(grid, sx, sy):
    peaks = [(x, y) for x in range(sx) for y in range(sy) if grid[y][x] == 9]
    scoring_grid = [[[set(), 0] for x in range(sx)] for _ in range(sy)]
    for peak in peaks:
        descent(grid, scoring_grid, sx, sy, peak, *peak)
    return scoring_grid

def task1(input_str):
    grid, sx, sy = input_grid(input_str, int)
    scoring_grid = get_scoring_grid(grid, sx, sy)
    trailheads = [(x, y) for x in range(sx) for y in range(sy) if grid[y][x] == 0]
    return sum(len(scoring_grid[y][x][0]) for x, y in trailheads)

def task2(input_str):
    grid, sx, sy = input_grid(input_str, int)
    scoring_grid = get_scoring_grid(grid, sx, sy)
    trailheads = [(x, y) for x in range(sx) for y in range(sy) if grid[y][x] == 0]
    return sum(scoring_grid[y][x][1] for x, y in trailheads)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
