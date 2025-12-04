"""
>>> task1(load_example_input())
1930

>>> task1(load_input())
1375574

>>> task2(load_example_input())
1206

>>> task2(load_input())
830566

"""

from dataclasses import dataclass
import functools
import itertools


@functools.cache
def parse_input_text(input_text):
    return Map(input_text.strip().splitlines())

@functools.cache
def load_example_input():
    return parse_input_text("""
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""")

@functools.cache
def load_input():
    with open(f"input_{__file__.split('_')[-1].split('.')[0]}.txt", "r") as file:
        return parse_input_text(file.read())


@dataclass
class Region:
    ch: str  # don't mutate
    x: int  # don't mutate
    y: int  # don't mutate
    plots: set
    num_sides: int

    def __init__(self, ch, x, y):
        self.ch = ch
        self.x = x
        self.y = y
        self.plots = {(x, y)}
        self.fence = 4
        self.num_sides = 0
        self.area = 0

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        return id(self) == id(other)


directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
outside_the_map = Region('', -1, -1)


class Map:
    def __init__(self, ingrid):
        self.ingrid = ingrid
        self.sx = len(ingrid[0])
        self.sy = len(ingrid)
        self.regions = {}

        for x, y in itertools.product(range(self.sx), range(self.sy)):
            self._scan_region(x, y)

    def _scan_region(self, x: int, y: int, region: Region = None):
        if (x, y) in self.regions:
            return  # entered already regionized plot
        if not region:
            region = Region(self.ingrid[y][x], x, y)  # start new region
        else:
            if region.ch == self.ingrid[y][x]:
                # entered regionized plot of the same region - how much fence to add?
                add = 4
                for dx, dy in directions:
                    if (
                        0 <= (nx := x + dx) < self.sx and 0 <= (ny := y + dy) < self.sy
                        and region == self.regions.get((nx, ny))
                    ):
                        add -= 2
                region.fence += add
            else:
                return  # entered unregionized plot of a different region

        self.regions[(x, y)] = region
        region.area += 1

        for dx, dy in directions:
            if not (0 <= (nx := x + dx) < self.sx and 0 <= (ny := y + dy) < self.sy):
                continue
            self._scan_region(nx, ny, region)

    def calculate_regions_sides(self):
        # calculate horizontal sides
        for y in range(self.sy + 1):
            prev_region_over = None
            prev_region_under = None
            prev_was_no_fence = True
            for x in range(self.sx):
                region_over = self.regions[(x, y-1)] if y >= 1 else outside_the_map
                region_under = self.regions[(x, y)] if y < self.sy else outside_the_map
                if region_over == region_under:
                    prev_was_no_fence = True
                else:
                    if prev_was_no_fence or region_over != prev_region_over:
                        region_over.num_sides += 1
                    if prev_was_no_fence or region_under != prev_region_under:
                        region_under.num_sides += 1
                    prev_was_no_fence = False
                prev_region_over = region_over
                prev_region_under = region_under

        # calculate vertical sides
        for x in range(self.sx + 1):
            prev_region_l = None
            prev_region_r = None
            prev_was_no_fence = True
            for y in range(self.sy):
                region_l = self.regions[(x-1, y)] if x >= 1 else outside_the_map
                region_r = self.regions[(x, y)] if x < self.sx else outside_the_map
                if region_l == region_r:
                    prev_was_no_fence = True
                else:
                    if prev_was_no_fence or region_l != prev_region_l:
                        region_l.num_sides += 1
                    if prev_was_no_fence or region_r != prev_region_r:
                        region_r.num_sides += 1
                    prev_was_no_fence = False
                prev_region_l = region_l
                prev_region_r = region_r

def task1(map):
    return sum(region.area * region.fence for region in set(map.regions.values()))

def task2(map):
    map.calculate_regions_sides()
    return sum(region.area * region.num_sides for region in set(map.regions.values()))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
