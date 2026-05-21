import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bot.db')
con = sqlite3.connect(DB_PATH)
try:
    con.execute("INSERT INTO geos (user_id, geo) VALUES (?, ?)", (8110065908, 'uy'))
    con.commit()
    print("Insert succeeded!")
except Exception as e:
    print("Insert failed:", repr(e))
