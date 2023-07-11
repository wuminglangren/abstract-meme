# import os
# from png_to_edge_detected import TREATED_EDGE_DATA
# import numpy as np
# import multiprocessing as mp

# def get_files_in_subdirectories(directory):
#     file_list = []
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             file_path = os.path.join(root, file)
#             file_list.append(file_path)
#     return file_list

# directory = TREATED_EDGE_DATA
# files = get_files_in_subdirectories(directory)

# def load_npy(filename):
#     return np.load(filename)

# files = files[:20]
# pool = mp.Pool()
# results = pool.map(np.load,files)
# pool.close()

# for result in results:
#     print(result)



import numpy as np

# Load the .npy file
data = np.load('/home/wuming/Documents/abstract-meme/database/fonts/treated_data-edge_detection/32_0x20/AnonymiceProNerdFontPropo-Bold_32_0x20_ .npy')

# Access and use the loaded data
print(data)
print(data.shape)

# /home/wuming/Documents/abstract-meme/database/fonts/treated_fonts/32_0x20/AbhayaLibre-Regular_32_0x20_ .png

from PIL import Image

# Load the PNG image
image = Image.open("/home/wuming/Documents/abstract-meme/database/fonts/treated_fonts/32_0x20/AbhayaLibre-Regular_32_0x20_ .png")

# Get the shape of the image
width, height = image.size

print("Image shape: {} x {}".format(width, height))
