"""
>>> task1(load_example_input())
14

>>> task1(load_input())
244

>>> task2(load_example_input())
34

>>> task2(load_input())
912

"""

import functools
import itertools


def parse_input_text(input_text):
    return [list(line) for line in input_text.strip().splitlines()]  # grid of chars

@functools.cache
def load_example_input():
    return parse_input_text("""
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""")

@functools.cache
def load_input():
    with open(f'input_{__file__.split('_')[-1].split('.')[0]}.txt', 'r') as file:
        return parse_input_text(file.read())


def calculate(grid, task2=False):
    antinodes = [list(line) for line in grid]
    sx, sy = len(grid[0]), len(grid)
    freqs = {}
    for x, y in itertools.product(range(sx), range(sy)):
        if (ch := grid[y][x]) == '.':
            continue
        freqs.setdefault(ch, []).append((x, y))
    for coords in freqs.values():
        for (x1, y1), (x2, y2) in itertools.combinations(coords, 2):
            dx = x1 - x2
            dy = y1 - y2
            if dx == dy == 0:
                break
            if task2:
                ax1, ay1 = x1, y1
                ax2, ay2 = x1, y1
                antinodes[ay1][ax1] = '#'
                updates = 1
                while updates:
                    updates = 0
                    if 0 <= ( ax1 := ax1 + dx ) < sx and 0 <= ( ay1 := ay1 + dy ) < sy:
                        antinodes[ay1][ax1] = '#'
                        updates += 1
                    if 0 <= ( ax2 := ax2 - dx ) < sx and 0 <= ( ay2 := ay2 - dy ) < sy:
                        antinodes[ay2][ax2] = '#'
                        updates += 1
            else:  # task 1
                if 0 <= ( ax1 := x1 + dx ) < sx and 0 <= ( ay1 := y1 + dy ) < sy:
                    antinodes[ay1][ax1] = '#'
                if 0 <= ( ax2 := x2 - dx ) < sx and 0 <= ( ay2 := y2 - dy ) < sy:
                    antinodes[ay2][ax2] = '#'
    return ''.join(ch for line in antinodes for ch in line).count('#')

def task1(lines):
    return calculate(lines)

def task2(lines):
    return calculate(lines, task2=True)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
