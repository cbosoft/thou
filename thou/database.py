import os
import sqlite3 as sql

class Database:

    def __init__(self, path):
        self.path = path
        if os.path.exists(path):

            if not os.path.isfile(path):
                raise Exception("database exists and is not a file")

            conn = sql.connect(path)
            try:
                res = conn.execute("SELECT * FROM A;");
                print("table loaded")
                conn.close()
            except:
                conn.close()
                self.init_tables()
        else:
            self.init_tables()


    def init_tables(self):
        print("initialising database")
        conn = sql.connect(self.path)
        conn.execute("CREATE TABLE \"A\" (\"id\" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT);");
        # TODO: create database scheme here


    def register_link(self, link, meta):
        print(link, meta)
        pass


if __name__ == "__main__":
    d = Database("a.db")
