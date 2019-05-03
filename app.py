from flask import Flask, jsonify, request, Response, json

app = Flask(__name__) 
#Flask knows where to look for templates, static files, packages and so on
print(__name__)

books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 978039400165
    },
    {
        'name': 'The Cat in the Hat',
        'price': 6.99,
        'isbn': 9782371000193
    }
]


#GET /books by default
@app.route('/books')
def get_books():
    return jsonify({'books': books})

def validBookObject(bookObject):
    # if "keyName" in dictionaryObject
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

#POST /books
#need to have request with details of book in body
#it will be a JSON  - need to get request body
@app.route('/books', methods=['POST'])
def add_book():
    request_data  = request.get_json()
    if(validBookObject(request_data)):
        new_book= {
            "name": request_data["name"],
            "isbn": request_data["isbn"],
            "price": request_data["price"],
        }
        books.insert(0, new_book)
        #in FLASK when return string automatically set contenttype to text/html and status to 200
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request.",
            "helpString": "Data should be passed similar to this: {'name': 'bookname', 'price': '7.99', 'isbn':'1234567890'}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400,mimetype='application/json')
        return response
    

#GET /books/isbn
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)


app.run(port=5000)
