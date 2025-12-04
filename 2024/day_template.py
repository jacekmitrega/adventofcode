"""
>>> task1(load_example_input())
12

# >>> task1(load_input())
# 12

# >>> task2(load_example_input())
# 13

# >>> task2(load_input())
# 13

"""

import functools
import itertools
import re


def parse_input_text(input_text):
    return input_text.strip().splitlines()

@functools.cache
def load_example_input():
    return parse_input_text("""
hello,
world
""")

@functools.cache
def load_input():
    with open(f"input_{__file__.split('_')[-1].split('.')[0]}.txt", "r") as file:
        return parse_input_text(file.read())


def calculate(lines, param=''):
    return len(f"{' '.join(lines)}{param}")

def task1(lines):
    return calculate(lines)

def task2(lines):
    return calculate(lines, '!')


if __name__ == "__main__":
    import doctest
    doctest.testmod()
