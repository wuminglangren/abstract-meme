from PIL import Image, ImageDraw, ImageFont
import fontforge as ff

# Load the font
font_file = "test_font.ttf"  # Replace with the path to your desired font file
font_size = 24  # Replace with the desired font size
font = ImageFont.truetype(font_file, font_size)

# Create a new image
image_width = 1500# Replace with the desired image width
image_height = 1500# Replace with the desired image height
background_color = (255, 255, 255)  # Replace with the desired background color (white in this example)
image = Image.new("RGB", (image_width, image_height), background_color)
draw = ImageDraw.Draw(image)

# Set the starting position
x = 0
y = 0


false_count = 0
true_count = 0

loaded_font = ff.open(font_file)

# Iterate over the Unicode character range
for char_code in range(0x00000, 0xFFFFF + 1):
    # print(hex(char_code), int(char_code), char, end=" ")
    print(hex(char_code), int(char_code), end=" ")

    try:
        char = loaded_font.__getitem__(char_code)

        true_count += 1
        print("True", true_count, false_count)
        
        # Calculate the size of the character
        char_width, char_height = draw.textsize(chr(char.unicode), font=font)
            
        # Check if the character exceeds the image width
        if x + char_width > image_width:
            x = 0
            y += char_height
            
        # Draw the character on the image
        draw.text((x, y), chr(char.unicode), font=font, fill=(0, 0, 0))
            
        # Move to the next position
        x += char_width
    except TypeError:
            false_count += 1
            print("False", true_count, false_count)
    char = None

# Save the image
image.save("test_test_test.png")  # Replace with the desired output file path and format
