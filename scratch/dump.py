import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bot.db')
con = sqlite3.connect(DB_PATH)
tables = con.execute("SELECT name, sql FROM sqlite_master WHERE type='table'").fetchall()
for name, sql in tables:
    print(f"Table {name}:")
    print(sql)
    print("-" * 40)
