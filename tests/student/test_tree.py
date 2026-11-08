import random
import unittest

from support import algorithms


def brute_weight(count, weights, edges):
    best = 0
    for mask in range(1 << count):
        if any(mask >> u & 1 and mask >> v & 1 for u, v in edges):
            continue
        best = max(best, sum(weights[v] for v in range(count) if mask >> v & 1))
    return best


def solve(weights, edges):
    return algorithms.tree({'task': 'tree', 'n': len(weights), 'weights': weights, 'edges': edges})


def random_tree(rng, count):
    return [[rng.randrange(v), v] for v in range(1, count)]


class TreeTests(unittest.TestCase):
    def assert_valid(self, weights, edges, expected_weight):
        result = solve(weights, edges)
        selected = result['selected']
        self.assertEqual(result['weight'], expected_weight)
        self.assertEqual(len(set(selected)), len(selected))
        self.assertEqual(sum(weights[v] for v in selected), expected_weight)
        chosen = set(selected)
        self.assertFalse(any(u in chosen and v in chosen for u, v in edges))

    def test_published_example(self):
        self.assertEqual(solve([4, 9, 6], [[0, 1], [1, 2]]), {'weight': 10, 'selected': [0, 2]})

    def test_empty_and_single_vertex(self):
        self.assertEqual(solve([], []), {'weight': 0, 'selected': []})
        self.assertEqual(solve([5], []), {'weight': 5, 'selected': [0]})
        self.assertEqual(solve([-5], []), {'weight': 0, 'selected': []})

    def test_all_negative(self):
        self.assert_valid([-3, -1, -2], [[0, 1], [1, 2]], 0)

    def test_zero_weights_and_ties(self):
        self.assert_valid([0, 0, 0, 0], [[0, 1], [1, 2], [2, 3]], 0)
        self.assert_valid([5, 5], [[0, 1]], 5)

    def test_random_trees_against_brute_force(self):
        rng = random.Random(15)
        for _ in range(300):
            count = rng.randint(1, 10)
            weights = [rng.randint(-5, 9) for _ in range(count)]
            edges = random_tree(rng, count)
            self.assert_valid(weights, edges, brute_weight(count, weights, edges))

    def test_relabelling_does_not_change_optimum(self):
        rng = random.Random(16)
        for _ in range(100):
            count = rng.randint(2, 10)
            weights = [rng.randint(-5, 9) for _ in range(count)]
            edges = random_tree(rng, count)
            mapping = list(range(count))
            rng.shuffle(mapping)
            moved_weights = [0] * count
            for v in range(count):
                moved_weights[mapping[v]] = weights[v]
            moved_edges = [[mapping[u], mapping[v]] for u, v in edges]
            self.assertEqual(solve(weights, edges)['weight'], solve(moved_weights, moved_edges)['weight'])

    def test_deep_chain(self):
        count = 100000
        edges = [[v, v + 1] for v in range(count - 1)]
        self.assert_valid([1] * count, edges, count // 2)

    def test_large_sum(self):
        count = 100000
        weights = [1] + [10 ** 9] * (count - 1)
        edges = [[0, v] for v in range(1, count)]
        self.assert_valid(weights, edges, (count - 1) * 10 ** 9)


if __name__ == '__main__':
    unittest.main()
