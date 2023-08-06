import numpy as np
import keras
import os

print("check 0")
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

num_dirs, dir_dict, dir_dict_reversed = get_subdirectories(TREATED_EDGE_DATA)
print(num_dirs)
print(dir_dict)
print(dir_dict_reversed)

print("check 1")
# from png_to_edge_detected import TREATED_EDGE_DATA
# from training import MODEL_WEIGHTS_PATH, MODEL_PATH
MODEL_PATH = "inceptionv3_model_and_weights.keras"
# MODEL_PATH = "inceptionv3_model.h5"


print("check 2")
# from predeiction import prediction

print("check 3")
import cv2

print("check 4")
TEST_IMAGE_FILE_PATH = 'database/fonts/treated_fonts/34_0x22/AbhayaLibre-Medium_34_0x22_".png'

print("check 5")
image = cv2.imread(TEST_IMAGE_FILE_PATH, cv2.IMREAD_GRAYSCALE)
print("check 6")
edges = cv2.Canny(image, 5, 250)
print("check 7")
edge_array = np.array(edges)
print(edge_array.shape)
# edge_array = np.reshape(edge_array, (edge_array.shape[0], edge_array.shape[1], 1))
edge_array = np.expand_dims(edge_array, axis=0)
edge_array = np.expand_dims(edge_array, axis=-1)
print(edge_array.shape)

print("check 8")
inceptionv3_model = keras.models.load_model(MODEL_PATH)

print("check 9")
predicted = inceptionv3_model.predict(edge_array, verbose = 1)

print("check 10")
print(predicted)

print("check 11")
print(np.argmax(predicted))
print()
print(dir_dict_reversed[np.argmax(predicted)])
print()
print(dir_dict)