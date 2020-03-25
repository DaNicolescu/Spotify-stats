import sys
import requests
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
	response = requests.post("http://server:5001/hello")
    return 'Hey, we have Flask in a Docker container!'

def get_artist_info(artist_name):
    # use search for an item from Spotify API to get info about an artist
    print("Artist name: -")
    print("Popularity: -")
    print("Followers: -")
    print("Genres: -")

def get_artist_top_tracks(artist_name):
    # use search for an item to get artist's ID and then use it as a param
    # for get an artist's top tracks
    print("Track 1")
    print("Track 2")
    print("Track 3")

def get_track_info(track_name):
    # use search to get the track's ID and then use get a track
    print("Track name: -")
    print("Album: -")
    print("Popularity: -")
    print("Duration: -")

def get_suggestions(genre):
    print("Suggestion 1")
    print("Suggestion 2")
    print("Suggestion 3")

def process_input():
    while True:
        print("-----------------------------")
        print("Available Commands:")
        print("1. Get artist info")
        print("2. Get artist's top tracks")
        print("3. Get track info")
        print("4. Get suggestions")
        print("5. Exit")
        print("-----------------------------")

        input = sys.stdin.readline()
        input = input.strip('\n')

        if int(input) == 1:
            print("Enter artist name:")
            artist_name = sys.stdin.readline()
            artist_name = artist_name.strip('\n')
            artist_name = artist_name.lower()

            get_artist_info(artist_name)
        elif int(input) == 2:
            print("Enter artist name:")
            artist_name = sys.stdin.readline()
            artist_name = artist_name.strip('\n')
            artist_name = artist_name.lower()

            get_artist_top_tracks(artist_name)
        elif int(input) == 3:
            print("Enter track name:")
            track_name = sys.stdin.readline()
            track_name = track_name.strip('\n')
            track_name = track_name.lower()

            get_track_info(track_name)
        elif int(input) == 4:
            print("Enter genre:")
            genre = sys.stdin.readline()
            genre = genre.strip('\n')
            genre = genre.lower()

            get_suggestions(genre)
        elif int(input) == 5:
            break
        else:
            print("Invalid input")

if __name__ == '__main__':
    app.run(host="0.0.0.0")