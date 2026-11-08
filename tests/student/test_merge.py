import random
import unittest

from support import algorithms


def brute_cost(sizes):
    if len(sizes) < 2:
        return 0
    best = None
    for i in range(len(sizes) - 1):
        joined = sizes[i] + sizes[i + 1]
        total = joined + brute_cost(sizes[:i] + [joined] + sizes[i + 2:])
        best = total if best is None else min(best, total)
    return best


def replay(sizes, plan):
    blocks = [(i, i) for i in range(len(sizes))]
    total = 0
    for left, cut, right in plan:
        index = blocks.index((left, cut))
        assert blocks[index + 1] == (cut + 1, right)
        blocks[index:index + 2] = [(left, right)]
        total += sum(sizes[left:right + 1])
    assert len(blocks) <= 1
    return total


def solve(sizes):
    return algorithms.merge({'task': 'merge', 'sizes': sizes})


class MergeTests(unittest.TestCase):
    def assert_optimal(self, sizes, expected_cost):
        result = solve(sizes)
        self.assertEqual(result['cost'], expected_cost)
        self.assertEqual(len(result['plan']), max(0, len(sizes) - 1))
        self.assertEqual(replay(sizes, result['plan']), expected_cost)

    def test_published_example(self):
        self.assertEqual(solve([2, 3, 4]), {'cost': 14, 'plan': [[0, 0, 1], [0, 1, 2]]})

    def test_zero_and_one_block(self):
        self.assertEqual(solve([]), {'cost': 0, 'plan': []})
        self.assertEqual(solve([7]), {'cost': 0, 'plan': []})

    def test_zero_sizes(self):
        self.assert_optimal([0, 0, 0, 0], 0)

    def test_adjacency_is_required(self):
        self.assert_optimal([1, 100, 1, 100], brute_cost([1, 100, 1, 100]))
        self.assert_optimal([5, 1, 5], 17)

    def test_equal_sizes_have_several_optima(self):
        self.assert_optimal([3, 3, 3, 3], 24)

    def test_random_against_brute_force(self):
        rng = random.Random(8)
        for _ in range(300):
            sizes = [rng.randint(0, 20) for _ in range(rng.randint(0, 7))]
            self.assert_optimal(sizes, brute_cost(sizes))

    def test_large_costs(self):
        sizes = [10 ** 9] * 200
        self.assert_optimal(sizes, 1544 * 10 ** 9)

    def test_plan_is_chronological(self):
        sizes = [4, 1, 7, 2, 9, 3]
        replay(sizes, solve(sizes)['plan'])


if __name__ == '__main__':
    unittest.main()
