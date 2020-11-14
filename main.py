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

from face_search import find_best_matches



if __name__ == "__main__":
    DATASET_PATH = r'./dataset.csv'
    df = pd.read_csv(DATASET_PATH, sep='|')

    # user_file_location = './test_images/curtis_b.jpg'
    user_file_location = './wiki/29/39301329_1997-01-07_2015.jpg'

    start = datetime.now()

    best = find_best_matches(df, user_file_location, up_to_n=3, show_user_face=True)
    
    print(best['name'])
    
    delta = datetime.now() - start
    print("Batch took ", delta.total_seconds(), "to complete.")

    wiki_page = wikipedia.page(title=best['name'][0])
    Image.open(best['path'][0]).show()
    webbrowser.open(wiki_page.url)







