# This is the main file to compare a users image to the dataset encodings

import face_recognition
from PIL import Image
import pandas as pd
import numpy as np
from datetime import datetime
from pprint import pprint
import wikipedia
import webbrowser
import argparse
from urllib.parse import quote


from face_search import find_best_matches


WIKI_BASE = 'https://en.wikipedia.org/wiki/'


def build_parser():
    """
    Builds parser for command line arguments
    """
    parser = argparse.ArgumentParser(description='Wiki Look-Alike: Find your look-alike on Wikipedia!')
    parser.add_argument(
        'user_filepath', 
        type=str, 
        help='filepath to user\'s image'
    )
    parser.add_argument(
        '-s', 
        default=None,
        type=str, 
        choices=['Male', 'Female'], 
        help='filter results to only show faces of the specified sex'
    )
    parser.add_argument(
        '-d',
        default=False,
        type=bool,
        help='go to first Wikipedia result even if link is ambigious'
    )
    parser.add_argument(
        '-n',
        default=1,
        type=int,
        help='number of matches to display to user'
    )
    parser.add_argument(
        '-f',
        default=True,
        type=bool,
        help='display user\'s face when match is found'
    )
    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    
    DATASET_PATH = r'./dataset.csv'
    df = pd.read_csv(DATASET_PATH, sep='|')

    start = datetime.now()

    best = find_best_matches(df, args.user_filepath, up_to_n=args.n, gender=args.s, show_user_face=args.f)
    
    delta = datetime.now() - start
    print("\nTook ", delta.total_seconds(), "seconds to complete!\n")

    print(best)

    # print found names
    for idx, row in best.iterrows():
        print(' ------------------------------------------------ ')
        print()
        print(f"Our search indicates that you look like {row['name']}.")
        print()
        if args.d:
            url = wikipedia.page(title=row['name']).url
        else:
            try:
                url = wikipedia.page(title=row['name'], auto_suggest=False).url
            except wikipedia.exceptions.DisambiguationError:
                print(f"However, the wikipedia page for that person is ambigious.")
                print(f"Try navigating to the page for {row['name']} (born {row['dob']})")
                print()
                url = WIKI_BASE + quote(row['name'])
        
        Image.open(row['path']).show()
        webbrowser.open(url)

        if (idx+1) != args.n:
            user_continue = input("Type quit to exit the program, or enter to continue... ")
            print()

            if user_continue.lower().strip() == 'quit':
                break
    
    print(' ------------------------------------------------ ')
    print()
    print()
    print()
    print("That was the last result! Thanks for using WikiLookAlike!")
    print()
    print()


