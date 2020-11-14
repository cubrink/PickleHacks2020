# This is the main file to compare a users image to the dataset encodings

import face_recognition
from PIL import Image
import pandas as pd
import numpy as np
import os
import pickle
import time
from multiprocessing import Process

from datetime import datetime

DATASET_PATH = r'./dataset.csv'

df = pd.read_csv(DATASET_PATH, sep='|')

ENCODINGS_DIR_BASE = os.path.join(os.getcwd(), 'encodings')


TIMEOUT_LENGTH = 60000      # timeout time in milliseconds


def compare_user_image(df_start_index, df_stop_index, timeout = 60000):
    pass


def test_timeout():
    print('Testing Timeout Function')
    while True:
        time.sleep(1)

process1 = Process(target=test_timeout, name='testing_timeout')
if __name__ == '__main__':
    process1.start()
    process1.join(timeout=5)
    process1.terminate()

# if process1.exitcode is None:
#     print(f'Oops, process1 timeouts!')











