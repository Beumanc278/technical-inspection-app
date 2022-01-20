import sqlite3
from typing import Tuple

from config import database_path
from utils import create_filter


class InspectionModel:

    def __init__(self, _id: int = None, inspection_name: str = None, inspection_cost: float = None,
                 mileage: int = None, lifetime: int = None, service_id: int = None, car_parameters: str = None):
        self.id = _id
        self.name = inspection_name
        self.cost = inspection_cost
        self.mileage = mileage
        self.lifetime = lifetime
        self.service_id = service_id
        if isinstance(car_parameters, dict):
            self.car_parameters = self.transform_car_parameters_to_string(car_parameters)
        else:
            self.car_parameters = car_parameters

    def json(self):
        return {
            'inspection-id': self.id,
            'inspection-name': self.name,
            'inspection-cost': self.cost,
            'inspection-mileage': self.mileage,
            'inspection-lifetime': self.lifetime,
            'inspection-service-id': self.service_id,
            'inspection-car-parameters': self.car_parameters
        }

    @classmethod
    def get_by_id(cls, inspection_id: int):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = f'SELECT * FROM inspections WHERE "inspection-id" = {inspection_id}'
        print(f'Sending query: {query}')
        result = cursor.execute(query).fetchone()
        if result:
            return cls(*result).json()
        else:
            return None

    @classmethod
    def get_inspections_by_car_parameters(cls, car_parameters: dict):
        string_interpretation = ','.join([str(element) for element in list(car_parameters.values())[1:]])
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = f'SELECT * FROM inspections WHERE "inspection-car-parameters" = "{string_interpretation}"'
        print(f'Sending query: {query}')
        result = cursor.execute(query)
        inspections = []
        for row in result:
            inspections.append(cls(*row).json())
        return inspections

    @classmethod
    def get_inspections_by_parameters(cls, parameters: dict):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        where_part = f' WHERE {create_filter(parameters)}'
        query = f'SELECT * FROM inspections{where_part}'
        print(f'Sending query: {query}')
        result = cursor.execute(query)
        inspections = []
        for row in result:
            inspections.append(cls(*row).json())
        return inspections

    def insert_to_database(self) -> Tuple[bool, int]:
        parameters = self.json()
        parameters.pop('inspection-id')

        inspection_id = self.is_inspection_exists(parameters)
        if inspection_id is not None:
            return False, inspection_id

        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        print(f'parameters for paste {parameters}')
        query = 'INSERT INTO inspections VALUES (NULL, ?, ?, ?, ?, ?, ?)'
        cursor.execute(query, (tuple(parameters.values())))
        print(f'Sending query: {query}')

        connection.commit()
        connection.close()
        print('INSERT query was completed successfully.')

        new_inspection_id = self.is_inspection_exists(parameters)
        return True, new_inspection_id

    def update_in_database(self, received_data: dict):
        received_data['inspection-car-parameters'] = self.transform_car_parameters_to_string(received_data['inspection-car-parameters'])
        parameters_to_change = {}
        existing_service = self.get_by_id(received_data['inspection-id'])
        for parameter, value in received_data.items():
            if value != existing_service[parameter]:
                parameters_to_change[parameter] = value
        if not parameters_to_change:
            return False, received_data['inspection-id']

        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = f'UPDATE inspections SET {create_filter(parameters_to_change, operation="UPDATE")} WHERE "inspection-id" = {received_data["inspection-id"]}'
        print(f'Sending query: {query}')
        cursor.execute(query)
        result = cursor.execute(f'SELECT * FROM inspections WHERE "inspection-id" = {received_data["inspection-id"]}').fetchone()
        updated_inspection = InspectionModel(*result)

        connection.commit()
        connection.close()
        print('UPDATE query was completed successfully.')
        return True, updated_inspection

    def delete_inspection(self):
        if not self.is_inspection_exists(self.json()):
            return None
        deleted_inspection = InspectionModel(*self.get_by_id(self.json()['inspection-id']).values())
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = f'DELETE FROM inspections WHERE "inspection-id" = {self.id}'
        cursor.execute(query)
        print(f'Sending query: {query}')

        connection.commit()
        connection.close()
        print('DELETE query was completed successfully.')
        return deleted_inspection

    def is_inspection_exists(self, parameters: dict) -> [int, None]:
        inspections = self.get_inspections_by_parameters(parameters)
        if inspections:
            existing_inspection = inspections[0]
            return existing_inspection['inspection-id']
        return None

    def transform_car_parameters_to_string(self, car_parameters: dict) -> str:
        output_string = ''
        if 'car-id' in car_parameters.keys():
            car_parameters.pop('car-id')
        for value in car_parameters.values():
            if not output_string:
                output_string = value
            else:
                output_string += f',{value}'
        return output_string

class InspectionListModel:

    @classmethod
    def get_all_inspections(cls):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'SELECT * FROM inspections'
        print(f'Sending query: {query}')
        result = cursor.execute(query)
        inspections = []
        for row in result:
            inspections.append(InspectionModel(*row).json())
        connection.close()
        return inspections


