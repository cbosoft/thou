from string import Formatter


class HTMLPage:

    proto = '''
<!DOCTYPE html>
<html>
  <head>
    <title>{title}</title>
    <style>{style}
    </style>
    {extra_head}
  </head>
  <body>
    {body}
  </body>
</html>
'''
    style = '''
      * {
        font-family: sans-serif;
      }
      body, html {
        height: 95%;
        min-height: 300px;
      }
      a {
        text-decoration: none;
      }
      #container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        flex-direction: column;
      }
      #justifyish {
        margin: auto;
        width: 80%;
      }
      #title {
        font-size: 4vmax;
        font-weight: bold;
        text-align: center;
        font-style: italic;
      }
      #searchbutton {
        font-size: large;
        border: none;
        background-color: white;
        color: black;
      }
      #searchbutton:hover {
        color: gray;
      }
      #searchbutton:onclick {
        color: black;
      }
      #link {
        color: black;
        font-weight: bold;
      }
      #url {
        color: gray;
        font-weight: bold;
      }
      #tags {
        color: gray;
        font-size: small;
      }
      #result {
        margin-top: 5px;
        margin-bottom: 5px;
        border-bottom: 1px solid gray;
      }
'''

    def __init__(self, body, title='thou', extra_head=''):
        self.title = title
        self.body = body
        self.extra_head = extra_head

    def as_string(self, **kwargs):
        draft_string = self.proto.format(
                title=self.title,
                style='{style}',
                extra_head='{extra_head}',
                body=self.body)
        desired_keys = {sv[1]:'' for sv in Formatter().parse(draft_string) if sv[1] is not None}
        kwargs = {**desired_keys, 'style': self.style, 'extra_head':self.extra_head, **kwargs}
        return draft_string.format(**kwargs)

    def as_bytes(self, **kwargs):
        s = self.as_string(**kwargs)
        return s.encode()


index_page = HTMLPage('''
            <div id="container">
              <span id="title">thou</span>
              <br>
              <form action="/search">
                <input type="text" id="query" name="query">
                <input type="submit" id="searchbutton" value="Search!">
              </form>
            </div>
            <span id="message">{message}</span>
            ''',
            extra_head='''
            <style>
            * {
              font-size: 4vmax;
            }
            #searchbutton {
              font-size: 4vmax;
            }
            #title {
              font-size: 10vmax;
            }
            </style>
            ''')

results_page = HTMLPage('''
            <div id="justifyish">
              <form action="/search">
                <a href="/home" style="color: black; font-size: 2vmax;" id="title">thou</a>
                &nbsp&nbsp<input type="text" id="query" name="query" style="font-size: 2vmax;">
                <input type="submit" id="searchbutton" value="Search!" style="font-size: 2vmax;">
              </form><br>
              {results}
            </div>''')


def format_result(idx, result):
    s = [
            f'<div id="result">',
            f'  <div id="link">{idx+1}: <a href="{result.url}">{result.title}</a></div>',
            f'  <div id="url">{result.url}</div>',
            f'  <div id="tags">{result.tags}</div>',
            f'</div>'
        ]
    return '\n'.join(s)


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
