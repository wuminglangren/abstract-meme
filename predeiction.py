import numpy as np
import keras
from keras.models import Model
from keras.layers import Dense, GlobalMaxPooling2D
from keras.preprocessing.image import img_to_array
from keras.applications.inception_v3 import InceptionV3

from training import get_subdirectories
from png_to_edge_detected import TREATED_EDGE_DATA

def predict_image(image_array, input_shape, weights_path):

    num_dirs, dir_dict, dir_dict_reversed = get_subdirectories(TREATED_EDGE_DATA)
    # Define the number of classes
    num_classes = num_dirs

    if input_shape != (100,100,1):
        raise ValueError("Please resize the input to (100,100,1)")

    # Load the pre-trained InceptionV3 model
    base_model = InceptionV3(weights=None, include_top=False, input_shape=input_shape)

    # Add a global max pooling layer
    x = base_model.output
    x = GlobalMaxPooling2D()(x)

    # Add a fully connected layer with 80 units (one for each class) and softmax activation
    predictions = Dense(num_classes, activation='softmax')(x)

    # Create the model
    model = Model(inputs=base_model.input, outputs=predictions)

    # Load the trained model weights
    model.load_weights(weights_path)

    # Preprocess the image
    image = img_to_array(image_array)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0

    # Make predictions
    predictions = model.predict(image)

    # Get the predicted class
    predicted_class = np.argmax(predictions[0])

    return predicted_class, predictions, dir_dict, dir_dict_reversed
