from PIL import Image, ImageDraw, ImageFont
import fontforge as ff
import numpy as np

# # Load the font
# font_file = "test_font.ttf"  # Replace with the path to your desired font file
# font_size = 30  # Replace with the desired font size
# font = ImageFont.truetype(font_file, font_size)

# # Create a new image
# image_width = 1500# Replace with the desired image width
# image_height = 1500# Replace with the desired image height
# background_color = (255, 255, 255)  # Replace with the desired background color (white in this example)
# image = Image.new("RGB", (image_width, image_height), background_color)
# draw = ImageDraw.Draw(image)

# # Set the starting position
# x = 0
# y = 0


# false_count = 0
# true_count = 0

# loaded_font = ff.open(font_file)

# # Iterate over the Unicode character range
# for char_code in range(0x00000, 0xFFFFF + 1):
#     # print(hex(char_code), int(char_code), char, end=" ")
#     print(hex(char_code), int(char_code), end=" ")

#     try:
#         char = loaded_font.__getitem__(char_code)

#         true_count += 1
#         print("True", true_count, false_count)
        
#         # Calculate the size of the character
#         char_width, char_height = draw.textsize(chr(char.unicode), font=font)
            
#         # Check if the character exceeds the image width
#         if x + char_width > image_width:
#             x = 0
#             y += char_height
            
#         # Draw the character on the image
#         draw.text((x, y), chr(char.unicode), font=font, fill=(0, 0, 0))
            
#         # Move to the next position
#         x += char_width
#     except TypeError:
#             false_count += 1
#             print("False", true_count, false_count)
#     char = None

# # Save the image
# image.save("test_test_test.png")  # Replace with the desired output file path and format

def print_all(font_file_path, font_size, image_width, image_height, font_color = (0,0,0), background_color = (255,255,255), output_file_path = "font_print_all.png"):
    # Load the font
    font = ImageFont.truetype(font_file_path, font_size)
    loaded_font = ff.open(font_file_path)

    # Create a new image
    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    # Set the starting position
    x = 0
    y = 0


    # Iterate over the Unicode character range
    for char_code in range(0x000000, 0xFFFFFF + 1):
        # print(hex(char_code), int(char_code), char, end=" ")
        # print(hex(char_code), int(char_code))

        try:
            char = loaded_font.__getitem__(char_code)

            # Calculate the size of the character
            # char_width, char_height = draw.textsize(chr(char.unicode), font=font)
            location_collection = font.getbbox(text=chr(char.unicode))
            char_width = location_collection[2] - location_collection[0]
            char_height = location_collection[3] - location_collection[1]
                
            # Check if the character exceeds the image width
            if x + char_width > image_width:
                x = 0
                y += char_height
                
            # Draw the character on the image
            draw.text((x, y), chr(char.unicode), font=font, fill=font_color)
                
            # Move to the next position
            x += char_width
        except TypeError:
            pass
        except ValueError:

            print("ValueError", hex(char_code), int(char_code))
            break

        char = None

    # Save the image
    image.save(output_file_path)  # Replace with the desired output file path and format

def print_all_seperately(font_file_path, font_size, font_color = (0,0,0), background_color = (255,255,255), output_dir_path = "font_all_seperately"):

    data_collection = None
    
    # Load the font
    font = ImageFont.truetype(font_file_path, font_size)
    loaded_font = ff.open(font_file_path)

    image_width = 1500
    image_height = 1500

    # Create a new image
    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    # Set the starting position
    x = 0
    y = 0
    rate = 1.5


    # Iterate over the Unicode character range
    for char_code in range(0x000000, 0xFFFFFF + 1):
        # print(hex(char_code), int(char_code), char, end=" ")

        try:
            char = loaded_font.__getitem__(char_code)

            # Calculate the size of the character
            # char_width, char_height = draw.textsize(chr(char.unicode), font=font)
            location_collection = font.getbbox(text=chr(char.unicode))
            char_width = location_collection[2] - location_collection[0]
            char_height = location_collection[3] - location_collection[1]

                
            # Check if the character exceeds the image width
            if x + char_width > image_width:
                x = 0
                y += char_height
                
            # Draw the character on the image
            draw.text((x, y), chr(char.unicode), font=font, fill=font_color)

            # part_image = Image.new("RGB", (char_width*rate, char_height*rate), background_color)
            # part_draw = ImageDraw.Draw(part_image)
            # part_draw.text((((char_width*rate)/2-(char_width/2)), ((char_height*rate)/2 - (char_height/2))), chr(char.unicode), font=font, fill=font_color)

            # preserve_path = output_dir_path + str(int(char_code)) + "_" + str(hex(char_code)) + " " + chr(char.unicode) + ".png"
            # part_image.save(preserve_path)

            part_image = Image.new("RGB", (char_width*rate, char_height*rate), color=background_color)
            part_draw = ImageDraw.Draw(part_image)
            part_draw.text((0,0),text=chr(char.unicode), font=font, anchor="lt", fill=font_color)

            if (0x2f == char_code):
                preserve_path = output_dir_path + str(int(char_code)) + "_" + str(hex(char_code)) + " " + "slash" + ".png"
            else:
                preserve_path = output_dir_path + str(int(char_code)) + "_" + str(hex(char_code)) + " " + chr(char.unicode) + ".png"

            print(preserve_path)
            part_image.save(preserve_path, "PNG")


            if data_collection is None:
                data_collection = np.array([char_width, char_height])
            else:
                data_collection = np.vstack((data_collection, np.array([char_width, char_height])))

            # print(hex(char_code), int(char_code), char_width, char_height)
            # Move to the next position
            x += char_width
        except TypeError:
            pass
        except ValueError:

            print("ValueError", hex(char_code), int(char_code))
        except SystemError:

            print("SystemError", hex(char_code), int(char_code))

        char = None
    
    # print(data_collection[:,0].max(), data_collection[:,0].min(), data_collection[:,0].mean(), data_collection[:,0].std())
    # print(data_collection[:,1].max(), data_collection[:,1].min(), data_collection[:,1].mean(), data_collection[:,1].std())


if __name__ =="__main__":

    # print_all("test_font.ttf", 72, 5000, 5000, (0,0,0), (255,255,255), "test_test_test.png")

    print_all_seperately("test_font.ttf", 72, (0,0,0), (255,255,255), "/home/wuming/Documents/abstract-meme/font_all_seperately/")
