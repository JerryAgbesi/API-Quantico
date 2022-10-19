# import sqlite3
import os
import pymysql
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.','.env')

load_dotenv(dotenv_path=env_path)

dbhost = os.getenv('Host')
dbname = os.getenv('database')
dbuser = os.getenv('user')
dbpassword= os.getenv('password')



# conn = sqlite3.connect('books.sqlite')
conn = pymysql.connect(host=  dbhost,
database=  dbname,
 user = dbuser,
 password = dbpassword,
 charset = "utf8mb4",
 cursorclass = pymysql.cursors.DictCursor)

cursor = conn.cursor()

sql_query = """ CREATE TABLE books(
    id integer PRIMARY KEY AUTO_INCREMENT,
    author VARCHAR(50) NOT NULL,
    language VARCHAR(50) NOT NULL,
    title VARCHAR(100) NOT NULL
)
"""
cursor.execute(sql_query)
cursor.close()