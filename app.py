from flask import Flask, jsonify

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


#POST /books
#need to have request with details of book in body
#it will be a JSON  - need to get request body
@app.route('/books', methods=['POST'])
def add_book():
    return jsonify(request.get_json())

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
