"""
This program is not generalized, it is specifically for my input of day 17.

>>> task1(load_example_input())
4,6,3,5,6,3,5,2,1,0

>>> task1(load_input())
7,3,1,3,6,3,6,0,2

>>> task1(load_example_input_2())
0,3,5,4,3,0

>>> verify_task2(load_input())

"""


def parse_input_text(input_text):
    inp_lns_it = iter(input_text.strip().splitlines())
    reg_a = int(next(inp_lns_it).split('Register A: ')[1])
    reg_b = int(next(inp_lns_it).split('Register B: ')[1])
    reg_c = int(next(inp_lns_it).split('Register C: ')[1])
    next(inp_lns_it)  # blank line
    bytecode = (next(inp_lns_it).split('Program: ')[1]).split(',')
    prog = [(int(opcode), int(operand)) for opcode, operand in zip(bytecode[::2], bytecode[1::2])]
    return reg_a, reg_b, reg_c, prog


def load_example_input():
    return parse_input_text("""
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
""")


def load_example_input_2():
    return parse_input_text("""
Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
""")


def load_input():
    with open(f"input_{__file__.split('_')[-1].split('.')[0]}.txt", "r") as file:
        return parse_input_text(file.read())


def calc_out_and_next_a(a):
    # Function returns the value output after one iteration of my program
    # as well as the value of register A after that iteration.

    # My input program in pseudo-assembly language:
    # a = ?
    # b = 0
    # c = 0
    # 2, 4 | bst 4 | b = a % 8
    # 1, 5 | bxl 5 | b ^= 5
    # 7, 5 | cdv 5 | c = a // (2 ** b)
    # 1, 6 | bxl 6 | b ^= 6
    # 0, 3 | adv 3 | a //= 2 ** 3
    # 4, 0 | bxc 0 | b ^= c
    # 5, 5 | out 5 | yield b % 8
    # 3, 0 | jnz 0 | if a != 0: code_ptr = 0

    # The above translates to this Python code:
    a8 = a % 8
    return (  ((a8)^3) ^ (a // (2 ** ((a8)^5)))  ) % 8,  a // 8


# I stepped backwards through the input program and figured out, that register A
# should be 3 for the last iteration to output 0 and exit the program.
# So let's work backwards from there (skipping the last iteration done manually):

# expected_outs_reversed = list(reversed(expected))[1:]
# last_iter_a = {3}
# for expected_out in expected_outs_reversed:
#     next_iter_a = set()
#     min_last_iter_a = min(last_iter_a)
#     max_last_iter_a = max(last_iter_a)
#     # This is still a lot of work, but I haven't figured out the exact formula.
#     # The input code has `adv 3` doing int division of A by 8, so I'm going
#     # to search the next value of A in the range of 8 times the previous values found.
#     for n in range(min_last_iter_a * 8, max_last_iter_a * 9):
#         o, na = calc_out_and_next_a(n)
#         if o == expected_out and na in last_iter_a:
#             print(n, o, na)
#             next_iter_a.add(n)
#     last_iter_a = next_iter_a


# Python version of my input code with some notes:
a = 105843716614554
b = 0
c = 0
result = []
while True:
    # in the last step, a = 3

    # b = a % 8
    # b ^= 5
    b = (a % 8) ^ 5  # last iter: after: a = 1-7, so b = 0,1,2,3,4,6,7
    # ^^ b = (a % 8) ^ 5

    # c = a // (2 ** b)
    c = a // (2 ** b)  # last iter: before: a = 1-7 / b = 0,1,2,3,4,6,7 / 2**b = 1,2,4,8,16,64,128, so after c = 0-7
    # ^^ c = a // (2 ** ((a % 8) ^ 5))

    # b ^= 6
    # b ^= c (reordered, was below the next instruction)
    b = (b ^ 6) ^ c  # last iter: after b=0, before: b = 0,1,2,3,4,6,7, c = 0-7, so b = 0-7  # {(b^6)^c for c in [0, 1, 2, 3, 4, 5, 6, 7] for b in [0,1,2,3,4,6,7]}
    # ^^ b = (((a % 8) ^ 5) ^ 6) ^ (a // (2 ** ((a % 8) ^ 5)))

    # a //= 2 ** 3
    a //= 8  # last iter: a = 0 after, so a = 1-7 before

    # yield b % 8
    result.append(b % 8)  # last iter: b = 0

    # if a != 0: code_ptr = 0
    if a == 0:
        break


def run(reg_a, reg_b, reg_c, prog):
    code_ptr = 0
    while 0 <= code_ptr < len(prog):
        opcode, operand = prog[code_ptr]

        if operand == 4:
            combo = reg_a
        elif operand == 5:
            combo = reg_b
        elif operand == 6:
            combo = reg_c
        else:
            combo = operand

        match opcode:
            case 0:  # adv
                reg_a //= 2 ** combo
            case 1:  # bxl
                reg_b ^= operand
            case 2:  # bst
                reg_b = combo % 8
            case 3:  # jnz
                if reg_a != 0:
                    code_ptr = operand
                    continue
            case 4:  # bxc
                reg_b ^= reg_c
            case 5:  # out
                yield combo % 8
            case 6:  # bdv
                reg_b = reg_a // (2 ** combo)
            case 7:  # cdv
                reg_c = reg_a // (2 ** combo)

        code_ptr += 1


def task1(input):
    print(','.join(str(ch) for ch in run(*input)))


def verify_task2(input):
    _, reg_b, reg_c, prog = input
    reg_a = 105843716614554
    assert [b for a in prog for b in a] == list(run(reg_a, reg_b, reg_c, prog))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
