import os
import sqlite3 as sql

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
        conn.execute('CREATE TABLE "STORE" ("id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "URL" TEXT NOT NULL, "TAGS" TEXT NOT NULL);');
        conn.execute('CREATE UNIQUE INDEX uniq_url_idx ON STORE (URL);');
        conn.commit()
        print('table created')
        conn.close()


    def register_link(self, url, meta):
        conn = sql.connect(self.path)
        meta = ' '.join(sorted(meta))
        meta = meta.replace('"', '')
        conn.execute(f'INSERT OR REPLACE INTO "STORE" ("URL", "TAGS") VALUES("{url}", "{meta}");')
        conn.commit()
        conn.close()


    def search(self, *, query):
        conn = sql.connect(self.path)
        query = query.split()
        query = '%'.join(list(sorted(query)))
        cur = conn.cursor()
        cur.execute(f'SELECT URL FROM STORE WHERE TAGS LIKE "%{query}%";')
        res = cur.fetchall()
        conn.close()
        return '<ul>' + '\n'.join([f'<li><a href="{r[0]}">{r[0]}</a></li>' for r in res]) + '</ul>'



if __name__ == "__main__":
    d = Database("a.db")
