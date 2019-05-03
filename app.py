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
    },
        {
        'name': 'harry potter and the lower case letters',
        'price': 16.99,
        'isbn': 9782371002424
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

#PUT - replace a book, requires all data
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i = 0
    for book in books:
        currentIsbn=book['isbn']
        if currentIsbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("", status=204)
    return response

#PATCH - only update 1 piece of data on object
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if("name" in request_data):
        updated_book['name'] = request_data['name']
    if("price" in request_data):
        updated_book['price'] = request_data['price']
    for book in books:
        if book['isbn'] == isbn:
            book.update(updated_book)
    response = Response('', status=204)
    response.headers['Location'] = '/book/' + str(isbn)
    return response

app.run(port=5000)
