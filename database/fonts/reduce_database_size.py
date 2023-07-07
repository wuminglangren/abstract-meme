import shutil
import os
import random
from collect_fonts_script import FONTS_DATABESE

def reduce_fonts_number(left_size = 20):

    # Get a list of all files in the directory
    files = [file for file in os.listdir(FONTS_DATABESE) if os.path.isfile(os.path.join(FONTS_DATABESE, file))]

    # Check if the number of files to delete exceeds the total number of files
    delete_size = len(files) - left_size

    # Randomly select the files to delete
    files_to_delete = random.sample(files, delete_size)

    for file_name in files_to_delete:
        file_path = os.path.join(FONTS_DATABESE, file_name)
        
        try:
            # Delete the file
            os.remove(file_path)
            print("File deleted successfully:", file_name)
        except OSError as e:
            print("Error occurred while deleting the file:", e)
    


    pass

if __name__ == "__main__":
    reduce_fonts_number(5)