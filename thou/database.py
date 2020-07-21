import os
import re
import sqlite3 as sql

from thou.rank import rank

def first_n_chars(s, n):
    l = len(s)
    return s[:min([l, n])]

class Database:

    def __init__(self, path):
        self.path = path
        if os.path.exists(path):

            if not os.path.isfile(path):
                raise Exception("database exists and is not a file")
            elif self.check_schema():
                print("table loaded")
            else:
                self.init_tables()
        else:
            self.init_tables()


    def check_schema(self):
        conn = sql.connect(self.path)
        rv = False
        try:
            res = conn.execute("SELECT * FROM STORE")
            rv = True
        except:
            pass
        conn.close()
        return rv


    def init_tables(self):
        conn = sql.connect(self.path)
        conn.execute('''CREATE TABLE "STORE" (
                "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                "URL" TEXT NOT NULL UNIQUE,
                "TITLE" TEXT NOT NULL,
                "TAGS" TEXT NOT NULL,
                "LINKCOUNT" NUMBER NOT NULL
                );''');
        conn.execute('CREATE UNIQUE INDEX uniq_url_idx ON STORE (URL);');
        conn.commit()
        print('table created')
        conn.close()


    def register_link(self, url, text, title, meta):
        url = url.lower()

        meta = ' '.join(sorted(meta))
        meta = meta.replace('"', '')
        text = text.replace('"', '""')
        text = '\n'.join([line for line in text.split('\n') if line])
        title = title.replace('"', '""')

        conn = sql.connect(self.path)
        cur = conn.cursor()
        cur.execute(f'SELECT LINKCOUNT FROM STORE WHERE URL="{url}";')
        res = cur.fetchall()
        link_count = 1
        if res:
            link_count += int(res[0][0])

        conn.execute(f'INSERT OR REPLACE INTO "STORE" ("URL", "TITLE", "TAGS", "LINKCOUNT") VALUES("{url}", "{title}", "{meta}", "{link_count}");')
        conn.commit()
        conn.close()
        print(f'({link_count}) {first_n_chars(url, 30)} {first_n_chars(title, 50)}')


    def search(self, *, query):
        query_orig = query
        conn = sql.connect(self.path)
        query = query.lower()
        query = query.split()
        query = '%' + '%'.join(list(sorted(query))) + '%'
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM STORE WHERE LOWER(TAGS) LIKE "{query}" OR URL LIKE "{query}" OR LOWER(TITLE) LIKE "{query}";')
        results = cur.fetchall()
        conn.close()

        if not results:
            return []

        query_as_re = re.compile(query.replace('%', '.*'))
        query_exact = re.compile(query_orig)
        query_lower_exact = re.compile(query_orig.lower())
        rank_and_result = [(rank(result, query_as_re, query_exact, query_lower_exact), result) for result in results]
        ranks, results = zip(*list(reversed(sorted(rank_and_result))))
        return results



if __name__ == "__main__":
    d = Database("a.db")
