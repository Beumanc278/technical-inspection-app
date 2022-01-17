import sqlite3

from utils import create_filter

database_path = '../database/data.db'


class UserDatabase:

    def create_table(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, car_id int)"
        cursor.execute(query)

        connection.commit()
        connection.close()


class CarDatabase:

    def create_table(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'CREATE TABLE IF NOT EXISTS cars (id INTEGER PRIMARY KEY, "car-brend" text, "car-model" text, "car-year" text, "car-engine-type" text, "car-engine-capacity" text, "car-transmission" text, "car-drive-unit" text)'
        cursor.execute(query)

        connection.commit()
        connection.close()

    def insert_mock_car(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        if not cursor.execute("SELECT * FROM cars WHERE id = 1").fetchone():
            query = 'INSERT INTO cars VALUES (1, "Lexus", "GS300", "2006", "Бензин", "3.0", "АКПП", "Задний")'
            cursor.execute(query)

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

        connection.close()

class ServiceDatabase:

    def create_table(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY, "service-description" text, "service-inspection-name" text, "service-inspection_cost" int, "service-car-id" int)'
        cursor.execute(query)

        connection.commit()
        connection.close()

    def insert_mock_service(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'INSERT INTO services VALUES (1, "Пиздатый сервис", "ТО для новичков", "100500", "1")'
        cursor.execute(query)

        query = 'INSERT INTO services VALUES (2, "Не самый пиздатый сервис", "ТО для профессионалов", "200000", "1")'
        cursor.execute(query)

        connection.commit()
        connection.close()


UserDatabase().create_table()
CarDatabase().create_table()
ServiceDatabase().create_table()

CarDatabase().insert_mock_car()
ServiceDatabase().insert_mock_service()