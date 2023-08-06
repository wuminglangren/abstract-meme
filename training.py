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
from keras.callbacks import TensorBoard

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

import multiprocessing as mp

import numpy as np
import matplotlib.pyplot as plt
from png_to_edge_detected import TREATED_EDGE_DATA
import pickle as pkl

# MODEL_WEIGHTS_PATH = 'inceptionv3_model.h5'
# MODEL_PATH = "inceptionv3_model_and_weights.keras"
# MODEL_HISTORY_PATH = "inceptionv3_model_history.pkl"

MODEL_WEIGHTS_PATH = 'inceptionv3_model.0~30.new.h5'
MODEL_PATH = "inceptionv3_model_and_weights.0~30.new.keras"
MODEL_HISTORY_PATH = "inceptionv3_model_history.0~30.new.pkl"

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

tmp_path_list, tmp_label_list = get_files_in_subdirectoreis(directory_path)
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
base_model = InceptionV3(weights=None, include_top=False, input_shape=input_shape, pooling=max, classes=num_classes, classifier_activation="softmax")

# Add a global max pooling layer
x = base_model.output
x = GlobalMaxPooling2D()(x)
x = Dense(1024, activation="relu")(x)

# Add a fully connected layer with 400 units (one for each class) and softmax activation
predictions = Dense(num_classes, activation='softmax')(x)

# Create the model
model = Model(inputs=base_model.input, outputs=predictions)

if os.path.exists(MODEL_WEIGHTS_PATH):
    model.load_weights(MODEL_WEIGHTS_PATH)

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


# Split the dataset into training and validation sets
train_images, validation_images, train_labels, validation_labels = train_test_split(
    dataset_images,
    dataset_labels,
    test_size=0.2,  # Adjust the validation set size as desired
    random_state=42  # Set a random seed for reproducibility
    # random_state=24 # Set a random seed for reproducibility
)

# Define the checkpoint to save the best model weights
checkpoint = ModelCheckpoint(MODEL_WEIGHTS_PATH, monitor='val_accuracy', save_best_only=True, mode='max')

# Train the model
epochs = 30
# batch_size = num_classes
batch_size = 1024

model.summary()

record = model.fit(train_images,
                   train_labels,
                   batch_size=batch_size,
                   epochs=epochs,
                   validation_data=(validation_images, validation_labels),
                   callbacks=[checkpoint],
                   verbose = 1)


loss, accuracy = model.evaluate(validation_images, validation_labels)
print(f"loss: {loss}, accuracy: {accuracy}")

# Save the model weights
model.save_weights(MODEL_WEIGHTS_PATH)

# Save the model
model.save(MODEL_PATH)

with open(MODEL_HISTORY_PATH, 'wb') as file:
    pkl.dump(record, file)

plt.plot(record.history['accuracy'], label = 'accuracy')
plt.plot(record.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.ylim([0.5,1])
plt.legend(loc='lower right')
plt.savefig("epoch-accuracy.png",dpi=600)
