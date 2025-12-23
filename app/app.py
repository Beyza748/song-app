from flask import Flask, request, jsonify, session, render_template
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

songs = [
    {"id": 1, "title": "Imagine", "artist": "John Lennon"},
    {"id": 2, "title": "Shape of You", "artist": "Ed Sheeran"},
    {"id": 3, "title": "Billie Jean", "artist": "Michael Jackson"},
    {"id": 4, "title": "Let It Be", "artist": "The Beatles"},
    {"id": 5, "title": "Rolling in the Deep", "artist": "Adele"}
]

@app.before_request
def setup_session():
    if 'favorites' not in session:
        session['favorites'] = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_song():
    query = request.args.get('q', '').lower()
    results = [song for song in songs if query in song['title'].lower()]
    for song in results:
        song['liked'] = song['id'] in session['favorites']
    return jsonify(results)

@app.route('/favorites', methods=['POST'])
def toggle_favorite():
    song_id = request.get_json().get('id')
    if song_id in session['favorites']:
        session['favorites'].remove(song_id)
        liked = False
    else:
        session['favorites'].append(song_id)
        liked = True
    session.modified = True
    return jsonify({"id": song_id, "liked": liked, "favorites": session['favorites']})

@app.route('/favorites', methods=['GET'])
def get_favorites():
    fav_songs = [song for song in songs if song['id'] in session['favorites']]
    return jsonify(fav_songs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
