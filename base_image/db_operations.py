import sqlite3

# Logging
import logging
logging.basicConfig(format='%(asctime)s -  %(levelname)s - %(message)s')
logger = logging.getLogger('dbops')
logger.setLevel(logging.INFO)

class DB:
    """
    Used to interact with the SQLLITE DB
    """
    def __init__(self, dbname):
        self.dbname = f'/app/db/{dbname}'
        # Initialize DB Cursor
        self.con = sqlite3.connect(self.dbname)

    def insert(self, query, params):
        cur = self.con.cursor()
        cur.execute(query,params)
        self.con.commit()

        return True

    def execute_and_fetch(self, query, params):

        cur = self.con.cursor()
        cur.execute(query,params)
        results = cur.fetchall()
        self.con.close()

        return results

