from flask import Flask, render_template, jsonify
from flask_restful import Api

from resources.car import Car, CarList
from resources.service import Service, ServicesList
from resources.user import User

app = Flask(__name__)
api = Api(app)

@app.route('/')
def home():
    return render_template('Main.html')

api.add_resource(Car, '/car')
api.add_resource(CarList, '/cars')
api.add_resource(User, '/user')
api.add_resource(Service, '/service')
api.add_resource(ServicesList, "/services")

app.run(port=5000, debug=True)