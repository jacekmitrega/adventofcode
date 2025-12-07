const std = @import("std");

const f_name = "d07-in.txt";
const f_max_size = 21000;
const f_max_cols = 150;
const f_max_rows = 150;

pub fn main() !void {
    var f = try std.fs.cwd().openFile(f_name, .{});
    defer f.close();
    var buf: [f_max_size]u8 = undefined;
    var r = f.reader(&buf);

    var result_1: usize = 0;
    var lines: [f_max_rows][]u8 = undefined;
    var num_lines: usize = 0;
    var prev_line: []u8 = "";
    while (try r.interface.takeDelimiter('\n')) |line| {
        for (0..prev_line.len) |x| {
            if (prev_line[x] == 'S') {
                if (line[x] == '^') {
                    result_1 += 1;
                    if (x > 0) line[x - 1] = 'S';
                    if (x < prev_line.len - 1) line[x + 1] = 'S';
                } else line[x] = 'S';
            }
        }
        prev_line = line;
        lines[num_lines] = line;
        num_lines += 1;
    }

    var result_2: usize = 0;
    var cache: [f_max_rows][f_max_cols]u64 = .{.{0} ** f_max_cols} ** f_max_rows;
    for (0..prev_line.len) |x| result_2 += timelines(&cache, lines[0..num_lines], x);

    std.debug.print("{} {}\n", .{ result_1, result_2 });
}

fn timelines(cache: *[f_max_rows][f_max_cols]u64, lines: [][]u8, x: usize) usize {
    const c = lines[0][x];
    if (c == '.') return 0;
    if (lines.len == 1 and c == 'S') return 1;

    const cached = cache[lines.len][x];
    if (cached != 0) return cached;

    const tls = blk: {
        if (c == 'S') break :blk timelines(cache, lines[1..], x);
        var lr: usize = 0;
        if (x > 0) lr += timelines(cache, lines[1..], x - 1);
        if (x < lines[0].len - 1) lr += timelines(cache, lines[1..], x + 1);
        break :blk lr;
    };
    cache[lines.len][x] = tls;
    return tls;
}
