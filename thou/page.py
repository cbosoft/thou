from functools import cached_property

import requests
from bs4 import BeautifulSoup

from thou.util import remove_escapes
from thou.words import top_words
from thou.exception import DocTypeError


def tags_with_href(tag):
    return tag.has_attr('href')


class Page:

    def __init__(self, url):
        self.url = url.lower()
        self.soup = self.get_soup()


    def get_soup(self):
        resp = requests.get(self.url)
        resp.raise_for_status()

        try:
            content_type = resp.headers['content-type']
            if not content_type.startswith('text/html'):
                raise DocTypeError(f'Document not html')
        except KeyError:
            pass

        return BeautifulSoup(resp.content, 'html.parser', from_encoding=resp.apparent_encoding)

    @cached_property
    def domain(self):
        urlnoprotocol = self.url.replace(self.protocol, '')
        if '/' in urlnoprotocol:
            return urlnoprotocol[:urlnoprotocol.index('/')]
        else:
            return urlnoprotocol

    @cached_property
    def protocol(self):
        if self.url.startswith('https://'):
            return 'https://'
        else:
            return 'http://'


    @cached_property
    def links(self):
        links = list()
        for tag in self.soup.findAll(tags_with_href):
            link = tag.get('href')

            if not link:
                continue

            if '"' in link:
                continue

            if '#' in link:
                continue

            if not link.startswith('http'):
                if link[0] != '/':
                    link = '/'+link
                link = self.protocol+self.domain+link

            links.append(link)
        return links


    @cached_property
    def tags(self):
        text = self.soup.getText()
        text = remove_escapes(text)
        tags = top_words(text)
        return tags


    @cached_property
    def title(self):
        title = self.soup.title
        if title:
            title = title.text
            title = title.replace('\n', '')
        else:
            title = self.url
        return title


    def tags_as_string(self):
        return ' '.join(sorted(self.tags))
