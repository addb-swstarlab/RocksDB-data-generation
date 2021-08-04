import os

def get_instance_index(count_file : int):
    instance_index = os.popen("hostname | cut -d'-' -f3").read()[:-1] # "data-generation-1" get the index "1"
    instance_count = int(instance_index) - 17 # -1 to the index of the instance
    range_start = instance_count * count_file + 1 # 0 * 1000 + 1 = 1
    range_end = (instance_count + 1) * count_file + 1 # (0 + 1) * 1000 + 1 = 1001
    
    return range_start, range_end, instance_count
