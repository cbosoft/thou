import re
import queue
from time import sleep
from threading import Thread

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


    def run_threads(self, n=0):

        self.running = True

        threads = list()
        for i in range(n):
            threads.append(Thread(target=self.run))
            threads[-1].start()

        for thread in threads:
            thread.join()


    def run(self):
        self.running = True
        while self.running:
            url = self.urls_q.get(timeout=30)
            new_links = self.scrape(url)
            sleep(0.1)
            for link in new_links:
                self.urls_q.put(link)


    def stop(self):
        self.running = False



    def scrape(self, url):
        resp = requests.get(url)
        if not resp:
            return []

        try:
            content_type = resp.headers['content-type']
            if not content_type.startswith('text/html'):
                return []
        except KeyError:
            pass

        # download page
        page = BeautifulSoup(resp.content, 'html.parser')

        # get page meta data
        text, meta = self.get_text_and_meta(page)
        self.database.register_link(url, text, page.title.text, meta)

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


    def get_text_and_meta(self, page):
        text = page.getText()
        text = remove_escapes(text)
        meta = top_words(text)
        return text, meta



