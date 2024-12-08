"""
>>> task1(load_example_input())
3749

>>> task2(load_example_input())
11387

>>> task1(load_input())
882304362421

>>> task2(load_input())
145149066755184

"""

import functools
import itertools
import re


def parse_input_text(input_text):
    return [[int(n) for n in re.split(r"[: ]", line) if n] for line in input_text.strip().splitlines()]

@functools.cache
def load_example_input():
    return parse_input_text("""
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""")

@functools.cache
def load_input():
    with open(f'input_{__file__.split('_')[-1].split('.')[0]}.txt', 'r') as file:
        return parse_input_text(file.read())


def calculate(lines, valid_ops):
    total = 0
    for test_value, *values in lines:
        for ops in itertools.product(valid_ops, repeat=len(values) - 1):
            values_it = iter(values)
            acc = next(values_it)
            for op, value in zip(ops, values_it):
                match op:
                    case "+":
                        acc += value
                    case "*":
                        acc *= value
                    case _:
                        acc = int(f"{acc}{value}")
            if acc == test_value:
                total += test_value
                break
    return total

def task1(lines):
    return calculate(lines, '+*')

def task2(lines):
    return calculate(lines, '+*|')


if __name__ == "__main__":
    import doctest
    doctest.testmod()
