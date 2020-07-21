class HTMLPage:

    def __init__(self, proto):
        self.proto = proto

    def as_bytes(self, **kwargs):
        s = self.proto.format(**kwargs)
        return s.encode()


index_page = HTMLPage('''
        <HTML>
          <HEAD>
            <TITLE>thou</TITLE>
            <style>
              * {{ font-family: Arial, Helvetica, sans-serif; }}
            </style>
          </HEAD>
          <BODY>
            <DIV style="display: flex; justify-content: center; align-items: center; height: 100%; flex-direction: column;">
              <span style="font-size: large; font-weight: bold; text-align: center;">thou</span>
              <br>
              <FORM action="/search" style="order: 1">
                <input type="text" id="query" name="query">
                <input type="submit" value="Search!">
              </FORM>
            </DIV>
          <BODY>
        </HTML>''')

index_with_message_page = HTMLPage('''
        <HTML>
          <HEAD>
            <TITLE>thou</TITLE>
            <style>
              * {{ font-family: Arial, Helvetica, sans-serif; }}
            </style>
          </HEAD>
          <BODY>
            <DIV style="display: flex; justify-content: center; align-items: center; height: 100%; flex-direction: column;">
              <span style="font-size: large; font-weight: bold; text-align: center;">thou</span>
              <br>
              <FORM action="/search" style="order: 1">
                <input type="text" id="query" name="query">
                <input type="submit" value="Search!">
              </FORM>
              <span style="font-weight: bold; order 10;">{message}</span>
            </DIV>
          <BODY>
        </HTML>''')

results_page = HTMLPage('''
        <HTML>
          <HEAD>
            <TITLE>thou</TITLE>
            <style>
              * {{ font-family: Arial, Helvetica, sans-serif; }}
            </style>
          </HEAD>
          <BODY>
            <DIV style="margin: auto; width: 80%; min-width: 300px;">
              <FORM action="/search" style="order: 1">
                <a href="/home" style="color: black; text-decoration: none; font-weight: bold;">thou</a>
                <input type="text" id="query" name="query">
                <input type="submit" value="Search!">
              </FORM><br>
              {results}
            </DIV>
          <BODY>
        </HTML>''')


def format_result(idx, result):
    return (f'<div style="padding: 5px; order: {2*(idx+1)};">{idx+1}: <a href="{result.url}">{result.title}</a><span style="font-size: small; color: gray; padding: 5px;">{result.url}</span></div>'+
            f'<div style="order: {2*(idx+1) + 1}; color: gray;">{result.tags}</div>')


def format_results(results, *, time_taken, query, max=30):

    rv = ''
    l = len(results)
    if 0 < l <= max:
        rv += f'<div style="order: 0; color: gray;">{len(results)} results returned for "{query}" in {time_taken}.</div>'
    elif l > max:
        rv += f'<div style="order: 0; color: black;">{len(results)} results returned for "{query}" in {time_taken}; showing top {max}</div>'
        results = results[:max]
    else:
        rv += f'<div style="order: 0; color: red; font-weight: bold;">No results returned for "{query}" ({time_taken}).</div>'

    for idx, result in enumerate(results):
        rv += format_result(idx, result)
    return rv
