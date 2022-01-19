import sqlite3

from config import database_path
from models.inspection import InspectionModel
from utils import create_filter


class ServiceModel:

    def __init__(self, _id: int = None, name: str = None, description: str = None):
        self.id = _id
        self.name = name
        self.description = description
        if self.id:
            self.inspection_options = self.get_inspections_for_service()

    def json(self) -> dict:
        return {
            'service-id': self.id,
            'service-name': self.name,
            'service-description': self.description,
            'service-inspections': self.inspection_options
                } if self.id else {
            'service-id': self.id,
            'service-name': self.name
        }

    @classmethod
    def get_services_by_parameters(cls, parameters: dict):
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
        parameters = {"service-id": self.id}
        return InspectionModel.get_inspections_by_parameters(parameters)

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

