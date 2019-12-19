from flask import Flask, jsonify, request, abort
from albumsDAO import albumsDAO

app = Flask(__name__, static_url_path='', static_folder='.')

#app = Flask(__name__)

#@app.route('/')
#def index():
#    return "Hello, World!"

#curl "http://127.0.0.1:5000/RapAlbums"

@app.route('/RapAlbums')
def getAll():
    
    results = albumsDAO.getAll()
    return jsonify(results)

#curl "http://127.0.0.1:5000/RapAlbums/2"
@app.route('/RapAlbums/<int:id>')
def findByID(id):
    foundalbum = albumsDAO.findByID(id)

    return jsonify(foundalbum)
    
#curl -i -H "Content-Type:application/json" -X POST -d "{\"Rapper\":\"Stormy\",\"Album\":\"bith\",\"Price\":1700}" http://127.0.0.1:5000/RapAlbums
@app.route('/RapAlbums', methods=['POST'])
def create():
    #global nextId
    if not request.json:
        abort(400)
    #other attributes that is properly formatted - more marksgo back to the lecture #properly formatted
    album = {
        "rapper": request.json['rapper'],
        "album": request.json['album'],
        "price": request.json['price']
    }

    values = (album['rapper'],album['album'],album['price'])
    newId = albumsDAO.create(values)
    album['id'] = newId
    return jsonify(album)

    #nextId += 1
    #RapAlbums.append(RapAlbum)
    #return jsonify(RapAlbum)

#curl -i -H "Content-Type:application/json" -X PUT -d "{\"Rapper\":\"Stormy\",\"Album\":\"bith\",\"Price\":1700}" http://127.0.0.1:5000/RapAlbums/2
@app.route('/RapAlbums/<int:id>', methods=['PUT'])
def update(id):
    foundalbum = albumsDAO.findByID(id)
    if not foundalbum:
        abort(404)
  
    if not request.json:
        abort(404)
    reqJson = request.json
    if 'price' in reqJson and type(reqJson['price']) is not int:
        abort(400)

    if 'rapper' in reqJson:
        foundalbum['rapper'] = reqJson['rapper']
    if 'album' in reqJson:
        foundalbum['album'] = reqJson['album']
    if 'price' in reqJson:
        foundalbum['price'] = reqJson['price']
    values = (foundalbum['rapper'],foundalbum['album'],foundalbum['price'],foundalbum['id'])
    albumsDAO.update(values)
    return jsonify(foundalbum)

#curl -X DELETE "http://127.0.0.1:5000/RapAlbums/1"
@app.route('/RapAlbums/<int:id>', methods=['DELETE'])
def delete(id):
    albumsDAO.delete(id)
    return jsonify({"done":True})

if __name__ == '__main__' :
    app.run(debug= True)