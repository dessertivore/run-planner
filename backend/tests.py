import pytest
from resources import add_run, find_run_func, add_plan

add_plan(1, "10k training plan")


def test_add_run():
    add_run(0, 1, 1, "5km, easy")
    assert find_run_func(0, 0, 0) == "5km, easy"
