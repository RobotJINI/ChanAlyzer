from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin
import re
import json
import sys
import argparse
import os
import time
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import stylecloud


class WordCloud():
    def __init__(self):
        self._words = []
        self._stop_words = set(stopwords.words('english'))
        self._stop_words.update(['gt', 'quot', 'http', 'https', 'thread', 'new', 'people', 't'])
    
    def load_from_threads(self, chan_threads):
        for chan_thread in chan_threads:
            new_words = chan_thread.get_words()
            new_words = self._remove_stop_words(new_words)
            self._words.extend(new_words)
    
    def save(self):
        stylecloud.gen_stylecloud(text=" ".join(self._words), collocations=False, output_name=f'ChanAlyzer_{int(time.time())}.png')
            
    def _remove_stop_words(self, words):
        words = [word.strip() for word in words if word.strip()]
        words = [word for word in words if not re.search('[^A-Za-z]', word)]
        return [word for word in words if (word.lower() not in self._stop_words) and (len(word) > 2)]
        


class ChanAlyzer:
    def __init__(self, url, new_snapshot=False, snapshot_loc='snapshot.txt', db_name='ChanAlyzer.db'):
        self._url = url
        self._new_snapshot = new_snapshot
        self._chan_threads = []
        self._db_name = db_name
        self._load_snapshot(new_snapshot, snapshot_loc)
        
    def word_cloud(self):
        wc = WordCloud()
        wc.load_from_threads(self._chan_threads)
        wc.save()
    
    def _parse_threads(self, soup):
        match = re.search(r'var catalog = ({.*?});', soup)
        if match:
            catalog_str = match.group(1)
            catalog_dict = json.loads(catalog_str)
            for val in catalog_dict['threads']:
                self._chan_threads.append(ChanThread.from_dict(urljoin(self._url, f'thread/{val}'), catalog_dict['threads'][val]))
        else:
            print("Could not find catalog variable")
    
    def _load_snapshot(self, new_snapshot, snapshot_loc):
        if not os.path.exists(snapshot_loc) or new_snapshot:
            print("Saving new snapshot")
            self._save_snapshot(snapshot_loc)
        soup = self._read_snapshot(snapshot_loc)
        self._parse_threads(soup)
        
    def _read_snapshot(self, snapshot_loc):
        with open(snapshot_loc, 'r') as file:
            return file.read()
        
    def _save_snapshot(self, snapshot_loc):
        req = urllib.request.Request(urljoin(self._url, 'catalog'), headers={'User-Agent': 'Mozilla/5.0'})
        r = urllib.request.urlopen(req).read()
        
        soup = str(BeautifulSoup(r, "lxml"))
        with open(snapshot_loc, 'w') as file:
            file.write(soup)
        
class ChanThread:
    def __init__(self, url, date, file, lr, country, author, imgurl, sub, teaser):
        self.url = url
        self.date = date
        self.file = file
        self.lr = lr
        self.country = country
        self.author = author
        self.imgurl = imgurl
        self.sub = sub
        self.teaser = teaser
        
    def get_words(self):
        return word_tokenize(self.sub) + word_tokenize(self.teaser)

    @classmethod
    def from_dict(cls, url, data):
        country = data['country'] if (data.get('country') is not None) else 'null'
        imgurl = data['imgurl'] if (data.get('imgurl') is not None) else 'null'
        return cls(url, data['date'], data['file'], data['lr'], country, data['author'], imgurl, data['sub'], data['teaser'])


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='ChanAlyzer')
    parser.add_argument('-s', '--new_snapshot', help='Save new snapshot', action='store_true')
    
    args = parser.parse_args()
    chanalyzer = ChanAlyzer('https://boards.4chan.org/biz/', args.new_snapshot)
    chanalyzer.word_cloud()
    
