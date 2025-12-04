const std = @import("std");
const in = @import("d02-in.zon");

pub fn main() !void {
    var in_r = std.io.Reader.fixed(in);
    var sum1: u64 = 0;
    var sum2: u64 = 0;
    while (try in_r.takeDelimiter('-')) |left| {
        const right = try in_r.takeDelimiter(',') orelse unreachable;
        const l = try std.fmt.parseInt(u64, left, 10);
        const r = try std.fmt.parseInt(u64, right, 10);
        var i = l;
        while (i <= r) : (i += 1) {
            var buf: [10]u8 = undefined;
            const str = buf[0..std.fmt.printInt(buf[0..], i, 10, .lower, .{})];
            switch (str.len) {
                1 => {
                    i = 11 - 1;
                    continue;
                },
                2 => if (repeated(2, str)) {
                    sum1 += i;
                    sum2 += i;
                },
                3 => {
                    if (repeated(3, str)) sum2 += i;
                },
                4 => {
                    if (repeated(2, str)) {
                        sum1 += i;
                        sum2 += i;
                    } else if (repeated(4, str)) sum2 += i;
                },
                5 => {
                    if (repeated(5, str)) sum2 += i;
                },
                6 => {
                    if (repeated(2, str)) {
                        sum1 += i;
                        sum2 += i;
                    } else if (repeated(3, str) or repeated(6, str)) sum2 += i;
                },
                7 => {
                    if (repeated(7, str)) sum2 += i;
                },
                8 => {
                    if (repeated(2, str)) {
                        sum1 += i;
                        sum2 += i;
                    } else if (repeated(4, str) or repeated(8, str)) sum2 += i;
                },
                9 => {
                    if (repeated(3, str) or repeated(9, str)) sum2 += i;
                },
                10 => {
                    if (repeated(2, str)) {
                        sum1 += i;
                        sum2 += i;
                    } else if (repeated(5, str) or repeated(10, str)) sum2 += i;
                },
                else => {},
            }
        }
    }
    std.debug.print("sum1: {} sum2: {}\n", .{ sum1, sum2 });
}

fn repeated(n: usize, str: []const u8) bool {
    const d = std.math.divExact(usize, str.len, n) catch return false;
    var r_idx = d;
    for (1..n) |_| {
        for (0..d) |i| {
            if (str[i] != str[r_idx]) return false;
            r_idx += 1;
        }
    }
    return true;
}
