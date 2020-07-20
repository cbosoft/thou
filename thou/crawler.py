import re
import queue
import random
from time import sleep
from threading import Thread, Lock
import pickle

import requests
from bs4 import BeautifulSoup

from thou.database import Database
from thou.words import top_words

ANSI_ESCAPE_RE = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')

def remove_escapes(s):
    return ANSI_ESCAPE_RE.sub('', s)

def tags_with_href(tag):
    return tag.has_attr('href')


class BackedUpQueue:

    def __init__(self):
        self.lock = Lock()
        self._contents = list()

    def put(self, item):
        with self.lock:
            l = len(self._contents)
            i = 0 if not l else random.randint(0, l - 1)
            self._contents.insert(i, item)

    def get(self, *args, **kwargs):
        with self.lock:
            item = self._contents.pop(0)
            return item

    def empty(self):
        with self.lock:
            return len(self._contents) == 0

    def save(self):
        print('Saving state')
        with open('thou_links.pickle', 'wb') as f:
            with self.lock:
                pickle.dump(self._contents, f)

    def load(self):
        with open('thou_links.pickle', 'rb') as f:
            with self.lock:
                self._contents = pickle.load(f)

class Crawler:
    '''crawls the web for links, and storing the result in a database'''

    def __init__(self, seed, database_path='./thou.db'):
        self.database = Database(database_path)
        self.urls_q = BackedUpQueue()

        try:
            self.urls_q.load()
        except:
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

        while threads:
            self.urls_q.save()
            threads[0].join(timeout=10.0)
            if not threads[0].is_alive():
                threads.pop(0)


    def run(self):
        self.running = True
        while self.running:

            if self.urls_q.empty():
                print('No more links.')
                return

            try:
                url = self.urls_q.get(timeout=30)
                new_links = self.scrape(url)
            except Exception as e:
                print(str(e))
                with open('thou_error_log.txt', 'a') as f:
                    f.write(f'{e}\n\n\n')
                continue
            sleep(0.1)
            for link in new_links:
                self.urls_q.put(link)


    def stop(self):
        self.running = False
        sleep(2)
        exit(0)



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
        if meta:
            title = page.title
            if title:
                title = title.text
            else:
                title = url
            self.database.register_link(url, text, title, meta)

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



