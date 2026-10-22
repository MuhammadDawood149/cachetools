# Assignment 3: Unit Test Automation (cachetools)

Project: [cachetools](https://github.com/tkem/cachetools) (version 7.2.4, forked)
Python used: 3.14.7 on Windows
Group: Mian Dawood (24F-3053), Muhammad Dawood (24F-3054)

## Setup

```
git clone https://github.com/MuhammadDawood149/cachetools.git
cd cachetools
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
pip install pytest pytest-xdist pytest-order
pytest
```

Expected result: 514 tests pass (366 from the upstream project in `tests/` and 148 from
`assignment_tests/`).

- Setup evidence (terminal output): `assignment_docs/setup_output_muhammad.txt`
- Setup video: `assignment_docs/setup_video.mp4`

## Layout

| Path | Contents |
|---|---|
| `notes/` | ECP/BVA notes, one file per person |
| `assignment_tests/` | Automated unit tests, `conftest.py` (suites and order) and `data/` (CSV test data) |
| `assignment_docs/` | Setup evidence, setup video and the Excel test case sheets |
| `pytest.ini` | Registers the test group names (markers) |
| `run_assignment_tests.py` | Helper to run a suite or group, or run in parallel |

## Running the assignment tests

Run these from the repository root with the virtual environment active.

| What | Command |
|---|---|
| Everything, in the configured order | `pytest assignment_tests -v` |
| One group | `pytest assignment_tests -m smoke` (or `boundary`, `data_driven`) |
| One suite | `pytest assignment_tests -m lru` (or `lfu`, `ttl`) |
| A group inside a suite | `pytest assignment_tests -m "smoke and lru"` |
| In parallel (all CPU cores) | `pytest assignment_tests -n auto` |
| Parallel, one file per worker | `pytest assignment_tests -n auto --dist loadfile` |
| Show the execution order only | `pytest assignment_tests --collect-only -q` |

The same runs are available through the helper script:

```
python run_assignment_tests.py all        # every test, in order
python run_assignment_tests.py order      # list the order only
python run_assignment_tests.py smoke      # also: boundary, data
python run_assignment_tests.py lru        # also: lfu, ttl
python run_assignment_tests.py groups     # smoke, then boundary, then data-driven
python run_assignment_tests.py parallel   # all CPU cores
```

### Groups and suites

- **Groups (markers):** `smoke`, `boundary`, `data_driven`. A test can be in several groups.
- **Suites (markers added automatically from the file name):** `lru`, `lfu`, `ttl`.
- Markers are registered in `pytest.ini`; suites and order are set in `assignment_tests/conftest.py`.

### Execution order

Tests run in this order: group `smoke`, then `boundary`, then `data_driven`, then all
other tests. Inside each group the suites run `lru`, then `lfu`, then `ttl`. Tests of
the same group and suite keep the order they are written in the file. A test with several
group markers runs with its earliest group. The order is implemented with pytest-order.

When tests run in parallel (`-n`), each worker keeps the same relative order, but tests
on different workers run at the same time, so use a normal run when the exact order matters.

### Parameterisation and data-driven tests

- `@pytest.mark.parametrize` is used in `test_lru_muhammad.py`, `test_ttl_expiry_muhammad.py`
  and `test_lfu_mian.py`.
- `test_lru_csv_muhammad.py` and `test_lfu_csv_mian.py` read every case from a CSV file in
  `assignment_tests/data/`, so adding a row adds a test.
- `LFUCache` removes an arbitrary key when several keys share the lowest use count, so no
  test depends on a tie.

## Who did what

| Item | Muhammad Dawood | Mian Dawood |
|---|---|---|
| Task 1: setup evidence and instructions | Yes | |
| Task 1: setup video | | Yes |
| Task 2: classes covered | `LRUCache` (all methods), `TTLCache` expiry half (`ttl`, `timer`, `__contains__`, `__iter__`, `expire`) | `LFUCache` (all methods), `TTLCache` basics (`__init__`, `__getitem__`, `__setitem__`, `__delitem__`, `popitem`, `clear`, `__len__`, `currsize`) |
| Task 2: notes | `notes/ecp_bva_muhammad.md` | `notes/ecp_bva_mian.md` |
| Task 2: tests | `test_lru_muhammad.py`, `test_ttl_expiry_muhammad.py` | `test_lfu_mian.py`, `test_ttl_basic_mian.py` |
| Task 3: CSV test data | `data/lru_cases_muhammad.csv` | `data/lfu_cases_mian.csv` |
| Task 3: data-driven tests | `test_lru_csv_muhammad.py` | `test_lfu_csv_mian.py` |
| Task 3: Excel test case sheet | `assignment_docs/test_cases_muhammad.xlsx` | `assignment_docs/test_cases_mian.xlsx` |
| Task 4: groups, suites and order | `pytest.ini`, `assignment_tests/conftest.py` | |
| Task 4: running and parallel execution | | `run_assignment_tests.py`, "Running the assignment tests" section of this file |

Notes on the commit history:

- The first commit (`ae6f5c6`, "Task 1: add setup evidence and run instructions") was made
  by Muhammad Dawood on a shared laptop whose global Git identity was `saimqamar149`, so
  GitHub shows that username as the author.
- Mian Dawood's Task 3 commit (`0b8c817`) was made while the branch `muhammad-tests` was
  checked out in his folder, so it sits on that branch. The author field of each commit
  shows who made it.
