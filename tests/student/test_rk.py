import random
import unittest

from search_contract import SearchContract, oracle
from support import algorithms


def fingerprint(word):
    value = 0
    for char in word:
        value = (value * 31 + ord(char)) % 101
    return value


class RkTests(SearchContract, unittest.TestCase):
    name = 'rk'

    def test_known_collision_is_verified(self):
        self.assertEqual(fingerprint('ab'), fingerprint('dj'))
        self.assertEqual(self.find('abdj', 'ab'), [0])
        self.assertEqual(self.find('abdj', 'dj'), [2])
        self.assertEqual(self.find('djdjab', 'ab'), [4])

    def test_every_candidate_window_is_checked(self):
        text = 'abdjdjabdj'
        self.assertEqual(self.find(text, 'dj'), oracle(text, 'dj'))

    def test_rolling_update_with_large_leading_character(self):
        text = '~~~ ~ ~~ ~ '
        for pattern in ('~ ', ' ~', '~~ ', ' ~ ~'):
            self.assertEqual(self.find(text, pattern), oracle(text, pattern))

    def test_maximum_domain(self):
        text = 'a' * 10000
        self.assertEqual(self.find(text, 'a' * 2000), list(range(8001)))
        self.assertEqual(self.find(text, 'a' * 1999 + 'b'), [])


class AgreementTests(unittest.TestCase):
    def test_all_searches_agree_on_common_domain(self):
        rng = random.Random(47)
        for alphabet in ('ab', 'abcdefgh'):
            text = ''.join(rng.choice(alphabet) for _ in range(3000))
            for size in (1, 2, 7, 50, 300):
                start = rng.randrange(3000 - size + 1)
                pattern = text[start:start + size]
                request = {'task': 'x', 'text': text, 'pattern': pattern}
                expected = oracle(text, pattern)
                for name in ('naive', 'kmp', 'rk'):
                    self.assertEqual(getattr(algorithms, name)(request)['positions'], expected)


if __name__ == '__main__':
    unittest.main()
