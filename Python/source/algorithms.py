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
    raise NotImplementedError("TODO merge")


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
