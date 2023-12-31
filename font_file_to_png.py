from PIL import Image, ImageDraw, ImageFont
# import fontforge as ff
from fontTools.ttLib import TTFont
import numpy as np
import re
import os
import math
from database.fonts.collect_fonts_script import FONTS_DATA
from sklearn.cluster import KMeans
import cv2

import multiprocessing as mp
import timeit

# CHAR_RANGE = [*range(0x20, 0x4f7+1), *range(0x1d24,0x232c+1), *range(0x259f, 0x27e9+1), *range(0x2c60, 0x2e53+1), *range(0xa71c,0xa7f5+1), *range(0xab30, 0xab68+1), *range(0x110000, 0x110369+1)]
CHAR_RANGE = [*range(0x20, 0x7e+1)] # 95
TREATED_FONTS = "/home/wuming/Documents/abstract-meme/database/fonts/treated_fonts/"

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
    for char_code in CHAR_RANGE:
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

def print_all_seperately(root_path, font_file_path, largest_font_size, font_color = (0,0,0), background_color = (255,255,255), frame_shape = (20,20), frame_edge_size = 3, output_dir_path = "font_all_seperately"):
# def print_all_seperately(root_path, font_file_path, start_font_size, font_size_limit, font_color = (0,0,0), background_color = (255,255,255), frame_shape = (20,20), frame_edge_size = 3, output_dir_path = "font_all_seperately"):

    data_collection = None
    
    # Load the font
    abs_file_path = os.path.join(root_path,font_file_path)
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    font_file_path = os.path.relpath(abs_file_path,current_file_path)
    try:
        font = ImageFont.truetype(font_file_path, largest_font_size)
        # font = ImageFont.truetype(font_file_path, start_font_size)
    except OSError as e:
        print("An error occurred:", str(e))
        return font_file_path
    loaded_font = TTFont(font_file_path)

    match_pattern = r"([^\/]+)\.ttf$"
    # print(font_file_path)
    # print(re.search(match_pattern, font_file_path))
    font_name = re.search(match_pattern, font_file_path).group(1)
    # print(font_name)


    # # Iterate over the Unicode character range
    # for char_code in range(0x00020, 0xFFFFFF + 1):
    #     # print(hex(char_code), int(char_code), char, end=" ")

    #     if has_glyph(loaded_font, char_code):

    #         location_collection = font.getbbox(text=chr(char_code))
    #         char_width = location_collection[2] - location_collection[0]
    #         char_height = location_collection[3] - location_collection[1]
            
    #         if data_collection is None:
    #             data_collection = np.array([char_width, char_height])
    #         else:
    #             tmp_data = np.array([char_width, char_height])
    #             data_collection = np.vstack((data_collection, tmp_data))
    #     else:
    #         pass

    #     char = None

    # print(data_collection.shape)
    # print(data_collection[0].max(), data_collection[0].mean())
    # print(data_collection[1].max(), data_collection[1].mean())

    # Iterate over the Unicode character range

    # print(font_file_path)
    # print("out of loop:", frame_shape)
    for char_code in CHAR_RANGE:
        # print("in loop:", frame_shape)
        # print(hex(char_code), int(char_code), char, end=" ")
        tmp_font_size = largest_font_size
        # tmp_font_size = start_font_size
        tmp_font = font.font_variant(size = tmp_font_size)

        if has_glyph(loaded_font, char_code):

            part_image = Image.new("RGB", frame_shape, color=background_color)
            part_draw = ImageDraw.Draw(part_image)
            part_draw_anchor = (math.floor(frame_shape[0] / 2),math.floor(frame_shape[0]/2))

            try:
                part_draw.text(part_draw_anchor,text=chr(char_code), font=tmp_font, anchor="mm", fill=font_color)
            except OSError as e:
                print(e)
                print("root path:", root_path)
                print("font_file_path:", font_file_path)
                print("largest_font_size:", largest_font_size)
                # print("start_font_size:", start_font_size)
                print("font_color:", font_color)
                print("background_color:", background_color)
                print("frame_shape:", frame_shape)
                print("frame_edge_size:", frame_edge_size)
                print("output_dir_path", output_dir_path)
                break


            # print("initialized part:", frame_shape, "|", char_code)

            counter = 0
            while touch_edge(part_image, detect_color=(0,0,0), edge_width=frame_edge_size):
            # while ((not(touch_edge(part_image, detect_color=(0,0,0), edge_width=frame_edge_size))) and  
                    #   (tmp_font_size <= font_size_limit)):
                # print("looped loop part:", frame_shape)
                try:
                    tmp_font_size -= 2
                    # tmp_font_size += 2
                    tmp_font = tmp_font.font_variant(size = tmp_font_size)

                    part_image = Image.new("RGB", frame_shape, color=background_color)
                    part_draw = ImageDraw.Draw(part_image)
                    part_draw_anchor = (math.floor(frame_shape[0] / 2),math.floor(frame_shape[0]/2))
                    part_draw.text(part_draw_anchor,text=chr(char_code), font=tmp_font, anchor="mm", fill=font_color)
                except OSError as e:
                    print(e)
                    print("looped time:", counter)
                    print("char code:", char_code)
                    print("root path:", root_path)
                    print("font_file_path:", font_file_path)
                    print("largest_font_size:", largest_font_size)
                    # print("start_font_size:", start_font_size)
                    print("current_font_size:", tmp_font_size)
                    print("font_color:", font_color)
                    print("background_color:", background_color)
                    print("frame_shape:", frame_shape)
                    print("frame_edge_size:", frame_edge_size)
                    print("output_dir_path", output_dir_path)

                counter += 1

                # if (tmp_font_size > font_size_limit):
                #     print("looped time:", counter)
                #     print("char code:", char_code)
                #     print("root path:", root_path)
                #     print("font_file_path:", font_file_path)
                #     # print("largest_font_size:", largest_font_size)
                #     print("start_font_size:", start_font_size)
                #     print("current_font_size:", tmp_font_size)
                #     print("font_color:", font_color)
                #     print("background_color:", background_color)
                #     print("frame_shape:", frame_shape)
                #     print("frame_edge_size:", frame_edge_size)
                #     print("output_dir_path", output_dir_path)

            # if (touch_edge(part_image, detect_color=(0,0,0), edge_width=frame_edge_size)):

            #     try:
            #         # tmp_font_size -= 2
            #         tmp_font_size -= 2
            #         tmp_font = tmp_font.font_variant(size = tmp_font_size)

            #         part_image = Image.new("RGB", frame_shape, color=background_color)
            #         part_draw = ImageDraw.Draw(part_image)
            #         part_draw_anchor = (math.floor(frame_shape[0] / 2),math.floor(frame_shape[0]/2))
            #         part_draw.text(part_draw_anchor,text=chr(char_code), font=tmp_font, anchor="mm", fill=font_color)
            #     except OSError as e:
            #         print(e)
            #         print("looped time:", counter)
            #         print("char code:", char_code)
            #         print("root path:", root_path)
            #         print("font_file_path:", font_file_path)
            #         # print("largest_font_size:", largest_font_size)
            #         print("start_font_size:", start_font_size)
            #         print("current_font_size:", tmp_font_size)
            #         print("font_color:", font_color)
            #         print("background_color:", background_color)
            #         print("frame_shape:", frame_shape)
            #         print("frame_edge_size:", frame_edge_size)
            #         print("output_dir_path", output_dir_path)


            preserve_dir_path = output_dir_path + str(int(char_code)) + "_" + str(hex(char_code))
            if (os.path.exists(preserve_dir_path)):
                # os.mkdir(preserve_dir_path)

                # print(char_code, type(char_code), char, type(char))
                if (int(char_code) == 47):
                    # print("first choice")
                    preserve_path = output_dir_path + str(int(char_code)) + "_" + str(hex(char_code)) + "/" + font_name + "_" + str(int(char_code)) + "_" + str(hex(char_code)) + "_" + "slash" + ".png"
                else:
                    # print("second choice")
                    # preserve_path = output_dir_path + str(int(char_code)) + "_" + str(hex(char_code)) + " " + chr(char_code) + ".png"
                    preserve_path = output_dir_path + str(int(char_code)) + "_" + str(hex(char_code)) + "/" + font_name + "_" + str(int(char_code)) + "_" + str(hex(char_code)) + "_" + chr(char_code) + ".png"
                # print(char_code, preserve_path)


                part_image.save(preserve_path, "PNG")
                # print(char, char_code)
                # print()

        else:
            # print("Does not exists:", int(char_code), hex(char_code))
            pass

        char = None

    return None

def clean_blanks_which_should_not_be_blank(dir_path):

    wait_list = []
    for root, dirs, files in os.walk(dir_path):

        for dir in dirs:
            # print(dir)
            if dir != "32_0x20":

                wait_list.append(os.path.join(root,dir))
                # print("dir")

                # scan_blank_under_a_dir(os.path.join(root,dir))
                for subroot, subdirs, subfiles in os.walk(os.path.join(root,dir)):
                    for subfile in subfiles:
                        path =os.path.join(subroot,subfile)
                        wait_list.append(path)
                        # if is_png_blank(path):
                        #     os.remove(path)
    
    pool = mp.Pool()
    pool.map(scan_blank_under_a_dir,wait_list)
    pool.close()
    pool.join()

    pass

# def is_png_blank(image_path):

#     image = Image.open(image_path)

#     image = image.convert("L")

#     data = np.array(image).flatten()

#     num_clusters = 2
#     kmeans = KMeans(n_clusters=num_clusters, n_init = 'auto')
#     kmeans.fit(data.reshape(-1,1))

#     labels = kmeans.labels_

#     pixels = np.array(image).flatten()
#     largest_values = []
#     try:
#         for cluster_id in range(num_clusters):
#             cluster_pixels = pixels[labels == cluster_id]
#             largest_value = np.max(cluster_pixels)
#             largest_values.append(largest_value)
#     except ValueError as e:
#         # print(e)
#         return True

            
#     return False

def is_png_blank(image_path, threshold =100):

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    _, thresholded = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    non_zero_pixels = cv2.countNonZero(thresholded)
    total_pixels = image.shape[0] * image.shape[1]

    # if (total_pixels - cv2.countNonZero(thresholded)) <= 0:
    #     return True
    # else:
    #     return False
    return non_zero_pixels<=0


def scan_blank_under_a_dir(dir_path):

    for subroot, subdirs, subfiles in os.walk(dir_path):
        for subfile in subfiles:
            path =os.path.join(subroot,subfile)
            if is_png_blank(path):
                os.remove(path)

def touch_edge(image, detect_color = (0,0,0), edge_width:int = 1 ):
    # detected = False
    # image_np = np.asarray(image)

    # Get the width and height of the image
    width, height = image.size

    # Check the top edge
    for x in range(width):
        if all(image.getpixel((x, y)) == detect_color for y in range(edge_width)):
            return True

    # Check the bottom edge
    for x in range(width):
        if all(image.getpixel((x, y)) == detect_color for y in range(height - edge_width, height)):
            return True

    # Check the left edge
    for y in range(height):
        if all(image.getpixel((x, y)) == detect_color for x in range( edge_width)):
            return True

    # Check the right edge
    for y in range(height):
        if all(image.getpixel((x, y)) == detect_color for x in range(width - edge_width, width)):
            return True

    # No black edge detected
    return False


    # if edge_width >= 1:

    #     for i in range(0,edge_width):
    #         detected = bool(detected + np.isin(detect_color, image_np[i]).any())
    #         detected = bool(detected + np.isin(detect_color, image_np[:][i]).any())
        
    #     for i in range(-edge_width, 0):
    #         detected = bool(detected + np.isin(detect_color, image_np[i]).any())
    #         detected = bool(detected + np.isin(detect_color, image_np[:][i]).any())

    #     pass
    # else:
    #     raise ValueError
    #     pass
    # return detected

def process_file_with_presets(file_path):
    result = print_all_seperately(root_path = FONTS_DATA, font_file_path=file_path, largest_font_size=176, font_color=(0,0,0), background_color=(255,255,255), frame_shape=(100,100), frame_edge_size= 5, output_dir_path=TREATED_FONTS)
    # result = print_all_seperately(root_path = FONTS_DATA, font_file_path=file_path, start_font_size=60, font_size_limit=176, font_color=(0,0,0), background_color=(255,255,255), frame_shape=(100,100), frame_edge_size= 5, output_dir_path=TREATED_FONTS)
    if result != None:
        print("error path: ",result)


if __name__ =="__main__":

    # print_all("test_font.ttf", 72, 5000, 5000, (0,0,0), (255,255,255), "test_test_test.png")


    file_paths = []
    for root, dirs, files in os.walk(FONTS_DATA):
        for file in files:
            # file_path = os.path.join(root, file)
            # file_paths.append(file_path)
            # print(file_path)
            # file_path = os.path.join(root, file)
            file_paths.append(file)
            # print(file)

            # print_all_seperately(file_path, 144, (0,0,0), (255,255,255), frame_shape=(50,50), frame_edge_size= 5, output_dir_path="/home/wuming/Documents/abstract-meme/database/fonts/treated_fonts/")

    start = timeit.timeit()
    # print(file_paths)
    pool = mp.Pool()
    pool.map(process_file_with_presets, file_paths)

    pool.close()
    pool.join()
    # print_all_seperately("test_font.ttf", 72, (0,0,0), (255,255,255), "/home/wuming/Documents/abstract-meme/font_all_seperately/")
    print("start to clean blank!")
    print(f"Used {(timeit.timeit() - start)}")

    start = timeit.timeit()
    clean_blanks_which_should_not_be_blank(TREATED_FONTS)
    print(f"complete cleaning the blank, used {timeit.timeit() - start}")
