import wikipedia
import webbrowser
from pprint import pprint
from urllib.parse import quote

WIKI_BASE = 'https://en.wikipedia.org/wiki/'

name = 'Daniel Smith'
dob = '1980-01-01'

try:
    page = wikipedia.page(title=name,auto_suggest=False)
    print(page.url)
except wikipedia.exceptions.DisambiguationError as e:
    print(f"Our search indicates the user looks like {name}.")
    print(f"However, the wikipedia page for that person is ambigious.")
    print(f"Try navigating to the page for {name} (born {dob})")

    url = WIKI_BASE + quote(name)
    webbrowser.open(url)

except UserWarning:
    pass