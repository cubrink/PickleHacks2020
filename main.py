# main file

print("Stupid")

import csv
import wikipedia

#print(wikipedia.summary('Wikipedia'))

broken_names = []
with open('wiki_data_updated_delim.csv', newline='') as csvfile:
    questionmark_reader = csv.reader(csvfile, delimiter='|')
    for idx, row in enumerate(questionmark_reader):
        if '?' in row[1]:
            broken_names.append((idx, row[1].strip()))


#print(broken_names[2][1].strip())
print(broken_names[2][1].replace('?', ''))
#sprint(wikipedia.search(broken_names[2][1].replace('?', '')))
#print(wikipedia.search(broken_names[2][1].partition('?')[0]))
print(wikipedia.suggest(broken_names[2][1].replace('?', '')))


full_name = wikipedia.suggest(broken_names[2][1].replace('?', ''))

person_keywords = ['people', 'player', 'person', 'female', 'male', 'boy', 'girl', 'birth', 'death']

bad_idxs = []

categories = set()

for idx, name in broken_names[:50]:
    suggested_name = wikipedia.suggest(name.replace('?', ''))
    print(f"Suggested name = {suggested_name}")
    try:
        page = wikipedia.page(title=suggested_name)
    except wikipedia.exceptions.PageError:
        bad_idxs.append(idx)
        continue
    categories.update(page.categories)




# print('------------------------------------------------')
# print('Full Name:', full_name)
# print('HTML Link')
# #print(wikipedia.html(full_name))
# print('Categories')
# #print(wikipedia.categories(full_name))
# print('------------------------------------------------')


