import sqlite3
from typing import Tuple

from config import database_path
from models.inspection import InspectionModel
from utils import create_filter


class ServiceModel:

    def __init__(self, _id: int = None, name: str = None, description: str = None, inspections: list = None):
        self.id = _id
        self.name = name
        self.description = description
        if self.id:
            self.inspection_options = self.get_inspections_for_service()
        else:
            self.inspection_options = inspections

    def json(self) -> dict:
        return {
            'service-id': self.id,
            'service-name': self.name,
            'service-description': self.description,
            'service-inspections': self.inspection_options
                } if self.id else {
            'service-id': self.id,
            'service-name': self.name,
            'service-description': self.description
        }

    @classmethod
    def get_by_parameters(cls, parameters: dict):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        where_part = f' WHERE {create_filter(parameters)}'
        query = f'SELECT * FROM services{where_part}'
        print(f'Sending query: {query}')
        result = cursor.execute(query)
        services = []
        for row in result:
            services.append(cls(*row).json())
        connection.close()
        return services

    def get_inspections_for_service(self):
        parameters = {"inspection-service-id": self.id}
        return InspectionModel.get_inspections_by_parameters(parameters)

    def insert_to_database(self) -> Tuple[bool, int]:
        parameters = self.json()
        parameters.pop('service-id')

        service_id = self.is_service_exists(parameters)
        if service_id is not None:
            return False, service_id

        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'INSERT INTO services VALUES (NULL, ?, ?)'
        cursor.execute(query, (tuple(parameters.values())))
        print(f'Sending query: {query}')

        connection.commit()
        connection.close()
        print('INSERT query was completed successfully.')

        new_service_id = self.is_service_exists(parameters)
        return True, new_service_id

    def update_in_database(self, received_data: dict):
        parameters_to_change = {}
        existing_service = self.get_by_parameters({"service-id": received_data['service-id']})[0]
        for parameter, value in received_data.items():
            if value != existing_service[parameter]:
                parameters_to_change[parameter] = value
        print(f'parameters_to_change 1: {parameters_to_change}')
        if not parameters_to_change:
            return False, received_data['service-id']

        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = f'UPDATE services SET {create_filter(parameters_to_change, operation="UPDATE")} WHERE "service-id" = {received_data["service-id"]}'
        print(f'Sending query: {query}')
        cursor.execute(query)
        result = cursor.execute(f'SELECT * FROM services WHERE "service-id" = {received_data["service-id"]}').fetchone()
        updated_service = ServiceModel(*result)

        connection.commit()
        connection.close()
        print('UPDATE query was completed successfully.')
        return True, updated_service

    def delete_service(self):
        if not self.is_service_exists(self.json()):
            return None
        deleted_service = ServiceModel(*self.get_by_parameters(self.json())[0].values())
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = f'DELETE FROM services WHERE "service-id" = {self.id}'
        cursor.execute(query)
        print(f'Sending query: {query}')

        connection.commit()
        connection.close()
        print('DELETE query was completed successfully.')
        return deleted_service

    def is_service_exists(self, parameters: dict) -> [int, None]:
        services = self.get_by_parameters(parameters)
        return services[0]['service-id'] if services and len(services) == 1 else None

class ServiceListModel:

    @classmethod
    def get_all_services(cls):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'SELECT * FROM services'
        print(f'Sending query: {query}')
        result = cursor.execute(query)
        services = []
        for row in result:
            services.append(ServiceModel(*row).json())
        connection.close()
        return services

