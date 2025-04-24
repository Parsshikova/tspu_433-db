import sqlite3
def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn
def create_albums_table(conn):
    sql = '''CREATE TABLE IF NOT EXISTS albums (
  id INTEGER primary key autoincrement,
  title VARCHAR(255),
  description TEXT,
  `year` YEAR
);'''
    conn.execute(sql)

def create_songs_table(conn):
    sql = '''CREATE TABLE IF NOT EXISTS songs (
                id INTEGER primary key autoincrement,
                 title VARCHAR(255),
                 duration INT(3),
                 album_id INTEGER
              );'''
    conn.execute(sql)

def create_song_authors_table(conn):
    sql = '''CREATE TABLE IF NOT EXISTS song_authors (
                song_id INTEGER,
                author_id INTEGER,
                FOREIGN KEY (song_id) REFERENCES songs(id),
                FOREIGN KEY (author_id) REFERENCES authors(id),
                PRIMARY KEY (song_id, author_id)
            );'''
    conn.execute(sql)

def add_album(conn, title, description, year):
    sql = '''INSERT INTO albums (title, description, year) VALUES (?, ?, ?);'''
    cur = conn.cursor()
    cur.execute(sql, (title, description, year))
    conn.commit()
    return cur.lastrowid



def add_song(conn, title, duration, album_id):
    sql = '''INSERT INTO songs (title, duration, album_id) VALUES (?, ?, ?);'''
    cur = conn.cursor()
    cur.execute(sql, (title, duration, album_id))
    conn.commit()
    return cur.lastrowid


def add_song_author(conn, song_id, author_id):
    sql = '''INSERT INTO song_authors (song_id, author_id) VALUES (?, ?);'''
    cur = conn.cursor()
    cur.execute(sql, (song_id, author_id))
    conn.commit()
    cur = conn.cursor()
    cur.execute(sql, (song_id, author_id))
    conn.commit()


if __name__ == "__main__":
    database = "music.db"


    conn = create_connection(database)

    
    create_albums_table(conn)
    create_songs_table(conn)
    create_song_authors_table(conn)

    
    album_id = add_album(conn, "Songs To Remember", "Songs to Remember is the debut studio album by the British pop Scritti Politti.", "1982")
    song_id = add_song(conn, "Hit Song", 240, album_id)
    
   
    add_song_author(conn, song_id, 1)

    conn.close()
