import os
import re
import sqlite3 as sql

from thou.util import first_n_chars, sql_friendly
from thou.result import Result


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


    def store(self, page):
        meta = sql_friendly(page.tags_as_string())
        title = sql_friendly(page.title)

        link_count = self.get_link_count(page)

        conn = sql.connect(self.path)
        conn.execute(f'INSERT OR REPLACE INTO "STORE" ("URL", "TITLE", "TAGS", "LINKCOUNT") '+
                f'VALUES("{page.url}", "{title}", "{meta}", "{link_count}");')
        conn.commit()
        conn.close()
        print(f'({link_count}) {first_n_chars(page.url, 30)} {first_n_chars(title, 50)}')


    def search(self, *, query):
        query_orig = query
        conn = sql.connect(self.path)
        query = query.lower()
        query = query.split()
        query = '%' + '%'.join(list(sorted(query))) + '%'
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM STORE WHERE LOWER(TAGS) LIKE "{query}" OR URL LIKE "{query}" OR LOWER(TITLE) LIKE "{query}";')
        rows = cur.fetchall()
        conn.close()

        if not rows:
            return []

        return sorted(Result(*columns, query) for columns in rows)


    def get_link_count(self, page):
        conn = sql.connect(self.path)
        cur = conn.cursor()
        try:
            command = f'SELECT LINKCOUNT FROM STORE WHERE URL="{page.url}";'
            cur.execute(command)
        except Exception:
            print(f'URL: >{page.url}<')
            print(f'CMD: >{command}<')
            raise
        res = cur.fetchall()
        link_count = 1
        if res:
            link_count += int(res[0][0])
        conn.close()
        return link_count



if __name__ == "__main__":
    d = Database("a.db")
