import requests
from bs4 import BeautifulSoup
from thou.database import Database

class Crawler:
    '''crawls the web for links, and storing the result in a database'''

    def __init__(self, seed, database_path='./thou.db'):
        self.database = Database(database_path)
        self.seed = seed

    def run(self):
        if isinstance(self.seed, list):
            for url in self.seed:
                self.scrape(url)
        else:
            self.scrape(self.seed)

    def scrape(self, url):
        resp = requests.get(url)
        if not resp:
            return []

        # download page
        page = BeautifulSoup(resp.content, 'html.parser')

    def get_links(self, url):
        '''get page pointed to by link, return link obj with meta data'''
        return []
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


