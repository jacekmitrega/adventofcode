import re

example_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
example_output_1 = 18
example_output_2 = 9

xmas = re.compile(r"XMAS")

with open('input4.txt', 'r') as file:
    input = file.read()

def count_xmas(lines):
    return sum(len(xmas.findall(line)) for line in lines)

def task1(input):
    lines = list(input.splitlines())
    assert (numlines := len(lines)) == len(lines[0])

    all_lines = lines + [''.join(n) for n in zip(*lines)]  # = horizontal + vertical

    for n in range(2 * numlines):  # + two diagonals
        line1 = line2 = ''
        for m in range(numlines):
            if n - m < 0:
                break
            elif n - m >= numlines:
                continue
            line1 += lines[n-m][m]
            line2 += lines[n-m][-m-1]
        all_lines += [line1, line2]

    return count_xmas(all_lines) + count_xmas(line[::-1] for line in all_lines)

def task2(input):
    lines = list(input.splitlines())

    return sum(
        1
        for n in range(1, len(lines)-1)
        for m in range(1, len(lines)-1)
        if 'A' == lines[n][m]
            and set('MS')
                == {lines[n-1][m-1], lines[n+1][m+1]}
                == {lines[n+1][m-1], lines[n-1][m+1]}
    )

assert example_output_1 == task1(example_input)
print("solution 1:", task1(input))  # 2507

assert example_output_2 == task2(example_input)
print("solution 2:", task2(input))  # 1969
