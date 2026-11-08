import random

from support import algorithms


def oracle(text, pattern):
    return [start for start in range(len(text) + 1) if text.startswith(pattern, start)]


class SearchContract:
    name = None

    def find(self, text, pattern):
        function = getattr(algorithms, self.name)
        return function({'task': self.name, 'text': text, 'pattern': pattern})['positions']

    def test_overlapping_matches(self):
        self.assertEqual(self.find('aaaaa', 'aaa'), [0, 1, 2])
        self.assertEqual(self.find('abababa', 'aba'), [0, 2, 4])

    def test_empty_pattern_matches_every_boundary(self):
        self.assertEqual(self.find('abc', ''), [0, 1, 2, 3])
        self.assertEqual(self.find('', ''), [0])

    def test_empty_text(self):
        self.assertEqual(self.find('', 'a'), [])

    def test_pattern_longer_than_text(self):
        self.assertEqual(self.find('ab', 'abc'), [])

    def test_pattern_equal_to_text(self):
        self.assertEqual(self.find('abc', 'abc'), [0])

    def test_case_and_punctuation_are_ordinary(self):
        self.assertEqual(self.find('Aa aA a.a', 'a'), [1, 3, 6, 8])
        self.assertEqual(self.find('a. b. a.', '. '), [1, 4])
        self.assertEqual(self.find('Abc', 'abc'), [])

    def test_last_valid_start(self):
        self.assertEqual(self.find('xxab', 'ab'), [2])

    def test_random_against_oracle(self):
        rng = random.Random(23)
        for alphabet in ('ab', 'abc', ''.join(chr(code) for code in range(32, 127))):
            for _ in range(300):
                text = ''.join(rng.choice(alphabet) for _ in range(rng.randint(0, 30)))
                pattern = ''.join(rng.choice(alphabet) for _ in range(rng.randint(0, 6)))
                self.assertEqual(self.find(text, pattern), oracle(text, pattern))
