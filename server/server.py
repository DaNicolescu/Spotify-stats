from flask import Flask, request, jsonify
import json
import mysql.connector
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

client_credentials_manager = SpotifyClientCredentials(client_id="adef179cbfaf472281e7f19291a20586", client_secret="d003550df96c4e49b9781018f1df709b")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def create_table():
    airplaneService_db = mysql.connector.connect(host='db', port='3306'
            , user='user', passwd='parola', database='test')

    airplaneService_cursor = airplaneService_db.cursor()

    airplaneService_cursor.execute('CREATE TABLE test (ID VARCHAR(255), Source VARCHAR(255), Dest VARCHAR(255), DepartureDay INT, DepartureHour INT, Duration INT, NumberofSeats INT, NumberofSeats_booked INT)'
                                   )

@app.route('/artist_info', methods=['GET','POST'])
def get_artist_info():
	request_info = request.get_json(silent=True)
	result = sp.search(request_info["artist_name"], type="artist")
	artist = result["artists"]["items"][0]
	top_tracks = sp.artist_top_tracks(artist["uri"])

	top_tracks_names = []
	top_tracks_album_names = []

	for track in top_tracks["tracks"]:
		top_tracks_names.append(track["name"])
		top_tracks_album_names.append(track["album"]["name"])

	return jsonify({"artist_name": artist["name"], "followers": artist["followers"]["total"], "genres": artist["genres"], "popularity": artist["popularity"], "image": artist["images"][0]["url"], "top_tracks": top_tracks_names, "album_names": top_tracks_album_names})

@app.route('/track_info', methods=['GET','POST'])
def get_track_info():
	request_info = request.get_json(silent=True)
	return jsonify({"track_name": request_info["track_name"], "album": "Nicolae Guță best of", "popularity": "100", "duration": "4:20"})

@app.route('/hello', methods=['GET', 'POST'])
def return_msg():
    if request.method == 'POST':
        return jsonify({'pula': 'pula_da'})
    return 'get method'


@app.route('/boss', methods=['GET', 'POST'])
def return_server_ok():
    # create_table()
    if request.method == 'POST':
        return jsonify({'server': 'merge serverul, boss'})
    return 'merge ceva'

@app.route('/test_spot', methods=['GET', 'POST'])
def check_spotipy():
	result = sp.artist_top_tracks("spotify:artist:12Chz98pHFMPJEknJQMWvI")
	return result

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)