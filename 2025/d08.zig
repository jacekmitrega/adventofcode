const std = @import("std");

const f_name = "d08-in.txt";
const f_max_size = 21000;
const f_max_rows = 1000;

const JBox = packed struct { // u64
    id: u10,
    x: u18,
    y: u18,
    z: u18,
};

const Connection = packed struct { // u64
    from_idx: u10,
    to_idx: u10,
    d: u44,
};

pub fn main() !void {
    var f = try std.fs.cwd().openFile(f_name, .{});
    defer f.close();
    var buf: [f_max_size]u8 = undefined;
    var r = f.reader(&buf);

    var jboxes_buf: [f_max_rows]JBox = undefined;
    var num_jboxes: usize = 0;
    while (try r.interface.takeDelimiter(',')) |x_str| {
        var jb = &jboxes_buf[num_jboxes];
        jb.id = 0;
        jb.x = try std.fmt.parseInt(u18, x_str, 10);
        jb.y = try std.fmt.parseInt(u18, try r.interface.takeDelimiter(',') orelse unreachable, 10);
        jb.z = try std.fmt.parseInt(u18, try r.interface.takeDelimiter('\n') orelse unreachable, 10);
        num_jboxes += 1;
    }
    const jboxes = jboxes_buf[0..num_jboxes];
    std.sort.block(u64, @ptrCast(jboxes), {}, comptime std.sort.asc(u64)); // by z, y, x, id on LE

    var distances_buf: [f_max_rows * f_max_rows]Connection = undefined;
    const num_distances = (num_jboxes * (num_jboxes - 1)) >> 1;
    const distances = distances_buf[0..num_distances];
    var dist_idx: usize = 0;
    for (0..num_jboxes - 1) |jb_from_idx| {
        const jb_from = &jboxes[jb_from_idx];
        for (jb_from_idx + 1..num_jboxes) |jb_to_idx| {
            const jb_to = &jboxes[jb_to_idx];
            const dx: u64 = @max(jb_to.x, jb_from.x) - @min(jb_to.x, jb_from.x);
            const dy: u64 = @max(jb_to.y, jb_from.y) - @min(jb_to.y, jb_from.y);
            const dz: u64 = jb_to.z - jb_from.z; // jboxes already sorted by z
            const d: u64 = std.math.sqrt(dx * dx + dy * dy + dz * dz);
            const dist = &distances[dist_idx];
            dist.from_idx = @intCast(jb_from_idx);
            dist.to_idx = @intCast(jb_to_idx);
            dist.d = @intCast(d);
            dist_idx += 1;
        }
    }
    std.sort.block(u64, @ptrCast(distances), {}, comptime std.sort.asc(u64)); // sort by d

    var temp_jboxes_buf: @TypeOf(jboxes_buf) = undefined;
    const temp_jboxes = temp_jboxes_buf[0..num_jboxes];

    var circuit_sizes_buf: [f_max_rows]u32 = .{1} ** f_max_rows;
    const circuit_sizes = circuit_sizes_buf[0..num_jboxes];
    var temp_circuit_sizes_buf: @TypeOf(circuit_sizes_buf) = undefined;
    const temp_circuit_sizes = temp_circuit_sizes_buf[0..num_jboxes];

    var circuit_id_seq: u10 = 1;
    var temp_circuit_id_seq: @TypeOf(circuit_id_seq) = undefined;

    const num_connections_p1 = 1000;
    const connections_p1 = distances[0..num_connections_p1];

    build_circuits(
        jboxes,
        connections_p1,
        circuit_sizes,
        &circuit_id_seq,
    );

    // part 1 only, so process in temp buffers:
    @memcpy(temp_jboxes, jboxes);
    @memcpy(temp_circuit_sizes, circuit_sizes);
    merge_circuits(temp_jboxes, connections_p1, temp_circuit_sizes);
    std.sort.block(u32, temp_circuit_sizes[0..num_jboxes], {}, comptime std.sort.desc(u32));
    const result_1: usize = temp_circuit_sizes[0] * temp_circuit_sizes[1] * temp_circuit_sizes[2];

    // part 2:
    var lower: usize = num_connections_p1;
    var upper: usize = num_distances;
    var is_final_approach = false;
    var needs_reset = true;

    const jbox = blk: for (0..100) |_| {
        if (needs_reset) {
            @memcpy(temp_jboxes, jboxes);
            @memcpy(temp_circuit_sizes, circuit_sizes);
            temp_circuit_id_seq = circuit_id_seq;
        }

        const n = lower + if (is_final_approach) 1 else (upper - lower) >> 1;

        // might be discarded so process in temp buffers:
        build_circuits(
            temp_jboxes,
            distances[lower..n],
            temp_circuit_sizes,
            &temp_circuit_id_seq,
        );

        merge_circuits(temp_jboxes, distances[0..n], temp_circuit_sizes);
        const max_circuit_size = std.sort.max(u32, temp_circuit_sizes[0..num_jboxes], {}, comptime std.sort.asc(u32)).?;
        if (max_circuit_size == 999) {
            is_final_approach = true;
            lower = n;
            needs_reset = false;
        } else if (max_circuit_size == 1000) {
            if (is_final_approach) break :blk distances[n - 1]; // FOUND!
            upper = n;
            needs_reset = true;
        } else { // commit work done so far to non-temp buffers
            lower = n;
            @memcpy(jboxes, temp_jboxes);
            @memcpy(circuit_sizes, temp_circuit_sizes);
            circuit_id_seq = temp_circuit_id_seq;
            needs_reset = false;
        }
    } else unreachable;

    const result_2 = @as(u64, @intCast(jboxes[jbox.from_idx].x)) * jboxes[jbox.to_idx].x;
    std.debug.print("{} {}\n", .{ result_1, result_2 });
}

fn build_circuits(
    jboxes: []JBox,
    connections: []const Connection,
    circuit_sizes: []u32,
    circuit_id_seq: *u10,
) void {
    for (connections) |conn| {
        const jb_from = &jboxes[conn.from_idx];
        const jb_to = &jboxes[conn.to_idx];
        const max_id = @max(jb_from.id, jb_to.id);
        const min_id = @min(jb_from.id, jb_to.id);
        if (max_id == 0) {
            jb_from.id = circuit_id_seq.*;
            jb_to.id = circuit_id_seq.*;
            circuit_sizes[circuit_id_seq.*] = 2;
            circuit_id_seq.* += 1;
        } else if (min_id == 0) {
            if (jb_from.id == 0) jb_from.id = max_id else jb_to.id = max_id;
            circuit_sizes[max_id] += 1;
        } // else: merge circuits (handle later) or loop within a circuit (ignore)
    }
}

fn merge_circuits(jboxes: []JBox, connections: []const Connection, circuit_sizes: []u32) void {
    var circuit_merges: [f_max_rows]u10 = .{0} ** f_max_rows; // [from] = to circuit_id
    for (connections) |conn| {
        const jb_from = &jboxes[conn.from_idx];
        const jb_to = &jboxes[conn.to_idx];
        const max_id = @max(jb_from.id, jb_to.id);
        const min_id = @min(jb_from.id, jb_to.id);
        if (min_id != max_id) {
            var source_id = max_id;
            while (circuit_merges[source_id] > 0) source_id = circuit_merges[source_id];
            var target_id = min_id;
            while (circuit_merges[target_id] > 0) target_id = circuit_merges[target_id];
            if (source_id != target_id) {
                circuit_merges[source_id] = target_id;
                circuit_sizes[target_id] += circuit_sizes[source_id];
                circuit_sizes[source_id] = 0;
            }
        }
    }
}
