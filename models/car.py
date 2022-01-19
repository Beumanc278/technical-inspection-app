import sqlite3
from typing import Tuple

from config import database_path
from utils import create_filter

class CarModel:

    def __init__(self, _id: int = None, brend: str = None,
                 model: str = None, year: str = None, engine_type: str = None,
                 engine_capacity: str = None, transmission: str = None, drive_unit: str = None):
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
        print(f'Sending query: {query}')
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
        print(f'Sending query: {query}')
        result = cursor.execute(query)
        if result:
            for row in result:
                cars.append(cls(*row).json())
        connection.close()
        return cars

    def insert_to_database(self) -> Tuple[bool, int]:
        parameters = self.json()
        parameters.pop('car-id')

        car_id = self.is_car_exists(parameters)
        if car_id is not None:
            return False, car_id

        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'INSERT INTO cars VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)'
        cursor.execute(query, (tuple(parameters.values())))
        print(f'Sending query: {query}')

        connection.commit()
        connection.close()
        print('INSERT query was completed successfully.')

        new_car_id = self.is_car_exists(parameters)
        return True, new_car_id

    def update_in_database(self, received_data: dict):
        parameters_to_change = {}
        existing_car = CarModel.get_by_car_id(received_data['car-id'])[0]
        for parameter, value in received_data.items():
            if value != existing_car[parameter]:
                parameters_to_change[parameter] = value
                print(f'parameters_to_change: {parameters_to_change}')

        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = f'UPDATE cars SET {create_filter(parameters_to_change)} WHERE "car-id" = {received_data["car-id"]}'
        print(f'Sending query: {query}')
        cursor.execute(query)

        connection.commit()
        connection.close()
        print('UPDATE query was completed successfully.')

    def delete_car(self):
        if not self.is_car_exists(self.json()):
            return None

        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = f'DELETE FROM cars WHERE "car-id" = {self.id}'
        cursor.execute(query)
        print(f'Sending query: {query}')

        connection.commit()
        connection.close()
        print('DELETE query was completed successfully.')
        return self

    def is_car_exists(self, parameters: dict) -> [int, None]:
        cars = self.get_by_parameters(parameters)
        return cars[0]['car-id'] if cars and len(cars) == 1 else None

class CarListModel:

    @classmethod
    def get_all_cars(cls):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'SELECT * FROM cars'
        print(f'Sending query: {query}')
        result = cursor.execute(query)
        cars = []
        for row in result:
            cars.append(CarModel(*row).json())
        connection.close()
        return cars

