import os
import sys
from PIL import Image

TARGET_IMAGES_DIR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_images/")

starter = 0

for root, dirs, files in os.walk(TARGET_IMAGES_DIR_PATH):

    for file in files:
        full_path = os.path.abspath(os.path.join(root,file))
        tmp_image = Image.open(full_path)
        file_name = f"test {starter:02d}.png"
        preserve_path = os.path.join(TARGET_IMAGES_DIR_PATH, file_name)
        tmp_image.save(preserve_path, "PNG")
        starter += 1
        os.remove(full_path)