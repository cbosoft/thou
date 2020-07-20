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


