const std = @import("std");

pub fn main() !void {
    var in_f = try std.fs.cwd().openFile("d03-in.txt", .{});
    defer in_f.close();

    var buf: [20200]u8 = undefined;
    var in_fr = in_f.reader(&buf);

    var result_1: usize = 0;
    var result_2: usize = 0;
    const in_r = &in_fr.interface;
    while (try in_r.takeDelimiter('\n')) |line| {
        result_1 += joltage(2, line);
        result_2 += joltage(12, line);
    }
    std.debug.print("{} {}\n", .{ result_1, result_2 });
}

fn joltage(comptime n: u8, line: []const u8) usize {
    var acc: [n]u8 = .{0} ** n;
    for (0..line.len - n + 1) |i| {
        for (0..n) |j| {
            const cur = line[i + j] - '0';
            if (cur > acc[j]) {
                acc[j] = cur;
                for (j + 1..n) |k| acc[k] = 0;
            }
        }
    }
    var j: usize = 0;
    for (0..n) |i| j += acc[i] * std.math.pow(usize, 10, n - i - 1);
    return j;
}
