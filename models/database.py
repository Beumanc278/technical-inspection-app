import sqlite3

from config import database_path

def create_filter(parameters: dict) -> str:
    where_query_part = ''
    for field, value in parameters.items():
        if value and not where_query_part:
            where_query_part += f'{field} = "{value}"'
        elif value and where_query_part:
            where_query_part += f' AND {field} = "{value}"'
    return where_query_part


class UserDatabase:

    def create_table(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, car_id int)"
        cursor.execute(query)

        connection.commit()
        connection.close()

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class CarDatabase:

    def create_table(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = "CREATE TABLE IF NOT EXISTS cars (id INTEGER PRIMARY KEY, brend text, model text, year text, engine_type text, engine_capacity text, transmission text, drive_unit text)"
        cursor.execute(query)

        connection.commit()
        connection.close()

    def get(self, car_parameters: dict) -> list:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = "SELECT * FROM cars ?"
        filter = create_filter(car_parameters)
        result = cursor.execute(query, (filter, ))

        connection.close()

        return result.fetchall()

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class ServiceDatabase:

    def create_table(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = "CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY, description text, inspection_name text, inspection_cost, car_id int)"
        cursor.execute(query)

        connection.commit()
        connection.close()

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


UserDatabase().create_table()
CarDatabase().create_table()
ServiceDatabase().create_table()