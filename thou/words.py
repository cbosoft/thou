from collections import defaultdict

common_words = ['the', 'and']

def top_words(s, n=10):

    words = list()
    for word in s.split():
        word = word.lower()
        if len(word) <= 2:
            continue
        elif word in common_words:
            continue
        else:
            words.append(word)

    # get popularity of the words
    hist = defaultdict(int)
    for word in words:
        hist[word] += 1

    if not hist:
        return []

    # sort words by most common
    hist_values = list(hist.items())
    hist_values = list(reversed(sorted(hist_values, key=lambda v: v[1])))
    words = list(zip(*hist_values))[0]
    l = len(words)

    # return up to $n words from sorted list
    return words[:min([l,n])]

