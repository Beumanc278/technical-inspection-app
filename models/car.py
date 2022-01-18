import sqlite3

from config import database_path
from utils import create_filter

class CarModel:

    def __init__(self, _id: int, brend: str, model: str, year: str, engine_type: str, engine_capacity: str, transmission: str, drive_unit: str):
        self.id = _id
        self.brend = brend
        self.model = model
        self.year = year
        self.engine_type = engine_type
        self.engine_capacity = engine_capacity
        self.transmission = transmission
        self.drive_unit = drive_unit

    def json(self) -> dict:
        return {
            'car-id': self.id,
            'car-brend': self.brend,
            'car-model': self.model,
            'car-year': self.year,
            'car-engine-type': self.engine_type,
            'car-engine-capacity': self.engine_capacity,
            'car-transmission': self.transmission,
            'car-drive-unit': self.drive_unit
                }

    @classmethod
    def get_by_parameters(cls, car_parameters: dict):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        where_part = f' WHERE {create_filter(car_parameters)}'
        query = f'SELECT * FROM cars{where_part}'
        print(query)
        result = cursor.execute(query)
        cars = []
        for row in result.fetchall():
            cars.append(CarModel(*row).json())
        return cars

    @classmethod
    def get_by_car_id(cls, car_id: int):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        cars = []

        where_part = f' WHERE "car-id" = {car_id}'
        query = f'SELECT * FROM cars{where_part}'
        print(query)
        result = cursor.execute(query)
        if result:
            for row in result:
                cars.append(cls(*row).json())
        connection.close()
        return cars

class CarListModel:

    @classmethod
    def get_all_cars(cls):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'SELECT * FROM cars'
        result = cursor.execute(query)
        cars = []
        for row in result:
            print(row)
            cars.append(CarModel(*row).json())
        connection.close()
        return cars

