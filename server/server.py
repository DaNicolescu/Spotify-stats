from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def connect_database():
    global airplaneService_cursor
    global airplaneService_db
    airplaneService_db = mysql.connector.connect(
        host='db',
        port='3306',
        user='user',
        passwd='parola',
        database='flights'
    )

    airplaneService_cursor = airplaneService_db.cursor()
    
    
def random_string():

    string_len = 10
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, string_len))

@app.route('/getRoute', methods=['GET','POST'])
def getOptimalRoute():
    global airplaneService_cursor
    global airplaneService_db
    global routes
    flight_data = request.get_json(silent=True)
    flights_list = []
    best_route = None
    minimum = 1000000
    
    sql = "SELECT Dest, DepartureDay, DepartureHour, Duration, ID from flights where Source = %s"
    val = (flight_data['source'], )
    airplaneService_cursor.execute(sql, val)
    flights = airplaneService_cursor.fetchall()

    #cautam destinatiile catre care putem ajunge intr-un singur zbor cu plecare in ziua solicitata
    for flight in flights:
        if int(flight[1]) == int(flight_data['departureDay']):
            flights_list.append((flight[0], 24 * (int(flight[1]) - 1) + flight[2], 24 * (int(flight[1]) - 1) + flight[2] + flight[3], [flight[4]]))
       
    #cautam cel mult numarul de zboruri maxim solicitat
    for i in range(int(flight_data['maxFlights']) - 1):
        #actualizam zborurile optime pentru destinatia ceruta cu cel mult i zboruri
        for elem in flights_list:
            if elem[0] == flight_data['dest']:
                if elem[2] - elem[1] < minimum:
                    best_route = elem
                    minimum = elem[2] - elem[1]
        flights_list_aux = []
        #cautam zborurile intermediare cu plecare din destinatiile in care putem ajunge direct
        for elem in flights_list:
            sql = "SELECT Dest, DepartureDay, DepartureHour, Duration, ID from flights where Source = %s"
            val = (elem[0], )
            airplaneService_cursor.execute(sql, val)
            flights = airplaneService_cursor.fetchall()
            for flight in flights:
                if 24 * (int(flight[1]) - 1) + int(flight[2]) >= int(elem[2]):
                    id_list = []
                    id_list = elem[3].copy()
                    id_list.append(flight[4])
                    flights_list_aux.append((flight[0], elem[1], 24 * (int(flight[1]) - 1) + flight[2] + flight[3], id_list))
        flights_list = flights_list_aux

    #stabilire ruta finala optima
    for elem in flights_list:
        if elem[0] == flight_data['dest']:
            if elem[2] - elem[1] < minimum:
                best_route = elem
                minimum = elem[2] - elem[1]
            
    if minimum == 1000000:
        return jsonify({'flight': ''})

    routes_details = []
    #aflare detalii despre ruta ceruta
    for route_id in best_route[3]:
        sql = "SELECT ID, Source, Dest, DepartureDay, DepartureHour, Duration from flights where ID = %s"
        val = (route_id, )
        airplaneService_cursor.execute(sql, val)
        route_details = airplaneService_cursor.fetchall()
        routes_details.append(route_details[0])

    return jsonify({'flights': routes_details})

@app.route('/bookTicket', methods=['GET','POST'])
def bookTicket():
    global routes
    global airplaneService_cursor
    global airplaneService_db
    global reservations_dict

    numberofSeats_dict = {}
    hasFreeSeat = True
    route = request.get_json(silent=True)

    #cauta daca sunt locuri libere pentru zborurile solictate
    for route_id in route['routes']:
        sql = "SELECT NumberofSeats_booked from flights WHERE ID = %s"
        val = (route_id, )
        airplaneService_cursor.execute(sql, val)
        numberofSeats = airplaneService_cursor.fetchall()
        numberofSeats_dict[route_id] = numberofSeats[0][0]
        if numberofSeats[0][0] == 0:
            hasFreeSeat = False
            return jsonify({'reservation_id' : ""})

    #daca exista locuri disponibile pe toate rutele atunci se genereaza reservation id
    if hasFreeSeat:
        for key in numberofSeats_dict.keys():
            sql = "UPDATE flights SET NumberofSeats_booked = %s WHERE ID = %s"
            numberofSeats_dict[key] -= 1
            val = (numberofSeats_dict[key], key)
            airplaneService_cursor.execute(sql, val)
            airplaneService_db.commit()
        reservation_id = random_string()
        reservations_dict[reservation_id] = route['routes']

    return jsonify({'reservation_id': reservation_id})

@app.route('/buyTicket', methods=['GET','POST'])
def buyTicket():
    global airplaneService_cursor
    global airplaneService_db
    global reservations_dict

    boarding_pass = []
    reservation = request.get_json(silent=True)

    # pentru reservation_id-ul solicitat se realizeaza cumpararea biletului
    if reservation['reservation_id'] in reservations_dict.keys(): 
        for route_id in reservations_dict[reservation['reservation_id']]:
            sql = "SELECT NumberofSeats from flights WHERE ID = %s"
            val = (route_id, )
            airplaneService_cursor.execute(sql, val)
            numberofSeats = airplaneService_cursor.fetchall()
            if numberofSeats[0][0] == 0:
                return jsonify({'boarding_pass': ''})
            numberofSeats_updated = numberofSeats[0][0] - 1
            sql = "UPDATE flights SET NumberofSeats = %s WHERE ID = %s"
            val = (numberofSeats_updated, route_id)
            airplaneService_cursor.execute(sql, val)
            airplaneService_db.commit()
            sql = "SELECT Source, Dest, DepartureDay, DepartureHour from flights WHERE ID = %s"
            val = (route_id, )
            airplaneService_cursor.execute(sql, val)
            boarding_pass_aux = airplaneService_cursor.fetchall()
            boarding_pass.append(boarding_pass_aux[0])
    else:
        return jsonify({'boarding_pass': ''})

    return jsonify({'boarding_pass': boarding_pass})

if __name__ == '__main__':
    connect_database()
    app.run('0.0.0.0', port=5000,debug=True)