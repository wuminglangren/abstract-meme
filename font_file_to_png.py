from PIL import Image, ImageDraw, ImageFont
# import fontforge as ff
from fontTools.ttLib import TTFont
import numpy as np
import re
import os
import math
from database.fonts.collect_fonts_script import FONTS_DATABESE

def has_glyph(font, char_code):
    for table in font['cmap'].tables:
        if char_code in table.cmap.keys():
            return True
        
    return False


def print_all(font_file_path, font_size, image_width, image_height, font_color = (0,0,0), background_color = (255,255,255), output_file_path = "font_print_all.png"):
    # Load the font
    font = ImageFont.truetype(font_file_path, font_size)
    # loaded_font = ff.open(font_file_path)
    loaded_font = TTFont(file=font_file_path)

    # Create a new image
    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    # Set the starting position
    x = 0
    y = 0


    # Iterate over the Unicode character range
    for char_code in range(0x00020, 0xFFFFF + 1):
        # print(hex(char_code), int(char_code), char, end=" ")
        # print(hex(char_code), int(char_code))

        # try:
        #     char = loaded_font.__getitem__(char_code)

        #     # Calculate the size of the character
        #     # char_width, char_height = draw.textsize(chr(char.unicode), font=font)
        #     location_collection = font.getbbox(text=chr(char.unicode), font=font)
        #     char_width = location_collection[2] - location_collection[0]
        #     char_height = location_collection[3] - location_collection[1]
                
        #     # Check if the character exceeds the image width
        #     if x + char_width > image_width:
        #         x = 0
        #         y += char_height
                
        #     # Draw the character on the image
        #     draw.text((x, y), chr(char.unicode), font=font, fill=font_color)
                
        #     # Move to the next position
        #     x += char_width
        # except TypeError:
        #     pass
        # except ValueError:

        #     print("ValueError", hex(char_code), int(char_code))
        #     break
        # except KeyError:
        #     print("KeyError", hex(char_code), int(char_code))

        if has_glyph(loaded_font, char_code):

            # Calculate the size of the character
            # char_width, char_height = draw.textsize(chr(char.unicode), font=font)
            location_collection = font.getbbox(text=chr(char_code))
            char_width = location_collection[2] - location_collection[0]
            char_height = location_collection[3] - location_collection[1]
                
            # Check if the character exceeds the image width
            if x + char_width > image_width:
                x = 0
                y += char_height
                
            # Draw the character on the image
            draw.text((x, y), chr(char_code), font=font, fill=font_color)
                
            # Move to the next position
            x += char_width
        else:
            # print("Does not exists:",int(char_code), hex(char_code))
            pass

        char = None

    # Save the image
    image.save(output_file_path)  # Replace with the desired output file path and format

# def print_all_seperately(font_file_path, font_size, font_color = (0,0,0), background_color = (255,255,255), output_dir_path = "font_all_seperately"):

#     data_collection = None
    
#     # Load the font
#     font = ImageFont.truetype(font_file_path, font_size)
#     loaded_font = ff.open(font_file_path)

#     edge = 12


#     # Iterate over the Unicode character range
#     for char_code in range(0x000000, 0xFFFFFF + 1):
#         # print(hex(char_code), int(char_code), char, end=" ")

#         try:

#             char = loaded_font.__getitem__(char_code)

#             location_collection = font.getbbox(text=chr(char.unicode))
#             char_width = location_collection[2] - location_collection[0]
#             char_height = location_collection[3] - location_collection[1]
            
#             if data_collection is None:
#                 data_collection = np.array([char_width, char_height])
#             else:
#                 tmp_data = np.array([char_width, char_height])
#                 data_collection = np.vstack((data_collection, tmp_data))

#         except TypeError:
#             pass
#         except ValueError:

#             print("ValueError", hex(char_code), int(char_code))
#         except SystemError:

#             print("SystemError", hex(char_code), int(char_code))

#         char = None

#     print(data_collection.shape)
#     print(data_collection[0].max(), data_collection[0].mean())
#     print(data_collection[1].max(), data_collection[1].mean())

#     # Iterate over the Unicode character range
#     for char_code in range(0x000000, 0xFFFFFF + 1):
#         # print(hex(char_code), int(char_code), char, end=" ")

#         try:

#             char = loaded_font.__getitem__(char_code)

#             location_collection = font.getbbox(text=chr(char.unicode))
#             char_width = location_collection[2] - location_collection[0]
#             char_height = location_collection[3] - location_collection[1]
            
#             part_image_frame_one_side = data_collection.max()
#             part_image_frame = (part_image_frame_one_side*2, part_image_frame_one_side*2)
#             part_image = Image.new("RGB", part_image_frame, color=background_color)
#             part_draw = ImageDraw.Draw(part_image)
#             part_draw_anchor = (part_image_frame_one_side, part_image_frame_one_side)
#             part_draw.text(part_draw_anchor,text=chr(char.unicode), font=font, anchor="mm", fill=font_color)

#             # print(char_code, type(char_code), char, type(char))
#             if (int(char_code) == 47):
#                 # print("first choice")
#                 preserve_path = output_dir_path + str(int(char_code)) + "_" + str(hex(char_code)) + " " + "slash" + ".png"
#             else:
#                 # print("second choice")
#                 preserve_path = output_dir_path + str(int(char_code)) + "_" + str(hex(char_code)) + " " + chr(char.unicode) + ".png"
#             # print(preserve_path)

#             part_image.save(preserve_path, "PNG")
#             # print(char, char_code)
#             # print()

#             if data_collection is None:
#                 data_collection = np.array([char_width, char_height])
#             else:
#                 tmp_data = np.array([char_width, char_height])
#                 data_collection = np.vstack((data_collection, tmp_data))

#         except TypeError:
#             pass
#         except ValueError:

#             print("ValueError", hex(char_code), int(char_code))
#         except SystemError:

#             print("SystemError", hex(char_code), int(char_code))

#         char = None

def print_all_seperately(font_file_path, font_size, font_color = (0,0,0), background_color = (255,255,255), output_dir_path = "font_all_seperately"):

    data_collection = None
    
    # Load the font
    font = ImageFont.truetype(font_file_path, font_size)
    loaded_font = TTFont(font_file_path)

    match_pattern = r"([^\/]+)\.ttf$"
    print(font_file_path)
    print(re.search(match_pattern, font_file_path))
    font_name = re.search(match_pattern, font_file_path).group(1)
    print(font_name)
    zoom_rate = 1


    # Iterate over the Unicode character range
    for char_code in range(0x00020, 0xFFFFF + 1):
        # print(hex(char_code), int(char_code), char, end=" ")

        if has_glyph(loaded_font, char_code):

            location_collection = font.getbbox(text=chr(char_code))
            char_width = location_collection[2] - location_collection[0]
            char_height = location_collection[3] - location_collection[1]
            
            if data_collection is None:
                data_collection = np.array([char_width, char_height])
            else:
                tmp_data = np.array([char_width, char_height])
                data_collection = np.vstack((data_collection, tmp_data))
        else:
            pass

        char = None

    print(data_collection.shape)
    print(data_collection[0].max(), data_collection[0].mean())
    print(data_collection[1].max(), data_collection[1].mean())

    # Iterate over the Unicode character range
    for char_code in range(0x000020, 0xFFFFFF + 1):
        # print(hex(char_code), int(char_code), char, end=" ")

        if has_glyph(loaded_font, char_code):

            location_collection = font.getbbox(text=chr(char_code))
            char_width = location_collection[2] - location_collection[0]
            char_height = location_collection[3] - location_collection[1]
            
            part_image_frame_one_side = data_collection.max()
            part_image_frame = (math.ceil(part_image_frame_one_side*zoom_rate), math.ceil(part_image_frame_one_side*zoom_rate))
            part_image = Image.new("RGB", part_image_frame, color=background_color)
            part_draw = ImageDraw.Draw(part_image)
            part_draw_anchor = (int(part_image_frame_one_side/2), int(part_image_frame_one_side/2))
            part_draw.text(part_draw_anchor,text=chr(char_code), font=font, anchor="mm", fill=font_color)

            preserve_dir_path = output_dir_path + str(int(char_code)) + "_" + str(hex(char_code))
            if not(os.path.exists(preserve_dir_path)):
                os.mkdir(preserve_dir_path)

            # print(char_code, type(char_code), char, type(char))
            if (int(char_code) == 47):
                # print("first choice")
                preserve_path = output_dir_path + str(int(char_code)) + "_" + str(hex(char_code)) + "/" + font_name + "_" + str(int(char_code)) + "_" + str(hex(char_code)) + "_" + "slash" + ".png"
            else:
                # print("second choice")
                # preserve_path = output_dir_path + str(int(char_code)) + "_" + str(hex(char_code)) + " " + chr(char_code) + ".png"
                preserve_path = output_dir_path + str(int(char_code)) + "_" + str(hex(char_code)) + "/" + font_name + "_" + str(int(char_code)) + "_" + str(hex(char_code)) + "_" + chr(char_code) + ".png"
            print(char_code, preserve_path)


            part_image.save(preserve_path, "PNG")
            # print(char, char_code)
            # print()

        else:
            # print("Does not exists:", int(char_code), hex(char_code))
            pass

        char = None

def clean_blanks_which_should_not_be_blank(dir_path):

    for root, dirs, files in os.walk(dir_path):

        for dir in dirs:
            print(dir)
            if dir != "32_0x20":
                for subroot, subdirs, subfiles in os.walk(os.path.join(root,dir)):
                    for subfile in subfiles:
                        path =os.path.join(subroot,subfile)
                        if is_png_blank(path):
                            os.remove(path)


    pass

def is_png_blank(image_path):

    image = Image.open(image_path)

    image = image.convert("RGB")

    width, height = image.size
    
    for y in range(height):
        for x in range(width):

            r,g,b = image.getpixel((x,y))

            if r != 255 or g != 255 or b != 255:
                return False
            
    return True

if __name__ =="__main__":

    # print_all("test_font.ttf", 72, 5000, 5000, (0,0,0), (255,255,255), "test_test_test.png")

    from database.fonts.collect_fonts_script import FONTS_DATABESE

    for root, dirs, files in os.walk(FONTS_DATABESE):
        for file in files:
            file_path = os.path.join(root, file)
            print_all_seperately(file_path, 72, (0,0,0), (255,255,255), "/home/wuming/Documents/abstract-meme/font_all_seperately/")

    # print_all_seperately("test_font.ttf", 72, (0,0,0), (255,255,255), "/home/wuming/Documents/abstract-meme/font_all_seperately/")

    clean_blanks_which_should_not_be_blank(FONTS_DATABESE)