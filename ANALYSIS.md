# Assignment 4 — analysis

## Environment and commands

- Language: Python 3.14.7 (CPython, default interpreter, no JIT enabled). No compilation step.
- OS/CPU/RAM: Windows 11 (10.0.26300), AMD64 (AMD Family 25 Model 68), <CPU MODEL>, <RAM> GB.
- Setup check: `python tools/run.py --setup`
- Public checks (44 public cases and the repeated mixed batch): `python tools/run.py --check`
- Own tests: `python -m unittest discover -s tests/student -v`
- Search comparison: `python tests/student/benchmark_search.py`
- Final commit URL is recorded in Moodle.

## Algorithm explanations

All algorithms live in `Python/source/algorithms.py`. Each takes the request dictionary and returns the result dictionary. Python integers are arbitrary precision, so costs and weights cannot overflow.

### lcs

- State: `table[i][j]` is the length of an LCS of the prefixes `a[:i]` and `b[:j]`.
- Base cases: `table[0][j] = table[i][0] = 0`, so empty inputs give length 0 and an empty sequence.
- Transition: if `a[i-1] == b[j-1]` then `table[i-1][j-1] + 1`, otherwise `max(table[i-1][j], table[i][j-1])`.
- Order: row by row, left to right. The three cells a cell depends on are already filled.
- Correctness: when the last characters are equal, some optimal subsequence matches them (exchange argument), so taking the diagonal is safe. When they differ, at least one of them is unused by any LCS, so the better of the two shorter problems is optimal.
- Reconstruction: walk from `(|a|, |b|)`. On equal characters emit the character and move diagonally; otherwise move to the neighbour with the larger value. Ties move up (`i - 1`), so one particular optimal sequence is returned. The collected letters are reversed at the end.
- Cost: O((|a|+1)(|b|+1)) time and memory for the table, O(length) for the output.
- Boundary test: `axbycz` against `abc` must return 3 (subsequence, not substring); a contiguous-match implementation returns 1.

### merge

- State: `cost[l][r]` is the minimum total cost of merging the original blocks `l..r` into one block. `split[l][r]` stores the best last split `k`.
- Base case: `cost[i][i] = 0`. For fewer than two blocks the answer is cost 0 and an empty plan.
- Transition: `cost[l][r] = min over l <= k < r of cost[l][k] + cost[k+1][r] + S(l, r)`, where `S(l, r)` is the total size of the interval, taken from prefix sums. The final merge of the interval joins `[l, k]` and `[k+1, r]` and pays `S(l, r)`.
- Order: by increasing interval length, so both sub-intervals are ready.
- Correctness: any merge process on an interval ends with one merge of two adjacent blocks covering a prefix and a suffix of it. Each side is an independent subproblem, so the optimal substructure holds. Adjacency is built in, because only contiguous splits are considered.
- Reconstruction: an explicit stack performs a post-order walk. A node is pushed back with a "ready" flag, then its right child and left child are pushed, so both children are emitted before the parent. This gives a chronological plan with exactly n-1 merges. Ties pick the smallest `k` because the minimum is taken over `(value, k)` pairs.
- Cost: O(n^3) time (about n^3/6 split candidates) and O(n^2) memory for `cost` and `split`.
- Boundary test: `[1, 100, 1, 100]` is compared with a brute-force search over all adjacent merge orders. A greedy "merge the two smallest blocks" would pair the two non-adjacent ones. 200 blocks of 10^9 give 1544·10^9, which does not fit in 32 bits.

### tree

- State: `take[v]` is the best weight in the subtree of `v` if `v` is selected, `skip[v]` if it is not.
- Base: a leaf has `take = w[v]` and `skip = 0`. Recurrence: `take[v] = w[v] + sum(skip[c])` and `skip[v] = sum(max(take[c], skip[c]))` over children `c`.
- Order: a breadth-first traversal from vertex 0 records parents and an order in which parents precede children. Processing that order in reverse is a post-order, so every child is final before it is added to its parent. No recursion is used, so a chain of 100000 vertices is safe.
- Answer: `max(take[root], skip[root])`. The empty set is allowed, so negative weights are simply never taken.
- Reconstruction: process the vertices in breadth-first order (parents first). A vertex is blocked if its parent was chosen; otherwise it is chosen exactly when `take > skip`. Ties choose "skip". This is how the parent's decision restricts the children, and it yields an independent set whose weight equals the optimum.
- Cost: O(n) time and memory (adjacency lists, parent, order, two value arrays). `n = 0` returns early.
- Boundary test: a 100000-vertex chain (detects recursion failure; expected weight 50000) and a star whose total exceeds 32 bits. Relabelling vertices randomly must not change the optimum.

### naive

- For every start `0..n-m`, compare characters one by one and record the start if all `m` match. Overlaps are found because every start is tried.
- Empty pattern: the range is `0..n`, the inner loop ends immediately and every boundary (including `n`) is recorded. A pattern longer than the text gives an empty range, so the result is `[]`.
- Invariant: when the inner loop stops, `offset` characters of the window equal the pattern prefix; a match is exactly `offset == m`.
- Cost: O(n·m) comparisons plus output (the empty pattern outputs n+1 starts); O(1) auxiliary memory besides the output list. No built-in search is used.
- Boundary test: the last valid start (`xxab`, `ab` gives `[2]`) detects an off-by-one in the range; an empty pattern detects a missing final boundary.

### kmp

- `pi[i]` is the length of the longest proper prefix of `pattern[:i+1]` that is also a suffix of it. It is built by the same matching loop applied to the pattern against itself: on a mismatch, fall back to `pi[matched - 1]`.
- Search: keep `matched`, the length of the longest pattern prefix that ends at the current text position. On a mismatch fall back with `matched = pi[matched - 1]` until the characters agree or `matched` is 0. When `matched == m`, record `i - m + 1` and continue with `matched = pi[m - 1]`, which keeps the overlapping matches.
- Amortisation: `matched` grows by at most one per text character and every fallback shrinks it, so the number of fallbacks is at most n. Time is O(n + m + z); auxiliary memory is O(m) for `pi`.
- The empty pattern returns all n+1 boundaries before any pattern indexing.
- Boundary test: `aabaabaaab` with `aabaa` must give `[0, 3]`. Resetting `matched` to 0 after a full match would miss start 3.

### rk

- Hash: `H(s) = sum(s[i] * 31^(m-1-i)) mod 101` using ASCII codes, so the leftmost character has the highest power.
- Rolling update: `H' = ((H - code(out) * 31^(m-1)) * 31 + code(in)) mod 101`, with `31^(m-1) mod 101` computed once by `pow`. Python's `%` always returns a non-negative result for a positive modulus, so negative intermediate values are normalised automatically.
- Equal hashes are only candidates: before reporting a start, the window `text[start:start+m]` is compared with the pattern character by character (string equality, not a search function). This removes false positives caused by the small modulus.
- Empty pattern and `m > n` are handled before any window is formed.
- Cost: O(n + m + c·m), where c is the number of equal-hash windows. With modulus 101 many windows can collide, and for repetitive input every window can be a candidate, so the safe bound over the whole domain is O(n·m + n + m + 1). It is not linear in the worst case. Auxiliary memory is O(m) (the window slice) plus the output.
- Boundary test: `ab` and `dj` both hash to 75, so `abdj` with `ab` must give `[0]` and with `dj` must give `[2]`. This detects a missing verification step.

### suffix

Prefix doubling:

- After round k, `rank[i]` is the equivalence class (in sorted order) of the first 2^k characters of suffix `i`; equal prefixes share a rank. Initial ranks are the character codes (one character).
- A round sorts suffixes by the pair `(rank[i], rank[i + step])`, where a missing second half counts as -1 so that a shorter suffix sorts first. The new rank increases by one whenever the pair differs from the previous suffix's pair. Then `step` doubles. Pairs of ranks describe 2·step characters because the second rank describes the next `step` characters.
- The loop stops when the largest rank is n-1, i.e. all ranks are distinct. The ranks are then the inverse permutation of `sa`, which Kasai needs.
- Cost: at most about log2(n) + 1 rounds, each with a comparison sort in O(n log n), so O(n log² n) time and O(n) memory. Python's sort with a key function is used. No sentinel and no suffix strings are materialised.

Kasai:

- `lcp[rank[i]]` is the common prefix length of suffix `i` and the suffix just before it in `sa`. Suffixes are visited in text order. If suffix `i` has common prefix `h` with its predecessor, then suffix `i+1` has at least `h - 1` with its own predecessor, so `h` is decreased by one and extended, never restarted. Total increments are bounded by about 2n, so Kasai is O(n). For `rank[i] == 0` there is no predecessor, so `h` is reset to 0.

Longest repeat:

- A substring with two occurrences is a common prefix of two suffixes. The LCP of two suffixes is the minimum of the adjacent LCPs between them, so the maximum is reached by an adjacent pair. The answer is `text[sa[p] : sa[p] + lcp[p]]` for the first position `p` of the maximum; overlaps are allowed. If the maximum is 0 the result is empty. Empty text returns early.
- Boundary test: `aaaa` (all equal, needs several doubling rounds) must give `sa=[3,2,1,0]`, `lcp=[0,1,2,3]`, repeated `aaa`; `banana` gives `ana` (overlapping occurrences). The tests compare `sa` and `lcp` with a sort of the actual suffixes and a direct prefix comparison.

### aho

- Trie: one dictionary of children per state (the alphabet is the printable ASCII characters). `terminal[i]` is the state of dictionary entry `i`, so duplicate patterns share one state but keep their own position in the output.
- Failure link of a state: the state of the longest proper suffix of its string that is also in the trie. Links are computed in breadth-first order: for child `c` of state `s` reached by character `x`, follow the failure chain from `fail[s]` until a transition on `x` exists (`advance`). Children of the root get link 0.
- Matching: from the current state follow failure links until a transition on the text character exists, then move; add one visit to the reached state.
- Counting: a visit to state `s` means that every string on the failure chain of `s` (all suffixes that are patterns) also ends at this text position. After the text is consumed, visits are propagated in reverse breadth-first order with `visits[fail[s]] += visits[s]`, so each state's total counts every occurrence of its string. The count of dictionary entry `i` is `visits[terminal[i]]`. Duplicates therefore receive equal counts and suffix patterns (such as `he` inside `she`) are counted.
- Independence: `visits` is created fresh for every text and the matching state starts at the root, so texts do not affect each other. Nothing is kept between requests.
- Edge cases: an empty dictionary gives an empty row per text; no texts gives `[]`; an empty text gives one zero per dictionary entry.
- Cost: building is O(L + p) amortised for L total pattern length (dictionary children instead of a 95-wide table; memory O(S + p)). Each text costs O(|text| + S + p) amortised, because failure walking is bounded by the depth gained, plus the propagation pass over all states. Output is O(q·p) for q texts. No list of individual matches is created.
- Boundary test: patterns `a`, `aa`, `aaa` in `aaaa` give `[4, 3, 2]` (overlaps and suffixes); `x`, `x`, `xx` in `xxx` give `[3, 3, 2]` (duplicates). A dense test uses 440 patterns `a^k` on 100 texts of length 2000.

## Own tests

All tests are in `tests/student`. Small random inputs are checked against independently written oracles (brute-force enumeration or `str.startswith` / sorting of real suffixes). The tests also cover maximum-size inputs. The command for every row except the last is `python -m unittest discover -s tests/student -v`; the file column shows which part it covers.

|Command|Input or fixture path|Expected result|Actual result / log|What it checks|
|---|---|---|---|---|
|unittest|`test_lcs.py` (9 tests)|Published example, empty inputs, `axbycz`/`abc`, repeated characters, `ab`/`ba`, 300 random pairs vs brute force, 1000x1000 domain|OK|Wrong base case, substring instead of subsequence, invalid witness|
|unittest|`test_merge.py` (8 tests)|`[2,3,4]` cost 14, 0/1 blocks, zeros, `[1,100,1,100]`, 300 random lists vs brute force over adjacent merge orders, 200 blocks of 10^9|OK|Non-adjacent merging, plan order (children before parent), 32-bit overflow|
|unittest|`test_tree.py` (8 tests)|`n=0`, one vertex, all negative, zero ties, 300 random trees vs subset enumeration, relabelling, chain of 100000, star with sum above 2^32|OK|Recursion failure, adjacent selected vertices, root dependence, negative handling|
|unittest|`test_naive.py` (9 tests)|Shared search contract plus `a^3000` vs `a^1499 b`|OK|Overlaps, empty pattern (n+1 starts), empty text, longer pattern, last start|
|unittest|`test_kmp.py` (12 tests)|Shared contract, fallback after full match, long borders, `a^200000` vs `a^100000`|OK|Missing overlap after a match, wrong `pi`, linear-time behaviour|
|unittest|`test_rk.py` (13 tests)|Shared contract, `ab`/`dj` collision, `~` heavy rolling window, `a^10000` vs `a^2000`, naive/KMP/RK agreement on n=3000|OK|Missing verification, negative remainder handling, disagreement between the three searches|
|unittest|`test_suffix.py` (9 tests)|Empty, one character, `aaaa`, `dcba`, `banana`, tied repeats, 600 random texts vs sorted suffixes, `a^50000`, `(ab)^25000`|OK|Wrong ordering or LCP, sentinel added, repeat validity, doubling termination|
|unittest|`test_aho.py` (12 tests)|Published example, empty dictionary/texts/text, suffix patterns, duplicates, case and punctuation, 600 random cases vs counting oracle, dense and 10000-pattern cases|OK|Missing suffix counts, duplicate handling, stale counts between texts|
|unittest|`test_process.py` (3 tests)|Mixed tasks through `main.py`, run twice in one process|OK|State reset, one output line per request, agreement with direct calls|
|`python tools/run.py --check`|`tests/public.json`|All 44 public cases and the repeated batch pass|PASS (all lines)|Contract format and state reset|

## Search comparison

Setup: the same inputs are given to naive, KMP and RK in the common domain (n, m ≤ 3000). Two cases are measured separately. `random`: text from `random.Random(2026)` over the alphabet `abcd`, with the pattern cut from the text at a random position, so each pattern occurs at least once (z = 1). `repetitive`: text `a^n` and pattern `a^(m-1)b`, which never matches but forces naive to compare almost m characters at every start. Before timing, each output is compared with an independent `startswith` oracle (column "Correct outputs checked"); all outputs were correct. Timing scope: only the call of the algorithm function is timed with `time.perf_counter`; JSON parsing is excluded. One untimed warm-up call is made first (CPython has no JIT warm-up in the default build, so this only warms caches), then three timed runs. Times are in milliseconds.

|Case|n|m|Seed/generator|Algorithm|Run 1|Run 2|Run 3|Median|Correct outputs checked|
|---|---:|---:|---|---|---:|---:|---:|---:|---|
|random|500|50|Random(2026), alphabet abcd, pattern cut from text|naive|0.046|0.045|0.044|0.045|yes, z=1|
|random|500|50|Random(2026), alphabet abcd, pattern cut from text|kmp|0.090|0.086|0.083|0.086|yes, z=1|
|random|500|50|Random(2026), alphabet abcd, pattern cut from text|rk|0.079|0.078|0.076|0.078|yes, z=1|
|random|1500|150|Random(2026), alphabet abcd, pattern cut from text|naive|0.131|0.131|0.131|0.131|yes, z=1|
|random|1500|150|Random(2026), alphabet abcd, pattern cut from text|kmp|0.126|0.125|0.124|0.125|yes, z=1|
|random|1500|150|Random(2026), alphabet abcd, pattern cut from text|rk|0.234|0.233|0.233|0.233|yes, z=1|
|random|3000|300|Random(2026), alphabet abcd, pattern cut from text|naive|0.261|0.261|0.267|0.261|yes, z=1|
|random|3000|300|Random(2026), alphabet abcd, pattern cut from text|kmp|0.472|0.245|0.245|0.245|yes, z=1|
|random|3000|300|Random(2026), alphabet abcd, pattern cut from text|rk|0.467|0.466|0.468|0.467|yes, z=1|
|repetitive|500|50|text a^n, pattern a^(m-1)b|naive|1.249|1.236|1.228|1.236|yes, z=0|
|repetitive|500|50|text a^n, pattern a^(m-1)b|kmp|0.137|0.136|0.134|0.136|yes, z=0|
|repetitive|500|50|text a^n, pattern a^(m-1)b|rk|0.074|0.073|0.073|0.073|yes, z=0|
|repetitive|1500|150|text a^n, pattern a^(m-1)b|naive|11.195|11.128|11.234|11.195|yes, z=0|
|repetitive|1500|150|text a^n, pattern a^(m-1)b|kmp|0.347|0.203|0.202|0.203|yes, z=0|
|repetitive|1500|150|text a^n, pattern a^(m-1)b|rk|0.317|0.228|0.227|0.228|yes, z=0|
|repetitive|3000|300|text a^n, pattern a^(m-1)b|naive|45.947|46.562|46.511|46.511|yes, z=0|
|repetitive|3000|300|text a^n, pattern a^(m-1)b|kmp|0.668|0.442|0.439|0.442|yes, z=0|
|repetitive|3000|300|text a^n, pattern a^(m-1)b|rk|0.457|0.456|0.463|0.457|yes, z=0|

Observations (these are measurements from one machine and are not a proof of asymptotic complexity):

- On random text, naive is faster than KMP at n = 500 (0.045 ms against 0.086 ms) and about equal to it at n = 1500 and n = 3000. A random window usually fails at the first or second character, so naive does close to n comparisons, and KMP and RK pay a constant-factor cost per character in interpreted Python (the `pi` table, the fallback loop, the hash arithmetic). RK is the slowest here, roughly twice naive at n = 3000.
- On the repetitive case naive grows with the product n·m: its median rose from 1.236 ms to 11.195 ms and 46.511 ms while n·m grew from 25,000 to 225,000 and 900,000. KMP and RK stay below 0.5 ms for these inputs, which matches their O(n + m) behaviour when few windows are candidates. I did not count the equal-hash candidates in this run.
- The modulus 101 is deliberately small, so false candidates exist (`ab` and `dj` collide). Each candidate costs an O(m) verification, which is why the RK bound is O(n + m + c·m) and can degrade to O(n·m) when many windows are candidates. This applies to this small modulus; it says nothing about production hash implementations with large moduli.
- Run-to-run variation is small. The first run of some rows is slightly slower (for example KMP 0.472 ms against 0.245 ms), which I treat as noise from caches and the operating system rather than an algorithmic effect.

## Sources and AI assistance

- Sources: the assignment specification and contracts in `docs/`, the Week 8 to 10 lecture materials, and standard descriptions of the algorithms (CLRS-style LCS and interval DP, the KMP prefix function, Rabin–Karp, prefix doubling and Kasai's algorithm, Aho–Corasick).
- AI assistance: Claude wrote the first version of the implementations in `Python/source/algorithms.py` and helped me draft this document.
- My own verification: I applied the commits, ran `python tools/run.py --check`, the unit tests and the benchmark on my machine (Windows 11, Python 3.14.7) and report those results here. I read each algorithm and can explain its invariant and complexity. The benchmark numbers above are from my machine.
