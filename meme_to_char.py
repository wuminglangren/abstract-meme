import os, sys, re
import numpy as np
import scipy.interpolate as spi
import matplotlib.pyplot as plt
import cv2
from PIL import Image

from predeiction import predict_image

def crop_one_to_specific_size(np_array, array_shape, fill_value = 255):


    pass

def add_frame(np_array, frame_width):

    pass

def load_test_graph(graph_path):

    # white = 255
    # black = 0
    graph = Image.open(graph_path)
    graph = np.array(graph)
    graph = cv2.cvtColor(graph, cv2.COLOR_BGR2GRAY)
    graph_collection = crop_one_to_specific_size(graph, )

    pass

if __name__ == "__main__":

    pass