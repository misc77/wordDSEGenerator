import sqlite3
class Connection:
    connection = None

    def __init__ (self):
        self.connection = sqlite3.connect("dse.db")

    def save(self):
        self.connection.commit()
        #todo

    def close(self):
        self.connection.close()
