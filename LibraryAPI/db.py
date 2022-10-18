import sqlite3

conn = sqlite3.connect('books.sqlite')

cursor = conn.cursor()

sql_query = """ CREATE TABLE books(
    id integer PRIMARY KEY,
    author VARCHAR(50) NOT NULL,
    language VARCHAR(50) NOT NULL,
    title VARCHAR(100) NOT NULL
)
"""
cursor.execute(sql_query)