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

# Provide the path to the directory you want to examine
directory_path = TREATED_EDGE_DATA

num_dirs, dir_dict, dir_dict_reversed = get_subdirectories(directory_path)

mapping_dict = dir_dict
mapping_dict_reversed = dir_dict_reversed

# Define the input shape for your images
input_shape = None

# Define the number of classes
num_classes = num_dirs

# Load and preprocess your entire dataset
dataset_images = []  # List of all dataset images (numpy arrays)
dataset_labels = []  # List of corresponding labels (one-hot encoded)

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

tmp_path_list, tmp_label_list = get_files_in_subdirectoreis(TREATED_EDGE_DATA)
# for i in range(len(tmp_label_list)):
#     dataset_labels.append(dir_dict[tmp_label_list[i]])

combined_list = []
for i in range(len(tmp_label_list)):
    combined_list.append((tmp_path_list[i], dir_dict[tmp_label_list[i]]))

with mp.Pool() as pool:
    results = pool.starmap(load_npy,combined_list)

for i in range(len(results)):
    dataset_images.append(results[i][0])
    dataset_labels.append(results[i][1])

input_shape = dataset_images[0].shape

# Convert the dataset to numpy arrays
dataset_images = np.array(dataset_images)
dataset_labels = np.array(dataset_labels)


# Load the pre-trained InceptionV3 model
base_model = InceptionV3(weights=None, include_top=False, input_shape=input_shape)

# Add a global max pooling layer
x = base_model.output
x = GlobalMaxPooling2D()(x)

# Add a fully connected layer with 400 units (one for each class) and softmax activation
predictions = Dense(num_classes, activation='softmax')(x)

# Create the model
model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


# Split the dataset into training and validation sets
train_images, validation_images, train_labels, validation_labels = train_test_split(
    dataset_images,
    dataset_labels,
    test_size=0.2,  # Adjust the validation set size as desired
    random_state=42  # Set a random seed for reproducibility
)

# Define the checkpoint to save the best model weights
checkpoint = ModelCheckpoint('inceptionv3_model.h5', monitor='val_accuracy', save_best_only=True, mode='max')

# Define the learning rate schedule function
def lr_schedule(epoch):
    lr = 0.001  # Initial learning rate

    if epoch > 50:
        lr *= 0.1
    elif epoch > 30:
        lr *= 0.5

    return lr

# Create the LearningRateScheduler callback
lr_scheduler = LearningRateScheduler(lr_schedule)

# Train the model
epochs = 10
batch_size = 64

model.summary()

model.fit(
    train_images,
    train_labels,
    batch_size=batch_size,
    epochs=epochs,
    validation_data=(validation_images, validation_labels),
    callbacks=[checkpoint])

# Save the model weights
model.save_weights('inceptionv3_weights.h5')
