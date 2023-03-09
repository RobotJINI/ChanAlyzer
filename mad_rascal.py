from bs4 import BeautifulSoup
import urllib.request
import re
import json
import sys
import argparse


def save_snapshot():
    req = urllib.request.Request('https://boards.4chan.org/pol/catalog', headers={'User-Agent': 'Mozilla/5.0'})
    r = urllib.request.urlopen(req).read()
    
    soup = str(BeautifulSoup(r, "lxml"))
    with open('snapshot.txt', 'w') as file:
        file.write(soup)
    return soup
        
def load_snapshot():
    with open('snapshot.txt', 'r') as file:
        return file.read()


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Mad rascal')
    parser.add_argument('-s', '--save_snapshot', help='Save new snapshot', action='store_true')
    
    args = parser.parse_args()
    if args.save_snapshot:
        soup = save_snapshot()
    else:
        soup = load_snapshot()
    
    match = re.search(r'var catalog = ({.*?});', soup)
    if match:
        catalog_str = match.group(1)
        # parse the JSON string into a Python dictionary
        catalog_dict = json.loads(catalog_str)
        for val in catalog_dict['threads']:
            print(catalog_dict['threads'][val])
        #print(catalog_dict)
    else:
        print("Could not find catalog variable")