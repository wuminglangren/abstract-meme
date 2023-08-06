import shutil
import os
import random
import re
import shutil
import sys
from fontTools.ttLib import TTFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from collect_fonts_script import FONTS_DATA
from font_file_to_png import CHAR_RANGE

PRESERVED_TREATED_FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "treated_fonts/")
STANDARD_FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cores/source-sans/TTF/SourceSans3-Regular.ttf")

def has_glyph_in_standard(char_code):
    font = TTFont(file=STANDARD_FONT)
    for table in font['cmap'].tables:
        if char_code in table.cmap.keys():
            return True
        
    return False

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
        if not(tmp_name in subdir_names) and has_glyph_in_standard(CHAR_RANGE[i]):
            os.mkdir(tmp_name_full)
    
    match_pattern = r"(\d.*)_"
    for i in subdir_names:

        result = re.match(match_pattern, i)
        # print(result)
        if not(int(result.group(1)) in CHAR_RANGE):
            shutil.rmtree(PRESERVED_TREATED_FONTS+i+"/")

def delete_font_depening_on_types():

    font_names= [name for name in os.listdir(FONTS_DATA) if os.path.isfile(os.path.join(FONTS_DATA, name))]

    specific_types = ['italic', 'highlight','oblique']

    for name in font_names:
        for specific_type in specific_types:

            if specific_type in name.lower():
                os.remove(os.path.join(FONTS_DATA,name))


# def delete_specific_fonts():
#     font_names= [name for name in os.listdir(FONTS_DATA) if os.path.isfile(os.path.join(FONTS_DATA, name))]

#     target_fonts = ['ubuntu-c_modified', 'adobeblank', 'akronim', 'aksarabaligalang', 'asar-regular', 'cabinsketch', 'codystar', 'fascinateinline', 'fascinate', 'flowblock', 'flowcircular', 'flowrounded','geo-oblique','geo-regular','geostarfill','geostar','hanalei','heavydatanerdfont','jsmath','librebarcode','monofett','missfajardose','monoton','monsterratsubrayada','moolahlah','mysoul','newrocker','portersansblock','redacted','raviprakash','rationale','revalia','rubik80sfade','rubik','zentokyozoo','zillaslabhighlight','londrina','yeonsung','alkalami','anybody','[','bungeeshade','carattere','josefin','subdrayada','mrbedfort','mrssaintdelafield','nosifercaps','nosifer','notoseriftibet','nuosusil', 'silkscreen', '3270','fuzzybulbbles','gwendolyn','hurricane','lavishlyyours','monoid-', 'themify', "notocoloremoji", "emoji", "KumarOne", "alexbrush", 'alison', 'allura', 'almendradisplay', 'astloch']

#     deleted = False
#     for font_name in font_names:
#         for target_name in target_fonts:
#             if target_name in font_name.lower():
#                 if not(deleted):
#                     try:
#                         os.remove(os.path.join(FONTS_DATA,font_name))
#                         font_names.remove(font_name)
#                         deleted = True
                        
#                     except FileNotFoundError as e:
#                         print (e, font_name)

def delete_specific_fonts():

    target_fonts = ['ubuntu-c_modified', 'adobeblank', 'akronim', 'aksarabaligalang', 'asar-regular', 'cabinsketch', 'codystar', 'fascinateinline', 'fascinate', 'flowblock', 'flowcircular', 'flowrounded','geo-oblique','geo-regular','geostarfill','geostar','hanalei','heavydatanerdfont','jsmath','librebarcode','monofett','missfajardose','monoton','monsterratsubrayada','moolahlah','mysoul','newrocker','portersansblock','redacted','raviprakash','rationale','revalia','rubik80sfade','rubik','zentokyozoo','zillaslabhighlight','londrina','yeonsung','alkalami','anybody','[','bungeeshade','carattere','josefin','subdrayada','mrbedfort','mrssaintdelafield','nosifercaps','nosifer','notoseriftibet','nuosusil', 'silkscreen', '3270','fuzzybulbbles','gwendolyn','hurricane','lavishlyyours','monoid-', 'themify', "notocoloremoji", "emoji", "KumarOne", "alexbrush", 'alison', 'allura', 'almendradisplay', 'astloch']

    for font_name in os.listdir(FONTS_DATA):
        for target_name in target_fonts:
            if target_name.lower() in font_name.lower():
                try:
                    font_path = os.path.join(FONTS_DATA, font_name)
                    os.remove(font_path)
                    print(f"Deleted: {font_name}")
                    
                except FileNotFoundError as e:
                    print (f"Error deleting {font_name}: {e}")


if __name__ == "__main__":
    # reduce_fonts_number(5)
    limit_fonts()
    delete_font_depening_on_types()
    delete_specific_fonts()
    pass