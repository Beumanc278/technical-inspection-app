import os
import sqlite3

from utils import create_filter

database_path = 'data.db'


class UserDatabase:

    def create_table(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'CREATE TABLE IF NOT EXISTS users ("user-id" INTEGER PRIMARY KEY, username text, "car-id" int)'
        cursor.execute(query)

        connection.commit()
        connection.close()

    def insert_mock_users(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        users_to_input = []
        with open('../tests/test_user_data.txt', encoding='utf-8') as file:
            for line in file.readlines():
                result = tuple(line.replace('\n', '').split(','))
                users_to_input.append(result)

        query = 'INSERT INTO users VALUES (NULL, ?, ?)'
        for user_data in users_to_input:
            cursor.execute(query, user_data)

        connection.commit()
        connection.close()

class CarDatabase:

    def create_table(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'CREATE TABLE IF NOT EXISTS cars ("car-id" INTEGER PRIMARY KEY, "car-brend" text, "car-model" text, "car-year" int, "car-engine-type" text, "car-engine-capacity" float, "car-transmission" text, "car-drive-unit" text)'
        cursor.execute(query)

        connection.commit()
        connection.close()

    def insert_mock_cars(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        cars_to_input = []
        with open(r'../tests/test_car_data.txt', encoding='utf-8') as file:
            for line in file.readlines():
                result = tuple(line.replace('\n', '').split(','))
                cars_to_input.append(result)

        query = 'INSERT INTO cars VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)'
        for car_data in cars_to_input:
            cursor.execute(query, car_data)

        connection.commit()
        connection.close()

    def get_mock_car(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        parameters = {'car-brend': 'Lexus', 'car-model': None, 'car-year': None, 'car-engine-type': None, 'car-engine-capacity': None, 'car-transmission': None, 'car-drive-unit': None}
        where_part = f' WHERE {create_filter(parameters)}'

        query = f"SELECT * FROM cars{where_part}"
        result = cursor.execute(query)
        row = result.fetchone()
        print(row)

        connection.close()

class ServiceDatabase:

    def create_table(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'CREATE TABLE IF NOT EXISTS services ("service-id" INTEGER PRIMARY KEY, "service-name" text, "service-description" text)'
        cursor.execute(query)

        connection.commit()
        connection.close()

    def insert_mock_services(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        services_to_input = []
        with open('../tests/test_service_data.txt', encoding='utf-8') as file:
            for line in file.readlines():
                result = line.replace('\n', '').replace('"', '').split(',')
                services_to_input.append(result)

        query = "INSERT INTO services VALUES (NULL, ?, ?)"
        for service in services_to_input:
            cursor.execute(query, service)

        connection.commit()
        connection.close()

class InspectionDatabase:

    def create_table(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'CREATE TABLE IF NOT EXISTS inspections ("inspection-id" INTEGER PRIMARY KEY, "inspection-name" text, "inspection-cost" float, "inspection-mileage" int, "inspection-lifetime" int, "inspection-service-id" int, "inspection-car-id" int)'
        cursor.execute(query)

        connection.commit()
        connection.close()

    def insert_mock_inspections(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        inspections_to_input = []
        with open('../tests/test_inspection_data.txt', encoding='utf-8') as file:
            for line in file.readlines():
                result = line.replace('\n', '')
                result = result.split(',')
                inspections_to_input.append(result)

        query = 'INSERT INTO inspections VALUES (NULL, ?, ?, ?, ?, ?, ?)'
        for inspection in inspections_to_input:
            cursor.execute(query, inspection)

        connection.commit()
        connection.close()

if os.path.exists(database_path):
    os.remove(database_path)
    print(f'The existing database was found and deleted.')

UserDatabase().create_table()
CarDatabase().create_table()
ServiceDatabase().create_table()
InspectionDatabase().create_table()

UserDatabase().insert_mock_users()
CarDatabase().insert_mock_cars()
ServiceDatabase().insert_mock_services()
InspectionDatabase().insert_mock_inspections()