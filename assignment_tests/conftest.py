"""Test suites and execution order for the assignment tests (Task 4).

Two things happen automatically for every test in this folder:

1. Suite markers. Tests get the marker lru, lfu or ttl from their file name, so that
   `pytest -m lru` runs only the LRUCache tests, and so on.

2. Execution order. Each test is given a pytest-order number so that the groups run in
   this order:   smoke  ->  boundary  ->  data_driven  ->  everything else
   and, inside each group, the suites run in this order:   lru  ->  lfu  ->  ttl
   Tests inside the same group and suite keep the order they are written in the file.
   A test that has several group markers runs with the earliest group.

Run `pytest assignment_tests --collect-only -q` to see the resulting order.
"""
import pytest

GROUP_ORDER = ["smoke", "boundary", "data_driven"]   # then everything else
SUITE_ORDER = ["lru", "lfu", "ttl"]
SUITE_FILE_PREFIX = {"lru": "test_lru", "lfu": "test_lfu", "ttl": "test_ttl"}


def _suite_of(item):
    for suite, prefix in SUITE_FILE_PREFIX.items():
        if item.path.name.startswith(prefix):
            return suite
    return None


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    for item in items:
        suite = _suite_of(item)
        if suite:
            item.add_marker(getattr(pytest.mark, suite))

        group_rank = len(GROUP_ORDER)          # "everything else" runs last
        for rank, group in enumerate(GROUP_ORDER):
            if item.get_closest_marker(group):
                group_rank = rank
                break
        suite_rank = SUITE_ORDER.index(suite) if suite else len(SUITE_ORDER)

        # pytest-order runs lower numbers first: group first, then suite.
        item.add_marker(pytest.mark.order(group_rank * 10 + suite_rank + 1))
