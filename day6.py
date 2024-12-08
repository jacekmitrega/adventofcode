#!/usr/bin/env python3
import itertools

def parse_input(input):
    grid = [[ch for ch in row_str] for row_str in input.strip().splitlines()]
    sx, sy = len(grid[0]), len(grid)
    x, y = next((x, y) for y in range(len(grid)) for x in range(len(grid[y])) if grid[y][x] == '^')
    return grid, sx, sy, x, y

directions = itertools.cycle([(0, -1), (1, 0), (0, 1), (-1, 0)])

def walk_the_grid(grid, sx, sy, x, y, idx=0, idy=-1):
    dx, dy = next(itertools.dropwhile(lambda d: d != (idx, idy), directions))
    positions = {}
    while True:
        if (position := (x, y, dx, dy)) in positions:
            return {(x, y, dx, dy): (x + dx, y + dy) for x, y, dx, dy in positions}, True
        positions[position] = position

        if not (0 <= (lx := x + dx) < sx and 0 <= (ly := y + dy) < sy):
            break  # looking to leave the map - end of the path
        elif grid[ly][lx] == '#':
            dx, dy = next(directions)  # looking at an obstacle - change direction
        else:
            x, y = lx, ly  # step forward
    return {(x, y, dx, dy): (x + dx, y + dy) for x, y, dx, dy in positions}, False

def task1(grid, sx, sy, x, y):
    positions, _ = walk_the_grid(grid, sx, sy, x, y)
    return len({(a, b) for a, b, _, _ in positions})

def task2(grid, sx, sy, ix, iy):
    positions, _ = walk_the_grid(grid, sx, sy, ix, iy)
    obstacle_positions = {}
    for pos, (lx, ly) in positions.items():
        if not (0 <= lx < sx and 0 <= ly < sy) or grid[ly][lx] in {'#', '^'}:
            continue
        obstacle_positions.setdefault((lx, ly), pos)  # rely on key insertion order

    new_obstacle_positions = set()
    for (lx, ly), (x, y, dx, dy) in obstacle_positions.items():
        orig_ch, grid[ly][lx] = grid[ly][lx], '#'
        positions, cycle_found = walk_the_grid(grid, sx, sy, x, y, dx, dy)
        if cycle_found:
            new_obstacle_positions.add((lx, ly))
        grid[ly][lx] = orig_ch

    return len(new_obstacle_positions)

example_input = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
example_parsed = parse_input(example_input)
assert 41 == task1(*example_parsed)
assert 6 == task2(*example_parsed)

with open('input6.txt', 'r') as file:
    input_text = file.read()
    parsed = parse_input(input_text)

print("task 1:", task1(*parsed))  # 5162
print("task 2:", task2(*parsed))  # 1909
