const std = @import("std");

const in_file_name = "d06-in.txt";
const in_file_max_size = 20000;
const in_file_max_lines = 10;
const in_file_max_cols = 1000;

pub fn main() !void {
    var in_f = try std.fs.cwd().openFile(in_file_name, .{});
    defer in_f.close();
    var in_buf: [in_file_max_size]u8 = undefined;
    var in_fr = in_f.reader(&in_buf);

    var tokens: [in_file_max_lines][in_file_max_cols][]u8 = undefined;
    var lines: [in_file_max_lines][]u8 = undefined;
    var max_line_len: usize = 0;
    var row: usize = 0;
    var col: usize = undefined;
    while (try in_fr.interface.takeDelimiter('\n')) |line| {
        lines[row] = line;
        max_line_len = @max(max_line_len, line.len);

        col = 0;
        var line_reader = std.io.Reader.fixed(line);
        for (0..in_file_max_cols + 1) |_| {
            while (line_reader.peekByte() catch null) |c| {
                if (c != ' ') break;
                line_reader.toss(1);
            }
            const token = try line_reader.takeDelimiter(' ') orelse break;
            tokens[row][col] = token;
            col += 1;
        } else unreachable;
        row += 1;
    }

    var result_1: u64 = 0;
    for (0..col) |c| {
        const op = tokens[row - 1][c];
        var acc: u64 = undefined;
        if (op[0] == '*') {
            acc = 1;
            for (0..row - 1) |r| acc *= try std.fmt.parseInt(u64, tokens[r][c], 10);
        } else {
            acc = 0;
            for (0..row - 1) |r| acc += try std.fmt.parseInt(u64, tokens[r][c], 10);
        }
        result_1 += acc;
    }

    var result_2: u64 = 0;
    const op_line = lines[row - 1];
    var op: u8 = undefined;
    var acc: u64 = 0;
    for (0..max_line_len) |c| {
        const op_c = if (c < op_line.len) op_line[c] else ' ';
        if (op_c == '*') {
            result_2 += acc;
            op = op_c;
            acc = 1;
        } else if (op_c == '+') {
            result_2 += acc;
            op = op_c;
            acc = 0;
        }

        var number: usize = 0;
        for (0..row - 1) |r| {
            const digit = lines[r][c];
            if (digit != ' ') number = number * 10 + digit - '0';
        }
        if (number != 0) acc = if (op == '*') acc * number else acc + number;
    } else result_2 += acc;

    std.debug.print("{} {}\n", .{ result_1, result_2 });
}
