import platform
import random
import statistics
import time

from support import algorithms

SEED = 2026
RUNS = 3
SIZES = ((500, 50), (1500, 150), (3000, 300))
NAMES = ('naive', 'kmp', 'rk')


def random_case(n, m):
    rng = random.Random(SEED)
    text = ''.join(rng.choice('abcd') for _ in range(n))
    start = rng.randrange(n - m + 1)
    return text, text[start:start + m]


def repetitive_case(n, m):
    return 'a' * n, 'a' * (m - 1) + 'b'


CASES = (
    ('random', 'Random(2026), alphabet abcd, pattern cut from text', random_case),
    ('repetitive', "text a^n, pattern a^(m-1)b", repetitive_case),
)


def expected_positions(text, pattern):
    return [start for start in range(len(text) - len(pattern) + 1) if text.startswith(pattern, start)]


def measure(name, request):
    function = getattr(algorithms, name)
    function(request)
    times = []
    for _ in range(RUNS):
        started = time.perf_counter()
        result = function(request)
        times.append((time.perf_counter() - started) * 1000)
    return result['positions'], times


def main():
    print(f'Python {platform.python_version()} on {platform.platform()}, {platform.processor() or platform.machine()}')
    print('Times in milliseconds; each run times only the algorithm call, warm-up call excluded.')
    print()
    print('|Case|n|m|Seed/generator|Algorithm|Run 1|Run 2|Run 3|Median|Correct outputs checked|')
    print('|---|---:|---:|---|---|---:|---:|---:|---:|---|')
    for label, generator, build in CASES:
        for n, m in SIZES:
            text, pattern = build(n, m)
            expected = expected_positions(text, pattern)
            request = {'task': 'search', 'text': text, 'pattern': pattern}
            for name in NAMES:
                positions, times = measure(name, request)
                verdict = f'yes, z={len(expected)}' if positions == expected else 'NO'
                runs = '|'.join(f'{value:.3f}' for value in times)
                print(f'|{label}|{n}|{m}|{generator}|{name}|{runs}|{statistics.median(times):.3f}|{verdict}|')


if __name__ == '__main__':
    main()
