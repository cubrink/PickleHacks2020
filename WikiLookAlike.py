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
import argparse

from face_search import find_best_matches


def build_parser():
    parser = argparse.ArgumentParser(description='Wiki Look-Alike: Find your look-alike on Wikipedia!')
    parser.add_argument(
        'user_filepath', 
        type=str, 
        help='filepath to user\'s image'
    )
    parser.add_argument(
        '-s', 
        default=None, 
        nargs=1, 
        type=str, 
        choices=['Male', 'Female'], 
        help='filter results to only show faces of the specified sex'
    )
    parser.add_argument(
        '-d',
        default=False,
        type=bool,
        nargs=1, 
        help='go to first Wikipedia result even if link is ambigious'
    )
    parser.add_argument(
        '-n',
        default=1,
        type=int,
        # nargs=1,
        help='number of matches to display to user'
    )
    parser.add_argument(
        '-f',
        default=True,
        type=bool,
        nargs=1,
        help='display user\'s face when match is found'
    )
    return parser



if __name__ == "__main__":
    
    parser = build_parser()
    args = parser.parse_args()
    
    DATASET_PATH = r'./dataset.csv'
    df = pd.read_csv(DATASET_PATH, sep='|')

    start = datetime.now()

    best = find_best_matches(df, args.user_filepath, up_to_n=args.n, gender=args.s[0], show_user_face=args.f)
    
    # print(best['name'])
    
    delta = datetime.now() - start
    print("\nTook ", delta.total_seconds(), "seconds to complete!\n")

    # print found names
    for idx, row in best.iterrows():
        print(row)

    wiki_page = wikipedia.page(title=best['name'][0])
    Image.open(best['path'][0]).show()
    webbrowser.open(wiki_page.url)







