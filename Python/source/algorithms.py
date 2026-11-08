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
    count = request['n']
    if count == 0:
        return {'weight': 0, 'selected': []}
    neighbours = [[] for _ in range(count)]
    for u, v in request['edges']:
        neighbours[u].append(v)
        neighbours[v].append(u)
    parent = [-1] * count
    order = [0]
    for vertex in order:
        for other in neighbours[vertex]:
            if other != parent[vertex]:
                parent[other] = vertex
                order.append(other)
    take = list(request['weights'])
    skip = [0] * count
    for vertex in reversed(order):
        up = parent[vertex]
        if up >= 0:
            take[up] += skip[vertex]
            skip[up] += max(take[vertex], skip[vertex])
    chosen = [False] * count
    for vertex in order:
        up = parent[vertex]
        blocked = up >= 0 and chosen[up]
        chosen[vertex] = not blocked and take[vertex] > skip[vertex]
    return {
        'weight': max(take[0], skip[0]),
        'selected': [vertex for vertex in range(count) if chosen[vertex]],
    }


def naive(request: dict) -> dict:
    text, pattern = request['text'], request['pattern']
    size = len(pattern)
    positions = []
    for start in range(len(text) - size + 1):
        offset = 0
        while offset < size and text[start + offset] == pattern[offset]:
            offset += 1
        if offset == size:
            positions.append(start)
    return {'positions': positions}


def prefix_function(pattern: str) -> list:
    pi = [0] * len(pattern)
    matched = 0
    for i in range(1, len(pattern)):
        while matched and pattern[i] != pattern[matched]:
            matched = pi[matched - 1]
        if pattern[i] == pattern[matched]:
            matched += 1
        pi[i] = matched
    return pi


def kmp(request: dict) -> dict:
    text, pattern = request['text'], request['pattern']
    size = len(pattern)
    if size == 0:
        return {'positions': list(range(len(text) + 1))}
    pi = prefix_function(pattern)
    positions = []
    matched = 0
    for i, char in enumerate(text):
        while matched and char != pattern[matched]:
            matched = pi[matched - 1]
        if char == pattern[matched]:
            matched += 1
        if matched == size:
            positions.append(i - size + 1)
            matched = pi[matched - 1]
    return {'positions': positions}


BASE = 31
MODULUS = 101


def rk(request: dict) -> dict:
    text, pattern = request['text'], request['pattern']
    length, size = len(text), len(pattern)
    if size == 0:
        return {'positions': list(range(length + 1))}
    if size > length:
        return {'positions': []}
    lead = pow(BASE, size - 1, MODULUS)
    target = window = 0
    for i in range(size):
        target = (target * BASE + ord(pattern[i])) % MODULUS
        window = (window * BASE + ord(text[i])) % MODULUS
    positions = []
    for start in range(length - size + 1):
        if window == target and text[start:start + size] == pattern:
            positions.append(start)
        if start + size < length:
            window = ((window - ord(text[start]) * lead) * BASE + ord(text[start + size])) % MODULUS
    return {'positions': positions}


def suffix(request: dict) -> dict:
    raise NotImplementedError("TODO suffix")


def aho(request: dict) -> dict:
    raise NotImplementedError("TODO aho")
