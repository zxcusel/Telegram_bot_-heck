import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bot.db')

def migrate():
    con = sqlite3.connect(DB_PATH)
    con.execute('PRAGMA foreign_keys=OFF')
    
    # 1. Create new table with updated CHECK constraint
    con.execute("""
        CREATE TABLE geos_new (
            user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
            geo TEXT NOT NULL CHECK(geo IN ('bo','pe','uy','py')),
            PRIMARY KEY (user_id, geo)
        )
    """)
    
    # 2. Copy data
    con.execute("INSERT INTO geos_new SELECT * FROM geos")
    
    # 3. Drop old table
    con.execute("DROP TABLE geos")
    
    # 4. Rename new to old
    con.execute("ALTER TABLE geos_new RENAME TO geos")
    
    con.commit()
    con.close()
    print("Migration successful")

if __name__ == '__main__':
    migrate()
