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

START_INC = 0
STOP_EXC = 100000


for idx, row in df.iterrows():
    if not (START_INC <= idx < STOP_EXC):
        continue
 
    # check if the encoding element is empty
    if row['encoding'] is None or row['encoding'] == '\n' or row['encoding'] == ' ':
        # erase row from df
        df.drop([idx])

df.to_csv("./dataset.csv", sep='|', index=False)
print("Done!")


        