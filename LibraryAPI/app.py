from flask import Flask,request,jsonify
import sqlite3

conn = sqlite3.connect('books.sqlite')

app =  Flask(__name__)



# books = open('book.json','r+')
# books = list(books.read())

@app.route('/',methods=["GET"])
def home():
    return "Welcome to the Library API"

@app.route('/books',methods = ['GET','POST'])
def books():
    if request.method == 'GET':
        if len(libBooks) > 0:
            return jsonify(libBooks)
        else:
            return 'No books found',400
    else:
        new_object = {
            "author": request.form['author'],
            "country": request.form['country'],
            "imageLink":  request.form['imageLink'],
            "language":  request.form['language'],
            "link":  request.form['link'],
            "pages":request.form['pages'],
            "title":  request.form['title'],
            "year": request.form['year']
        }
        libBooks.append(new_object)
        return jsonify(libBooks),201 

@app.route('/books/<title>',methods=["GET","PUT","DELETE"])
def manipulate(title):
    if request.method == 'GET':
        for book in libBooks:
            if book['title'] == title:
                return jsonify(book),200
                pass
           
    elif request.method == 'PUT':
         for book in libBooks:
            if book['title'] == title:
                 book['author'] = request.form['author']
                 book['country'] =  request.form['country']
                 book["imageLink"] =  request.form['imageLink']
                 book["language"] = request.form['language']
                 book["link"] =  request.form['link']
                 book["pages"]=request.form['pages']
                 book["title"] = request.form['title']
                 book["year"] = request.form['year']

                 return jsonify(book),200
    elif request.method == 'DELETE':  
         for index,book in enumerate(libBooks):
            if book['title'] == title:
                libBooks.pop(index)
                return jsonify(book),200  
    else:
        return 'Operation failed',400                     




if __name__ == '__main__':
    app.run(debug=True)

