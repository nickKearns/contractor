from flask import Flask, render_template

app = Flask(__name__)


albums = [
    {'title': 'Led Zeppelin III', 'description': 'Third self titled led zeppelin album', 'category': 'classic rock'},
    {'title': 'Led Zeppelin II', 'description': 'Second self titled led zeppelin album', 'category': 'classic rock'}
]



@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg = 'Nicks Records')

@app.route('/albums')
def albums_index():
    '''display all albums'''
    return render_template('albums_index.html', albums=albums)
if __name__ == '__main__':
    app.run(debug=True)