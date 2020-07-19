import re
import queue
from time import sleep

import requests
from bs4 import BeautifulSoup

from thou.database import Database
from thou.words import top_words

ANSI_ESCAPE_RE = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')

def remove_escapes(s):
    return ANSI_ESCAPE_RE.sub('', s)

def tags_with_href(tag):
    return tag.has_attr('href')

class Crawler:
    '''crawls the web for links, and storing the result in a database'''

    def __init__(self, seed, database_path='./thou.db'):
        self.database = Database(database_path)
        self.urls_q = queue.Queue()

        if isinstance(seed, list):
            for url in seed:
                if not isinstance(url, str):
                    raise TypeError('URLs are expected to be in str format.')
                self.urls_q.put(url)
        elif isinstance(seed, str):
            self.urls_q.put(seed)
        else:
            raise TypeError('URLs are expected to be in str format.')


    def run(self):
        while True:
            url = self.urls_q.get()
            new_links = self.scrape(url)
            sleep(0.1)
            for link in new_links:
                self.urls_q.put(link)


    def scrape(self, url):
        resp = requests.get(url)
        if not resp:
            return []

        # download page
        page = BeautifulSoup(resp.content, 'html.parser')

        # get page meta data
        meta = self.get_meta(page)
        self.database.register_link(url, meta)

        # return links
        links = self.get_links(page, url)
        return links


    def get_links(self, page, url):
        '''given page, return list of links on page'''
        links = list()
        for tag in page.findAll(tags_with_href):
            link = tag.get('href')
            if not link.startswith('http'):
                link = url+'/'+link
            links.append(link)
        return links


    def get_meta(self, page):
        s = page.getText()
        s = remove_escapes(s)
        s = top_words(s)
        return s



