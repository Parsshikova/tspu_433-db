import sqlite3

connection = sqlite3.connect('database.sqlite')

def create_table_authors(conn):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL
) 
''')
    conn.commit()