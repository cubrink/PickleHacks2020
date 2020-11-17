import pandas as pd
import os

"""

This script was used to fix an index error in encode_faces.py after running the encodings on 40,000 images.
The error has since been fixed and this file is essential useless.

"""


# Path to dataset
DATASET_PATH = r'./dataset.csv'

# Read the current dataset
df = pd.read_csv(DATASET_PATH, sep='|')

# Directory to save the encodings to
SAVE_DIR_BASE = os.path.join(os.getcwd(), 'encodings')

# Range of idexes in the dataset to created encodings for
START_INC = 15000
STOP_EXC = 30000

# Iterate through each row in the dataset
for idx, row in df.iterrows():
    # if the row index is not in the valid range
    if not (START_INC <= idx < STOP_EXC):
        continue
 
    # We could use pickle... but efficiency :(
    filename = row['path'].partition('wiki')[-1].partition('.jpg')[0] + '.npy'
    filename = '/' + filename.replace('/', '_')

    path_to_open = SAVE_DIR_BASE + filename

    # check for valid file and update the dataset with the encoding location
    if os.path.isfile(path_to_open):
        df.iloc[idx]['encoding'] = './encoding' + filename

    # Save the dataset
    df.to_csv("./dataset.csv", sep='|', index=False)


print("Done!")


        