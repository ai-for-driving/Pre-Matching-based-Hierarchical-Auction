import sys
sys.path.append(r"/Users/neardws/Documents/GitHub/Pre-Matching-based-Hierarchical-Auction/")

from Utilities.vehicular_trajectories_processing import TrajectoriesProcessing
from Utilities.time_calculation import transform_timestamp_ms_into_str_data_time

time_stamp = 1113433136200
print(transform_timestamp_ms_into_str_data_time(timestamp=time_stamp))

tP = TrajectoriesProcessing()

file_name_keys = ["I-80-Emeryville-CA-1650feet-0400pm-0415pm", 
                "I-80-Emeryville-CA-1650feet-0500pm-0515pm", 
                "I-80-Emeryville-CA-1650feet-0515pm-0530pm",
                "Lankershim-Boulevard-LosAngeles-CA-1600feet",
                "Peachtree-Street-Atlanta-GA-2100feet",
                "US-101-SanDiego-CA-1500feet-0750am-0805am",
                "US-101-SanDiego-CA-1500feet-0805am-0820am",
                "US-101-SanDiego-CA-1500feet-0820am-0835am",]

for file_name_key in file_name_keys:
    tP.set_file_name_key(file_name_key)
    print(tP.get_file_name_key())
    tP.read_csv()
    print(tP.get_all_data())
    max_time, min_time = tP.get_max_and_min_global_time()
    print("\nmax_time: ", max_time, "   min_time: ", min_time)
    max_time_data = transform_timestamp_ms_into_str_data_time(max_time)
    min_time_data = transform_timestamp_ms_into_str_data_time(min_time)
    print("\nmax_time_data: ", max_time_data, "   min_time_data: ", min_time_data)
    