import random
import unittest

from support import algorithms


def solve(patterns, texts):
    return algorithms.aho({'task': 'aho', 'patterns': patterns, 'texts': texts})['counts']


def count(text, pattern):
    return sum(text.startswith(pattern, start) for start in range(len(text)))


def expected(patterns, texts):
    return [[count(text, pattern) for pattern in patterns] for text in texts]


class AhoTests(unittest.TestCase):
    def test_published_example(self):
        self.assertEqual(
            solve(['he', 'she', 'he'], ['sheshe', 'sheshe', '']),
            [[2, 2, 2], [2, 2, 2], [0, 0, 0]],
        )

    def test_empty_dictionary(self):
        self.assertEqual(solve([], ['abc', '']), [[], []])

    def test_empty_texts(self):
        self.assertEqual(solve(['a'], []), [])

    def test_empty_text_gives_zero_row(self):
        self.assertEqual(solve(['a', 'b', 'c'], ['']), [[0, 0, 0]])

    def test_suffix_patterns_and_overlaps(self):
        self.assertEqual(solve(['a', 'aa', 'aaa'], ['aaaa']), [[4, 3, 2]])
        self.assertEqual(solve(['abab', 'bab', 'ab'], ['ababab']), [[2, 2, 3]])

    def test_duplicate_patterns_have_equal_counts(self):
        self.assertEqual(solve(['x', 'x', 'xx'], ['xxx']), [[3, 3, 2]])

    def test_pattern_contained_in_another(self):
        self.assertEqual(solve(['hers', 'he', 'her', 's'], ['ushers']), [[1, 1, 1, 2]])

    def test_case_and_punctuation_are_ordinary(self):
        self.assertEqual(solve(['A', 'a', ' ', '.'], ['Aa a.']), [[1, 2, 1, 1]])

    def test_requests_are_independent(self):
        first = solve(['ab'], ['abab'])
        solve(['zz', 'ab', 'b'], ['zzabzz'])
        self.assertEqual(solve(['ab'], ['abab']), first)

    def test_random_against_oracle(self):
        rng = random.Random(77)
        for alphabet in ('ab', 'abc'):
            for _ in range(300):
                patterns = [
                    ''.join(rng.choice(alphabet) for _ in range(rng.randint(1, 4)))
                    for _ in range(rng.randint(0, 6))
                ]
                texts = [
                    ''.join(rng.choice(alphabet) for _ in range(rng.randint(0, 20)))
                    for _ in range(rng.randint(0, 4))
                ]
                self.assertEqual(solve(patterns, texts), expected(patterns, texts))

    def test_dense_matches(self):
        patterns = ['a' * size for size in range(1, 441)]
        texts = ['a' * 2000] * 100
        counts = solve(patterns, texts)
        row = [max(0, 2000 - size + 1) for size in range(1, 441)]
        self.assertEqual(counts, [row] * 100)

    def test_large_dictionary(self):
        rng = random.Random(78)
        patterns = [''.join(rng.choice('abcd') for _ in range(10)) for _ in range(10000)]
        texts = [''.join(rng.choice('abcd') for _ in range(2000)) for _ in range(100)]
        counts = solve(patterns, texts)
        for index in rng.sample(range(10000), 10):
            for row, text in zip(counts[:5], texts[:5]):
                self.assertEqual(row[index], count(text, patterns[index]))


if __name__ == '__main__':
    unittest.main()
