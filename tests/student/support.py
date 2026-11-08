import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'Python' / 'source'))

import algorithms


def is_subsequence(part, whole):
    chars = iter(whole)
    return all(char in chars for char in part)
