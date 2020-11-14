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


print('------------------------------------------------')
print('Full Name:', full_name)
print('HTML Link')
#print(wikipedia.html(full_name))
print('Categories')
#print(wikipedia.categories(full_name))
print('------------------------------------------------')
