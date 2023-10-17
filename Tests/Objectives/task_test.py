import sys
sys.path.append(r"/Users/neardws/Documents/GitHub/Pre-Matching-based-Hierarchical-Auction/")
from Objectives.task import task


def test_task():
    t = task(
        input_data_size = 1.0,
        cqu_cycles = 2.0,
        deadline = 3.0,
    )
    assert isinstance(t, task)
    assert isinstance(t.get_input_data_size(), float)
    assert isinstance(t.get_cqu_cycles(), float)
    assert isinstance(t.get_deadline(), float)
    assert t.get_input_data_size() == 1.0
    assert t.get_cqu_cycles() == 2.0
    assert t.get_deadline() == 3.0