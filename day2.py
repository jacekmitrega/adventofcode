def is_safe(l, error_margin=1):
    it = iter(l)
    p = next(it)
    s = new_s = uninitialized = object()  # sign to be set to -1 or +1

    for i, n in enumerate(it, start=1):
        d = n - p
        absd = abs(d)
        if not (1 <= absd <= 3) or ((new_s := d / absd) != s and s is not uninitialized):
            if not error_margin:
                return False

            return (
                is_safe(l[:i] + l[i+1:], error_margin - 1)
                or is_safe(l[:i-1] + l[i:], error_margin - 1)
                or is_safe(l[:i-2] + l[i-1:], error_margin - 1)
            )
        p = n
        s = new_s
    return True

with open('input2.txt', 'r') as file:
    print(sum(1 for line in file if is_safe([int(s) for s in line.split()])))
