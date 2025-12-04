"""
>>> task1(load_example_input('str'))
10092

>>> task1(load_input('str'))
1559280

>>> task2(load_example_input('wide_cell'))
9021

>>> task2(load_input('wide_cell'))
1576353

"""
visualize = False


import itertools


def wide_cell(char):
    match char:
        case '#':
            return '##'
        case '.':
            return '..'
        case 'O':
            return '[]'
        case '@':
            return '@.'

def input_grid(input_str, cell_fn_name):
    cell_type = eval(cell_fn_name)
    grid = [[cell_element for char in line for cell_element in cell_type(char)] for line in input_str]
    sx, sy = len(grid[0]), len(grid)
    return grid, sx, sy


def parse_input_text(input_text, cell_fn_name):
    lines_it = iter(input_text.strip().splitlines())
    grid, sx, sy = input_grid(itertools.takewhile(lambda line: line != '', lines_it), cell_fn_name)
    moves = ''.join(lines_it)
    return grid, sx, sy, moves


def load_example_input(cell_fn_name):
    return parse_input_text("""
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""", cell_fn_name)

def load_input(cell_fn_name):
    with open(f"input_{__file__.split('_')[-1].split('.')[0]}.txt", "r") as file:
        return parse_input_text(file.read(), cell_fn_name)

directions = {
    '^': (0, -1),
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
}

def step(grid, sx, sy, x, y, dx, dy):
    nx, ny = x + dx, y + dy
    if not (0 <= nx < sx) or not (0 <= ny < sy):
        return x, y
    if grid[ny][nx] == '#':
        return x, y
    if grid[ny][nx] == 'O':
        step(grid, sx, sy, nx, ny, dx, dy)
    if grid[ny][nx] == '.':
        grid[y][x], grid[ny][nx] = grid[ny][nx], grid[y][x]
        return nx, ny
    return x, y

def simulate(grid, sx, sy, moves):
    x, y = next((x, y) for x in range(sx) for y in range(sy) if grid[y][x] == '@')
    for move in moves:
        dx, dy = directions[move]
        x, y = step(grid, sx, sy, x, y, dx, dy)
        if visualize:
            import time
            print(move)
            for line in grid:
                print(''.join(line))
            time.sleep(0.0166)
    return sum(100*y + x for x in range(sx) for y in range(sy) if grid[y][x] == 'O')

def step2(grid, sx, sy, x, y, dx, dy, dry_run=False):
    nx, ny = x + dx, y + dy
    if not (0 <= nx < sx) or not (0 <= ny < sy):
        return x, y
    if grid[ny][nx] == '#':
        return x, y
    ok = True
    if (box_side := grid[ny][nx]) in '[]':
        ok = False
        if dy == 0:
            step2(grid, sx, sy, nx, ny, dx, dy)
            if grid[ny][nx] == '.':
                ok = True
        else:
            nx2 = nx + 1 if box_side == '[' else nx - 1
            if (
                step2(grid, sx, sy, nx, ny, dx, dy, dry_run=True) == (nx+dx, ny+dy) and
                step2(grid, sx, sy, nx2, ny, dx, dy, dry_run=True) == (nx2+dx, ny+dy)
            ):
                ok = True
                if not dry_run:
                    step2(grid, sx, sy, nx, ny, dx, dy)
                    step2(grid, sx, sy, nx2, ny, dx, dy)

    if ok:
        if not dry_run:
            grid[y][x], grid[ny][nx] = grid[ny][nx], grid[y][x]
        return nx, ny
    return x, y

def simulate2(grid, sx, sy, moves):
    x, y = next((x, y) for x in range(sx) for y in range(sy) if grid[y][x] == '@')
    for move in moves:
        dx, dy = directions[move]
        if visualize:
            print(move)
        x, y = step2(grid, sx, sy, x, y, dx, dy)
        if visualize:
            import time
            for line in grid:
                print(''.join(line))
            time.sleep(0.0166)
    return sum(100*y + x for x in range(sx) for y in range(sy) if grid[y][x] == '[')

def task1(input):
    grid, sx, sy, moves = input
    return simulate(grid, sx, sy, moves)

def task2(input):
    grid, sx, sy, moves = input
    return simulate2(grid, sx, sy, moves)


if __name__ == "__main__":
    if visualize:
        task1(load_example_input('str'))
        task2(load_example_input('wide_cell'))
    visualize = False
    import doctest
    doctest.testmod()
