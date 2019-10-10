from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient()
db = client.Contractor
albums = db.albums

app = Flask(__name__)


# albums = [
#     {'title': 'Led Zeppelin III', 'description': 'Third self titled led zeppelin album', 'category': 'classic rock'},
#     {'title': 'Led Zeppelin II', 'description': 'Second self titled led zeppelin album', 'category': 'classic rock'}
# ]



@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg = 'Nicks Records')

@app.route('/albums')
def albums_index():
    '''display all albums'''
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
    albums.insert_one(album)
    print(request.form.to_dict())
    return redirect(url_for('albums_index'))


@app.route('/album/new')
def create_album():
    '''create a new album'''
    return render_template('album_new.html')





if __name__ == '__main__':
    app.run(debug=True)