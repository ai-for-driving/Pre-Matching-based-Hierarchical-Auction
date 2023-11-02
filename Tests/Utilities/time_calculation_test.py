import sys
sys.path.append(r"/Users/neardws/Documents/GitHub/Pre-Matching-based-Hierarchical-Auction/")
from Utilities.time_calculation import *

def test_transform_str_data_time_into_timestamp():
    time = "2005-06-16 08:28:00"
    timestamp = transform_str_data_time_into_timestamp(time)
    assert timestamp == 1118935680
    
def test_transform_str_data_time_into_timestamp_ms():
    time = "2005-06-16 08:28:00"
    timestamp = transform_str_data_time_into_timestamp_ms(time)
    assert timestamp == 1118935680000
    
def test_transform_timestamp_into_str_data_time():
    timestamp = 1118935680
    time = transform_timestamp_into_str_data_time(timestamp)
    assert time == "2005-06-16 08:28:00"
    
def test_transform_timestamp_ms_into_str_data_time():
    timestamp = 1118935680200
    time = transform_timestamp_ms_into_str_data_time(timestamp)
    assert time == "2005-06-16 08:28:00"