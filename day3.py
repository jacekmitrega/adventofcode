import re

example_input_1 = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
example_output_1 = 161  # (2*4 + 5*5 + 11*8 + 8*5)

example_input_2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
example_output_2 = 48  # (2*4 + 8*5)

with open('input3.txt', 'r') as file:
    input = file.read()

re_mul = r"mul\((\d{1,3}),(\d{1,3})\)"

def task1(input):
    return sum(int(a) * int(b) for a, b in re.findall(re_mul, input))

def task2(input, do=True):
    sum = 0
    for op, a, b in re.findall(fr"(do\(\)|don't\(\)|{re_mul})", input):
        match op:
            case "do()":
                do = True
            case "don't()":
                do = False
            case _ if do:
                sum += int(a) * int(b)
    return sum

assert example_output_1 == task1(example_input_1)
print(f"task1: {task1(input)}")

assert example_output_2 == task2(example_input_2)
print(f"task2: {task2(input)}")
