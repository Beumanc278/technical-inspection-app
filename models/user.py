import sqlite3

from config import database_path


class UserModel:

    def __init__(self, _id: int, username: str, car_id: int = None, car_parameters: dict = None):
        self.id = _id
        self.username = username
        self.car_id = car_id
        self.car_parameters = car_parameters

    def json(self) -> dict:
        return {"id": self.id, "username": self.username, "car_id": self.car_id}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(*row)

    def insert(self):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"

