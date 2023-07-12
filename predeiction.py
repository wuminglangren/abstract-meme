import numpy as np
import keras
from keras.models import Model
from keras.layers import Dense, GlobalMaxPooling2D
from keras.preprocessing.image import img_to_array
from keras.applications.inception_v3 import InceptionV3

from training import get_subdirectories
import math
import multiprocessing as mp
import timeit
import cv2
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

from png_to_edge_detected import TREATED_EDGE_DATA
from training import MODEL_WEIGHTS_PATH

STANDARD_FONT_PATH = "standard-font.ttf"

class prediction:
    def __init__(self):
        self.num_dirs = None
        self.dir_dict = None
        self.dir_dict_reversed = None
        self.num_dirs, self.dir_dict, self.dir_dict_reversed = get_subdirectories(TREATED_EDGE_DATA)
        self.num_classes = self.num_dirs
        self.model = keras.models.load_model(MODEL_WEIGHTS_PATH)
        self.parts = []
        self.predicted =[]
        self.image = None
        pass

    def predict_one_part_image(self, image_array, input_shape):

        if input_shape != (100,100,1):
            raise ValueError("Please resize the input to (100,100,1)")

        predictions = self.model.predict(image_array)

        predicted_class = np.argmax(predictions[0])

        return predicted_class, predictions

    def open_image(self, image_path):
        pass


    def crop_one_to_many(self, body_shape = (90,90), aim_width = 20, frame_width = 5 ):
        pass

    def generate(self):
        # process:
        # graph
        # to grayscale
        # crop/split
        # edge detect
        # add frame
        # increase resolution
        # prediction
        pass


    def get_strings(self):
        pass

    def get_image(self):
        pass


        pass