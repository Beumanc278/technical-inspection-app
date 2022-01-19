import sqlite3
from typing import Tuple

from config import database_path
from utils import create_filter


class UserModel:

    def __init__(self, user_id: int = None, username: str = None, car_id: int = None):
        self.user_id = user_id
        self.username = username
        self.car_id = car_id

    def json(self) -> dict:
        return {"user-id": self.user_id, "username": self.username, "car-id": self.car_id}

    @classmethod
    def get_by_parameters(cls, parameters: dict) -> list:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        where_part = f' WHERE {create_filter(parameters)}'
        query = f"SELECT * FROM users{where_part}"
        print(f'Sending query: {query}')
        result = cursor.execute(query)
        users = []
        for row in result:
            users.append(cls(*row).json())
        return users

    def insert_to_database(self) -> Tuple[bool, int]:
        parameters = self.json()
        parameters.pop('user-id')

        user_id = self.is_user_exists(parameters)
        if user_id is not None:
            return False, user_id

        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'INSERT INTO users VALUES (NULL, ?, ?)'
        cursor.execute(query, (tuple(parameters.values())))
        print(f'Sending query: {query}')

        connection.commit()
        connection.close()
        print('INSERT query was completed successfully.')

        new_user_id = self.is_user_exists(parameters)
        return True, new_user_id

    def update_in_database(self, received_data: dict):
        parameters_to_change = {}
        existing_user = UserModel.get_by_parameters({'user-id': received_data['user-id']})[0]
        for parameter, value in received_data.items():
            if value != existing_user[parameter]:
                parameters_to_change[parameter] = value
                print(f'parameters_to_change: {parameters_to_change}')
        if not parameters_to_change:
            return False, received_data['user-id']

        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = f'UPDATE users SET {create_filter(parameters_to_change, operation="UPDATE")} WHERE "user-id" = {received_data["user-id"]}'
        print(f'Sending query: {query}')
        cursor.execute(query)
        result = cursor.execute(f'SELECT * FROM users WHERE "user-id" = {received_data["user-id"]}').fetchone()
        updated_user = UserModel(*result)

        connection.commit()
        connection.close()
        print('UPDATE query was completed successfully.')
        return True, updated_user

    def delete_user(self):
        if not self.is_user_exists(self.json()):
            return None
        deleted_user = UserModel(*self.get_by_parameters(self.json())[0].values())
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = f'DELETE FROM users WHERE "user-id" = {self.user_id}'
        cursor.execute(query)
        print(f'Sending query: {query}')

        connection.commit()
        connection.close()
        print('DELETE query was completed successfully.')
        return deleted_user

    def is_user_exists(self, parameters: dict) -> [int, None]:
        users = self.get_by_parameters(parameters)
        return users[0]['user-id'] if users and len(users) == 1 else None


class UserListModel:

    @classmethod
    def get(cls) -> list:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'SELECT * FROM users'
        print(f'Sending query: {query}')
        result = cursor.execute(query)
        users = []
        for row in result:
            users.append(UserModel(*row).json())
        return users