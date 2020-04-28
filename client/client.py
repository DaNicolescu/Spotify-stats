from flask import Flask, render_template, request, url_for, redirect
from prometheus_flask_exporter import PrometheusMetrics
import sys
import requests
import json

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/artists', methods=['GET', 'POST'])
def artists():
    if request.method == 'GET':
        return render_template("artists.html")
    else:
        artist = request.form["artist_name"]
        response = requests.post("http://server:5001/artist_info",
        	json={"artist_name":artist})
        response_data = response.json()
        return render_template("artist_info.html",
        	artist_name=response_data["artist_name"],
        	followers=response_data["followers"],
        	genres=response_data["genres"],
        	popularity=response_data["popularity"],
        	image=response_data["image"],
        	top_tracks=response_data["top_tracks"],
        	album_names=response_data["album_names"])

@app.route('/tracks', methods=['GET', 'POST'])
def tracks():
    if request.method == 'GET':
        return render_template("tracks.html")
    else:
        track = request.form['track_name']
        response = requests.post("http://server:5001/track_info",
        	json={"track_name":track})
        response_data = response.json()
        return render_template("track_info.html",
        	track_name=response_data["track_name"],
        	artist_name=response_data["artist_name"],
        	album=response_data["album"],
        	album_photo=response_data["album_photo"],
        	release_date=response_data["release_date"],
        	popularity=response_data["popularity"],
        	duration=response_data["duration"])

@app.route('/recommendations')
def recommendations():
    return render_template("recommendations.html")

@app.route('/server')
def check_server():
    response = requests.post("http://server:5001/boss")
    return response.json()['server']

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)