import sqlite3

from flask_restful import Resource, reqparse
from models.car import CarModel
from config import database_path


class Car(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('car-brend')
    parser.add_argument('car-model')
    parser.add_argument('car-year')
    parser.add_argument('car-engine-type')
    parser.add_argument('car-engine-capacity')
    parser.add_argument('car-transmission')
    parser.add_argument('car-drive-unit')

    def get(self):
        data = Car.parser.parse_args()
        print(data)
        car = CarModel.find_by_parameters(data)
        if car:
            return car.json()
        return {"message": "Car not found"}, 404


class CarList(Resource):

    def get(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'SELECT * FROM cars'
        result = cursor.execute(query)
        cars = []
        for row in result:
            print(row)
            cars.append(CarModel(*row).json())

        connection.close()

        return {"cars": cars}
