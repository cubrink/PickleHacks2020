import face_recognition
from PIL import Image
import pandas as pd
import numpy as np
import os
import pickle

from datetime import datetime

DATASET_PATH = r'./dataset.csv'

df = pd.read_csv(DATASET_PATH, sep='|')

SAVE_DIR_BASE = os.path.join(os.getcwd(), 'encodings')

START_INC = 30000
STOP_EXC = 100000

BACKUP_LENGTH = 500

for idx, row in df.iterrows():
    if not (START_INC <= idx < STOP_EXC):
        continue

    if idx%BACKUP_LENGTH == 0:
        df.to_csv(f"./dataset-{START_INC}-{idx}.csv", sep='|', index=False)
        

    print("Starting: #", idx)    
    # Load image from row
    image = face_recognition.load_image_file(row['path'])
    
    # image = face_recognition.load_image_file("family.jpeg")

    # Get all face locations
    face_locations = face_recognition.face_locations(image)

    # Determine largest face in picture, store to variable
    if len(face_locations) == 0:
        continue
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
    # pil_image = Image.fromarray(face_image)
    # pil_image.show()

    # Create encoding
    my_face_encodings = face_recognition.face_encodings(face_image)

    try:
        my_face_encoding = my_face_encodings[0]
    except IndexError:
        with open('error.log', 'a') as outfile:
            outfile.write(f"{row['path']} had no face encodings.\n")
        continue
        

    # We could use pickle... but efficiency :(
    filename = row['path'].partition('wiki')[-1].partition('.jpg')[0] + '.npy'
    filename = '/' + filename.replace('/', '_')

    path_to_open = SAVE_DIR_BASE + filename


    print(f"Saving to {filename}")

    with open(path_to_open, 'wb') as outfile:
        np.save(outfile, my_face_encoding)
        df.iloc[0]['encoding'] = './encoding' + filename

    print()
    print(' -------------------------------- ')
    print()






df.to_csv(f"./dataset-{START_INC}-DONE.csv", sep='|', index=False)

print("Done!")


        