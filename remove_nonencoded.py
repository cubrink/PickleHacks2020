import pandas as pd

"""

This script was used to remove all the data from the dataset that did not have an encodings

"""

DATASET_PATH = r'./dataset.csv'

df = pd.read_csv(DATASET_PATH, sep='|')
df = df[df['encoding'] != " "]

df.to_csv("./dataset.csv", sep='|', index=False)
print("Done!")


        