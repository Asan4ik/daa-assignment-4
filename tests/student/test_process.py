import json
import subprocess
import sys
import unittest

from support import ROOT, algorithms

MAIN = ROOT / 'Python' / 'source' / 'main.py'

REQUESTS = [
    {'task': 'ping'},
    {'task': 'lcs', 'a': 'tea_time', 'b': 'team'},
    {'task': 'aho', 'patterns': ['he', 'she', 'he'], 'texts': ['sheshe', '']},
    {'task': 'merge', 'sizes': [2, 3, 4]},
    {'task': 'suffix', 'text': 'banana'},
    {'task': 'tree', 'n': 3, 'weights': [4, 9, 6], 'edges': [[0, 1], [1, 2]]},
    {'task': 'rk', 'text': 'abdj', 'pattern': 'ab'},
    {'task': 'kmp', 'text': 'abababa', 'pattern': 'aba'},
    {'task': 'naive', 'text': 'aaaaa', 'pattern': 'aaa'},
    {'task': 'aho', 'patterns': [], 'texts': ['abc']},
    {'task': 'suffix', 'text': ''},
]


def run_batch(requests):
    data = ''.join(json.dumps(request) + '\n' for request in requests)
    result = subprocess.run(
        [sys.executable, str(MAIN)], input=data, capture_output=True, text=True, timeout=60, check=True
    )
    return [json.loads(line) for line in result.stdout.splitlines()]


class ProcessTests(unittest.TestCase):
    def test_mixed_tasks_match_direct_calls(self):
        answers = run_batch(REQUESTS)
        expected = [{'status': 'ready'}] + [
            getattr(algorithms, request['task'])(request) for request in REQUESTS[1:]
        ]
        self.assertEqual(answers, expected)

    def test_repeated_batch_has_no_stale_state(self):
        answers = run_batch(REQUESTS + REQUESTS)
        self.assertEqual(answers[:len(REQUESTS)], answers[len(REQUESTS):])

    def test_one_result_line_per_request(self):
        self.assertEqual(len(run_batch(REQUESTS)), len(REQUESTS))


if __name__ == '__main__':
    unittest.main()
