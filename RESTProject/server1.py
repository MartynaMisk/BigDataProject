from flask import Flask, jsonify, request, abort

app = Flask(__name__, static_url_path='', static_folder='.')

books=[
    {"id":1, "Title":"harry potter", "Author":"JK", "Price":1000},
    {"id":2, "Title":"blackr", "Author":"jesse", "Price":800},
    {"id":3, "Title":"rap", "Author":"snoop", "Price":1100},
]
nextId=4 
#app = Flask(__name__)

#@app.route('/')
#def index():
#    return "Hello, World!"

#curl "http://127.0.0.1:5000/books"

@app.route('/books')
def getAll():
    return jsonify(books)

#curl "http://127.0.0.1:5000/books/2"
@app.route('/books/<int:id>')
def findByID(id):
    foundBooks = list(filter(lambda b: b['id'] == id, books))
    if len(foundBooks) == 0:
        return jsonify ({}) ,204
    
    return jsonify(foundBooks[0])

@app.route('/books', methods=['POST'])
def create():
    global nextId
    if not request.json:
        abort(400)
    #other attributes that is properly formatted - more marksgo back to the lecture
    book = {
        "id": nextId,
        "Title": request.json['Title'],
        "Author": request.json['Author'],
        "Price": request.json['Price']
    }
    nextId += 1
    books.append(book)
    return jsonify(book)
#curl -H "Content-Type:application/json" -X PUT -d "{\"Title\":\"hello\",\"Author\":\"someone\",\"Price\":123}" "http://127.0.0.1:5000/books/1"
@app.route('/books/<int:id>', methods=['PUT'])
def update(id):
    foundBooks = list(filter(lambda b: b['id']== id, books))
    if (len(foundBooks) == 0):
        abort(404)
    foundBook = foundBooks[0]
    if not request.json:
        abort(404)
    reqJson = request.json
    if 'Price' in reqJson and type(reqJson['Price']) is not int:
        abort(400)

    if 'Title' in reqJson:
        foundBook['Title'] = reqJson['Title']
    if 'Author' in reqJson:
        foundBook['Author'] = reqJson['Author']
    if 'Price' in reqJson:
        foundBook['Price'] = reqJson['Price']
    
    return jsonify(foundBooks)

    return "in update for id"+str(id)
#curl -X DELETE "http://127.0.0.1:5000/books/1"
@app.route('/books/<int:id>', methods=['DELETE'])
def delete(id):
    foundBooks = list(filter(lambda b: b['id']== id, books))
    if (len(foundBooks) == 0):
        abort(404)
    books.remove(foundBooks[0])
    return jsonify({"done":True})

if __name__ == '__main__' :
    app.run(debug= True)