import face_recognition
from PIL import Image
import pandas as pd
import numpy as np
import os
import pickle

from datetime import datetime

DATASET_PATH = r'./dataset.csv'

df = pd.read_csv(DATASET_PATH, sep='|')

for idx, row in df.iterrows():
    start = datetime.now()
    print(idx)
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
        print(row['path'])
        input("No face detected: Press enter to continue...")
        
    
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

    print(f"{len(my_face_encodings) =}")

    if len(my_face_encodings) == 0:
        print(" ------------------------ ")
        print(row['path'], "is broken")
        print(" ------------------------ ")

        input("Press enter to continue...")


    try:
        my_face_encoding = my_face_encodings[0]
    except:
        print(row['path'])
        orig_image = Image.fromarray(face_image_orig)
        orig_image.show("Original")
        input("Showing original: Press enter to continue...")

        pil_image = Image.fromarray(face_image)
        pil_image.show("Modified")
        input("Showing Modified: Press enter to continue...")
        

    # We could use pickle... but efficiency :(
    with open(r'./that_dude.npy', 'wb') as outfile:
        np.save(outfile, my_face_encoding)
   

    unknown_encoding = face_recognition.face_encodings(image)

    delta = datetime.now() - start

    print("Total seconds: ", delta.total_seconds())

    # for encoding in unknown_encoding:
    #     results = face_recognition.compare_faces([my_face_encoding], encoding)
    #     print(results)

        