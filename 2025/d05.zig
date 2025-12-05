const std = @import("std");

const in_file_name = "d05-in.txt";
const in_file_size = 21737;
const in_file_lines = 1188;

pub fn main() !void {
    var in_f = try std.fs.cwd().openFile(in_file_name, .{});
    defer in_f.close();

    var in_buf: [in_file_size]u8 = undefined;
    var in_fr = in_f.reader(&in_buf);
    const in_r = &in_fr.interface;

    var ranges: [2 * in_file_lines]u64 = undefined;
    var num_ranges: usize = 0;
    while (try in_r.takeDelimiter('\n')) |line| {
        if (line.len == 0) break;
        var line_reader = std.io.Reader.fixed(line);
        const range_begin_str = try line_reader.takeDelimiterExclusive('-');
        const range_idx = num_ranges << 1;
        ranges[range_idx] = try std.fmt.parseInt(u64, range_begin_str, 10);
        ranges[range_idx + 1] = try std.fmt.parseInt(u64, line[range_begin_str.len + 1 ..], 10);
        num_ranges += 1;
    } else unreachable;

    // whether it sorts by range start or end depends on endianness, merging below works wither way
    const ranges_u128: [*]u128 = @ptrCast(@alignCast(&ranges));
    std.sort.block(u128, ranges_u128[0..num_ranges], {}, comptime std.sort.asc(u128));

    var merged_ranges: usize = 1;
    for (1..num_ranges) |r| {
        const m_idx = (merged_ranges - 1) << 1;
        const r_idx = r << 1;
        const left_gap: i128 = @as(i128, @intCast(ranges[m_idx])) - ranges[r_idx + 1];
        const right_gap: i128 = @as(i128, @intCast(ranges[r_idx])) - ranges[m_idx + 1];
        if (left_gap > 1 or right_gap > 1) { // no overlap/adjoin - advance
            ranges[m_idx + 2] = ranges[r_idx];
            ranges[m_idx + 3] = ranges[r_idx + 1];
            merged_ranges += 1;
        } else { // overlap/adjoin - merge ranges
            ranges[m_idx] = @min(ranges[m_idx], ranges[r_idx]);
            ranges[m_idx + 1] = @max(ranges[m_idx + 1], ranges[r_idx + 1]);
        }
    }

    var result_1: usize = 0;
    while (try in_r.takeDelimiter('\n')) |line| {
        const id = try std.fmt.parseInt(u64, line, 10);
        for (0..merged_ranges) |r| {
            const idx = r << 1;
            if (ranges[idx] <= id and id <= ranges[idx + 1]) {
                result_1 += 1;
                break;
            }
        }
    }

    var result_2: usize = merged_ranges; // all ranges are inclusive on both ends
    for (0..merged_ranges) |r| {
        const idx = r << 1;
        result_2 += ranges[idx + 1] - ranges[idx];
    }

    std.debug.print("{} {}\n", .{ result_1, result_2 });
}
