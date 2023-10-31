import sys
sys.path.append(r"/Users/neardws/Documents/GitHub/Pre-Matching-based-Hierarchical-Auction/")

from Strategy.strategy import action
from Algorithms.random_action import random_action
import numpy as np

def test_random_action():
    action_obj = random_action(2, 3, 4, 5)
    assert isinstance(action_obj, action)
    assert isinstance(action_obj.get_offloading_decision(), np.ndarray)
    assert isinstance(action_obj.get_computing_resource_decision(), np.ndarray)
    assert action_obj.get_offloading_decision().shape == (2, 14)
    assert action_obj.get_computing_resource_decision().shape == (2, 14)
    assert np.sum(action_obj.get_offloading_decision()) == 2
    assert np.sum(action_obj.get_computing_resource_decision()) > 0
    assert np.sum(action_obj.get_computing_resource_decision()) < 2 * 14
    assert np.sum(action_obj.get_computing_resource_decision()) == np.sum(action_obj.get_offloading_decision())
    assert action_obj.check_validity() == True
    assert np.sum(action_obj.get_computing_resource_decision()) == 2
    assert np.sum(action_obj.get_computing_resource_decision()[:][0]) == 1
    assert np.sum(action_obj.get_computing_resource_decision()[:][1]) == 1
    assert np.sum(action_obj.get_computing_resource_decision()[:][2]) == 1
    assert np.sum(action_obj.get_computing_resource_decision()[:][3]) == 1
    assert np.sum(action_obj.get_computing_resource_decision()[:][4]) == 1
    assert np.sum(action_obj.get_computing_resource_decision()[:][5]) == 1
    assert np.sum(action_obj.get_computing_resource_decision()[:][6]) == 1
    assert np.sum(action_obj.get_computing_resource_decision()[:][7]) == 1
    assert np.sum(action_obj.get_computing_resource_decision()[:][8]) == 1
    assert np.sum(action_obj.get_computing_resource_decision()[:][9]) == 1
    assert np.sum(action_obj.get_computing_resource_decision()[:][10]) == 1
    assert np.sum(action_obj.get_computing_resource_decision()[:][11]) == 1
    assert np.sum(action_obj.get_computing_resource_decision()[:][12]) == 1
    assert np.sum(action_obj.get_computing_resource_decision()[:][13]) == 1
    