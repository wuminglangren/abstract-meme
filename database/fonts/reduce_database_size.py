import shutil
import os
import random
import re
import shutil
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from collect_fonts_script import FONTS_DATA
from font_file_to_png import CHAR_RANGE

PRESERVED_TREATED_FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "treated_fonts/")

def reduce_fonts_number(left_size = 20):

    # Get a list of all files in the directory
    files = [file for file in os.listdir(FONTS_DATA) if os.path.isfile(os.path.join(FONTS_DATA, file))]

    # Check if the number of files to delete exceeds the total number of files
    delete_size = len(files) - left_size

    # Randomly select the files to delete
    files_to_delete = random.sample(files, delete_size)

    for file_name in files_to_delete:
        file_path = os.path.join(FONTS_DATA, file_name)
        
        try:
            # Delete the file
            os.remove(file_path)
            print("File deleted successfully:", file_name)
        except OSError as e:
            print("Error occurred while deleting the file:", e)
    


    pass

def limit_fonts():

    subdir_names = [name for name in os.listdir(PRESERVED_TREATED_FONTS) if os.path.isdir(os.path.join(PRESERVED_TREATED_FONTS, name))]

    for i in range(len(CHAR_RANGE)):

        tmp_name = str(int(CHAR_RANGE[i])) + "_" + str(hex(CHAR_RANGE[i]))
        tmp_name_full = PRESERVED_TREATED_FONTS + tmp_name + "/"
        # print(tmp_name)
        # print(tmp_name in subdir_names)
        # print(subdir_names)
        if not(tmp_name in subdir_names):
            os.mkdir(tmp_name_full)
    
    match_pattern = r"(\d.*)_"
    for i in subdir_names:

        result = re.match(match_pattern, i)
        print(result)
        if not(int(result.group(1)) in CHAR_RANGE):
            shutil.rmtree(PRESERVED_TREATED_FONTS+i+"/")

if __name__ == "__main__":
    # reduce_fonts_number(5)
    limit_fonts()
    pass