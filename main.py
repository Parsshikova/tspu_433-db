import sqlite3
from ddl import create_table_authors
from dml import add_authors 

connection = sqlite3.connect('database.sqlite')

    

create_table_authors(connection)
add_authors(connection)


print("Hello world")
connection.close()