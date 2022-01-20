from flask import Flask, render_template, jsonify
from flask_restful import Api
from flask_cors import CORS

from resources.car import Car, CarList
from resources.inspection import InspectionsList, Inspection
from resources.service import Service, ServicesList
from resources.user import User, UsersList

app = Flask(__name__)
CORS(app, origins=["http://localhost:5000", "http://127.0.0.1:5000"])
api = Api(app)

@app.route('/')
def home():
    return render_template('Main.html')

@app.route('/service-station')
def service_station_page():
    return render_template('service-station.html')

@app.route('/login')
def login_page():
    return render_template('Login.html')

api.add_resource(Car, '/car')
api.add_resource(CarList, '/cars')
api.add_resource(User, '/user')
api.add_resource(UsersList, '/users')
api.add_resource(Service, '/service')
api.add_resource(ServicesList, "/services")
api.add_resource(Inspection, '/inspection')
api.add_resource(InspectionsList, '/inspections')

app.run(port=5000, debug=True)