import os
import sys
import re
import shutil
import timeit

SYSTEM_INSTALLED_FONTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "installed_fonts.txt")
FONTS_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "collected_fonts/")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

installed_fonts_abs_path = []

def collect_all_fonts():

    installed_fonts_collection = []

    with open(SYSTEM_INSTALLED_FONTS_FILE, "r") as file:
        lines = file.readlines()

        for line in lines:
            installed_fonts_collection.append(line)

    # match_pattern = r"^(\/.*\.(ttf|otf|ttc)).*?$"
    match_pattern = r"^(\/.*\.(ttf)).*?$"
    for font in installed_fonts_collection:
        matched = re.search(match_pattern, font)
        if matched:
            # print(matched, "|", matched.group(1))
            installed_fonts_abs_path.append(matched.group(1))
        else:
            print(font)
    
    if not(os.path.exists(FONTS_DATA)):
        os.makedirs(FONTS_DATA)


    for font in installed_fonts_abs_path:
        shutil.copy(font, FONTS_DATA)

    

    for root, dirs, files in os.walk(SCRIPT_DIR):

        for file_name in files:
            tmp_string = os.path.join(root, file_name)

            matched = re.search(match_pattern, tmp_string)

            if matched:
                try:
                    shutil.copy(matched.group(1), FONTS_DATA)
                except shutil.SameFileError as e:
                    print("uncopied", e)
                except FileNotFoundError as e:
                    print("Cannot copy:", e )
                


    pass


if __name__ == "__main__":
    collect_all_fonts()
    pass