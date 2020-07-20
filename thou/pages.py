class HTMLPage:

    def __init__(self, **kwargs):
        self.proto = '''
        <HTML>
          <HEAD>
            <TITLE>{title}</TITLE>
            <style>
              * {{{{ font-family: Arial, Helvetica, sans-serif; }}}}
            </style>
          </HEAD>
          <BODY>
            <DIV style="display: flex; justify-content: center; align-items: center; height: 100%; flex-direction: column;">
              {content}
            </DIV>
          <BODY>
        </HTML>'''.format(**kwargs)

    def as_bytes(self, **kwargs):
        s = self.proto.format(**kwargs)
        return s.encode()


index_page = HTMLPage(title='thou', content='''
            <span style="font-size: large; font-weight: bold; text-align: center;">thou</span>
            <br>
            <FORM action="/search" style="order: 1">
              <input type="text" id="query" name="query">
              <input type="submit" value="Search!">
            </FORM>''')

results_page = HTMLPage(title='thou results', content='{results}')


def format_result(idx, url, text, title, tags):
    #lines = text.split('\n')
    #lines = lines[:min([10, len(lines)])]
    #text = '\n'.join(lines)

    return (f'<div style="padding: 5px; order: {2*(idx+1)};">{idx+1}: <a href="{url}">{title}</a></div>'+
            f'<div style="order: {2*(idx+1) + 1}; color: gray;">{tags}</div>')

def format_results(results):
    style = 'color: gray;' if len(results) else 'color: red; font-weight: bold;'
    rv = f'<div style="order: 0; {style};">{len(results)} results returned.</div>'
    for idx, (__, url, text, title, tags) in enumerate(results):
        rv += format_result(idx, url, text, title, tags)
    return rv
