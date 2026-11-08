import unittest

from search_contract import SearchContract, oracle


class NaiveTests(SearchContract, unittest.TestCase):
    name = 'naive'

    def test_quadratic_case_in_common_domain(self):
        text, pattern = 'a' * 3000, 'a' * 1499 + 'b'
        self.assertEqual(self.find(text, pattern), [])
        self.assertEqual(self.find(text, 'a' * 1500), oracle(text, 'a' * 1500))


if __name__ == '__main__':
    unittest.main()
