from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os


host = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/contractor')
client = MongoClient(host=host)
db = client.get_default_database()
albums = db.albums

client = MongoClient()
db = client.Contractor
albums = db.albums

app = Flask(__name__)






@app.route('/')
def index():
    """Return homepage."""
    return render_template('albums_index.html', albums=albums.find())


@app.route('/albums', methods=['POST'])
def submit_album():
    '''submit a new album'''
    album = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'year_released': request.form.get('year_released'),
        'category': request.form.get('category')
    }
    print(request.form.to_dict())
    album_id = albums.insert_one(album).inserted_id
    return redirect(url_for('show_album', album_id=album_id))

@app.route('/albums/<album_id>')
def show_album(album_id):
    '''show a single album'''
    album = albums.find_one({'_id': ObjectId(album_id)})
    return render_template('album_show.html', album=album)


@app.route('/album/new')
def create_album():
    '''create a new album'''
    return render_template('album_new.html', album = {}, title = 'New Album')


@app.route('/albums/<album_id>/edit')
def albums_edit(album_id):
    """Show the edit form for a playlist."""
    album = albums.find_one({'_id': ObjectId(album_id)})
    return render_template('album_edit.html', album=album, title = 'Edit Album')


@app.route('/albums/<album_id>', methods=['POST'])
def album_update(album_id):
    updated_album = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'year_released': request.form.get('year_released'),
        'category': request.form.get('category')
    }
    albums.update_one(
        {'_id': ObjectId(album_id)},
        {'$set': updated_album}
    )
    return redirect(url_for('show_album', album_id=album_id))

@app.route('/albums/<album_id>/delete', methods=['POST'])
def delete_album(album_id):
    albums.delete_one({'_id': ObjectId(album_id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv('PORT', 5000))