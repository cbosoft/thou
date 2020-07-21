import re
import random
from time import sleep
from threading import Thread, Lock

import requests
from bs4 import BeautifulSoup

from thou.database import Database
from thou.words import top_words
from thou.colours import BOLD, FG_GREEN, FG_YELLOW, FG_RED, RESET
from thou.backed_up_queue import BackedUpQueue
from thou.util import remove_escapes
from thou.page import Page


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


    def startup_splash(self, n):
        print(f'Crawler starting with {n} threads.')
        sleep(2)


    def run(self, n=1, **kwargs):

        if n <= 1:
            self.run(**kwargs)
            return

        self.startup_splash(n)

        threads = list()
        for i in range(n):
            threads.append(Thread(target=self._run, kwargs=kwargs))
            threads[-1].start()

        while threads:
            self.urls_q.save()
            threads[0].join(timeout=10.0)
            if not threads[0].is_alive():
                threads.pop(0)


    def _run(self, wait_on_fail=10, wait_forever=True, **kwargs):
        self.running = True
        while self.running:

            while self.urls_q.empty():
                print(f'{FG_YELLOW}No links: waiting {wait_on_fail}s and trying again.{RESET}')
                sleep(wait_on_fail)
                if not wait_forever:
                    break

            if self.urls_q.empty():
                print(f'{FG_RED}No links! Stopping.{RESET}')
                return

            try:
                url = self.urls_q.get(timeout=30)
                page = Page(url, **kwargs)
            except Exception as e:
                print(f'{FG_RED}Encountered error: {e}{RESET}')
                with open('thou_error_log.txt', 'a') as f:
                    f.write(f'{e}\n\n\n')
                continue

            self.database.store(page)

            sleep(0.1)
            for link in page.links:
                self.urls_q.put(link)


    def stop(self):
        self.running = False
        sleep(2)
        exit(0)
