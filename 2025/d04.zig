const std = @import("std");

pub fn main() !void {
    var f = try std.fs.cwd().openFile("d04-in.txt", .{});
    defer f.close();

    const in_grid_size = 138;
    const in_buf_size = in_grid_size * (in_grid_size + 1); // +1 for \n's
    var in_buf: [in_buf_size]u8 = undefined;
    var fr = f.reader(&in_buf);
    _ = try fr.interface.take(in_buf_size);
    const in_grid: *[in_grid_size][in_grid_size + 1]u8 = @ptrCast(@constCast(&in_buf));

    const out_grid_size = in_grid_size + 2; // padding
    const out_buf_size = out_grid_size * out_grid_size;
    var out_buf: [out_buf_size]u8 = .{0} ** out_buf_size;
    const out_grid: *[out_grid_size][out_grid_size]u8 = @ptrCast(@constCast(&out_buf));

    var result_1: usize = 0;
    var result_2: usize = 0;

    for (0..100) |round| {
        const adj_yx = .{
            .{ 0, 0 },
            .{ 0, 1 },
            .{ 0, 2 },
            .{ 1, 0 },
            .{ 1, 2 },
            .{ 2, 0 },
            .{ 2, 1 },
            .{ 2, 2 },
        };

        for (0..in_grid_size) |y| {
            for (0..in_grid_size) |x| {
                if (in_grid[y][x] == '@') {
                    inline for (0..adj_yx.len) |a| {
                        const dy, const dx = adj_yx[a];
                        out_grid[y + dy][x + dx] +|= 1;
                    }
                }
            }
        }

        var removed_this_round: usize = 0;
        for (0..in_grid_size) |y| {
            for (0..in_grid_size) |x| {
                if (in_grid[y][x] == '@' and out_grid[y + 1][x + 1] < 4) {
                    in_grid[y][x] = 'x';
                    removed_this_round += 1;
                }
                out_grid[y + 1][x + 1] = 0;
            }
        }
        if (round == 0) result_1 = removed_this_round;
        result_2 += removed_this_round;
        if (removed_this_round == 0) break;
    } else unreachable;

    std.debug.print("{} {}\n", .{ result_1, result_2 });
}
