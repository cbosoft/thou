
def rank(result, query_as_re, query_exact, query_lower_exact, *, exact_points=100, exact_insensitive_points=80, url_points=10, title_points=5, tags_points=5):
    weights = url_points, title_points, tags_points
    __, url, title, __, titlenocase, tagsnocase, link_count = result
    result = (url, titlenocase, tagsnocase)

    rank = link_count
    if query_exact.match(title):
        rank += exact_points

    if query_lower_exact.match(title):
        rank += exact_insensitive_points

    for weight, component in zip(weights, result):
        #rank += len(query_as_re.findall(component))*weight
        if query_as_re.match(component):
            rank += weight

    return rank
