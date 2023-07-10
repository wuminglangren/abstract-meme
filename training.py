import os
import sys
import time
import timeit

import training_fonts_connection as database_connection

import tensorflow as tf
import keras
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D, GlobalMaxPool2D
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.inception_v3 import InceptionV3
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split

import numpy as np
import matplotlib.pyplot as plt


# Define the input shape for your images
input_shape = (100, 100, 1)

# Define the number of classes
num_classes = 400

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

# Load and preprocess your entire dataset
dataset_images = [...]  # List of all dataset images (numpy arrays)
dataset_labels = [...]  # List of corresponding labels (one-hot encoded)

# Convert the dataset to numpy arrays
dataset_images = np.array(dataset_images)
dataset_labels = np.array(dataset_labels)

# Split the dataset into training and validation sets
train_images, validation_images, train_labels, validation_labels = train_test_split(
    dataset_images,
    dataset_labels,
    test_size=0.2,  # Adjust the validation set size as desired
    random_state=42  # Set a random seed for reproducibility
)

# Define the checkpoint to save the best model weights
checkpoint = ModelCheckpoint('inceptionv3_model.h5', monitor='val_accuracy', save_best_only=True, mode='max')

# Train the model
epochs = 10
batch_size = 32

model.fit(
    train_images,
    train_labels,
    batch_size=batch_size,
    epochs=epochs,
    validation_data=(validation_images, validation_labels),
    callbacks=[checkpoint])

# Save the model weights
model.save_weights('inceptionv3_weights.h5')
