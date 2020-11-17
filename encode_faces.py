import face_recognition
import pandas as pd
import numpy as np
import os

"""

This script is used to take a dataset of images and create an encoding for each image based on
the library face_recognition. 

Our dataset consisted of "path|name|dob|gender" and we added "|encoding" with this script

"""

# Path to dataset
DATASET_PATH = r'./dataset.csv'

# Read the current dataset
df = pd.read_csv(DATASET_PATH, sep='|')

# Directory to save the encodings to
SAVE_DIR_BASE = os.path.join(os.getcwd(), 'encodings')

# Range of idexes in the dataset to created encodings for
START_INC = 0
STOP_EXC = 100000

# Number of files converted before a backup dataset is created
# This is used un case an error occurs during the enconding process
BACKUP_LENGTH = 500

# Iterate through each row in the dataset
for idx, row in df.iterrows():
    # if the row index is not in the valid range
    if not (START_INC <= idx < STOP_EXC):
        continue

    # Save a backup of the dataset if correct number of images have been processed
    if idx%BACKUP_LENGTH == 0:
        df.to_csv(f"./dataset-{START_INC}-{idx}.csv", sep='|', index=False)
        
    # Tell user what idex is being processed
    print("Starting: #", idx)    
    # Load image from row
    image = face_recognition.load_image_file(row['path'])

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

    # crop image to the largest face
    face_image = image[top:bottom, left:right]

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

    # Save the file
    print(f"Saving to {filename}")
    with open(path_to_open, 'wb') as outfile:
        np.save(outfile, my_face_encoding)
        df.iloc[idx]['encoding'] = './encoding' + filename

    print()
    print(' -------------------------------- ')
    print()





# overwrite and save the dataset
df.to_csv(f"./dataset-{START_INC}-DONE.csv", sep='|', index=False)

print("Done!")


        