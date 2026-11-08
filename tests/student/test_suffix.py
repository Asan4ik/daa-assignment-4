import random
import unittest

from support import algorithms


def solve(text):
    return algorithms.suffix({'task': 'suffix', 'text': text})


def common_prefix(a, b):
    size = 0
    while size < min(len(a), len(b)) and a[size] == b[size]:
        size += 1
    return size


def expected_arrays(text):
    sa = sorted(range(len(text)), key=lambda i: text[i:])
    lcp = [0] + [common_prefix(text[sa[i - 1]:], text[sa[i]:]) for i in range(1, len(sa))]
    return sa, lcp


def longest_repeat_length(text):
    best = 0
    for i in range(len(text)):
        for j in range(i + 1, len(text)):
            best = max(best, common_prefix(text[i:], text[j:]))
    return best


def occurrences(text, part):
    return sum(text.startswith(part, start) for start in range(len(text)))


class SuffixTests(unittest.TestCase):
    def assert_valid(self, text):
        result = solve(text)
        sa, lcp = expected_arrays(text)
        self.assertEqual(result['sa'], sa)
        self.assertEqual(result['lcp'], lcp)
        self.assertEqual(len(result['repeated']), longest_repeat_length(text))
        if result['repeated']:
            self.assertGreaterEqual(occurrences(text, result['repeated']), 2)

    def test_published_example(self):
        self.assertEqual(
            solve('banana'),
            {'sa': [5, 3, 1, 0, 4, 2], 'lcp': [0, 1, 3, 0, 0, 2], 'repeated': 'ana'},
        )

    def test_empty_and_single_character(self):
        self.assertEqual(solve(''), {'sa': [], 'lcp': [], 'repeated': ''})
        self.assertEqual(solve('x'), {'sa': [0], 'lcp': [0], 'repeated': ''})

    def test_all_equal_characters(self):
        self.assertEqual(
            solve('aaaa'),
            {'sa': [3, 2, 1, 0], 'lcp': [0, 1, 2, 3], 'repeated': 'aaa'},
        )

    def test_all_distinct_characters(self):
        self.assertEqual(solve('dcba'), {'sa': [3, 2, 1, 0], 'lcp': [0, 0, 0, 0], 'repeated': ''})

    def test_tied_longest_repeats(self):
        text = 'abcabcxyzxyz'
        result = solve(text)
        self.assertEqual(len(result['repeated']), 3)
        self.assertGreaterEqual(occurrences(text, result['repeated']), 2)

    def test_spaces_and_case_are_ordinary(self):
        self.assert_valid('Ab ab AB ab')

    def test_random_against_oracle(self):
        rng = random.Random(61)
        for alphabet in ('a', 'ab', 'abc'):
            for _ in range(200):
                text = ''.join(rng.choice(alphabet) for _ in range(rng.randint(1, 14)))
                self.assert_valid(text)

    def test_medium_random_text(self):
        rng = random.Random(62)
        self.assert_valid(''.join(rng.choice('ab') for _ in range(400)))

    def test_maximum_domain(self):
        for text, repeat in (('a' * 50000, 49999), ('ab' * 25000, 49998)):
            result = solve(text)
            sa = result['sa']
            self.assertEqual(sorted(sa), list(range(50000)))
            self.assertTrue(all(text[sa[i - 1]:] < text[sa[i]:] for i in range(1, len(sa))))
            self.assertEqual(len(result['repeated']), repeat)


if __name__ == '__main__':
    unittest.main()
