class HTMLPage:

    def __init__(self, proto):
        self.proto = proto

    def as_bytes(self, **kwargs):
        s = self.proto.format(**kwargs)
        return s.encode()

index = HTMLPage('''
        <HTML>
          <HEAD>
            <TITLE>thou</TITLE>
          </HEAD>
          <BODY>
            <FORM action="/search">
              <b>Query?</b><input type="text" id="query" name="query">
              <input type="submit" value="Search!">
            </FORM>
          <BODY>
        </HTML>''')

results = HTMLPage('''
        <HTML>
          <HEAD>
            <TITLE>thou</TITLE>
          </HEAD>
          <BODY>
            {results}
          <BODY>
        </HTML>''')
