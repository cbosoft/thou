import time
import http.server
import urllib.parse
import math

from thou.pages import index_page, results_page, format_results
from thou.database import Database

database = 0

def format_dt(dt):
    if dt == 0.0:
        return '0s'
    e = int(math.log10(dt))
    unit = 's'
    if e < -6:
        unit = 'ns'
        dt *= 1e9
    elif e < -3:
        unit = 'us'
        dt *= 1e6
    elif e < 0:
        unit = 'ms'
        dt *= 1e3
    return f'{dt:.2f}{unit}'

class ServerHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/search?'):
            before = time.time()
            query_string = self.path.split('?', 1)[1]
            query_string = urllib.parse.unquote_plus(query_string)
            query_data = query_string.split('=')
            query_dict = {k:v for k,v in zip(query_data[:-1], query_data[1:])}
            self.send_response(200)
            self.end_headers()
            results = database.search(**query_dict)
            dt = time.time() - before
            dt = format_dt(dt)
            formatted_results = format_results(results, time_taken=dt)
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

