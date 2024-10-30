import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO content (name, text, numeric) VALUES (?, ?, ?)",
            ('First Item', 'This is the first item in our database.', 42)
            )

cur.execute("INSERT INTO content (name, text, numeric) VALUES (?, ?, ?)",
            ('Second Item', 'Here\'s another item with different content.', 123)
            )

connection.commit()
connection.close()