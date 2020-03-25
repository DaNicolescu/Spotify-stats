from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/hello', methods=['GET','POST'])
def return_msg():
    if request.method == "POST":
        return jsonify({'pula': 'pula_da'})
    return 'get method'

@app.route('/server', methods=['GET','POST'])
def return_server_ok():
    if request.method == "POST":
        return jsonify({'server': 'merge'})
    return "get method"

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)