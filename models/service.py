import sqlite3

from config import database_path
from models.car import CarModel
from utils import create_filter

class ServiceModel:

    def __init__(self, _id: int, description: str, inspection_name: str, inspection_cost: int, car_id: int):
        self.id = _id
        self.description = description
        self.inspection_name = inspection_name
        self.inspection_cost = inspection_cost
        self.car_id = car_id

    def json(self) -> dict:
        return {"service_parameters": {
            'service-id': self.id,
            'service-description': self.description,
            'service-inspection-name': self.inspection_name,
            'service-inspection-cost': self.inspection_cost,
            'service-car-id': self.car_id
        }}

    @classmethod
    def find_by_car_id(cls, car_id: int):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        services = []

        where_part = f' WHERE "service-car-id" = {car_id}'
        query = f'SELECT * FROM services{where_part}'
        result = cursor.execute(query)
        if result:
            for row in result:
                services.append(cls(*row).json())
        connection.close()
        return services

    @classmethod
    def find_by_car_parameters(cls, car_parameters: dict):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        car = None
        where_part = f' WHERE {create_filter(car_parameters)}'
        query = f'SELECT * FROM cars{where_part}'
        result = cursor.execute(query)
        row = result.fetchone()
        if row:
            car = CarModel(*row)
        connection.close()

        if car:
            return cls.find_by_car_id(car.id)
