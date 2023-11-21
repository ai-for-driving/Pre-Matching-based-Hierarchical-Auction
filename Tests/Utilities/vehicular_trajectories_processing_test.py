import sys
sys.path.append(r"/Users/neardws/Documents/GitHub/Pre-Matching-based-Hierarchical-Auction/")

from Utilities.vehicular_trajectories_processing import TrajectoriesProcessing
from Utilities.time_calculation import transform_timestamp_ms_into_str_data_time

def test_min_max_time():

    time_stamp = 1113433136200
    print(transform_timestamp_ms_into_str_data_time(timestamp=time_stamp))

    file_name_keys = ["I-80-Emeryville-CA-1650feet-0400pm-0415pm", 
                    "I-80-Emeryville-CA-1650feet-0500pm-0515pm", 
                    "I-80-Emeryville-CA-1650feet-0515pm-0530pm",
                    "Lankershim-Boulevard-LosAngeles-CA-1600feet",
                    "Peachtree-Street-Atlanta-GA-2100feet",
                    "US-101-SanDiego-CA-1500feet-0750am-0805am",
                    "US-101-SanDiego-CA-1500feet-0805am-0820am",
                    "US-101-SanDiego-CA-1500feet-0820am-0835am",]

    tP = TrajectoriesProcessing(file_name_key=file_name_keys[0])
    
    for file_name_key in file_name_keys:
        tP.set_file_name_key(file_name_key)
        print(tP.get_file_name_key())
        tP.read_all_csv()
        # print(tP.get_all_data())
        max_time, min_time = tP.get_max_and_min_global_time()
        print("\nmax_time: ", max_time, "   min_time: ", min_time)
        max_time_data = transform_timestamp_ms_into_str_data_time(max_time)
        min_time_data = transform_timestamp_ms_into_str_data_time(min_time)
        print("\nmax_time_data: ", max_time_data, "   min_time_data: ", min_time_data)
    

if __name__ == '__main__':
    # vehicle_num = 10
    # slot_length = 300
    # vehicle_mobility_file_name_key = 'Peachtree-Street-Atlanta-GA-2100feet'
    # vehicular_trajectories_processing_chunk_size=100000
    # vehicular_trajectories_processing_selection_way='max_duration'
    # vehicular_trajectories_processing_filling_way='linear'
    # vehicular_trajectories_processing_start_time='2006-11-08 16:00:00'
    # trajectoriesProcessing = TrajectoriesProcessing(
    #     file_name_key=vehicle_mobility_file_name_key,
    #     vehicle_number=vehicle_num,
    #     start_time=vehicular_trajectories_processing_start_time,
    #     slot_length=slot_length,
    #     slection_way=vehicular_trajectories_processing_selection_way,
    #     filling_way=vehicular_trajectories_processing_filling_way,
    #     chunk_size=vehicular_trajectories_processing_chunk_size,
    # )
    # # trajectoriesProcessing.processing()
    
    # trajectoriesProcessing.read_csv()
    # trajectoriesProcessing.print_analysis()
    # test_min_max_time()
    
    file_name_keys = ["I-80-Emeryville-CA-1650feet-0400pm-0415pm", 
                    "I-80-Emeryville-CA-1650feet-0500pm-0515pm", 
                    "I-80-Emeryville-CA-1650feet-0515pm-0530pm",
                    "Lankershim-Boulevard-LosAngeles-CA-1600feet",
                    "Peachtree-Street-Atlanta-GA-2100feet",
                    "US-101-SanDiego-CA-1500feet-0750am-0805am",
                    "US-101-SanDiego-CA-1500feet-0805am-0820am",
                    "US-101-SanDiego-CA-1500feet-0820am-0835am",]

    tP = TrajectoriesProcessing(
        file_name_key=file_name_keys[3], 
        vehicle_number=100,
        slection_way='max_duration', 
        filling_way='linear', 
        chunk_size=100000
    )
    # tP.set_start_time("2005-04-13 16:00:00")
    tP.set_start_time("2005-06-16 08:30:00")
    tP.processing()
    
    # tP.read_all_csv()
    # tP.print_analysis(data=tP.get_all_data())