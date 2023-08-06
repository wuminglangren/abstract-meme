# import os

# def count_files_in_subdirectories(dir_path):
#     file_count_per_subdir = {}

#     for root, _, files in os.walk(dir_path):
#         num_files = len(files)
#         file_count_per_subdir[root] = num_files

#     return file_count_per_subdir

# # Example usage:
# dir_path = "database/fonts/treated_fonts/"  # Replace with the path to your directory
# file_count_per_subdir = count_files_in_subdirectories(dir_path)

# numbers = []
# # Print the result
# for subdir, num_files in file_count_per_subdir.items():
#     print(f"Subdirectory '{subdir}' has {num_files} file(s).")
#     if num_files != 0:
#         numbers.append(num_files)

# print(f"Smallest value in the list: {min(numbers)}")
# print(f"Largest value in the list: {max(numbers)}")

import os

def count_files_in_subdirectories(dir_path):
    file_count_per_subdir = {}

    for root, _, files in os.walk(dir_path):
        num_files = len(files)
        file_count_per_subdir[root] = num_files

    return file_count_per_subdir

def find_min_max_in_subdirectories(dir_path):
    file_count_per_subdir = count_files_in_subdirectories(dir_path)

    if not file_count_per_subdir:
        print("No subdirectories found.")
        return

    num_files_list = list(file_count_per_subdir.values())[1:]
    min_value = min(num_files_list)
    max_value = max(num_files_list)

    return min_value, max_value

# Example usage:
dir_path = "database/fonts/treated_fonts/"  # Replace with the path to your directory
min_value, max_value = find_min_max_in_subdirectories(dir_path)

print(f"Smallest value in the list: {min_value}")
print(f"Largest value in the list: {max_value}")