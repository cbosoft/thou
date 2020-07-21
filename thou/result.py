import re
from functools import lru_cache


@lru_cache
def get_query_regexes(query):
    query_as_re = re.compile(query.replace(' ', '.*'))
    query_exact_re = re.compile(query)
    query_lower_re = re.compile(query, re.IGNORECASE)
    return query_as_re, query_exact_re, query_lower_re


class Result:

    def __init__(self, id, url, title, tags, link_count, query):
        self.id = id
        self.url = url
        self.title = title
        self.tags = tags
        self.link_count = link_count
        self.query_regexes = get_query_regexes(query)


    @lru_cache
    def rank(self, *, exact_points=100, exact_insensitive_points=80, url_points=10, title_points=5, tags_points=5):
        query_as_re, query_exact_re, query_lower_re = self.query_regexes

        if query_exact_re.match(self.title) or query_exact_re.match(self.url):
            return exact_points + self.link_count
        elif query_lower_re.match(self.title.lower()):
            return exact_insensitive_points + self.link_count

        rank = self.link_count
        weights = url_points, title_points, tags_points
        components = (self.url, self.title, self.tags)
        for weight, component in zip(weights, components):
            rank += weight

        return rank


    def __lt__(self, other):
        '''return true if OTHER is GREATER than SELF'''
        return self.rank() > other.rank()
