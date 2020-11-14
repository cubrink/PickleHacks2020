# main file

print("Stupid")

import csv
import wikipedia
import urllib.parse 

url = 'https://en.wikipedia.org/wiki/'
person_keywords = ['people', 'player', 'person', 'female', 'male', 'boy', 'girl', 'birth', 'death']

broken_names = []
with open('wiki_data_no_marks.csv', 'w', newline='') as writecsv:
    with open('wiki_data_updated_delim.csv', newline='') as readcsv:
        questionmark_reader = csv.reader(readcsv, delimiter='|')
        writer_helper = csv.writer(writecsv, delimiter='|')

        # loop through each row in the csv
        for idx, row in enumerate(questionmark_reader):
            image_location = row[0]
            name_of_person = row[1].strip()
            gender_of_person = row[2]

            if '?' in row[1]:
                name_of_person = wikipedia.suggest(name_of_person.replace('?', '').strip())
                broken_names.append((idx, row[1].strip()))
            
            try:
                wiki_page = wikipedia.page(title=name_of_person)
            except wikipedia.exceptions.PageError:
                pass

            
            if image_location is not None and name_of_person is not None and gender_of_person is not None:
                writer_helper.writerow([image_location, name_of_person, gender_of_person])



#print(broken_names[2][1].strip())
#    print(broken_names[2][1].replace('?', ''))
#sprint(wikipedia.search(broken_names[2][1].replace('?', '')))
#print(wikipedia.search(broken_names[2][1].partition('?')[0]))
#    print(wikipedia.suggest(broken_names[2][1].replace('?', '')))


# full_name = wikipedia.suggest(broken_names[2][1].replace('?', ''))




# Goals/TODO
# 1. find a way to remove the ? from each person's name
# 2. 


print('------------------------------------------------')
# print('Full Name:', full_name)
print('HTML Link')
#print(wikipedia.html(full_name))
print('Categories')
#print(wikipedia.categories(full_name))
print('------------------------------------------------')
