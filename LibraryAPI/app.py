from flask import Flask,request,jsonify
import sqlite3


app =  Flask(__name__)

def db_connection():
  conn = None
  try:
   conn = sqlite3.connect('books.sqlite')
   print("database connected")
  except sqlite3.error as e:
    print(e) 
  return conn   

# books = open('book.json','r+')
# books = list(books.read())

@app.route('/',methods=["GET"])
def home():
    return "Welcome to the Library API"

@app.route('/books',methods = ['GET','POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        query = conn.execute('SELECT * FROM books')

        books = [dict(id=row[0],author = row[1],language = row[2],title = row[3] )
        for row in query.fetchall()]
    
        if books is not None:
          return jsonify(books)

    if request.method == 'POST':
      newAuthor = request.form["author"]
      newLanguage = request.form["language"]
      newTitle = request.form["title"]

      command = """ INSERT INTO books(author, language, title)
      VALUES(?, ?, ?)"""

      cursord =  cursor.execute(command,(newAuthor, newLanguage, newTitle))
      conn.commit()

      return f"Book with index: {cursord.lastrowid} created successfully",200  

@app.route('/books/<int:id>',methods=["GET","PUT","DELETE"])
def manipulate(id):
    conn =  db_connection()
    cursor = conn.cursor()
    book = None

    if request.method == 'GET':
        cursor.execute('SELECT * FROM books WHERE id = ?',(id,))
        row = cursor.fetchall()
        for r in row:
          book = r
        if book is not None:
          return jsonify(book),200
        else:
          return "Id not found",404 
            
    if request.method == 'PUT':
      script = """UPDATE books
      SET author=?,
      language = ?,
      title = ?
      WHERE id = ?"""
      
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
      cursor.execute("DELETE FROM books WHERE id=?",(id,))
      conn.commit()
      return f"Book with ID {id},has been deleted"



      



if __name__ == '__main__':
    app.run(debug=True)

