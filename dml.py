def add_authors(conn):
    authors = [
        {
            'name':  'Scritti Politti',

        },
        {
            'name': 'Radiohead',
        },
    ]
    for author in authors:
        add_author_to_db(conn, author.get('name'))
    print(authors)
   


def add_author_to_db(conn, name: str):
    cursor = conn.cursor()
    cursor.execute(f''' 
INSERT INTO authors (name) VALUES ('{name}')
    ''')
    conn.commit()


    