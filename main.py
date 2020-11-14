# main file

print("Stupid")

import csv
import wikipedia
import urllib.parse 

url = 'https://en.wikipedia.org/wiki/'

keys = ['people', 'player', 'person', 'female', 'male', 'boy', 'girl', 'birth', 'death', 'artist', 'member', 'writer', 'musician', 'actor', 'actress']


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
            if idx > 9:
                break

            # hold temporary data
            image_location = row[0]
            name_of_person = row[1].strip()
            gender_of_person = row[2]
            url_to_add = ''

            # check if ? is in the name
            if '?' in name_of_person:
                # replace the ? with nothing and check the wiki suggest
                name_of_person = wikipedia.suggest(name_of_person.replace('?', '').strip())
                broken_names.append((idx, row[1].strip()))
            
            try:
                # try to get wiki page details and create url
                wiki_page = wikipedia.page(title=name_of_person)

                # make sure it is actually a person
                # check the categories
                # make sure any of the keywords are in the categories
                is_person = False
                for key in keys:
                    if any([key in cat.lower() for cat in wiki_page.categories]):
                        is_person = True
                        break

                if not is_person:
                    continue
                        
                url_to_add = url + urllib.parse.quote_plus(name_of_person)
            except Exception:
                continue

            # write to new csv
            if image_location is not None and name_of_person is not None:
                writer_helper.writerow([image_location, name_of_person, gender_of_person, url_to_add])















