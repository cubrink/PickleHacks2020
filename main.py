# This is the main file to compare a users image to the dataset encodings

import face_recognition
from PIL import Image
import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys
from pprint import pprint
import wikipedia
import webbrowser


def create_face_encoding(image_loc, show_image = False):
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


def get_face_encoding(filepath):
    with open(os.path.abspath(filepath), 'rb') as infile:
        encoding = np.load(infile)
    return encoding

    
def compare_faces(face_encodings_fp, face_to_compare):
    # start = datetime.now()
    face_encodings =  [get_face_encoding(fp) for fp in face_encodings_fp]
    results = face_recognition.face_distance(face_encodings, face_to_compare)
    results = [(fp, r) for fp, r in zip(face_encodings_fp, results)]
    # pprint(results)

    # sys.exit(1)
    results.sort(key=lambda x: x[1])


    # delta = datetime.now() - start
    # print("Batch took ", delta.total_seconds(), "to complete.")
    return results[:5]



def batches(df, batch_size):
    i = 0
    while i*batch_size < df.shape[0]:
        max_idx = min( (i+1) * batch_size, df.shape[0])
        yield df.iloc[range(i*batch_size, max_idx)]
        i += 1


if __name__ == "__main__":
    DATASET_PATH = r'./dataset.csv'
    df = pd.read_csv(DATASET_PATH, sep='|')

    # df = df[df['gender'] == 'Female']

    best = [(None, 10)] * 5

    # user_file_location = './wiki/29/39301329_1997-01-07_2015.jpg'
    user_file_location = './test_images/jeff_pic.jpg'
    user_face_encoding = create_face_encoding(user_file_location, True)

    start = datetime.now()
    for batch in batches(df, 128):
        results = compare_faces(list(batch['encoding']), user_face_encoding)
        best.extend(results)
        best.sort(key=lambda x: x[1])
        best = best[:5]
        # pprint("best: ", list(best))
    
    print("Best = ", [b[0] for b in best])
    
    delta = datetime.now() - start
    print("Batch took ", delta.total_seconds(), "to complete.")
    # print(best)

        
    best_person_in_df = df[df['encoding'] == best[0][0]].reset_index()

    wiki_page = wikipedia.page(title=best_person_in_df['name'][0])
    webbrowser.open(wiki_page.url)







