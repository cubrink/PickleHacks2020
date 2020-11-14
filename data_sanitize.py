#!/usr/bin/python

import pandas as pd
import wikipedia


df = pd.read_csv(r'wiki_data_updated_delim.csv', delimiter='|')

df['gender'].replace(['.*0.000000', '.*1.000000'], ['Female', 'Male'], inplace=True, regex=True)
df['name'] = df['name'].apply(lambda x: x.strip())

bad_rows = df[df.name.str.contains('\?')]

broken_names = bad_rows.name

person_keywords = ['people', 'player', 'person', 'female', 'male', 'boy', 'girl', 'birth', 'death', 'artist', 'member', 'writer', 'musician', 'actor', 'actress']

bad_names = []

categories = set()

for name in broken_names[:50]:
    suggested_name = wikipedia.suggest(name.replace('?', ''))
    print(f"Suggested name = {suggested_name}")
    try:
        page = wikipedia.page(title=suggested_name)
    except Exception:
        bad_names.append(name)
        continue
    categories.update(page.categories)
