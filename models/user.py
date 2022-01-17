from .car import CarModel
from .database import CarDatabase

class UserModel:

    def __init__(self, _id: int, username: str, car_parameters: dict):
        self.id = _id
        self.username = username
        self.car = CarModel(car_parameters)
        self.car_id = UserModel.find_car_id_by_parameters()

    @classmethod
    def find_car_id_by_parameters(cls, car_parameters: dict) -> int:
        result = CarDatabase.get(car_parameters)
        if result:
            return result[0][0]
        else:
            return None

