import itertools
import functools

example_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
example_output_1 = 143
example_output_2 = 123

with open('input5.txt', 'r') as file:
    input_text = file.read()

def parse_input(input):
    it = iter(input.splitlines())
    rules = {(int(x), int(y)) for x, y in [s.split('|') for s in itertools.takewhile(lambda x: "|" in x, it)]}
    updates = [tuple(int(x) for x in upd.split(',')) for upd in it]
    return rules, updates

def make_cmp(rules):
    return lambda a, b: -1 if (a, b) in rules else 1 if (b, a) in rules else 0

def fix(upd, rules):
    return sorted(upd, key=functools.cmp_to_key(make_cmp(rules)))

def is_good(upd, rules):
    return all(((upd[i], upd[j]) in rules) for i in range(len(upd)) for j in range(i+1, len(upd)))

def task1(input):
    rules, updates = parse_input(input)
    return sum(upd[(len(upd) - 1) // 2] for upd in updates if is_good(upd, rules))

def task2(input):
    rules, updates = parse_input(input)
    return sum(fixed[(len(fixed) - 1) // 2] for upd in updates if not is_good(upd, rules) and (fixed := fix(upd, rules)))

assert example_output_1 == task1(example_input)
print("task 1:", task1(input_text))  # 6260

assert example_output_2 == task2(example_input)
print("task 2:", task2(input_text))  # 5346
