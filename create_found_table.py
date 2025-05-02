import sqlite3

conn = sqlite3.connect('lost_found.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS found_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    contact TEXT NOT NULL,
    found_time TEXT NOT NULL,
    found_place TEXT NOT NULL,
    image_path TEXT,
    username TEXT NOT NULL,
    is_approved INTEGER DEFAULT 0
)
''')

conn.commit()
conn.close()

print("✅ Table 'found_items' created successfully.")
