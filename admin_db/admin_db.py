import mysql.connector
from mysql.connector import errorcode
from flask import Flask, request, jsonify
import time
import json
import random
import string
import sys

app = Flask(__name__)

database = None
database_cursor = None

TABLES = {}
TABLES["artists"] = (
    "CREATE TABLE IF NOT EXISTS `artists` ("
    "   `artist_name` varchar(255) NOT NULL,"
    "   `followers` int NOT NULL,"
    "   `genres` text NOT NULL,"
    "   `popularity` int NOT NULL,"
    "   `image` varchar(1000) NOT NULL,"
    "   `top_tracks` text NOT NULL,"
    "   `album_names` text NOT NULL,"
    "      PRIMARY KEY (`artist_name`)"
    ") ENGINE=InnoDB")

TABLES["tracks"] = (
    "CREATE TABLE IF NOT EXISTS `tracks` ("
    "   `track_name` varchar(255) NOT NULL,"
    "   `artist_name` varchar(255) NOT NULL,"
    "   `album` varchar(255) NOT NULL,"
    "   `album_photo` varchar(1000) NOT NULL,"
    "   `release_date` varchar(255) NOT NULL,"
    "   `popularity` int NOT NULL,"
    "   `duration` varchar(255) NOT NULL,"
    "      PRIMARY KEY (`track_name`)"
    ") ENGINE=InnoDB")

#creeaza tabelul flights in baza de date
def create_table():
    global database
    global database_cursor

    database = mysql.connector.connect(
        host="db",
        port="3306",
        user="user",
        password="password",
        database="dbase"
    )

    database_cursor = database.cursor()

    database_cursor.execute(TABLES["artists"])
    database_cursor.execute(TABLES["tracks"])

@app.route('/check_artist_exists', methods=['GET','POST'])
def check_artist_exists():
    request_info = request.get_json(silent=True)

    query = ("SELECT artist_name FROM artists"
            "WHERE artist_name = %s")
    val = (request_info["artist_name"], )

    database_cursor.execute(query, val)
    result = database_cursor.fetchall()
    artist_exists = False

    if result:
        artist_exists = True

    return jsonify({"artist_exists": artist_exists})

def list_to_string(list_param):
    result = "|"
    result = result.join(list_param)

    return result

@app.route('/get_artist', methods=['GET','POST'])
def get_artist():
    request_info = request.get_json(silent=True)

    query = "SELECT * FROM artists WHERE artist_name = %s"
    val = (request_info["artist_name"], )

    database_cursor.execute(query, val)
    result = database_cursor.fetchall()

    if not result:
        return jsonify({"artist_exists": False})
    
    artist_touple = result[0]

    artist_name = artist_touple[0]
    followers = artist_touple[1]
    genres = artist_touple[2].split("|")
    popularity = artist_touple[3]
    image = artist_touple[4]
    top_tracks = artist_touple[5].split("|")
    album_names = artist_touple[6].split("|")

    return jsonify({"artist_exists": True,
        "artist_name": artist_name,
        "followers": followers,
        "genres": genres,
        "popularity": popularity,
        "image": image,
        "top_tracks": top_tracks,
        "album_names": album_names})

@app.route('/add_artist', methods=['GET','POST'])
def add_artist():
    request_info = request.get_json(silent=True)

    query = "INSERT INTO artists (artist_name, followers, genres, popularity, image, top_tracks, album_names) VALUES (%(artist_name)s, %(followers)s, %(genres)s, %(popularity)s, %(image)s, %(top_tracks)s, %(album_names)s)"

    val = {
        "artist_name": request_info["artist_name"],
        "followers": request_info["followers"],
        "genres": list_to_string(request_info["genres"]),
        "popularity": request_info["popularity"],
        "image": request_info["image"],
        "top_tracks": list_to_string(request_info["top_tracks"]),
        "album_names": list_to_string(request_info["album_names"])
    }

    database_cursor.execute(query, val)
    database.commit()

    return jsonify({"artist_added": True})

@app.route('/get_track', methods=['GET','POST'])
def get_track():
    request_info = request.get_json(silent=True)

    query = "SELECT * FROM tracks WHERE track_name = %s"
    val = (request_info["track_name"], )

    database_cursor.execute(query, val)
    result = database_cursor.fetchall()

    if not result:
        return jsonify({"track_exists": False})
    
    track_touple = result[0]

    track_name = track_touple[0]
    artist_name = track_touple[1]
    album = track_touple[2]
    album_photo = track_touple[3]
    release_date = track_touple[4]
    popularity = track_touple[5]
    duration = track_touple[6]

    return jsonify({"track_exists": True,
        "track_name": track_name,
        "artist_name": artist_name,
        "album": album,
        "album_photo": album_photo,
        "release_date": release_date,
        "popularity": popularity,
        "duration": duration})

@app.route('/add_track', methods=['GET','POST'])
def add_track():
    request_info = request.get_json(silent=True)

    query = "INSERT INTO tracks (track_name, artist_name, album, album_photo, release_date, popularity, duration) VALUES (%(track_name)s, %(artist_name)s, %(album)s, %(album_photo)s, %(release_date)s, %(popularity)s, %(duration)s)"

    val = {
        "track_name": request_info["track_name"],
        "artist_name": request_info["artist_name"],
        "album": request_info["album"],
        "album_photo": request_info["album_photo"],
        "release_date": request_info["release_date"],
        "popularity": request_info["popularity"],
        "duration": request_info["duration"]
    }

    database_cursor.execute(query, val)
    database.commit()

    return jsonify({"track_added": True})

@app.route('/test')
def test():
    query = "SELECT artist_name FROM artists WHERE artist_name = %s"
    val = ('Powerwolf', )

    database_cursor.execute(query, val)
    result = database_cursor.fetchall()
    artist_exists = False

    if not result:
        return jsonify({"artist_exists": False})
    
    artist_touple = result[0]

    artist_name = artist_touple[0]
    followers = artist_touple[1]
    genres = artist_touple[2].split(",")
    popularity = artist_touple[3]
    image = artist_touple[4]
    top_tracks = artist_touple[5].split(",")
    album_names = artist_touple[6].split(",")

    return jsonify({"artist_exists": True,
        "artist_name": artist_name,
        "followers": followers,
        "genres": genres,
        "popularity": popularity,
        "image": image,
        "top_tracks": top_tracks,
        "album_names": album_names})

@app.route('/destroy_db', methods=['GET','POST'])
def destroy_db():
    database_cursor.close()
    database.close()

    return jsonify({"destroyed": True})
    
if __name__ == "__main__":
    create_table()
    app.run('0.0.0.0', port=5002, debug=True)