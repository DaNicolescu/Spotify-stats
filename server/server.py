from flask import Flask, request, jsonify
import json
import mysql.connector

app = Flask(__name__)


def create_table():
    airplaneService_db = mysql.connector.connect(host='db', port='3306'
            , user='user', passwd='parola', database='test')

    airplaneService_cursor = airplaneService_db.cursor()

    airplaneService_cursor.execute('CREATE TABLE test (ID VARCHAR(255), Source VARCHAR(255), Dest VARCHAR(255), DepartureDay INT, DepartureHour INT, Duration INT, NumberofSeats INT, NumberofSeats_booked INT)'
                                   )


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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)