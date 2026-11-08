import random
import unittest

from search_contract import SearchContract, oracle


class KmpTests(SearchContract, unittest.TestCase):
    name = 'kmp'

    def test_fallback_after_full_match(self):
        self.assertEqual(self.find('aabaabaaab', 'aabaa'), [0, 3])
        self.assertEqual(self.find('abababab', 'abab'), [0, 2, 4])

    def test_pattern_with_long_borders(self):
        self.assertEqual(self.find('aaabaaaabaaaa', 'aaaab'), [4])
        self.assertEqual(self.find('abcabcabcabd', 'abcabd'), [6])

    def test_maximum_domain(self):
        text = 'a' * 200000
        self.assertEqual(self.find(text, 'a' * 100000), list(range(100001)))
        self.assertEqual(self.find(text, 'a' * 99999 + 'b'), [])

    def test_large_random_against_oracle(self):
        rng = random.Random(31)
        text = ''.join(rng.choice('ab') for _ in range(3000))
        for size in (1, 5, 12, 40):
            pattern = text[500:500 + size]
            self.assertEqual(self.find(text, pattern), oracle(text, pattern))


if __name__ == '__main__':
    unittest.main()
