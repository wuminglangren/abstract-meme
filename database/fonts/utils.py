import os

def count_files_in_directory(directory):
    file_count = 0

    # Iterate over all items in the directory
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        # Check if the current item is a file
        if os.path.isfile(item_path):
            file_count += 1

    return file_count

if __name__ == "__main__":
    pass