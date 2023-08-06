import os
import re
from collect_fonts_script import FONTS_DATA

for root, dirs, files in os.walk(FONTS_DATA):
    for file in files:
        if not(file.endswith(".ttf")):
            os.remove(os.path.join(root,file))