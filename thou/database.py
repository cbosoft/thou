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
        print('table created')
        conn.close()


    def register_link(self, url, meta):
        conn = sql.connect(self.path)
        meta = ' '.join(sorted(meta))
        conn.execute(f'INSERT OR REPLACE INTO "STORE" ("URL", "TAGS") VALUES("{url}", "{meta}");')
        conn.commit()
        conn.close()


if __name__ == "__main__":
    d = Database("a.db")
