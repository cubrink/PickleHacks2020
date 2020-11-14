# This is the main file to compare a users image to the dataset encodings

import face_recognition
from PIL import Image
import pandas as pd
import numpy as np
import os
import pickle
import time
from multiprocessing import Process

from datetime import datetime

DATASET_PATH = r'./dataset.csv'

df = pd.read_csv(DATASET_PATH, sep='|')

ENCODINGS_DIR_BASE = os.path.join(os.getcwd(), 'encodings')


TIMEOUT_LENGTH = 60000      # timeout time in milliseconds





def get_face_encoding(image_loc, show_image = False):
    # this function returns the face encoding of the image
    # this function returns None is not face


    image = face_recognition.load_image_file(image_loc)

    # Get all face locations
    face_locations = face_recognition.face_locations(image)

    # Determine largest face in picture, store to variable
    if len(face_locations) == 0:
        return None
    elif len(face_locations) > 1:
        face = sorted(face_locations, key=lambda x: (x[2] - x[0]) * (x[1] - x[3]), reverse=True)[0]
    else:
        face = face_locations[0]
        

    # Extract face from image
    border_mult = 1.5
    top, right, bottom, left = face
    face_image_orig = image[top:bottom, left:right]

    vertical_border = int((bottom - top) * border_mult / 2)
    horizontal_border = int((right - left) * border_mult / 2)

    # np.array.shape -> y, x
    top = max(0, top-vertical_border)
    bottom = min(image.shape[0], bottom+vertical_border)
    left = max(0, left-horizontal_border)
    right = min(image.shape[1], right+horizontal_border)

    face_image = image[top:bottom, left:right]

    if show_image:
        pil_image = Image.fromarray(face_image)
        pil_image.show()

    # Create encoding
    my_face_encodings = face_recognition.face_encodings(face_image)

    try:
        return my_face_encodings[0]
    except IndexError:
        print('No Face Found!')
        return None






# have user input a file location
user_file_location = 'jeff_pic.jpg'

user_face_encoding = get_face_encoding(user_file_location, True)
if user_face_encoding is not None:
    print('Face Found!')
















# def compare_user_image(df_start_index, df_stop_index, timeout = 60000):
#     pass


# def test_timeout():
#     print('Testing Timeout Function')
#     while True:
#         time.sleep(1)

# process1 = Process(target=test_timeout, name='testing_timeout')
# if __name__ == '__main__':
#     process1.start()
#     process1.join(timeout=5)
#     process1.terminate()

# if process1.exitcode is None:
#     print(f'Oops, process1 timeouts!')











