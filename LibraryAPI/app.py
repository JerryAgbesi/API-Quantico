from flask import Flask,request,jsonify
# import sqlite3
import pymysql
from dotenv import load_dotenv
import os
from pathlib import Path



env_path = Path('.','.env')

load_dotenv(dotenv_path=env_path)

dbhost = os.getenv('Host')
dbname = os.getenv('database')
dbuser = os.getenv('user')
dbpassword= os.getenv('password')

app =  Flask(__name__)

def db_connection():
  conn = None
  try:
   conn = pymysql.connect(host=  dbhost,
database=  dbname,
 user = dbuser,
 password = dbpassword,
 charset = "utf8mb4",
 cursorclass = pymysql.cursors.DictCursor)
   print("database connected")
  except pymysql.error as e:
    print(e) 
  return conn   


@app.route('/',methods=["GET"])
def home():
    return "Welcome to the Library API"

@app.route('/books',methods = ['GET','POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM books')

        books = [dict(id=row['id'],author = row['author'],language = row['language'],title = row['title'] )
        for row in cursor.fetchall()]
    
        if books is not None:
          return jsonify(books)

    if request.method == 'POST':
      newAuthor = request.form["author"]
      newLanguage = request.form["language"]
      newTitle = request.form["title"]

      command = """ INSERT INTO books(author, language, title)
      VALUES(%s, %s, %s)"""

      cursor.execute(command,(newAuthor, newLanguage, newTitle))
      conn.commit()

      return f"Book with index: {cursor.lastrowid} created successfully",200  

@app.route('/books/<int:id>',methods=["GET","PUT","DELETE"])
def manipulate(id):
    conn =  db_connection()
    cursor = conn.cursor()
    book = None

    if request.method == 'GET':
        cursor.execute('SELECT * FROM books WHERE id = %s',(id,))
        row = cursor.fetchall()
        for r in row:
          book = r
        if book is not None:
          return jsonify(book),200
        else:
          return "Id not found",404 
            
    if request.method == 'PUT':
      script = """UPDATE books
      SET author=%s,
      language = %s,
      title = %s
      WHERE id = %s"""
      
      update_title = request.form["title"]
      update_author= request.form['author']
      update_language = request.form['language']

      updated_book = {
        "id":id,
        "author":update_author,
        "language":update_language,
        "title":update_title

      }

      cursor.execute(script,(update_author,update_language,update_title,id))
      conn.commit()
      return jsonify(updated_book),200

    if request.method == 'DELETE': 
      cursor.execute("DELETE FROM books WHERE id=%s",(id,))
      conn.commit()
      return f"Book with ID {id},has been deleted"



      



if __name__ == '__main__':
    app.run(debug=True)

