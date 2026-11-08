# Your own tests

Run from the repository root:

    python -m unittest discover -s tests/student -v
    python tools/run.py --check
    python tests/student/benchmark_search.py

Each `test_*.py` file covers one part and compares the implementation with an independent brute-force oracle on small random inputs, plus published boundaries and maximum-size inputs. `test_process.py` sends mixed tasks through `main.py` twice in one process to detect stale state. `benchmark_search.py` prints the naive/KMP/RK comparison table for `ANALYSIS.md`.
