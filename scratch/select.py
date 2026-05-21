import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bot.db')
con = sqlite3.connect(DB_PATH)
print("Geos:", con.execute("SELECT * FROM geos").fetchall())
