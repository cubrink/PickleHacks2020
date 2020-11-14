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


    print("Starting: #", idx)    
        


    # try:
    #     my_face_encoding = my_face_encodings[0]
    # except IndexError:
    #     with open('error.log', 'a') as outfile:
    #         outfile.write(f"{row['path']} had no face encodings.\n")
    #     continue
        

    # We could use pickle... but efficiency :(
    filename = row['path'].partition('wiki')[-1].partition('.jpg')[0] + '.npy'
    filename = '/' + filename.replace('/', '_')

    path_to_open = SAVE_DIR_BASE + filename


    # print(f"Saving to {filename}")

    if os.path.isfile(path_to_open):
        df.iloc[idx]['encoding'] = './encoding' + filename


    # print()
    # print(' -------------------------------- ')
    # print()




df.to_csv(f"./dataset.csv", sep='|', index=False)

print("Done!")



        