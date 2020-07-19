from collections import defaultdict

def top_words(s, n=10):
    words = s.split()

    # get popularity of the words
    hist = defaultdict(int)
    for word in words:
        hist[word] += 1

    # sort words by most common
    hist_values = list(hist.items())
    hist_values = list(reversed(sorted(hist_values, key=lambda v: v[1])))
    words = list(zip(*hist_values))[0]
    l = len(words)

    # return up to $n words from sorted list
    return words[:min([l,n])]

