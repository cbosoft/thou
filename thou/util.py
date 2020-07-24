import re
from functools import lru_cache

ANSI_ESCAPE_RE = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')

def remove_escapes(s):
    return ANSI_ESCAPE_RE.sub('', s)

def sql_friendly(s):
    s = s.replace('"', '""')
    return s

def first_n_chars(s, n):
    l = len(s)
    return s[:min([l, n])]

@lru_cache
def levenshtein(s, t, i=None, j=None):

    if i is None:
        i = len(s) - 1

    if j is None:
        j = len(t) - 1

    if min([i, j]) == 0:
        return max([i + 1, j + 1])

    ind = 0 if s[i] == t[j] else 1

    return min([
            levenshtein(s, t, i - 1, j) + 1,
            levenshtein(s, t, i, j - 1) + 1,
            levenshtein(s, t, i - 1, j - 1) + ind
        ])
