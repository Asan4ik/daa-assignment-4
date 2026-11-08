import itertools
import random
import unittest

from support import algorithms, is_subsequence


def brute_length(a, b):
    for size in range(min(len(a), len(b)), 0, -1):
        for indices in itertools.combinations(range(len(a)), size):
            if is_subsequence(''.join(a[i] for i in indices), b):
                return size
    return 0


def solve(a, b):
    return algorithms.lcs({'task': 'lcs', 'a': a, 'b': b})


class LcsTests(unittest.TestCase):
    def assert_valid(self, a, b, expected_length):
        result = solve(a, b)
        self.assertEqual(result['length'], expected_length)
        self.assertEqual(len(result['sequence']), expected_length)
        self.assertTrue(is_subsequence(result['sequence'], a))
        self.assertTrue(is_subsequence(result['sequence'], b))

    def test_published_example(self):
        self.assertEqual(solve('tea_time', 'team'), {'length': 4, 'sequence': 'team'})

    def test_empty_inputs(self):
        for a, b in (('', ''), ('abc', ''), ('', 'abc')):
            self.assertEqual(solve(a, b), {'length': 0, 'sequence': ''})

    def test_subsequence_is_not_substring(self):
        self.assert_valid('axbycz', 'abc', 3)

    def test_repeated_characters(self):
        self.assert_valid('aaaa', 'aa', 2)
        self.assert_valid('abcabcabc', 'cba', 3)

    def test_alternative_optima(self):
        self.assert_valid('ab', 'ba', 1)
        self.assertIn(solve('ab', 'ba')['sequence'], ('a', 'b'))

    def test_case_and_punctuation_are_ordinary(self):
        self.assert_valid('A b!', 'a B!', 2)
        self.assertEqual(solve('A b!', 'a B!')['sequence'], ' !')

    def test_no_common_characters(self):
        self.assertEqual(solve('abc', 'xyz'), {'length': 0, 'sequence': ''})

    def test_random_against_brute_force(self):
        rng = random.Random(4)
        for _ in range(300):
            a = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 8)))
            b = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 8)))
            self.assert_valid(a, b, brute_length(a, b))

    def test_maximum_domain(self):
        self.assert_valid('ab' * 500, 'ba' * 500, 999)
        self.assert_valid('x' * 1000, 'x' * 1000, 1000)


if __name__ == '__main__':
    unittest.main()
