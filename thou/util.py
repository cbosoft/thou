import re

ANSI_ESCAPE_RE = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')

def remove_escapes(s):
    return ANSI_ESCAPE_RE.sub('', s)

def first_n_chars(s, n):
    l = len(s)
    return s[:min([l, n])]
