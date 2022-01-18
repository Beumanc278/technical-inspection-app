import sqlite3

from config import database_path
from utils import create_filter


class InspectionModel:

    def __init__(self, _id: int, inspection_name: str, inspection_cost: float, mileage: int, lifetime: int, service_id: int, car_parameters: str):
        self.id = _id
        self.name = inspection_name
        self.cost = inspection_cost
        self.mileage = mileage
        self.lifetime = lifetime
        self.service_id = service_id
        self.car_parameters = car_parameters

    def json(self):
        return {
            'insection-id': self.id,
            'inspection-name': self.name,
            'inspection-cost': self.cost,
            'inspection-mileage': self.mileage,
            'inspection-lifetime': self.lifetime,
            'inspection-service-id': self.service_id,
            'inspection-car-parameters': self.car_parameters
        }

    @classmethod
    def get_inspections_by_car_parameters(cls, car_parameters: dict):
        string_interpretation = ','.join([str(element) for element in list(car_parameters.values())[1:]])
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = f'SELECT * FROM inspections WHERE "car-parameters" = "{string_interpretation}"'
        print(query)
        result = cursor.execute(query)
        inspections = []
        for row in result:
            print(row)
            inspections.append(cls(*row).json())
        return inspections

    @classmethod
    def get_inspections_by_parameters(cls, parameters: dict):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        where_part = f' WHERE {create_filter(parameters)}'
        query = f'SELECT * FROM inspections{where_part}'
        print(query)
        result = cursor.execute(query)
        inspections = []
        for row in result:
            print(row)
            inspections.append(cls(*row).json())
        return inspections

class InspectionListModel:

    @classmethod
    def get_all_inspections(cls):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'SELECT * FROM inspections'
        result = cursor.execute(query)
        inspections = []
        for row in result:
            print(row)
            inspections.append(InspectionModel(*row).json())
        connection.close()
        return inspections


