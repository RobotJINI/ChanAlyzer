from bs4 import BeautifulSoup
import urllib.request
from IPython.display import HTML
import re

req = urllib.request.Request('https://boards.4chan.org/pol/catalog', headers={'User-Agent': 'Mozilla/5.0'})
r = urllib.request.urlopen(req).read()
soup = BeautifulSoup(r, "lxml")
type(soup)

print(soup.prettify())