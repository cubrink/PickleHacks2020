# main file

print("Stupid")

import csv
import wikipedia
import urllib.parse 

url = 'https://en.wikipedia.org/wiki/'
person_keywords = ['people', 'player', 'person', 'female', 'male', 'boy', 'girl', 'birth', 'death']

# hold the broken names and their indexes
broken_names = []
# open new csv file to write to
with open('wiki_data_no_marks.csv', 'w', newline='') as writecsv:
    # open csv file to read from
    with open('wiki_data_updated_delim.csv', newline='') as readcsv:
        # reader and writer helper
        questionmark_reader = csv.reader(readcsv, delimiter='|')
        writer_helper = csv.writer(writecsv, delimiter='|')

        # loop through each row in the csv
        for idx, row in enumerate(questionmark_reader):
            # hold temporary data
            image_location = row[0]
            name_of_person = row[1].strip()
            gender_of_person = row[2]
            url_to_add = ''

            # check if ? is in the name
            if '?' in row[1]:
                # replace the ? with nothing and check the wiki suggest
                name_of_person = wikipedia.suggest(name_of_person.replace('?', '').strip())
                broken_names.append((idx, row[1].strip()))
            
            try:
                # try to get wiki page details and create url
                wiki_page = wikipedia.page(title=name_of_person)
                url_to_add = url + urllib.parse.quote_plus(name_of_person)

            except wikipedia.exceptions.PageError:
                continue

            # write to new csv
            if image_location is not None and name_of_person is not None and gender_of_person is not None:
                writer_helper.writerow([image_location, name_of_person, gender_of_person, url_to_add])







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


