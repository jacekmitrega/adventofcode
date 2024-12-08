"""
>>> task1(load_example_input())
14

# >>> task1(load_input())
# 'hello, world'

# >>> task2(load_example_input())
# 'hello, world!'

# >>> task2(load_input())
# 'hello, world!'

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


def calculate(lines, param=''):
    grid_copy = [list(line) for line in lines]
    flatten = ''.join()
    return lines

def task1(lines):
    return calculate(lines)

# def task2(lines):
#     return calculate(lines, '!')


if __name__ == "__main__":
    import doctest
    doctest.testmod()
