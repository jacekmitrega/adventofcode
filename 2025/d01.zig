const std = @import("std");

// wc -lc d01-in.txt
// 4168   17150 d01-in.txt
const in_chars = 17150;
const in_lines = 4168;

pub fn main() !void {
    var buf: [in_chars]u8 = undefined;

    var in_f = try std.fs.cwd().openFile("d01-in.txt", .{});
    defer in_f.close();
    var in_fr = in_f.reader(&buf);
    var in_r = &in_fr.interface;

    var l: usize = 0;
    var dial: i64 = 50;
    var zeros_part1: u64 = 0;
    var zeros_part2: i64 = 0;
    var prev_dial_divfloor_100: i64 = @divFloor(dial, 100);
    var prev_dial_minus_1_divfloor_100: i64 = @divFloor(dial - 1, 100);

    while (l < in_lines) : (l += 1) {
        const line = try in_r.takeDelimiter('\n') orelse unreachable;

        const clicks = try std.fmt.parseInt(i32, line[1..], 10);
        const is_left = line[0] == 'L';
        dial += if (is_left) -clicks else clicks;
        if (@mod(dial, 100) == 0) zeros_part1 += 1;

        const new_dial_minus_1_divfloor_100: i64 = @divFloor(dial - 1, 100);
        const new_dial_divfloor_100 = @divFloor(dial, 100);
        zeros_part2 += if (is_left)
            prev_dial_minus_1_divfloor_100 - new_dial_minus_1_divfloor_100
        else
            new_dial_divfloor_100 - prev_dial_divfloor_100;
        prev_dial_minus_1_divfloor_100 = new_dial_minus_1_divfloor_100;
        prev_dial_divfloor_100 = new_dial_divfloor_100;
    }
    std.debug.print("part1: {} part2: {}\n", .{ zeros_part1, zeros_part2 });
}
