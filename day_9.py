"""
>>> task1(load_example_input())
1928

>>> task1(load_input())
6262891638328

>>> task2(load_example_input())
2858

>>> task2(load_input())
6287317016845

"""

import functools
import itertools


def parse_input_text(input_text):
    return input_text.strip()

@functools.cache
def load_example_input():
    return parse_input_text("""2333133121414131402""")

@functools.cache
def load_input():
    with open(f'input_{__file__.split('_')[-1].split('.')[0]}.txt', 'r') as file:
        return parse_input_text(file.read())


def get_fs_blocks(input):
    if len(input) % 2 != 0:
        input += '0'
    disk_map = list(zip(input[::2], input[1::2]))

    fs_blocks = []
    for file_id, (file_size, free_space_size) in enumerate(disk_map):
        fs_blocks.extend([file_id] * int(file_size))
        fs_blocks.extend([None] * int(free_space_size))
    return fs_blocks

def fs_checksum(fs_blocks):
    return sum(idx * file_id for idx, file_id in enumerate(fs_blocks) if file_id is not None)

def task1(input):
    fs_blocks = get_fs_blocks(input)

    def empty_blocks():
        yield from (idx for idx, block in enumerate(fs_blocks) if block is None)

    def blocks_to_defragment():
        last_block_idx = len(fs_blocks) - 1
        yield from (last_block_idx - idx for idx, block in enumerate(reversed(fs_blocks)) if block is not None)

    empty_block_it = iter(empty_blocks())
    defragment_it = iter(blocks_to_defragment())
    try:
        while (empty_block_idx := next(empty_block_it)) < (defragment_idx := next(defragment_it)):
            fs_blocks[empty_block_idx] = fs_blocks[defragment_idx]
            fs_blocks[defragment_idx] = None
    except StopIteration:
        pass

    return fs_checksum(fs_blocks)

def task2(input):
    fs_blocks = get_fs_blocks(input)
    if not fs_blocks:
        return 0
    fs_blocks_defragged = fs_blocks.copy()

    min_empty_block_idx_by_size = {n: 0 for n in range(10)}

    def files_to_defragment():
        block_idx = len(fs_blocks)
        for _, group in itertools.groupby(iter(reversed(fs_blocks))):
            blocks = list(reversed(list(group)))
            block_idx -= len(blocks)
            if blocks[0] is not None:
                yield blocks, block_idx

    def find_empty_block(size):
        min_idx = min_empty_block_idx_by_size[size]
        block_idx = min_idx
        for _, group in itertools.groupby(iter(fs_blocks_defragged[min_idx:]), ):
            blocks = list(group)
            if blocks[0] is None and len(blocks) >= size:
                min_empty_block_idx_by_size[size] = block_idx
                return block_idx
            block_idx += len(blocks)

    for file_to_defrag, file_to_defrag_idx in files_to_defragment():
        if (empty_block_idx := find_empty_block(len(file_to_defrag))) and empty_block_idx < file_to_defrag_idx:
            for n in range(len(file_to_defrag)):
                fs_blocks_defragged[empty_block_idx + n] = file_to_defrag[n]
                fs_blocks_defragged[file_to_defrag_idx + n] = None

    return fs_checksum(fs_blocks_defragged)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
