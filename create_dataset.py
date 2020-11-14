import pandas as pd
from scipy.io import loadmat
from datetime import date

MAT_PATH = r'./wiki.mat'

matfile = loadmat(MAT_PATH)

names  =    matfile['wiki']['name'][0][0][0]
dob    =    matfile['wiki']['dob'][0][0][0]
gender =    matfile['wiki']['gender'][0][0][0]
path   =    matfile['wiki']['full_path'][0][0][0]

df = pd.DataFrame([path, names, dob, gender])
df = df.transpose()

df.columns = ['path', 'name', 'dob', 'gender']

encodings = pd.Series([" "] * df.shape[0], dtype=str)
df['encoding'] = encodings

df = df[df['name'].apply(lambda x: len(x)) == 1]

for col in ['path', 'name']:
    df[col] = df[col].apply(lambda x: x[0])


df['path'] = df['path'].apply(lambda x: r'./wiki/' + x)
df['dob'] = df['dob'].apply(lambda x: date.fromordinal(x))
df['gender'].replace([0.0, 1.0], ['Female', 'Male'], inplace=True)

df.to_csv("./dataset.csv", sep='|', index=False)

