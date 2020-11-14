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

START_INC = 15000
STOP_EXC = 30000

BACKUP_LENGTH = 500

for idx, row in df.iterrows():
    if not (START_INC <= idx < STOP_EXC):
        continue
 

    # We could use pickle... but efficiency :(
    filename = row['path'].partition('wiki')[-1].partition('.jpg')[0] + '.npy'
    filename = '/' + filename.replace('/', '_')

    path_to_open = SAVE_DIR_BASE + filename


    if os.path.isfile(path_to_open):
        df.iloc[idx]['encoding'] = './encoding' + filename


    df.to_csv("./dataset.csv", sep='|', index=False)


print("Done!")


        