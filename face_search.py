import face_recognition
from PIL import Image
import pandas as pd
import numpy as np
import os


def create_face_encoding(filepath):
    """
    Returns the face encoding of an image at a specified filepath

    filepath    : Path to image file to get face from
    """
    face_image = create_face_image(filepath)

    # Create encoding
    my_face_encodings = face_recognition.face_encodings(face_image)

    try:
        return my_face_encodings[0]
    except IndexError:
        print('No Face Found!')
        return None


def create_face_image(filepath):
    """
    Returns np.array that contains the largest face at a specified filepath

    filepath    : Path to image file to get face from
    """
    image = face_recognition.load_image_file(filepath)
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

    vertical_border = int((bottom - top) * border_mult / 2)
    horizontal_border = int((right - left) * border_mult / 2)

    # np.array.shape -> y, x
    top = max(0, top-vertical_border)
    bottom = min(image.shape[0], bottom+vertical_border)
    left = max(0, left-horizontal_border)
    right = min(image.shape[1], right+horizontal_border)
    return image[top:bottom, left:right]


def get_face_encoding(filepath):
    """
    Loads a face encoding from a specified filepath

    filepath            : Path to face encoding
    """
    with open(os.path.abspath(filepath), 'rb') as infile:
        encoding = np.load(infile)
    return encoding

    
def compare_faces(face_encodings_fp, face_to_compare, up_to_n=5):
    """
    Returns face top faces from a batch of encodings

    face_encodings_fp   : List of filepaths to face encodings
    face_to_compare     : Encoding of user's face
    up_to_n             : Integer specifying the amount of results to return

    """
    face_encodings =  [get_face_encoding(fp) for fp in face_encodings_fp]
    results = face_recognition.face_distance(face_encodings, face_to_compare)
    results = [(fp, r) for fp, r in zip(face_encodings_fp, results)]

    results.sort(key=lambda x: x[1])

    return results[:up_to_n]


def batches(df, batch_size):
    """
    Generator that yields a specified amount of rows from a DataFrame

    df              : DataFrame containing image metadata
    batch_size      : Size of batches to use
    """
    i = 0
    while i*batch_size < df.shape[0]:
        max_idx = min( (i+1) * batch_size, df.shape[0])
        yield df.iloc[range(i*batch_size, max_idx)]
        i += 1


def find_best_matches(df, user_image, up_to_n=5, gender=None, show_user_face=False):
    """
    Returns a dataframe of the best matches of a user image

    df              : DataFrame containing image metadata
    user_image      : Filepath to the user image
    up_to_n         : The amount of results to return
    show_user_face  : Toggles whether the user will see their own face
    """
    if gender is not None:
        df = df[df['gender'] == gender]

    # Set bounds on n
    up_to_n = max(min(up_to_n, 128), 1)

    # Create temp list of best results
    best = [(None, 10)] * up_to_n

    user_face_encoding = create_face_encoding(user_image)
    for batch in batches(df, 128):
        # Iterate through faces encodings, 128 at a time
        results = compare_faces(list(batch['encoding']), user_face_encoding)
        best.extend(results)
        best.sort(key=lambda x: x[1])
        best = best[:up_to_n]

    # Sanitize results
    df = df[df['encoding'].isin([b[0] for b in best])]
    df.reset_index(inplace=True)

    # Sort by best result first
    # STILL TO COME.....

    if show_user_face:
        # Show user face, if specified
        face_image = create_face_image(user_image)
        Image.fromarray(face_image).show()
    return df
    



if __name__ == "__main__":
    from datetime import datetime

    DATASET_PATH = r'./dataset.csv'
    df = pd.read_csv(DATASET_PATH, sep='|')

    user_file_location = './test_images/jeff_pic.jpg'

    start = datetime.now()
    results = find_best_matches(df, user_file_location, up_to_n=10, show_user_face=True)
    delta = datetime.now() - start
    print("Batch took ", delta.total_seconds(), "to complete.")
    print(results)
