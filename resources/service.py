import sqlite3
import json

from flask_restful import Resource, reqparse
from config import database_path
from models.service import ServiceModel


class Service(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("car-parameters", type=dict)
    parser.add_argument("car-id", type=int)

    def get(self):
        data = Service.parser.parse_args()
        print(data["car-id"], type(data['car-id']))
        print(data['car-parameters'])
        if data['car-id']:
            services = ServiceModel.find_by_car_id(data["car-id"])
        elif data['car-parameters']:
            services = ServiceModel.find_by_car_parameters(data['car-parameters'])
        else:
            return {'message': f'Unexpected fields in data {data.keys()}'}, 404
        if services:
            return {"services": services}, 200
        return {"message": "Service not found"}, 404


class ServicesList(Resource):

    def get(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'SELECT * FROM services'
        result = cursor.execute(query)
        services = []
        for row in result:
            print(row)
            services.append(ServiceModel(*row).json())

        connection.close()

        return {"services": services}
