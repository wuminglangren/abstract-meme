import cv2
import numpy as np
import os
import re
import multiprocessing
from font_file_to_png import TREATED_FONTS

TREATED_EDGE_DATA = "/home/wuming/Documents/abstract-meme/database/fonts/treated_data-edge_detection"


def detect_edges(filename):
    # Read the PNG image
    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    match_pattern = r".*?\/([\d\w]+)\/([0-9a-zA-Z_-]+).png"
    file_info = re.match(match_pattern, filename)
    print(filename)
    print("info", file_info)
    print(file_info.group(1), file_info.group(2))

    # Perform edge detection
    edges = cv2.Canny(image, 5, 250)  # Adjust the threshold values as needed

    # Convert the edge image to a NumPy array
    edge_array = np.array(edges)

    # Save the edge data as a grayscale image
    output_path = os.path.join(TREATED_EDGE_DATA, file_info.group(1) )
    output_path = output_path + "/" + file_info.group(2) + ".npy"
    print(output_path)
    # cv2.imwrite(output_path, edge_array)


if __name__ == '__main__':
    # List of PNG files
    png_files = []  
    # Add your PNG file paths here
    for root, dirs, files in os.walk(TREATED_FONTS):
        for file in files:
            file_path = os.path.join(root, file)
            abs_path = os.path.abspath(file_path)
            png_files.append(abs_path)

    source_directory = TREATED_FONTS
    destination_directory = TREATED_EDGE_DATA  

    # Walk through the source directory and its subdirectories
    for root, dirs, files in os.walk(source_directory):
        # Get the relative path within the source directory
        relative_path = os.path.relpath(root, source_directory)
        # Construct the corresponding destination directory path
        destination_path = os.path.join(destination_directory, relative_path)

        # Create the directory in the destination directory if it doesn't exist
        os.makedirs(destination_path, exist_ok=True)

    detect_edges(png_files[0])
    # # Create a multiprocessing Pool
    # pool = multiprocessing.Pool()

    # # Use the Pool to process the images in parallel
    # pool.map(detect_edges, png_files)

    # # Close the Pool
    # pool.close()
    # pool.join()
