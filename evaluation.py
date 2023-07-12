import os
import sys
import time
import timeit
import re

import training_fonts_connection as database_connection

import tensorflow as tf
import keras
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D, GlobalMaxPooling2D
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.inception_v3 import InceptionV3
from keras.callbacks import ModelCheckpoint, LearningRateScheduler
from keras.utils import to_categorical

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

import multiprocessing as mp

import numpy as np
import matplotlib.pyplot as plt
from png_to_edge_detected import TREATED_EDGE_DATA

MODEL_WEIGHTS_PATH = 'inceptionv3_model.h5'

print("checkpoint0")

def get_subdirectories(path):
    subdirectories = {}
    subdirectories_reversed = {}
    tmp_list = []
    count = 0
    distinct_value = 0  # Replace with your desired distinct value
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            count += 1
            tmp_list.append(item)

    tmp_list.sort()
    for i in range(count):
        subdirectories[tmp_list[i]] = distinct_value
        subdirectories_reversed[distinct_value] = tmp_list[i]
        distinct_value += 1
    return count, subdirectories, subdirectories_reversed


def get_files_in_subdirectoreis(directory):
    file_path_list = []
    file_label_list = []
    match_pattern = r".*?\/([^\/]+)$"
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root,file)
            file_path_list.append(file_path)
            # print(re.match(match_pattern,root).group(1))
            file_label_list.append(re.match(match_pattern, root).group(1))
    
    return file_path_list, file_label_list

def load_npy(filename, label):
    return np.load(filename), label

print("checkpoint1")
directory_path = TREATED_EDGE_DATA

print("checkpoint2")
num_dirs, dir_dict, dir_dict_reversed = get_subdirectories(directory_path)
print("checkpoint3")

mapping_dict = dir_dict
mapping_dict_reversed = dir_dict_reversed

dataset_images = []
dataset_labels = []

print("checkpoint4")
tmp_path_list, tmp_label_list = get_files_in_subdirectoreis(directory_path)
print("checkpoint5")

combined_list = []

print("checkpoint6")
for i in range(len(tmp_label_list)):
    combined_list.append((tmp_path_list[i], dir_dict[tmp_label_list[i]]))
print("checkpoint7")

print("checkpoint8")
with mp.Pool() as pool:
    results = pool.starmap(load_npy,combined_list)
print("checkpoint8")

print("checkpoint9")
for i in range(len(results)):
    dataset_images.append(results[i][0])
    dataset_labels.append(results[i][1])
print("checkpoint10")

input_shape = dataset_images[0].shape

# Convert the dataset to numpy arrays
dataset_images = np.array(dataset_images)
dataset_labels = np.array(dataset_labels)

print("checkpoint11")
model = keras.models.load_model(MODEL_WEIGHTS_PATH)
print("checkpoint12")

print("checkpoint13")
train_images, validation_images, train_labels, validation_labels = train_test_split(
    dataset_images,
    dataset_labels,
    test_size=0.2,
    random_state=42)
print("checkpoint14")

print("checkpoint15")
model.summary()
print("checkpoint16")

print("checkpoint17")
loss, accuracy = model.evaluate(validation_images, validation_labels)
print(f"loss: {loss}, accuracy: {accuracy}")
print("checkpoint18")