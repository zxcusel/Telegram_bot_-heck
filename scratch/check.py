import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bot.db')

def check():
    con = sqlite3.connect(DB_PATH)
    try:
        con.execute("DROP TABLE geos_new")
    except:
        pass
    cols = con.execute("PRAGMA table_info('geos')").fetchall()
    print("Columns in geos:", [x[1] for x in cols])
    
    schema = con.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='geos'").fetchone()
    print("Schema of geos:", schema[0] if schema else "None")
    
if __name__ == '__main__':
    check()
