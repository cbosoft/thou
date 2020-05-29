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
        links = self.get_links(url)
        self.database.register_link(links)

    def get_links(self, url):
        '''get page pointed to by link, return link obj with meta data'''
        return []


