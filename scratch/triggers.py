import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bot.db')
con = sqlite3.connect(DB_PATH)
triggers = con.execute("SELECT name FROM sqlite_master WHERE type='trigger'").fetchall()
print("Triggers:", [x[0] for x in triggers])
