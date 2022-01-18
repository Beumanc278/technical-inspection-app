import sqlite3

from config import database_path
from utils import create_filter


class UserModel:

    def __init__(self, user_id: int, username: str, car_id: int):
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
        result = cursor.execute(query)
        users = []
        for row in result:
            users.append(cls(*row).json())
        return users


class UserListModel:

    @classmethod
    def get(cls) -> list:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = 'SELECT * FROM users'
        result = cursor.execute(query)
        users = []
        for row in result:
            users.append(UserModel(*row).json())
        return users