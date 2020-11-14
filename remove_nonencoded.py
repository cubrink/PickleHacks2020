import pandas as pd

DATASET_PATH = r'./dataset.csv'

df = pd.read_csv(DATASET_PATH, sep='|')
df = df[df['encoding'] != " "]

df.to_csv("./dataset.csv", sep='|', index=False)
print("Done!")


        