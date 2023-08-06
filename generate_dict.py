import os
import json
import pickle
from png_to_edge_detected import TREATED_EDGE_DATA

def get_subdirectories(path):
    subdirectories = {}
    subdirectories_reversed = {}
    tmp_list = []
    count = 0
    distinct_value = 0  # Replace with your desired distinct value
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            count += 1
            tmp_list.append(item)

    tmp_list.sort()
    for i in range(count):
        subdirectories[tmp_list[i]] = distinct_value
        subdirectories_reversed[distinct_value] = tmp_list[i]
        distinct_value += 1
    return count, subdirectories, subdirectories_reversed

num_dirs, dir_dict, dir_dict_reversed = get_subdirectories(TREATED_EDGE_DATA)

dir_dict_path = "dir_dict.pkl"
dir_dict_reversed_path = "dir_dict_reversed.pkl"

with open(dir_dict_path, 'wb') as file:
    # json.dump(dir_dict, file)
    pickle.dump(dir_dict, file)

with open(dir_dict_reversed_path, 'wb') as file:
    # json.dump(dir_dict_reversed, file)
    pickle.dump(dir_dict_reversed, file)