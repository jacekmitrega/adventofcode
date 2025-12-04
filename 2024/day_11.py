"""
>>> task1(load_example_input())
55312

>>> task1(load_input())
191690

>>> task2(load_input())
228651922369703

"""

import functools


def parse_input_text(input_text):
    return tuple(int(n) for n in input_text.strip().split())

@functools.cache
def load_example_input():
    return parse_input_text("""125 17""")

@functools.cache
def load_input():
    with open(f"input_{__file__.split('_')[-1].split('.')[0]}.txt", "r") as file:
        return parse_input_text(file.read())


@functools.cache
def calculate(stones, blinks):
    if blinks == 0:
        return len(stones)

    total = 0
    for stone in stones:
        if stone == 0:
            total += calculate((1,), blinks - 1)
        elif len(ss := str(stone)) % 2 == 0:
            lss = len(ss) // 2
            left, right = int(ss[:lss]), int(ss[lss:])
            total += calculate((int(left), int(right)), blinks - 1)
        else:
            total += calculate((2024 * stone,), blinks - 1)
    return total

def task1(stones):
    return calculate(stones, blinks=25)

def task2(stones):
    return calculate(stones, blinks=75)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
