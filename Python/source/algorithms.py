def lcs(request: dict) -> dict:
    a, b = request['a'], request['b']
    rows, cols = len(a) + 1, len(b) + 1
    table = [[0] * cols for _ in range(rows)]
    for i in range(1, rows):
        for j in range(1, cols):
            if a[i - 1] == b[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    letters = []
    i, j = rows - 1, cols - 1
    while i and j:
        if a[i - 1] == b[j - 1]:
            letters.append(a[i - 1])
            i -= 1
            j -= 1
        elif table[i - 1][j] >= table[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return {'length': table[-1][-1], 'sequence': ''.join(reversed(letters))}


def merge(request: dict) -> dict:
    sizes = request['sizes']
    count = len(sizes)
    if count < 2:
        return {'cost': 0, 'plan': []}
    prefix = [0]
    for size in sizes:
        prefix.append(prefix[-1] + size)
    cost = [[0] * count for _ in range(count)]
    split = [[0] * count for _ in range(count)]
    for length in range(2, count + 1):
        for left in range(count - length + 1):
            right = left + length - 1
            best, cut = min((cost[left][k] + cost[k + 1][right], k) for k in range(left, right))
            cost[left][right] = best + prefix[right + 1] - prefix[left]
            split[left][right] = cut
    plan = []
    stack = [(0, count - 1, False)]
    while stack:
        left, right, ready = stack.pop()
        if left == right:
            continue
        cut = split[left][right]
        if ready:
            plan.append([left, cut, right])
        else:
            stack.append((left, right, True))
            stack.append((cut + 1, right, False))
            stack.append((left, cut, False))
    return {'cost': cost[0][count - 1], 'plan': plan}


def tree(request: dict) -> dict:
    raise NotImplementedError("TODO tree")


def naive(request: dict) -> dict:
    raise NotImplementedError("TODO naive")


def kmp(request: dict) -> dict:
    raise NotImplementedError("TODO kmp")


def rk(request: dict) -> dict:
    raise NotImplementedError("TODO rk")


def suffix(request: dict) -> dict:
    raise NotImplementedError("TODO suffix")


def aho(request: dict) -> dict:
    raise NotImplementedError("TODO aho")
