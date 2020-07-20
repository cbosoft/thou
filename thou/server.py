import http.server
import urllib.parse

from thou.pages import index_page, results_page, format_results
from thou.database import Database

database = 0

class ServerHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/search?'):
            query_string = self.path.split('?', 1)[1]
            query_string = urllib.parse.unquote_plus(query_string)
            query_data = query_string.split('=')
            query_dict = {k:v for k,v in zip(query_data[:-1], query_data[1:])}
            self.send_response(200)
            self.end_headers()
            results = database.search(**query_dict)
            formatted_results = format_results(results)
            self.wfile.write(results_page.as_bytes(results=formatted_results))

        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(index_page.as_bytes())

def run(db_path):
    global database
    database = Database(db_path)
    with http.server.ThreadingHTTPServer( ('', 8000), ServerHandler) as server:
        server.serve_forever()

